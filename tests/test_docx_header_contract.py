from docx_header import BODY_FONT, CONTACT_PARTS


def test_locked_header_uses_garamond_body_default():
    assert BODY_FONT == "EB Garamond"


def test_locked_header_excludes_location_and_preserves_four_item_order(monkeypatch):
    labels = [label for label, _ in CONTACT_PARTS]

    assert "Lakeville, MN" not in labels
    assert labels[-3:] == [
        "TroyHokanson@iCloud.com",
        "linkedin.com/in/troyhokanson",
        "troyhokanson.com",
    ]
    assert len(labels) in (3, 4)
