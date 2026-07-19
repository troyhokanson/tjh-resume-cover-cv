import pytest
from PIL import Image, ImageDraw

from header_render_validator import validate_header


def make_header(path, *, shift=0, edge_gap=0):
    image = Image.new("RGB", (850, 1100), "#FFFFFF")
    draw = ImageDraw.Draw(image)
    draw.rectangle((edge_gap, 0, 849, 129), fill="#0D1B2A")
    draw.rectangle((300 + shift, 30, 550 + shift, 55), fill="#FFFFFF")
    draw.rectangle((200 + shift, 65, 650 + shift, 68), fill="#C9A84C")
    draw.rectangle((250 + shift, 80, 600 + shift, 95), fill="#C9A84C")
    image.save(path)


def test_centered_full_bleed_header_passes(tmp_path):
    image = tmp_path / "pass.png"
    make_header(image)
    result = validate_header(image, background="#0D1B2A", accent="#C9A84C")
    assert result["status"] == "pass"


def test_shifted_header_fails(tmp_path):
    image = tmp_path / "shifted.png"
    make_header(image, shift=-25)
    with pytest.raises(AssertionError):
        validate_header(image, background="#0D1B2A", accent="#C9A84C")


def test_edge_gap_fails(tmp_path):
    image = tmp_path / "gap.png"
    make_header(image, edge_gap=5)
    with pytest.raises(AssertionError):
        validate_header(image, background="#0D1B2A", accent="#C9A84C")
