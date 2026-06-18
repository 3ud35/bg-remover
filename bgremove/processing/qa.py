import numpy as np
from PIL import Image
from bgremove.processing.edges import get_edge_band

def analyze_image(image: Image.Image) -> dict:
    w, h = image.size
    return {
        "type": "auto",
        "low_contrast": False, # stub
        "has_many_edges": False, # stub
        "resolution": [w, h]
    }

def select_strategy(analysis: dict, quality: str) -> dict:
    return {
        "primary_model": "birefnet",
        "fallback_models": [],
        "refinement": "general",
        "ensemble": quality == "max"
    }

def score_alpha_quality(image: Image.Image, alpha: np.ndarray) -> dict:
    edge_band = get_edge_band(alpha)
    edge_ratio = np.sum(edge_band) / alpha.size
    
    fg_ratio = np.sum(alpha > 0.95) / alpha.size
    
    warnings = []
    if fg_ratio < 0.01:
        warnings.append("Very little foreground detected")
    if fg_ratio > 0.99:
        warnings.append("Almost entire image is foreground")
        
    score = 1.0
    if edge_ratio > 0.1: # Very noisy edges
        score -= 0.1
        
    return {
        "quality_score": float(max(0.0, min(1.0, score))),
        "edge_confidence": float(max(0.0, min(1.0, 1.0 - edge_ratio))),
        "halo_risk": "high" if edge_ratio > 0.15 else ("medium" if edge_ratio > 0.05 else "low"),
        "warnings": warnings
    }
