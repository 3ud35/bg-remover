<div id="top">

<!-- HEADER STYLE: MODERN -->
<div align="left" style="position: relative; width: 100%; height: 100%; ">

<img src="readmeai/assets/logos/purple.svg" width="30%" style="position: absolute; top: 0; right: 0;" alt="Project Logo"/>

# <code>bgremove</code>

*Powerful, Zero-Install Background Removal with CLI and GUI.*

<!-- BADGES -->
<!-- local repository, no metadata badges. -->

<em>Built with professional-grade tools:</em>

<img src="https://img.shields.io/badge/Gradio-FFBB00.svg?style=flat-square&logo=Gradio&logoColor=black" alt="Gradio">
<img src="https://img.shields.io/badge/PyTorch-EE4C2C.svg?style=flat-square&logo=PyTorch&logoColor=white" alt="PyTorch">
<img src="https://img.shields.io/badge/Typer-000000.svg?style=flat-square&logo=Typer&logoColor=white" alt="Typer">
<img src="https://img.shields.io/badge/OpenCV-5C3EE8.svg?style=flat-square&logo=OpenCV&logoColor=white" alt="OpenCV">
<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat-square&logo=Python&logoColor=white" alt="Python">

</div>
</div>

<br clear="right">

---

## 🔴 Overview

`bgremove` is a high-performance background removal tool designed to be **completely portable and autonomous**. It leverages the state-of-the-art **BiRefNet** model combined with **Guided Filter Matting** to provide studio-quality results for both objects and complex subjects like hair or fur.

Whether you are a developer looking for a scriptable CLI or a user needing a simple drag-and-drop interface, `bgremove` handles everything—including automatic environment setup and local model confinement.

---

## 🟠 Features

*   **🚀 Zero-Install Ready**: Designed for portability. All models and caches are stored locally in the application folder (`internal_models`), ensuring a "clean" installation.
*   **🎨 Pro UI**: Full-featured **Gradio** interface for interactive processing with real-time previews.
*   **🔍 Intelligent Analysis**: Automatically detects image complexity (hair, low contrast, extreme lighting) to apply specialized refinement strategies.
*   **✂️ Guided Filter Matting**: Professional-grade alpha refinement that recovers fine details around hair and complex edges.
*   **🌑 Advanced Shadows**: Built-in support for realistic `drop` and `soft` shadows.
*   **📦 Batch Processing**: Command-line support for processing entire folders with progress tracking.
*   **⚡ Multiple Qualities**: Modes ranging from `fast` to `max` to balance speed and pixel-perfection.

---

## 🔵 Getting Started

### 🟣 Prerequisites

*   **Python 3.10+** (if running from source)
*   **CUDA** (optional, for ultra-fast GPU processing)

### ⚫ Installation (Source)

```bash
# Clone the repository
git clone https://github.com/3ud35/bg-remover.git
cd bg-remover

# Create and activate environment
python3 -m venv .venv
source .venv/bin/activate

# Install in editable mode
pip install -e .
```

---

## ⚪ Usage

### 🖥️ GUI (Recommended)
Launch the interactive web interface:
```bash
bgremove-gui
```

### ⌨️ CLI
Remove background from a single image:
```bash
bgremove myimage.jpg --quality pro --shadow drop
```

Process a whole folder (Batch mode):
```bash
bgremove ./input_folder --batch --out ./output_folder --preview
```

---

## 🌟 Roadmap

*   [x] **Logic Confinement**: Isolated `internal_models` storage.
*   [x] **Gradio GUI**: Interactive drag-and-drop interface.
*   [x] **Advanced Matting**: Guided Filter implementation.
*   [ ] **PyInstaller Packaging**: Standalone executables for Win/Mac/Linux.
*   [ ] **Secondary Model**: Fallback to IS-Net for low-contrast cases.

---

## 🟡 Project Structure

```sh
└── bg-remover-cli/
    ├── README.md
    ├── bgremove
    │   ├── __init__.py
    │   ├── api
    │   ├── cli.py
    │   ├── io
    │   ├── models
    │   ├── pipeline.py
    │   ├── processing
    │   ├── result.py
    │   └── utils
    ├── docs
    │   ├── product-requirements-document.md
    │   └── step-by-step-build-plan.md
    ├── pyproject.toml
    └── tests
        └── __init__.py
```

### 🟢 Project Index

