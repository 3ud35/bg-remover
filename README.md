# bgremove

Portable background removal tool, CLI and GUI, powered by BiRefNet and Guided Filter Matting.

![Python](https://img.shields.io/badge/Python-3776AB.svg?style=flat-square&logo=Python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C.svg?style=flat-square&logo=PyTorch&logoColor=white)
![Gradio](https://img.shields.io/badge/Gradio-FFBB00.svg?style=flat-square&logo=Gradio&logoColor=black)
![Typer](https://img.shields.io/badge/Typer-000000.svg?style=flat-square&logo=Typer&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8.svg?style=flat-square&logo=OpenCV&logoColor=white)

This project started as a fork of [johneadams88/bg-remover-cli](https://github.com/johneadams88/bg-remover-cli) and has since diverged into a self-contained tool with a Gradio GUI, portable model storage, and an image-analysis driven refinement pipeline.

## Overview

`bgremove` removes backgrounds from images using the **BiRefNet** segmentation model, then refines the resulting alpha mask with **Guided Filter Matting** to recover fine detail around hair and complex edges. It runs either from the command line or through a local Gradio web interface, and keeps all downloaded model weights inside the project folder (`internal_models/`) instead of the user's home directory.

## Features

- **Portable model storage**: model weights and the Hugging Face cache live under `internal_models/`, isolated from the system-wide cache.
- **Gradio GUI**: drag-and-drop interface with live preview, served locally via `bgremove-gui`.
- **Image analysis**: inspects each image (hair, low contrast, extreme lighting) to pick a refinement strategy before running the model.
- **Guided Filter Matting**: alpha refinement pass tuned for hair/fur edges (`processing/matting.py`).
- **Quality scoring with automatic re-run**: if the initial alpha mask scores below threshold on quality/edge-confidence/halo-risk, the pipeline reprocesses with a fallback strategy (`pipeline.py`).
- **Shadows**: optional `drop` or `soft` shadow compositing.
- **Batch mode**: process a whole folder from the CLI with a progress bar.

## Installation

Requires Python 3.10+. A CUDA-capable GPU is optional but recommended for `pro`/`max` quality.

```bash
git clone https://github.com/3ud35/bg-remover.git
cd bg-remover

python3 -m venv .venv
source .venv/bin/activate

pip install -e .
```

On first run, `bgremove` downloads the BiRefNet weights from Hugging Face into `internal_models/` (roughly 400 MB).

## Usage

### GUI

```bash
bgremove-gui
```

Opens a local Gradio interface to upload an image, pick quality/background/shadow/format, and download the result.

### CLI

```bash
bgremove path/to/image.png --quality pro --shadow drop
```

Batch mode processes every image in a folder:

```bash
bgremove ./input_folder --batch --out ./output_folder --preview
```

### CLI options

| Option | Default | Description |
| --- | --- | --- |
| `input_path` | — | Path to an image or, with `--batch`, a folder |
| `--out` | auto | Output file path (single image mode) |
| `--quality` | `pro` | `fast` / `balanced` / `pro` / `max` |
| `--background` | `transparent` | `transparent`, a named color, or a hex code (`#f0f0f0`) |
| `--shadow` | `auto` | `none` / `drop` / `soft` / `auto` |
| `--batch` | off | Treat `input_path` as a folder and process every image in it |
| `--preview` | off | Save a before/after preview image |
| `--debug` | off | Save intermediate masks (raw alpha, refined alpha) |
| `--report` | off | Save a JSON quality report |
| `--format` | `png` | Output image format |
| `--device` | `auto` | `auto` / `cpu` / `cuda` |

## Project structure

```
bgremove/
├── cli.py               # Typer CLI entry point
├── gui.py                # Gradio GUI entry point
├── pipeline.py           # Orchestrates analysis, model inference, refinement, fallback
├── result.py             # Result dataclasses
├── api/
│   └── service.py        # High-level remove_background() API
├── io/
│   ├── reader.py          # Image loading
│   └── writer.py          # Output saving
├── models/
│   ├── base.py             # Model interface
│   ├── birefnet.py         # BiRefNet inference wrapper
│   └── registry.py         # Model lookup/instantiation
├── processing/
│   ├── qa.py                # Image analysis, strategy selection, quality scoring
│   ├── matting.py           # Guided filter alpha refinement
│   ├── alpha.py              # Alpha channel utilities
│   ├── edges.py               # Edge detection helpers
│   └── compose.py             # Background/shadow compositing
└── utils/
    └── config.py            # Portable model/cache directory setup
```

## Roadmap

- [x] BiRefNet as the primary segmentation model
- [x] Portable model storage (`internal_models/`)
- [x] Gradio GUI
- [x] Guided Filter Matting refinement
- [ ] Secondary model (IS-Net) as a real fallback for low-contrast cases
- [ ] PyInstaller packaging for standalone Win/Mac/Linux executables
- [ ] Video background removal

## Testing

```bash
pytest
```

## Acknowledgments

- [johneadams88/bg-remover-cli](https://github.com/johneadams88/bg-remover-cli) — the original project this repository was forked from.
- [BiRefNet](https://github.com/ZhengPeng7/BiRefNet) — the segmentation model used for background removal.
- [Hugging Face](https://huggingface.co/) — hosts and serves the model weights.

## License

MIT. See [LICENSE](LICENSE).
