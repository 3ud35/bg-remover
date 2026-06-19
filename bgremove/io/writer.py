from pathlib import Path
from PIL import Image
import numpy as np
import json


def save_rgba(image: Image.Image, path: Path) -> None:
    """Save image, converting to RGB if format doesn't support transparency."""
    ext = path.suffix.lower()
    if ext in [".jpg", ".jpeg"]:
        # Convert to RGB, if it has alpha it will use a white background by default if we do it this way?
        # Actually if we want to save as JPEG we should ensure it's RGB.
        if image.mode == "RGBA":
            # Create a white background if user chose JPG (consistent with most expectations)
            background = Image.new("RGB", image.size, (255, 255, 255))
            background.paste(image, mask=image.getchannel("A"))
            image = background
        else:
            image = image.convert("RGB")

    image.save(path, format=path.suffix[1:].upper() if path.suffix else "PNG")


def save_alpha(alpha: np.ndarray, path: Path) -> None:
    alpha_img = Image.fromarray((alpha * 255).astype(np.uint8), mode="L")
    alpha_img.save(path)


def save_preview(original: Image.Image, result: Image.Image, path: Path) -> None:
    # Create checkerboard background for the result
    w, h = result.size
    cb_size = 20
    checkerboard = Image.new("RGBA", (w, h), (255, 255, 255, 255))
    pixels = checkerboard.load()
    for y in range(h):
        for x in range(w):
            if ((x // cb_size) + (y // cb_size)) % 2 == 0:
                pixels[x, y] = (200, 200, 200, 255)

    cb_result = Image.alpha_composite(checkerboard, result.convert("RGBA"))

    preview = Image.new("RGB", (w * 2, h))
    preview.paste(original.convert("RGB"), (0, 0))
    preview.paste(cb_result.convert("RGB"), (w, 0))
    preview.save(path)


def save_report(report: dict, path: Path) -> None:
    with open(path, "w") as f:
        json.dump(report, f, indent=2)
