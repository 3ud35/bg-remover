import os
import sys
from pathlib import Path


def get_app_root() -> Path:
    """
    Returns the root directory of the application.
    If running as a frozen executable (e.g., PyInstaller), returns the directory of the executable.
    Otherwise, returns the parent directory of this file (assuming structure bgremove/utils/config.py).
    """
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    # This file is in bgremove/utils/config.py, so we go up 2 levels
    return Path(__file__).resolve().parent.parent.parent


def setup_portable_environment():
    """
    Configure environment variables to point to local application directories.
    This ensures models and caches are stored within the application folder.
    """
    app_root = get_app_root()
    models_dir = app_root / "internal_models"
    cache_dir = models_dir / "cache"
    shared = os.environ.get("HF_HUB_CACHE")
    if shared and Path(shared).is_dir():
        # Poids des modèles centralisés (voir ~/Code/alfred/ai-models) ; le reste reste local
        cache_dir = Path(shared)

    # Create directories if they don't exist
    models_dir.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)

    # Set Hugging Face home and cache directories
    os.environ["HF_HOME"] = str(models_dir)
    os.environ["HUGGINGFACE_HUB_CACHE"] = str(cache_dir)
    os.environ["TRANSFORMERS_CACHE"] = str(cache_dir)

    # Optionally isolate other potential home-based caches
    os.environ.setdefault("TORCH_HOME", str(models_dir / "torch"))

    return models_dir, cache_dir


# Export commonly used paths
APP_ROOT = get_app_root()
MODELS_DIR = APP_ROOT / "internal_models"
