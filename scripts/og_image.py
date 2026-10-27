"""Render static/og.png (1200×630), the link-preview card for LinkedIn, Slack and messengers.

Run after changing the name, tagline or portrait; the output is committed.
"""

import logging
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import data  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "static" / "og.png"
PORTRAIT = ROOT / "static" / "img" / "portrait.webp"

WIDTH, HEIGHT = 1200, 630
BG = (15, 17, 20)
SURFACE = (29, 33, 39)
TEXT = (231, 233, 236)
MUTED = (149, 156, 168)
ACCENT = (242, 193, 78)

# Windows fonts first (where the script is usually run), then common Linux ones.
SANS_BOLD = [
    "C:/Windows/Fonts/segoeuib.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
MONO = ["C:/Windows/Fonts/consola.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"]
MONO_BOLD = [
    "C:/Windows/Fonts/consolab.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
]

logger = logging.getLogger("og_image")


def font(candidates: list[str], size: int) -> ImageFont.FreeTypeFont:
    for path in candidates:
        if Path(path).is_file():
            return ImageFont.truetype(path, size)
    raise OSError(f"none of the fonts exist: {candidates}")


def dotted_grid(draw: ImageDraw.ImageDraw) -> None:
    """Faint dot grid that fades out towards the left, behind the portrait."""
    for x in range(600, WIDTH, 28):
        for y in range(14, HEIGHT, 28):
            alpha = (x - 600) / (WIDTH - 600)
            shade = tuple(
                round(b + (s - b) * alpha * 0.9) for b, s in zip(BG, SURFACE, strict=True)
            )
            draw.ellipse((x - 1.5, y - 1.5, x + 1.5, y + 1.5), fill=shade)


def dashed_circle(draw: ImageDraw.ImageDraw, center: tuple[int, int], radius: int) -> None:
    dashes = 56
    for i in range(dashes):
        start = 360 / dashes * i
        box = (center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius)
        draw.arc(box, start, start + 360 / dashes * 0.55, fill=ACCENT, width=3)


def portrait(size: int) -> Image.Image:
    with Image.open(PORTRAIT) as opened:
        photo = opened.convert("RGB").resize((size, size), Image.Resampling.LANCZOS)
    mask = Image.new("L", (size * 4, size * 4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size * 4, size * 4), fill=255)
    photo.putalpha(mask.resize((size, size), Image.Resampling.LANCZOS))
    return photo


def render() -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)
    dotted_grid(draw)

    center, size = (905, 315), 340
    dashed_circle(draw, center, size // 2 + 26)
    ring = size // 2 + 9
    draw.ellipse(
        (center[0] - ring, center[1] - ring, center[0] + ring, center[1] + ring), fill=ACCENT
    )
    gap = size // 2 + 4
    draw.ellipse((center[0] - gap, center[1] - gap, center[0] + gap, center[1] + gap), fill=BG)
    photo = portrait(size)
    image.paste(photo, (center[0] - size // 2, center[1] - size // 2), photo)

    profile = data.PROFILE
    left = 72
    draw.text((left, 70), "tkoralewski", font=font(MONO_BOLD, 30), fill=TEXT)
    brand_width = draw.textlength("tkoralewski", font=font(MONO_BOLD, 30))
    draw.text((left + brand_width, 70), "_", font=font(MONO_BOLD, 30), fill=ACCENT)

    draw.text((left, 200), profile["location"].lower(), font=font(MONO, 26), fill=MUTED)
    name_font = font(SANS_BOLD, 76)
    first, _, last = profile["name"].lower().partition(" ")
    draw.text((left, 240), first, font=name_font, fill=TEXT)
    draw.text((left, 322), last, font=name_font, fill=TEXT)
    draw.text((left, 428), profile["tagline"], font=font(MONO_BOLD, 30), fill=ACCENT)

    domain = profile["site_url"].removeprefix("https://")
    draw.text((left, 540), domain, font=font(MONO, 24), fill=MUTED)
    arrow_x = left + draw.textlength(domain, font=font(MONO, 24)) + 14
    draw.text((arrow_x, 538), "→", font=font(MONO, 26), fill=ACCENT)
    # Thin accent rule above the domain, echoing the section heading flash on the site.
    draw.line((left, 515, left + math.floor(brand_width * 0.4), 515), fill=ACCENT, width=3)
    return image


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    try:
        render().save(OUT, "PNG", optimize=True)
    except (OSError, UnidentifiedImageError, KeyError) as exc:
        logger.error("og image failed: %s", exc)
        return 1
    logger.info("wrote %s", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
