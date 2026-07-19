"""Rendered-header quality gate for resume and cover-letter page images."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image


def rgb(value: str) -> tuple[int, int, int]:
    value = value.strip().lstrip("#")
    if len(value) != 6:
        raise ValueError("Colors must use six-digit RGB hex values")
    return tuple(int(value[index:index + 2], 16) for index in (0, 2, 4))


def distance(a: tuple[int, int, int], b: tuple[int, int, int]) -> int:
    return sum(abs(x - y) for x, y in zip(a, b))


def bbox(points: list[tuple[int, int]]) -> tuple[int, int, int, int]:
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    return min(xs), min(ys), max(xs), max(ys)


def center(box: tuple[int, int, int, int]) -> tuple[float, float]:
    return (box[0] + box[2]) / 2, (box[1] + box[3]) / 2


def validate_header(
    image_path: str | Path,
    *,
    background: str,
    accent: str,
    white: str = "#FFFFFF",
    max_horizontal_error_px: float = 2.0,
    vertical_offset_min: float = -0.08,
    vertical_offset_max: float = 0.02,
) -> dict:
    image = Image.open(image_path).convert("RGB")
    width, height = image.size
    background_rgb = rgb(background)
    accent_rgb = rgb(accent)
    white_rgb = rgb(white)

    top_limit = max(1, int(height * 0.20))
    band_bottom = -1
    edge_sample = max(1, min(6, width // 100))
    for y in range(top_limit):
        edge_pixels = [image.getpixel((x, y)) for x in range(edge_sample)]
        edge_pixels += [image.getpixel((width - 1 - x, y)) for x in range(edge_sample)]
        matches = sum(distance(pixel, background_rgb) <= 24 for pixel in edge_pixels)
        if matches / len(edge_pixels) >= 0.80:
            band_bottom = y
        elif band_bottom >= 0:
            break
    if band_bottom < 1:
        raise AssertionError("Header background band was not detected at the top of the page")

    failures: list[str] = []
    for x in range(width):
        if distance(image.getpixel((x, 0)), background_rgb) > 24:
            failures.append(f"top edge is not full bleed at x={x}")
            break
    for edge_x, edge_name in ((0, "left"), (width - 1, "right")):
        for y in range(band_bottom + 1):
            if distance(image.getpixel((edge_x, y)), background_rgb) > 24:
                failures.append(f"{edge_name} edge is not full bleed at y={y}")
                break

    foreground: list[tuple[int, int]] = []
    name_pixels: list[tuple[int, int]] = []
    accent_pixels: list[tuple[int, int]] = []
    for y in range(band_bottom + 1):
        for x in range(width):
            pixel = image.getpixel((x, y))
            is_white = distance(pixel, white_rgb) <= 120
            is_accent = distance(pixel, accent_rgb) <= 120
            if is_white or is_accent:
                foreground.append((x, y))
            if is_white and y <= band_bottom * 0.58:
                name_pixels.append((x, y))
            if is_accent and band_bottom * 0.25 <= y <= band_bottom * 0.72:
                accent_pixels.append((x, y))

    if not foreground or not name_pixels or not accent_pixels:
        failures.append("name, accent rule, or contact block could not be detected")
        metrics = {}
    else:
        page_center_x = (width - 1) / 2
        band_center_y = band_bottom / 2
        composition_box = bbox(foreground)
        name_box = bbox(name_pixels)
        accent_box = bbox(accent_pixels)
        composition_center = center(composition_box)
        name_center = center(name_box)
        accent_center = center(accent_box)
        composition_error = composition_center[0] - page_center_x
        name_error = name_center[0] - page_center_x
        accent_error = accent_center[0] - page_center_x
        vertical_offset = (composition_center[1] - band_center_y) / (band_bottom + 1)
        for element, error in (
            ("header composition", composition_error),
            ("name", name_error),
            ("accent rule", accent_error),
        ):
            if abs(error) > max_horizontal_error_px:
                failures.append(
                    f"{element} is {error:.2f}px from the physical page center; "
                    f"maximum is {max_horizontal_error_px:.2f}px"
                )
        if not vertical_offset_min <= vertical_offset <= vertical_offset_max:
            failures.append(
                f"header composition vertical offset is {vertical_offset:.4f}; "
                f"required range is {vertical_offset_min:.4f} to {vertical_offset_max:.4f}"
            )
        header_height_inches = (band_bottom + 1) / height * 11.0
        if not 1.15 <= header_height_inches <= 1.40:
            failures.append(
                f"rendered header height is approximately {header_height_inches:.3f} inches; "
                "required range is 1.15 to 1.40 inches"
            )
        metrics = {
            "image_size": [width, height],
            "header_bottom_px": band_bottom,
            "header_height_inches_estimate": round(header_height_inches, 4),
            "page_center_x": page_center_x,
            "composition_bbox": composition_box,
            "name_bbox": name_box,
            "accent_bbox": accent_box,
            "composition_horizontal_error_px": round(composition_error, 4),
            "name_horizontal_error_px": round(name_error, 4),
            "accent_horizontal_error_px": round(accent_error, 4),
            "composition_vertical_offset_fraction": round(vertical_offset, 6),
        }

    result = {
        "status": "pass" if not failures else "fail",
        "image": str(image_path),
        "metrics": metrics,
        "failures": failures,
    }
    if failures:
        raise AssertionError(json.dumps(result, indent=2))
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a rendered document header")
    parser.add_argument("image", help="Rendered first-page PNG")
    parser.add_argument("--background", required=True, help="Header background hex color")
    parser.add_argument("--accent", required=True, help="Rule/accent hex color")
    parser.add_argument("--white", default="#FFFFFF")
    parser.add_argument("--max-horizontal-error-px", type=float, default=2.0)
    args = parser.parse_args(argv)
    try:
        result = validate_header(
            args.image,
            background=args.background,
            accent=args.accent,
            white=args.white,
            max_horizontal_error_px=args.max_horizontal_error_px,
        )
    except AssertionError as exc:
        print(exc)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
