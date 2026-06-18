# 🧾 PRODUCT REQUIREMENTS DOCUMENT (PRD)

## Product Name

**bgremove**

---

## 🎯 Objective

Build a **production-grade, CLI-first background removal tool** that delivers **Canva-level quality** (comparable to Canva and remove.bg), while keeping the user experience extremely simple:

```bash
bgremove image.jpg
```

The system must automatically handle:

- Model selection
    
- Edge refinement
    
- Alpha matting
    
- Quality fallback
    

**User should not think about models. Ever.**

---

## 🧠 Core Product Philosophy

> **Simplicity outside, intelligence inside**

- CLI is minimal
    
- Pipeline is sophisticated
    
- Quality is non-negotiable
    
- Architecture is API-ready
    

---

## 👤 Target Users

- Developers building pipelines
    
- E-commerce sellers (product photos)
    
- Content creators
    
- Homesteaders / small business owners (your use case)
    
- Future SaaS/API users
    

---

# 🚫 Non-Negotiables

- Must output **true alpha transparency**
    
- Must handle:
    
    - Hair / fur
        
    - Soft edges
        
    - Shadows
        
    - Semi-transparent objects
        
- No visible:
    
    - Jagged edges
        
    - White halos
        
    - Missing subject parts
        
- Must support:
    
    - CPU + GPU
        
    - Batch processing
        
- Must be:
    
    - Fast
        
    - Deterministic
        
    - Extensible
        

---

# ⚙️ CLI DESIGN

## Default Usage (Primary UX)

```bash
bgremove input.jpg
```

Output:

```text
input-bgremoved.png
```

---

## Common Usage

```bash
bgremove input.jpg --out output.png
bgremove input.jpg --quality pro
bgremove input.jpg --background white
bgremove input.jpg --shadow soft
bgremove folder/ --batch
```

---

## CLI Options (User-Facing)

|Option|Values|Description|
|---|---|---|
|`--out`|path|Output file|
|`--quality`|fast / balanced / pro / max|Processing level|
|`--background`|transparent / color / image|Replace background|
|`--shadow`|auto / keep / soft / remove|Shadow behavior|
|`--batch`|flag|Process folder|
|`--preview`|flag|Save before/after|
|`--format`|png / webp|Output format|

---

## Hidden / Developer Options

|Option|Purpose|
|---|---|
|`--force-model`|Debug model selection|
|`--engine-debug`|Show pipeline decisions|
|`--save-alpha`|Save alpha matte|
|`--save-mask`|Save raw mask|
|`--disable-fallback`|Disable retries|

---

# 🧠 SYSTEM ARCHITECTURE

## High-Level Pipeline

```text
Input Image
→ Image Analyzer
→ Auto Strategy Selection
→ Primary Model Inference
→ Quality Check
→ Fallback / Ensemble (if needed)
→ Alpha Matte Refinement
→ Edge Cleanup
→ Shadow Processing
→ Background Handling
→ Output Image
```

---

# 🧩 AUTO ENGINE (CORE FEATURE)

## Requirement

User MUST NOT choose a model.

System decides internally:

```python
strategy = AutoEngine.select(image)
```

---

## Image Analyzer

Classifies:

- person
    
- animal
    
- product
    
- food
    
- multi-subject
    
- low contrast
    
- transparent object
    

---

## Strategy Selection

Example:

```python
if type == "person":
    models = ["rmbg2", "birefnet"]
    refinement = "hair"

elif type == "product":
    models = ["birefnet"]
    refinement = "clean_edge"

elif type == "animal":
    models = ["birefnet"]
    refinement = "general"

else:
    models = ["birefnet"]
    refinement = "general"
```

---

# 🤖 MODEL LAYER

## Supported Models

- BiRefNet (primary)
    

---

## Model Requirements

- Load once per process
    
- Support CPU/GPU
    
- Pluggable architecture
    

---

## Model Registry

```python
MODEL_REGISTRY = {
  "birefnet": BiRefNetModel()
}
```

---

# 🎨 IMAGE PROCESSING PIPELINE

## 1. Preprocessing

