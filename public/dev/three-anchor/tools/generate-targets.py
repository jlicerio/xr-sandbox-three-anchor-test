#!/usr/bin/env python3
"""Generate three rounded, ArUco-inspired image targets for both AR engines."""

from pathlib import Path
from time import time
import json

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
TARGET_DIR = ROOT / "targets"
EIGHTH_WALL_DIR = ROOT / "8thwall"
SCALE = 3
SIZE = (480, 640)

PATTERNS = (
    ("110010", "001101", "101110", "011001", "110101", "010011"),
    ("101101", "011010", "100111", "111000", "000110", "101011"),
    ("011110", "100001", "111010", "010111", "101000", "110101"),
)

PAPER = "#f3f1ea"
INK = "#111716"
WHITE = "#fffdf7"
MID = "#67716e"


def point(value):
    return round(value * SCALE)


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(
        tuple(point(value) for value in box),
        radius=point(radius),
        fill=fill,
        outline=outline,
        width=point(width),
    )


def font(size):
    candidates = (
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/Library/Fonts/Arial.ttf",
    )
    for path in candidates:
        try:
            return ImageFont.truetype(path, point(size))
        except OSError:
            continue
    return ImageFont.load_default(size=point(size))


def draw_corner_glyph(draw, target_index):
    """Add one unique, rounded glyph to improve grayscale image detail."""
    if target_index == 0:
        draw.arc(
            tuple(point(value) for value in (187, 495, 293, 601)),
            start=35,
            end=320,
            fill=INK,
            width=point(8),
        )
        for x, y, radius in ((226, 536, 7), (259, 520, 5), (277, 558, 6), (207, 574, 4)):
            rounded(draw, (x - radius, y - radius, x + radius, y + radius), radius, INK)
    elif target_index == 1:
        for x, y, width, height in ((197, 523, 67, 12), (217, 548, 48, 12), (193, 573, 84, 12)):
            rounded(draw, (x, y, x + width, y + height), height / 2, INK)
        rounded(draw, (278, 545, 292, 559), 7, MID)
    else:
        draw.arc(
            tuple(point(value) for value in (185, 510, 292, 598)),
            start=205,
            end=520,
            fill=INK,
            width=point(8),
        )
        rounded(draw, (238, 543, 253, 558), 7, INK)
        rounded(draw, (268, 569, 284, 585), 7, MID)


def build_target(index, rows):
    image = Image.new("RGB", (point(SIZE[0]), point(SIZE[1])), PAPER)
    draw = ImageDraw.Draw(image)

    # The rounded outer plaque frames the marker as a printed poster card.
    rounded(draw, (12, 12, 468, 628), 43, INK)
    rounded(draw, (20, 20, 460, 620), 36, PAPER)

    # Each card uses black and white shapes so grayscale conversion keeps its identity.
    draw.text((point(44), point(44)), "ROUNDED IMAGE TARGET", fill=MID, font=font(16))
    draw.text((point(394), point(40)), f"0{index + 1}", fill=INK, font=font(26))

    # Rounded-square black field and six-by-six asymmetric code pattern.
    rounded(draw, (52, 88, 428, 464), 34, INK)
    cell = 40
    gap = 5
    grid_size = 6 * cell + 5 * gap
    start_x = (SIZE[0] - grid_size) / 2
    start_y = 124
    for row_index, row in enumerate(rows):
        for column_index, bit in enumerate(row):
            if bit != "1":
                continue
            left = start_x + column_index * (cell + gap)
            top = start_y + row_index * (cell + gap)
            radius = 9 if (row_index + column_index + index) % 3 else 15
            rounded(draw, (left, top, left + cell, top + cell), radius, WHITE)

    # A unique rounded glyph adds irregular detail beyond the repeated code cells.
    draw_corner_glyph(draw, index)
    draw.text((point(46), point(554)), f"ANCHOR 0{index + 1}", fill=INK, font=font(22))
    draw.text((point(46), point(586)), "IMAGE TRACKING  /  GRAYSCALE", fill=MID, font=font(12))

    image = image.resize(SIZE, Image.Resampling.LANCZOS)
    return image


