import numpy as np
import cv2
from PIL import Image
from bgremove.processing.alpha import normalize_alpha
from bgremove.processing.edges import feather_uncertain_edges


def guided_filter(guide: np.ndarray, src: np.ndarray, radius: int, eps: float) -> np.ndarray:
    """
    Implementation of Fast Guided Filter for edge-preserving smoothing and alpha refinement.
    guide: guidance image (the original RGB image)
    src: source image (the raw alpha mask)
    """
    guide = guide.astype(np.float32) / 255.0
    src = src.astype(np.float32)

    # Convert RGB guide to grayscale if needed, but usually works better per channel
    # Here we simplify to a single channel or average
    if len(guide.shape) == 3:
        guide_gray = cv2.cvtColor(guide, cv2.COLOR_RGB2GRAY)
    else:
        guide_gray = guide

    mean_I = cv2.blur(guide_gray, (radius, radius))
    mean_p = cv2.blur(src, (radius, radius))
    mean_Ip = cv2.blur(guide_gray * src, (radius, radius))
    cov_Ip = mean_Ip - mean_I * mean_p

    mean_II = cv2.blur(guide_gray * guide_gray, (radius, radius))
    var_I = mean_II - mean_I * mean_I

    a = cov_Ip / (var_I + eps)
    b = mean_p - a * mean_I

    mean_a = cv2.blur(a, (radius, radius))
    mean_b = cv2.blur(b, (radius, radius))

    return mean_a * guide_gray + mean_b


def refine_alpha(image: Image.Image, alpha: np.ndarray, mode: str = "general") -> np.ndarray:
    """
    Refines the alpha mask using the original image as a guide.
    Modes:
    - general: basic smoothing
    - hair: guided filter for fine details
    """
    alpha = normalize_alpha(alpha)
    img_np = np.array(image.convert("RGB"))

    if mode == "hair":
        # Fine refinement for hair/fur using Fast Guided Filter
        refined = guided_filter(img_np, alpha, radius=8, eps=1e-4)
        # Re-apply strictness to background
        refined = np.where(alpha < 0.05, 0.0, refined)
        refined = np.where(alpha > 0.95, 1.0, refined)
        return np.clip(refined, 0.0, 1.0)

    if mode in ["general", "clean_edge"]:
        # Basic feathering
        alpha = feather_uncertain_edges(alpha, radius=2)

    return alpha