- Resize (keep aspect ratio)
    
- Normalize
    
- Enhance low-quality images
    

---

## 2. Segmentation

- Output: soft mask (not binary)
    
- Preserve probability values
    

---

## 3. Alpha Matting

Convert mask into:

- Smooth alpha transitions
    
- Preserve transparency zones
    

---

## 4. Edge Refinement

Focus only on uncertain regions:

```text
foreground (1.0)
background (0.0)
edges (0.1–0.9) → refine here
```

Must:

- Preserve hair/fur
    
- Remove halos
    
- Smooth edges naturally
    

---

## 5. Shadow Processing

Modes:

|Mode|Behavior|
|---|---|
|auto|detect best|
|keep|preserve|
|soft|reduce|
|remove|delete|

---

## 6. Background Handling

```bash
--background transparent
--background white
--background #f5f5f5
--background new.jpg
```

---

## 7. Output

- PNG (default)
    
- WebP (optional)
    
- Full resolution preserved
    

---

# 🧪 QUALITY SYSTEM

## Quality Levels

|Level|Behavior|
|---|---|
|fast|single model|
|balanced|+ refinement|
|pro|+ fallback|
|max|+ ensemble + QA scoring|

Default:

```bash
--quality pro
```

---

## Quality Checks

Evaluate:

- Edge smoothness
    
- Missing subject parts
    
- Transparency errors
    
- Halo detection
    
- Mask confidence
    

---

## Fallback Logic

```text
Run model A
→ quality check fails
→ run model B
→ compare outputs
→ choose best
```

---

# 📊 REPORTING SYSTEM

## CLI

```bash
bgremove image.jpg --report
```

## Output

```json
{
  "model_used": "rmbg2",
  "fallback_used": false,
  "quality_score": 0.94,
  "edge_confidence": 0.91,
  "halo_risk": "low"
}
```

---

# 🔍 DEBUG MODE

```bash
bgremove image.jpg --debug
```

Outputs:

```text
debug/
├── original.png
├── raw-mask.png
├── alpha.png
├── edge-map.png
├── final.png
└── report.json
```

---

# 📦 FILE STRUCTURE

```text
bgremove/
├── cli.py
├── pipeline.py
├── config.py
├── result.py
│
├── models/
│   ├── base.py
│   ├── rmbg2.py
│   ├── birefnet.py
│   ├── sam2.py
│   └── registry.py
│
├── processing/
│   ├── preprocess.py
│   ├── alpha.py
│   ├── edges.py
│   ├── matting.py
│   ├── shadows.py
│   ├── compose.py
│   └── qa.py
│
├── io/
│   ├── reader.py
│   ├── writer.py
│
├── api/
│   ├── service.py
│   ├── schemas.py
│
├── utils/
│   ├── device.py
│   ├── logging.py
│
└── tests/
```

---

# ⚡ PERFORMANCE TARGETS

|Metric|Target|
|---|---|
|GPU processing|< 1 sec|
|CPU processing|< 5 sec|
|Max image size|4K+|
|Batch support|Yes|

---

# 🔌 API-READY DESIGN

Internal function:

```python
remove_background(
    image_path,
    quality="pro",
    background="transparent",
    shadow="auto"
)
```

Future API:

```http
POST /remove-background
```

---

# 🚀 FUTURE FEATURES (PHASE 2)

- Prompt-based selection (“keep the dog”)
    
- Click/point segmentation
    
- Video background removal
    
- Real-time processing
    
- Mobile optimization
    
- GUI app
    

---

# ✅ DEFINITION OF DONE

The tool is complete when:

- `bgremove image.jpg` works flawlessly
    
- Produces clean transparent PNG
    
- Handles hair/fur correctly
    
- No halos or jagged edges
    
- Works on CPU and GPU
    
- Batch processing works
    
- Debug + report modes work
    
- Internal API exists
    

---

# 💡 FINAL NOTE

Your competitive advantage is NOT the model.

It’s:

- Smart auto engine
    
- Clean edges
    
- Reliability
    
- Simple UX
    
- Speed
    