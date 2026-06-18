from PIL import Image, ImageColor
import numpy as np

def compose_rgba(image: Image.Image, alpha: np.ndarray) -> Image.Image:
    img_rgba = image.convert("RGBA")
    alpha_img = Image.fromarray((alpha * 255).astype(np.uint8), mode="L")
    img_rgba.putalpha(alpha_img)
    return img_rgba

def apply_background(rgba: Image.Image, background: str) -> Image.Image:
    if background == "transparent":
        return rgba
        
    w, h = rgba.size
    
    if background.startswith("#") or background in ImageColor.colormap:
        bg = Image.new("RGBA", (w, h), ImageColor.getcolor(background, "RGBA"))
        return Image.alpha_composite(bg, rgba)
        
    try:
        bg_img = Image.open(background).convert("RGBA")
        bg_img = bg_img.resize((w, h), Image.Resampling.LANCZOS)
        return Image.alpha_composite(bg_img, rgba)
    except Exception:
        # Fallback to white if not a valid image path or color
        bg = Image.new("RGBA", (w, h), (255, 255, 255, 255))
        return Image.alpha_composite(bg, rgba)
