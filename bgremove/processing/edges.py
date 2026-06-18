import numpy as np
import cv2
from PIL import Image

def get_edge_band(alpha: np.ndarray, low=0.05, high=0.95) -> np.ndarray:
    return ((alpha > low) & (alpha < high)).astype(np.float32)

def feather_uncertain_edges(alpha: np.ndarray, radius: int = 2) -> np.ndarray:
    kernel_size = radius * 2 + 1
    blurred = cv2.GaussianBlur(alpha, (kernel_size, kernel_size), 0)
    
    # Only apply blur to uncertain regions
    edge_mask = get_edge_band(alpha)
    return alpha * (1 - edge_mask) + blurred * edge_mask

def remove_small_holes(alpha: np.ndarray) -> np.ndarray:
    binary = (alpha > 0.5).astype(np.uint8)
    kernel = np.ones((3,3), np.uint8)
    closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    return np.where(get_edge_band(alpha) > 0, alpha, closed.astype(np.float32))

def reduce_halo(image: Image.Image, alpha: np.ndarray) -> np.ndarray:
    # simple erode on alpha to reduce halo
    eroded = cv2.erode(alpha, np.ones((3,3), np.uint8), iterations=1)
    edge_mask = get_edge_band(alpha, 0.1, 0.9)
    return alpha * (1 - edge_mask) + eroded * edge_mask
