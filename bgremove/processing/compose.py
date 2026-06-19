from PIL import Image, ImageColor, ImageFilter
import numpy as np


def compose_rgba(image: Image.Image, alpha: np.ndarray) -> Image.Image:
    img_rgba = image.convert("RGBA")
    alpha_img = Image.fromarray((alpha * 255).astype(np.uint8), mode="L")
    img_rgba.putalpha(alpha_img)
    return img_rgba


def _create_drop_shadow(alpha: Image.Image, offset=(10, 10), iterations=3, opacity=0.5) -> Image.Image:
    """Creates a drop shadow based on the alpha channel."""
    # Create a black image the size of the original
    shadow = Image.new("RGBA", alpha.size, (0, 0, 0, 0))
    # Create the shadow content (black where alpha is)
    shadow_content = Image.new("RGBA", alpha.size, (0, 0, 0, int(255 * opacity)))
    shadow.paste(shadow_content, mask=alpha)

    # Blur it to make it soft
    for _ in range(iterations):
        shadow = shadow.filter(ImageFilter.GaussianBlur(radius=5))

    # Create a canvas to hold the offset shadow
    canvas = Image.new("RGBA", alpha.size, (0, 0, 0, 0))
    canvas.paste(shadow, offset)
    return canvas


def apply_background(rgba: Image.Image, background: str, shadow_mode: str = "none") -> Image.Image:
    w, h = rgba.size
    alpha = rgba.getchannel("A")

    # 1. Start with the appropriate background
    bg_lower = background.lower()
    if bg_lower == "transparent":
        final_bg = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    elif background.startswith("#") or bg_lower in ImageColor.colormap:
        final_bg = Image.new("RGBA", (w, h), ImageColor.getcolor(background, "RGBA"))
    else:
        try:
            final_bg = Image.open(background).convert("RGBA")
            final_bg = final_bg.resize((w, h), Image.Resampling.LANCZOS)
        except Exception:
            final_bg = Image.new("RGBA", (w, h), (255, 255, 255, 255))

    # 2. Add Shadow if requested
    if shadow_mode == "drop":
        shadow = _create_drop_shadow(alpha, offset=(w // 100 + 5, h // 100 + 5))
        final_bg = Image.alpha_composite(final_bg, shadow)
    elif shadow_mode == "soft":
        shadow = _create_drop_shadow(alpha, offset=(0, 0), iterations=5, opacity=0.3)
        final_bg = Image.alpha_composite(final_bg, shadow)

    # 3. Composite original foreground on top
    return Image.alpha_composite(final_bg, rgba)
