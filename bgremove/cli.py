import typer
from pathlib import Path
from typing import Optional
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
    if resolved_input.is_dir() and not batch:
        _exit_with("Error: Input is a directory. Use --batch to process directories.")
    if batch:
        _exit_with("Batch mode not fully implemented yet.", color=typer.colors.YELLOW, code=0)

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
