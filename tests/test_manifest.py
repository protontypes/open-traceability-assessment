"""Offline tests for the Open Traceability manifest feature.

These tests exercise manifest parsing and evidence-bundle construction without any
network access or LLM calls: ``fetch_url_text`` is monkeypatched, so the tests are
deterministic and free to run.

Run with:
    pip install pytest pyyaml
    pytest tests/test_manifest.py -v
"""

from __future__ import annotations

from pathlib import Path

import pytest

import open_traceability_assessment as ota

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = REPO_ROOT / "examples"


# ---------------------------------------------------------------------------
# Key normalization and aliases
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "heading, expected",
    [
        ("open_data", "open_data"),
        ("OpenData", "open_data"),
        ("Open Data", "open_data"),
        ("Open Access", "open_publications"),   # alias from the original sketch
        ("publications", "open_publications"),
        ("Open Software", "open_software"),
        ("reproducibility", "open_execution"),
        ("review", "open_community"),
        ("Totally Unknown", None),
    ],
)
def test_normalize_manifest_key(heading, expected):
    assert ota.normalize_manifest_key(heading) == expected


# ---------------------------------------------------------------------------
# Entry coercion: bare string, single mapping, and lists
# ---------------------------------------------------------------------------

def test_coerce_entries_accepts_bare_string():
    entries = ota._coerce_entries("https://example.org/x")
    assert len(entries) == 1
    assert entries[0].url == "https://example.org/x"
    assert entries[0].note == ""


def test_coerce_entries_accepts_mapping_with_note():
    entries = ota._coerce_entries([{"url": "https://example.org/x", "note": "why"}])
    assert entries[0].url == "https://example.org/x"
    assert entries[0].note == "why"


def test_coerce_entries_skips_empty_and_malformed():
    entries = ota._coerce_entries(["", {"note": "no url"}, 42, "https://ok.org"])
    assert [e.url for e in entries] == ["https://ok.org"]


# ---------------------------------------------------------------------------
# Manifest parsing
# ---------------------------------------------------------------------------

SAMPLE_MANIFEST = """
claim: A test claim.
claim_url: https://example.org/claim
namespace: https://github.com/example-org
open_data:
  - https://example.org/data
  - url: https://example.org/data2
    note: with a note
Open Access:                       # alias -> open_publications
  - https://example.org/paper
open_software:
  - https://example.org/code
"""


def write_manifest(tmp_path: Path, text: str) -> str:
    path = tmp_path / "manifest.yml"
    path.write_text(text, encoding="utf-8")
    return str(path)


def test_load_manifest_parses_fields(tmp_path):
    manifest = ota.load_manifest(write_manifest(tmp_path, SAMPLE_MANIFEST))

    assert manifest.claim == "A test claim."
    assert manifest.claim_url == "https://example.org/claim"
    assert [e.url for e in manifest.namespaces] == ["https://github.com/example-org"]

    assert [e.url for e in manifest.dimensions["open_data"]] == [
        "https://example.org/data",
        "https://example.org/data2",
    ]
    assert manifest.dimensions["open_data"][1].note == "with a note"
    # "Open Access" heading must normalize to open_publications
    assert [e.url for e in manifest.dimensions["open_publications"]] == [
        "https://example.org/paper"
    ]


def test_load_manifest_rejects_non_mapping(tmp_path):
    with pytest.raises(ValueError, match="not a YAML mapping"):
        ota.load_manifest(write_manifest(tmp_path, "- just\n- a\n- list\n"))


def test_load_manifest_rejects_no_recognized_dimensions(tmp_path):
    text = "claim: x\nunrelated_section:\n  - https://example.org/x\n"
    with pytest.raises(ValueError, match="no URLs under any recognized dimension"):
        ota.load_manifest(write_manifest(tmp_path, text))


# ---------------------------------------------------------------------------
# Evidence-bundle construction (network stubbed)
# ---------------------------------------------------------------------------

@pytest.fixture
def stub_fetch(monkeypatch):
    """Replace fetch_url_text with a deterministic stub; record fetched URLs."""
    fetched: list[str] = []

    def fake_fetch(url, max_chars=50_000):
        fetched.append(url)
        if "broken" in url:
            raise RuntimeError("boom")
        return f"CONTENT OF {url}"

    monkeypatch.setattr(ota, "fetch_url_text", fake_fetch)
    return fetched


def test_collect_manifest_evidence_groups_and_labels(tmp_path, stub_fetch):
    manifest = ota.load_manifest(write_manifest(tmp_path, SAMPLE_MANIFEST))
    bundle, items = ota.collect_manifest_evidence(
        manifest, max_file_chars=5_000, max_total_chars=100_000
    )

    # Namespace is fetched once, up front, and labelled as such.
    assert any(it.label.startswith("Namespace") for it in items)
    assert "## Namespace (organization / project home)" in bundle

    # Every manifest URL (1 namespace + 4 dimension URLs) becomes an evidence item.
    assert len(items) == 5
    assert all("CONTENT OF" in it.text for it in items)

    # Stage headers appear in stage order with the canonical stage names.
    assert "## Stage 1: Open Input Data and Measurement Evidence (open_data)" in bundle
    assert "## Stage 5: Open Publications and Communication (open_publications)" in bundle
    # The claim is carried into the bundle for the model.
    assert "A test claim." in bundle


def test_collect_manifest_evidence_handles_fetch_failure(tmp_path, stub_fetch):
    text = "claim: x\nopen_data:\n  - https://example.org/broken\n"
    manifest = ota.load_manifest(write_manifest(tmp_path, text))
    _, items = ota.collect_manifest_evidence(
        manifest, max_file_chars=5_000, max_total_chars=100_000
    )
    # A failed fetch is captured, not raised, so one bad URL never aborts a run.
    assert len(items) == 1
    assert items[0].text.startswith("[Could not fetch:")


def test_collect_manifest_evidence_respects_total_budget(tmp_path, stub_fetch):
    text = (
        "claim: x\nopen_data:\n"
        + "".join(f"  - https://example.org/{i}\n" for i in range(20))
    )
    manifest = ota.load_manifest(write_manifest(tmp_path, text))
    _, items = ota.collect_manifest_evidence(
        manifest, max_file_chars=100, max_total_chars=300
    )
    # The total-character budget caps how many URLs are pulled in.
    assert 0 < len(items) < 20


# ---------------------------------------------------------------------------
# The shipped example manifests must stay valid (parse only, no network)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "filename",
    ["open-traceability.yml", "invest-open-traceability.yml"],
)
def test_example_manifests_parse(filename):
    manifest = ota.load_manifest(str(EXAMPLES / filename))
    assert manifest.claim
    assert manifest.namespaces                       # both examples set a namespace
    assert any(manifest.dimensions.values())          # at least one dimension populated
    # Only canonical keys should survive parsing.
    assert set(manifest.dimensions).issubset(
        {key for key, _, _ in ota.MANIFEST_DIMENSIONS}
    )
