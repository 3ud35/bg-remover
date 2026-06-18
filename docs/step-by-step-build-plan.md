# Build Plan: Production Background Remover CLI

## Goal

Build a Python CLI called `bgremove` where the user can run:

```bash
bgremove image.jpg
```

and receive:

```text
image-bgremoved.png
```

The user should not choose models. The app should automatically handle model selection, alpha output, edge refinement, fallback, batch mode, debug outputs, and future API-readiness.

---

# Phase 1 — Project Setup

## 1. Create Python package

Use this structure:

```text
bgremove/
├── pyproject.toml
├── README.md
├── bgremove/
│   ├── __init__.py
│   ├── cli.py
│   ├── pipeline.py
│   ├── config.py
│   ├── result.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── service.py
│   │   └── schemas.py
│   ├── io/
│   │   ├── __init__.py
│   │   ├── reader.py
│   │   └── writer.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── registry.py
│   │   └── birefnet.py
│   ├── processing/
│   │   ├── __init__.py
│   │   ├── preprocess.py
│   │   ├── alpha.py
│   │   ├── edges.py
│   │   ├── matting.py
│   │   ├── shadows.py
│   │   ├── compose.py
│   │   └── qa.py
│   └── utils/
│       ├── __init__.py
│       ├── device.py
│       └── logging.py
└── tests/
```

---

## 2. Dependencies

Use:

```toml
[project]
name = "bgremove"
version = "0.1.0"
dependencies = [
  "typer",
  "rich",
  "pillow",
  "numpy",
  "opencv-python",
  "torch",
  "torchvision",
  "transformers",
  "huggingface-hub",
  "pydantic"
]

[project.scripts]
bgremove = "bgremove.cli:app"
```

---

# Phase 2 — CLI Shell

## 3. Build `cli.py`

Create a Typer CLI supporting:

```bash
bgremove image.jpg
bgremove image.jpg --out output.png
bgremove folder/ --batch
bgremove image.jpg --quality pro
bgremove image.jpg --preview
bgremove image.jpg --debug
bgremove image.jpg --report
```

Options:

```python
input_path: Path
out: Optional[Path]
quality: str = "pro"
background: str = "transparent"
shadow: str = "auto"
batch: bool = False
preview: bool = False
debug: bool = False
report: bool = False
format: str = "png"
device: str = "auto"
```

Validation:

- Input must exist.
    
- If folder, require `--batch`.
    
- Default output should be `{stem}-bgremoved.png`.
    

---

# Phase 3 — Internal API Layer

## 4. Build `api/service.py`

Create one main function:

```python
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
) -> BackgroundRemovalResult:
```

The CLI should call this function.

---

## 5. Build `result.py`

Create a dataclass:

```python
@dataclass
class BackgroundRemovalResult:
    input_path: Path
    output_path: Path
    model_used: str
    fallback_used: bool
    quality_score: float
    edge_confidence: float
    halo_risk: str
    warnings: list[str]
    debug_dir: Optional[Path] = None
    report_path: Optional[Path] = None
```

---

# Phase 4 — Image I/O

## 6. Reader

`io/reader.py`

```python
def load_image(path: Path) -> Image.Image:
    # open image
    # convert to RGB
    # preserve EXIF orientation
```

---

## 7. Writer

`io/writer.py`

Functions:

```python
def save_rgba(image: Image.Image, path: Path) -> None
def save_alpha(alpha: np.ndarray, path: Path) -> None
def save_preview(original: Image.Image, result: Image.Image, path: Path) -> None
def save_report(report: dict, path: Path) -> None
```

Preview should create side-by-side:

- original
    
- result over checkerboard or white background
    

---

# Phase 5 — Model Abstraction

## 8. Base Model Interface

`models/base.py`

```python
class BackgroundModel(Protocol):
    name: str

    def load(self, device: str) -> None:
        ...

    def predict_alpha(self, image: Image.Image) -> np.ndarray:
        ...
```

Rules:

- Output alpha must be float32.
    
- Shape must match original image size.
    
- Values must be 0.0–1.0.
    

---

## 9. Model Registry

`models/registry.py`

```python
def get_model(name: str, device: str) -> BackgroundModel:
    ...
```

Also support:

```python
PRIMARY_MODELS = ["birefnet"]
```

---

# Phase 6 — First Working Model

## 10. Implement RMBG-2.0

`models/rmbg2.py`

Cursor task:

```text
Implement RMBG-2.0 using Hugging Face transformers.
Load model and processor lazily.
Accept PIL image.
Return alpha matte as float32 numpy array resized to original image size.
```

Requirements:

- Use GPU if available.
    
- Cache model after first load.
    
- Do not reload model for each image.
    
- Fail gracefully with clear error if weights cannot be downloaded.
    

---

# Phase 7 — Pipeline

## 11. Build `pipeline.py`

Create:

```python
class BackgroundRemovalPipeline:
    def __init__(self, quality="pro", background="transparent", shadow="auto", device="auto"):
        ...

    def run(self, image: Image.Image, debug_dir: Optional[Path] = None) -> PipelineOutput:
        ...
```

Pipeline:

