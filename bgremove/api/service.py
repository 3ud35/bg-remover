from pathlib import Path
from typing import Optional
from PIL import Image

from bgremove.result import BackgroundRemovalResult
from bgremove.pipeline import BackgroundRemovalPipeline
from bgremove.io.reader import load_image
from bgremove.io.writer import save_rgba, save_preview, save_report


def _crop_box_from_transparency(rgba: Image.Image) -> Optional[tuple[int, int, int, int]]:
    """Return strict trim box based on non-zero alpha content.

    Equivalent to a classic "crop to content/trim transparency": only fully
    transparent borders are removed.
    """
    alpha_channel = rgba.convert("RGBA").getchannel("A")
    return alpha_channel.getbbox()


def remove_background(
    image_path: Path,
    output_path: Optional[Path] = None,
    quality: str = "pro",
    background: str = "transparent",
    shadow: str = "auto",
    preview: bool = False,
    debug: bool = False,
    report: bool = False,
    device: str = "auto",
    format: str = "png",
    force_model: Optional[str] = None,
) -> BackgroundRemovalResult:
    pipeline = BackgroundRemovalPipeline(quality=quality, background=background, shadow=shadow, device=device)

    image = load_image(image_path)
    debug_dir = image_path.parent / f"debug_{image_path.stem}" if debug else None
    if debug_dir:
        debug_dir.mkdir(parents=True, exist_ok=True)
    out_img_path = output_path or image_path.with_name(f"{image_path.stem}-bgremoved.{format}")

    pipeline_out = pipeline.run(image, debug_dir=debug_dir, force_model=force_model)

    # Auto-crop by trimming fully transparent borders.
    crop_box = _crop_box_from_transparency(pipeline_out.rgba)
    final_rgba = pipeline_out.rgba.crop(crop_box) if crop_box else pipeline_out.rgba

    # Save output
    save_rgba(final_rgba, out_img_path)
    if debug_dir:
        for name, image in pipeline_out.debug_images.items():
            save_rgba(image, debug_dir / f"{name}.png")

    report_path = None
    if report or debug:
        report_data = {
            "model_used": pipeline_out.model_used,
            "fallback_used": pipeline_out.fallback_used,
            **pipeline_out.quality_report,
        }
        report_path = debug_dir / "report.json" if debug_dir else image_path.parent / f"{image_path.stem}-report.json"
        save_report(report_data, report_path)

    if preview:
        preview_path = debug_dir / "preview.png" if debug_dir else image_path.parent / f"{image_path.stem}-preview.png"
        preview_original = image.crop(crop_box) if crop_box else image
        save_preview(preview_original, final_rgba, preview_path)

    return BackgroundRemovalResult(
        input_path=image_path,
        output_path=out_img_path,
        model_used=pipeline_out.model_used,
        fallback_used=pipeline_out.fallback_used,
        quality_score=pipeline_out.quality_report.get("quality_score", 0.0),
        edge_confidence=pipeline_out.quality_report.get("edge_confidence", 0.0),
        halo_risk=pipeline_out.quality_report.get("halo_risk", "low"),
        warnings=pipeline_out.quality_report.get("warnings", []),
        debug_dir=debug_dir,
        report_path=report_path,
    )
