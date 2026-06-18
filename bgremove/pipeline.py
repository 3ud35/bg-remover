from pathlib import Path
from typing import Optional
from dataclasses import dataclass
from PIL import Image
import numpy as np

from bgremove.processing.qa import analyze_image, select_strategy, score_alpha_quality
from bgremove.processing.matting import refine_alpha
from bgremove.processing.compose import compose_rgba, apply_background
from bgremove.models.registry import get_model

@dataclass
class PipelineOutput:
    rgba: Image.Image
    alpha: np.ndarray
    model_used: str
    fallback_used: bool
    quality_report: dict
    debug_images: dict[str, Image.Image]

class BackgroundRemovalPipeline:
    def __init__(self, quality="pro", background="transparent", shadow="auto", device="auto"):
        self.quality = quality
        self.background = background
        self.shadow = shadow
        self.device = device

    def run(self, image: Image.Image, debug_dir: Optional[Path] = None, force_model: Optional[str] = None) -> PipelineOutput:
        analysis = analyze_image(image)
        strategy = select_strategy(analysis, self.quality)
        
        primary_model_name = force_model if force_model else strategy["primary_model"]
        model = get_model(primary_model_name, self.device)
        
        raw_alpha = model.predict_alpha(image)
        refined_alpha = refine_alpha(image, raw_alpha, mode=strategy["refinement"])
        
        qa_report = score_alpha_quality(image, refined_alpha)
        
        fallback_used = False
        final_alpha = refined_alpha
        final_model_name = primary_model_name
        
        # Fallback Logic
        if strategy["fallback_models"] and (
            qa_report["quality_score"] < 0.82 or 
            qa_report["edge_confidence"] < 0.70 or 
            qa_report["halo_risk"] == "high"
        ):
            fallback_model_name = strategy["fallback_models"][0]
            fallback_model = get_model(fallback_model_name, self.device)
            fb_raw_alpha = fallback_model.predict_alpha(image)
            fb_refined_alpha = refine_alpha(image, fb_raw_alpha, mode=strategy["refinement"])
            fb_qa_report = score_alpha_quality(image, fb_refined_alpha)
            
            if fb_qa_report["quality_score"] > qa_report["quality_score"]:
                final_alpha = fb_refined_alpha
                qa_report = fb_qa_report
                final_model_name = fallback_model_name
                fallback_used = True
                
        rgba = compose_rgba(image, final_alpha)
        final_img = apply_background(rgba, self.background)
        
        debug_images = {}
        if debug_dir:
            debug_images["original"] = image
            debug_images["raw-alpha"] = Image.fromarray((raw_alpha * 255).astype(np.uint8), mode="L")
            debug_images["refined-alpha"] = Image.fromarray((final_alpha * 255).astype(np.uint8), mode="L")
            debug_images["final"] = final_img
            
        return PipelineOutput(
            rgba=final_img,
            alpha=final_alpha,
            model_used=final_model_name,
            fallback_used=fallback_used,
            quality_report=qa_report,
            debug_images=debug_images
        )