<details open>
	<summary><b><code>/</code></b></summary>
	<!-- __root__ Submodule -->
	<details>
		<summary><b>Root Files</b></summary>
		<blockquote>
			<table>
			<thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<th style='padding: 8px; text-align: left;'>File</th>
					<th style='padding: 8px; text-align: left;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='/pyproject.toml'>pyproject.toml</a></b></td>
					<td style='padding: 8px;'>Core project configuration and metadata.</td>
				</tr>
			</table>
		</blockquote>
	</details>
	<!-- bgremove Submodule -->
	<details>
		<summary><b>bgremove</b></summary>
		<blockquote>
			<table>
			<thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<th style='padding: 8px; text-align: left;'>File</th>
					<th style='padding: 8px; text-align: left;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='/bgremove/result.py'>result.py</a></b></td>
					<td style='padding: 8px;'>Image processing result classes and data structures.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='/bgremove/cli.py'>cli.py</a></b></td>
					<td style='padding: 8px;'>Main CLI entry point and command-line argument handling.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='/bgremove/pipeline.py'>pipeline.py</a></b></td>
					<td style='padding: 8px;'>Orchestrates the image processing workflow and model selection.</td>
				</tr>
			</table>
			<!-- processing Submodule -->
			<details>
				<summary><b>processing</b></summary>
				<blockquote>
					<table>
					<thead>
						<tr style='border-bottom: 1px solid #eee;'>
							<th style='padding: 8px; text-align: left;'>File</th>
							<th style='padding: 8px; text-align: left;'>Summary</th>
						</tr>
					</thead>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='/bgremove/processing/compose.py'>compose.py</a></b></td>
							<td style='padding: 8px;'>Handles alpha compositing and background replacement.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='/bgremove/processing/edges.py'>edges.py</a></b></td>
							<td style='padding: 8px;'>Edge detection and alpha mask refinement logic.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='/bgremove/processing/matting.py'>matting.py</a></b></td>
							<td style='padding: 8px;'>Soft matting and transparency processing.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='/bgremove/processing/alpha.py'>alpha.py</a></b></td>
							<td style='padding: 8px;'>Alpha channel generation and manipulation.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='/bgremove/processing/qa.py'>qa.py</a></b></td>
							<td style='padding: 8px;'>Quality assurance metrics and model strategy selection.</td>
						</tr>
					</table>
				</blockquote>
			</details>
			<!-- io Submodule -->
			<details>
				<summary><b>io</b></summary>
				<blockquote>
					<table>
					<thead>
						<tr style='border-bottom: 1px solid #eee;'>
							<th style='padding: 8px; text-align: left;'>File</th>
							<th style='padding: 8px; text-align: left;'>Summary</th>
						</tr>
					</thead>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='/bgremove/io/reader.py'>reader.py</a></b></td>
							<td style='padding: 8px;'>Image loading and preprocessing utilities.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='/bgremove/io/writer.py'>writer.py</a></b></td>
							<td style='padding: 8px;'>Output saving and export management.</td>
						</tr>
					</table>
				</blockquote>
			</details>
			<!-- models Submodule -->
			<details>
				<summary><b>models</b></summary>
				<blockquote>
					<table>
					<thead>
						<tr style='border-bottom: 1px solid #eee;'>
							<th style='padding: 8px; text-align: left;'>File</th>
							<th style='padding: 8px; text-align: left;'>Summary</th>
						</tr>
					</thead>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='/bgremove/models/registry.py'>registry.py</a></b></td>
							<td style='padding: 8px;'>Dynamic model registration and loading factory.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='/bgremove/models/birefnet.py'>birefnet.py</a></b></td>
							<td style='padding: 8px;'>BiRefNet model implementation and inference wrapper.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='/bgremove/models/base.py'>base.py</a></b></td>
							<td style='padding: 8px;'>Base classes for image segmentation models.</td>
						</tr>
					</table>
				</blockquote>
			</details>
		</blockquote>
	</details>
</details>

---

## 🔵 Getting Started

### 🟣 Prerequisites

*   **Python 3.10+**
*   **NVIDIA GPU** (Recommended for "pro" quality performance)
*   **FFmpeg** (Optional, for advanced compositing)

### ⚫ Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/Fr0z3nRebel/bg-remover-cli.git
    ```

2. **Navigate to the project directory:**
    ```sh
    cd bg-remover-cli
    ```

3. **Install the dependencies:**
    ```sh
    pip install -e .
    ```

### ⚪ Usage

Run the project with:
```sh
bgremove path/to/your/image.png --quality pro --debug --report
```

### 🟤 Testing

This project uses `pytest`. Run the test suite with:
```sh
pytest
```

---

## 🌟 Roadmap

- [X] **`Task 1`**: Integrate BiRefNet as primary commercial-friendly model.
- [ ] **`Task 2`**: Implement batch processing mode.
- [ ] **`Task 3`**: Add support for video background removal.
- [ ] **`Task 4`**: Vers une application portable autonome (voir [TODO.md](TODO.md)).

---

## 🤝 Contributing

Contributions are welcome! Whether it's a bug report, a new feature, or a documentation fix, we value your help.

1. **Fork the Repository**: Create your own copy of the project.
2. **Clone Locally**: `git clone https://github.com/Fr0z3nRebel/bg-remover-cli.git`
3. **Create a Branch**: `git checkout -b feature/my-new-feature`
4. **Commit & Push**: Make your changes and push them to your fork.
5. **Submit a PR**: Open a Pull Request against the main branch.

- **💬 [Join the Discussions](https://github.com/Fr0z3nRebel/bg-remover-cli/discussions)**
- **🐛 [Report Issues](https://github.com/Fr0z3nRebel/bg-remover-cli/issues)**
- **💡 [Submit Pull Requests](https://github.com/Fr0z3nRebel/bg-remover-cli/pulls)**

---

## 📜 License

This project is protected under the **MIT License**. See the `LICENSE` file for details.

---

## ✨ Acknowledgments

- [BiRefNet](https://github.com/ZhengPeng7/BiRefNet) for the bilateral reference network for high-resolution background removal.
- [Hugging Face](https://huggingface.co/) for providing the infrastructure to host and serve model weights.
- [readme-ai](https://github.com/eli64s/readme-ai) for the automated README generation and structure.

---

### 🛠️ Behind the Scenes
Curious about how this was built or want to see more "Vibe Coding" projects? Check out the deep dive on [DevsPlsFix.com](https://devsplsfix.com).

<div align="right">

[![][back-to-top]](#top)

</div>

[back-to-top]: https://img.shields.io/badge/-BACK_TO_TOP-151515?style=flat-square

---
