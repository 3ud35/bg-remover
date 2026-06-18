import numpy as np
from PIL import Image
from bgremove.processing.alpha import normalize_alpha
from bgremove.processing.edges import feather_uncertain_edges

def refine_alpha(image: Image.Image, alpha: np.ndarray, mode: str = "general") -> np.ndarray:
    alpha = normalize_alpha(alpha)
    if mode in ["general", "hair", "fur", "clean_edge"]:
        alpha = feather_uncertain_edges(alpha)
    return alpha
