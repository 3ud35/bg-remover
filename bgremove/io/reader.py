from pathlib import Path
from PIL import Image, ImageOps

def load_image(path: Path) -> Image.Image:
    """Load image, handle EXIF orientation, convert to RGB."""
    img = Image.open(path)
    img = ImageOps.exif_transpose(img)
    return img.convert("RGB")
