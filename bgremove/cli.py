import typer
from pathlib import Path
from typing import Optional
from bgremove.utils.config import setup_portable_environment

# Configure environment before anything else
# This must happen before importing any library that uses torch/transformers
MODELS_DIR, CACHE_DIR = setup_portable_environment()

from bgremove.api.service import remove_background

app = typer.Typer(help="Production Background Remover CLI")

DOWNLOADS_DIR = Path("/home/youdz/Téléchargements")
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff", ".tif"}


def _list_download_images(directory: Path) -> list[Path]:
    if not directory.is_dir():
        return []
    return sorted(
        (
            p
            for p in directory.iterdir()
            if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS and not p.stem.lower().endswith("-bgremoved")
        ),
        key=lambda p: p.name.lower(),
    )


def _exit_with(message: str, color=typer.colors.RED, code: int = 1) -> None:
    typer.secho(message, fg=color)
    raise typer.Exit(code)


def _choose_image_from_downloads(directory: Path) -> Path:
    images = _list_download_images(directory)

    if not images:
        _exit_with(f"Error: No image found in {directory}.")

    typer.secho(f"Images found in {directory}:", fg=typer.colors.CYAN)
    for idx, image in enumerate(images, start=1):
        typer.echo(f"  {idx}. {image.name}")

    while True:
        choice = typer.prompt("Choose an image number", type=int)
        if 1 <= choice <= len(images):
            return images[choice - 1]
        typer.secho(f"Invalid selection. Enter a number between 1 and {len(images)}.", fg=typer.colors.YELLOW)


@app.command()
def main(
    input_path: Optional[Path] = typer.Argument(None, help="Path to input image or folder"),
    out: Optional[Path] = typer.Option(None, "--out", help="Output file path"),
    quality: str = typer.Option("pro", "--quality", help="Processing level (fast/balanced/pro/max)"),
    background: str = typer.Option("transparent", "--background", help="Background replacement"),
    shadow: str = typer.Option("auto", "--shadow", help="Shadow behavior"),
    batch: bool = typer.Option(False, "--batch", help="Process folder"),
    preview: bool = typer.Option(False, "--preview", help="Save before/after preview"),
    debug: bool = typer.Option(False, "--debug", help="Save debug outputs"),
    report: bool = typer.Option(False, "--report", help="Save report JSON"),
    format: str = typer.Option("png", "--format", help="Output format"),
    device: str = typer.Option("auto", "--device", help="Device to use (auto/cpu/cuda)"),
    force_model: Optional[str] = typer.Option(None, "--force-model", hidden=True, help="Force specific model"),
):
    """
    Remove background from an image.
    """
    resolved_input = input_path or _choose_image_from_downloads(DOWNLOADS_DIR)
    if input_path is None:
        typer.secho(f"Selected: {resolved_input}", fg=typer.colors.BLUE)

    if not resolved_input.exists():
        _exit_with(f"Error: Input path {resolved_input} does not exist.")
    if batch:
        input_dir = resolved_input
        if not input_dir.is_dir():
            _exit_with(f"Error: {input_dir} is not a directory.")

        images = _list_download_images(input_dir)
        if not images:
            _exit_with(f"No images found in {input_dir}")

        typer.secho(f"Processing {len(images)} images in batch mode...", fg=typer.colors.CYAN)

        with typer.progressbar(images, label="Processing") as progress:
            for image_p in progress:
                try:
                    remove_background(
                        image_path=image_p,
                        output_path=None,  # Auto-generate name
                        quality=quality,
                        background=background,
                        shadow=shadow,
                        preview=preview,
                        debug=debug,
                        report=report,
                        device=device,
                        format=format,
                        force_model=force_model,
                    )
                except Exception as e:
                    typer.secho(f"\nError processing {image_p.name}: {e}", fg=typer.colors.RED)

        typer.secho("\nBatch processing complete!", fg=typer.colors.GREEN)
        raise typer.Exit(0)

    try:
        result = remove_background(
            image_path=resolved_input,
            output_path=out,
            quality=quality,
            background=background,
            shadow=shadow,
            preview=preview,
            debug=debug,
            report=report,
            device=device,
            format=format,
            force_model=force_model,
        )
        typer.secho(f"Success: Saved to {result.output_path}", fg=typer.colors.GREEN)
    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
