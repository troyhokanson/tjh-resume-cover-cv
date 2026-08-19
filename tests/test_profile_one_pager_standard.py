import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_profile_layout_delegates_to_locked_header_helpers():
    text = (ROOT / "profile_one_pager.py").read_text(encoding="utf-8")
    for required in (
        "from docx_header import",
        "build_navy_header",
        "add_section_heading",
        "add_bullet",
        "add_job_block",
        "body_top_margin_inches=1.55",
    ):
        assert required in text


def test_profile_contract_preserves_breathing_room():
    contract = json.loads(
        (ROOT / "skills" / "build-troy-application" / "workflow_contract.json").read_text(
            encoding="utf-8"
        )
    )
    layout = contract["layout_minimums"]
    assert layout["header_to_first_heading"] >= 360
    assert layout["major_section_before"] >= 280
    assert layout["major_section_after"] >= 120
    assert layout["major_entry_before"] >= 160


def test_node_standard_uses_current_locked_tokens():
    text = (ROOT / "DOCX_NODE_STANDARD.md").read_text(encoding="utf-8")
    assert "0D1B2A" in text
    assert "C9A84C" in text
    assert "2D6A9F" in text
    assert "1C2B4A" not in text
    assert "C09A20" not in text