```text
load image
→ choose strategy
→ run primary model
→ refine alpha
→ score quality
→ fallback if needed
→ compose RGBA
→ return output
```

---

## 12. Pipeline Output

```python
@dataclass
class PipelineOutput:
    rgba: Image.Image
    alpha: np.ndarray
    model_used: str
    fallback_used: bool
    quality_report: dict
    debug_images: dict[str, Image.Image]
```

---

# Phase 8 — Auto Engine

## 13. Image Analyzer

Add simple first version:

`processing/qa.py` or `processing/analyzer.py`

```python
def analyze_image(image: Image.Image) -> dict:
    return {
        "type": "auto",
        "low_contrast": bool,
        "has_many_edges": bool,
        "resolution": [w, h]
    }
```

Do not overbuild yet.

---

## 14. Strategy Selection

```python
def select_strategy(analysis: dict, quality: str) -> dict:
    return {
        "primary_model": "rmbg2",
        "fallback_models": ["birefnet"] if quality in ["pro", "max"] else [],
        "refinement": "general",
        "ensemble": quality == "max"
    }
```

Important:

- User never sees this.
    
- Hidden debug can print it.
    

---

# Phase 9 — Alpha Refinement

## 15. `processing/alpha.py`

Functions:

```python
def normalize_alpha(alpha: np.ndarray) -> np.ndarray
def clamp_alpha(alpha: np.ndarray) -> np.ndarray
def resize_alpha(alpha: np.ndarray, size: tuple[int, int]) -> np.ndarray
```

---

## 16. `processing/edges.py`

Functions:

```python
def get_edge_band(alpha: np.ndarray, low=0.05, high=0.95) -> np.ndarray
def feather_uncertain_edges(alpha: np.ndarray, radius: int = 2) -> np.ndarray
def remove_small_holes(alpha: np.ndarray) -> np.ndarray
def reduce_halo(image: Image.Image, alpha: np.ndarray) -> np.ndarray
```

Keep it conservative. Do not destroy hair detail.

---

## 17. `processing/matting.py`

Create:

```python
def refine_alpha(image: Image.Image, alpha: np.ndarray, mode: str = "general") -> np.ndarray:
    ...
```

Initial behavior:

- normalize
    
- smooth uncertain edge band
    
- preserve strong foreground/background
    
- avoid global blur
    

---

# Phase 10 — Compositing

## 18. `processing/compose.py`

```python
def compose_rgba(image: Image.Image, alpha: np.ndarray) -> Image.Image
def apply_background(rgba: Image.Image, background: str) -> Image.Image
```

Background values:

- transparent
    
- white
    
- black
    
- hex color
    
- image path
    

---

# Phase 11 — Quality Scoring

## 19. `processing/qa.py`

Implement:

```python
def score_alpha_quality(image: Image.Image, alpha: np.ndarray) -> dict:
    return {
        "quality_score": float,
        "edge_confidence": float,
        "halo_risk": "low" | "medium" | "high",
        "warnings": []
    }
```

Initial scoring can be heuristic:

- Too little foreground = warning
    
- Too much foreground = warning
    
- Very jagged edge = lower score
    
- Large holes = warning
    
- Alpha mostly binary = lower edge score
    

---

## 20. Fallback Trigger

Fallback if:

```python
quality_score < 0.82
edge_confidence < 0.70
halo_risk == "high"
```

For Phase 1, fallback can be stubbed until BiRefNet is implemented.

---

# Phase 12 — Debug + Report Outputs

## 21. Debug Mode

When `--debug`:

Create folder:

```text
debug/{input-stem}/
├── original.png
├── raw-alpha.png
├── refined-alpha.png
├── edge-band.png
├── final.png
├── preview.png
└── report.json
```

---

## 22. Report Mode

When `--report`:

Save:

```text
input-report.json
```

Also print readable summary:

```text
Model: rmbg2
Quality: 0.94
Edge confidence: 0.91
Halo risk: low
Fallback used: no
```

---

# Phase 13 — Batch Mode

## 23. Folder Processing

Support:

```bash
bgremove ./images --batch
```

Default output:

```text
./images/bgremoved/
```

Options:

- skip unsupported files
    
- continue on errors
    
- print summary
    

Supported:

- jpg
    
- jpeg
    
- png
    
- webp
    

---

# Phase 14 — BiRefNet Fallback

## 24. Implement `models/birefnet.py`

Cursor task:

```text
Add BiRefNet as fallback model.
Use same BackgroundModel interface.
Return alpha as float32 numpy array matching original dimensions.
```

Then enable actual fallback:

```text
RMBG result weak
→ run BiRefNet
→ refine alpha
→ score
→ choose better result
```

---

# Phase 15 — Production Polish

## 25. Logging

Use Rich:

- progress bars
    
- clear errors
    
- batch summary
    

---

## 26. Error Handling

Handle:

- missing file
    
- unsupported image
    
- model download failure
    
- CUDA unavailable
    
- output permission error
    

---

## 27. Tests

Add tests for:

- CLI default output path
    
- alpha range 0–1
    
- output is RGBA
    
- batch skips unsupported files
    
- report JSON exists
    
- fallback decision logic
    