def save_target(index, rows):
    name = f"anchor-{index + 1}"
    image = build_target(index, rows)
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    EIGHTH_WALL_DIR.mkdir(parents=True, exist_ok=True)

    image.save(TARGET_DIR / f"{name}.png", optimize=True)
    image.save(EIGHTH_WALL_DIR / f"{name}_original.png", optimize=True)
    image.save(EIGHTH_WALL_DIR / f"{name}_cropped.png", optimize=True)
    image.resize((263, 350), Image.Resampling.LANCZOS).save(
        EIGHTH_WALL_DIR / f"{name}_thumbnail.png", optimize=True
    )
    image.convert("L").convert("RGB").save(
        EIGHTH_WALL_DIR / f"{name}_luminance.png", optimize=True
    )


def build_composite():
    sheet = Image.new("RGB", (point(SIZE[0]), point(SIZE[1])), PAPER)
    positions = ((20, 100), (252, 100), (136, 332))
    panel_size = 208
    for index, rows in enumerate(PATTERNS):
        artwork = build_target(index, rows)
        marker = artwork.crop((52, 88, 428, 464)).resize(
            (point(panel_size), point(panel_size)), Image.Resampling.LANCZOS
        )
        sheet.paste(marker, (point(positions[index][0]), point(positions[index][1])))
    return sheet.resize(SIZE, Image.Resampling.LANCZOS)


def save_composite():
    name = "composite"
    image = build_composite()
    image.save(TARGET_DIR / f"{name}.png", optimize=True)
    image.save(EIGHTH_WALL_DIR / f"{name}_original.png", optimize=True)
    image.save(EIGHTH_WALL_DIR / f"{name}_cropped.png", optimize=True)
    image.resize((263, 350), Image.Resampling.LANCZOS).save(
        EIGHTH_WALL_DIR / f"{name}_thumbnail.png", optimize=True
    )
    image.convert("L").convert("RGB").save(
        EIGHTH_WALL_DIR / f"{name}_luminance.png", optimize=True
    )
    target = {
        "imagePath": f"{name}_luminance.png",
        "metadata": None,
        "name": name,
        "type": "PLANAR",
        "properties": {
            "left": 0,
            "top": 0,
            "width": SIZE[0],
            "height": SIZE[1],
            "isRotated": False,
            "originalWidth": SIZE[0],
            "originalHeight": SIZE[1],
        },
        "resources": {
            "originalImage": f"{name}_original.png",
            "croppedImage": f"{name}_cropped.png",
            "thumbnailImage": f"{name}_thumbnail.png",
            "luminanceImage": f"{name}_luminance.png",
        },
        "created": int(time() * 1000),
        "updated": int(time() * 1000),
    }
    (EIGHTH_WALL_DIR / f"{name}.json").write_text(
        json.dumps(target, indent=2) + "\n"
    )


def rotate_pattern(rows):
    return tuple("".join(row[column] for row in reversed(rows)) for column in range(len(rows)))


def validate_patterns():
    for index, rows in enumerate(PATTERNS):
        if len(rows) != 6 or any(len(row) != 6 or set(row) - {"0", "1"} for row in rows):
            raise ValueError("Each target pattern must have six binary rows and columns.")
        for other in PATTERNS[index + 1 :]:
            rotated = other
            for _ in range(4):
                distance = sum(a != b for row_a, row_b in zip(rows, rotated) for a, b in zip(row_a, row_b))
                if distance < 12:
                    raise ValueError("Target patterns need stronger separation after rotation.")
                rotated = rotate_pattern(rotated)


def main():
    validate_patterns()
    for index, rows in enumerate(PATTERNS):
        save_target(index, rows)
    save_composite()


if __name__ == "__main__":
    main()
