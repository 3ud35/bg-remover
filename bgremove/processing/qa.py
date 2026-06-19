import numpy as np
import cv2
from PIL import Image
from bgremove.processing.edges import get_edge_band


def analyze_image(image: Image.Image) -> dict:
    """
    Analyzes the input image to identify characteristics that influence the background removal strategy.
    Checks for: low contrast, complexity of edges (hair/fur), and general resolution.
    """
    img_np = np.array(image.convert("RGB"))
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    w, h = image.size

    # 1. Contrast Analysis (using Standard Deviation and Histogram Spread)
    std_dev = np.std(gray)
    low_contrast = std_dev < 40  # Threshold for flat/low contrast images

    # 2. Edge / Complexity Analysis (using Laplacian variance as a proxy for detail)
    # High variance often means sharp details (hair, jewelry), low variance means smooth edges.
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    complex_scene = laplacian_var > 500

    # 3. Brightness level (to detect very dark or very bright images)
    avg_brightness = np.mean(gray)
    extreme_lighting = avg_brightness < 30 or avg_brightness > 225

    return {
        "low_contrast": bool(low_contrast),
        "complex_scene": bool(complex_scene),
        "extreme_lighting": bool(extreme_lighting),
        "detail_score": float(laplacian_var),
        "resolution": [w, h],
    }


def select_strategy(analysis: dict, quality: str) -> dict:
    """
    Determines the best models and post-processing steps based on the image analysis and requested quality.
    """
    # Base strategy
    strategy = {
        "primary_model": "birefnet",
        "fallback_models": [],
        "refinement": "general",
        "ensemble": quality == "max",
    }

    # If it's a complex scene (hair, many details) and we want pro/max quality
    if analysis["complex_scene"] and quality in ["pro", "max"]:
        strategy["refinement"] = "hair"
        # In a real scenario, we might add a secondary matting model here

    # Low contrast images often need a fallback if the primary fails
    if analysis["low_contrast"] and quality != "fast":
        # placeholder for an future alternative model (e.g. isnet or u2net)
        # strategy["fallback_models"] = ["isnet"]
        pass

    return strategy


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
    if edge_ratio > 0.1:  # Very noisy edges
        score -= 0.1

    return {
        "quality_score": float(max(0.0, min(1.0, score))),
        "edge_confidence": float(max(0.0, min(1.0, 1.0 - edge_ratio))),
        "halo_risk": "high" if edge_ratio > 0.15 else ("medium" if edge_ratio > 0.05 else "low"),
        "warnings": warnings,
    }
