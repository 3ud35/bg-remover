import numpy as np
from PIL import Image

def normalize_alpha(alpha: np.ndarray) -> np.ndarray:
    min_val = alpha.min()
    max_val = alpha.max()
    if max_val - min_val > 0:
        return (alpha - min_val) / (max_val - min_val)
    return alpha

def clamp_alpha(alpha: np.ndarray) -> np.ndarray:
    return np.clip(alpha, 0.0, 1.0)

def resize_alpha(alpha: np.ndarray, size: tuple[int, int]) -> np.ndarray:
    img = Image.fromarray((alpha * 255).astype(np.uint8), mode="L")
    img = img.resize(size, Image.Resampling.BILINEAR)
    return np.array(img, dtype=np.float32) / 255.0
