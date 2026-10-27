"""Export web images from assets/: WebP screenshots (full + thumbnail) and the hero portrait.

Run after adding or changing a file in assets/; the outputs in static/img/ are committed.
"""

import logging
import sys
from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "assets" / "img"
PORTRAIT = ROOT / "assets" / "photo-source.jpg"
OUT = ROOT / "static" / "img"

FULL_WIDTH = 1600
THUMB_WIDTH = 640
PORTRAIT_SIZE = 480
# Head-and-shoulders square in the 1786×2500 source photo (left, top, right, bottom).
PORTRAIT_BOX = (0, 170, 1786, 1956)

logger = logging.getLogger("optimize_images")


def resized(image: Image.Image, width: int) -> Image.Image:
    """Downscale to `width` keeping the aspect ratio; never upscale."""
    if image.width <= width:
        return image.copy()
    height = round(image.height * width / image.width)
    return image.resize((width, height), Image.Resampling.LANCZOS)


def export_screenshot(source: Path) -> None:
    with Image.open(source) as opened:
        image = opened.convert("RGB")
    resized(image, FULL_WIDTH).save(OUT / f"{source.stem}.webp", "WEBP", quality=82, method=6)
    resized(image, THUMB_WIDTH).save(
        OUT / f"{source.stem}-thumb.webp", "WEBP", quality=78, method=6
    )


def export_portrait() -> None:
    with Image.open(PORTRAIT) as opened:
        # exif_transpose applies the camera rotation; saving without exif drops the metadata.
        image = ImageOps.exif_transpose(opened).convert("RGB")
    square = image.crop(PORTRAIT_BOX).resize(
        (PORTRAIT_SIZE, PORTRAIT_SIZE), Image.Resampling.LANCZOS
    )
    square.save(OUT / "portrait.webp", "WEBP", quality=85, method=6)


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    OUT.mkdir(parents=True, exist_ok=True)
    try:
        for source in sorted(SOURCES.glob("*.png")):
            export_screenshot(source)
            logger.info("exported %s", source.name)
        export_portrait()
        logger.info("exported portrait")
    except (OSError, UnidentifiedImageError) as exc:
        logger.error("export failed: %s", exc)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
