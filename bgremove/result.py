from dataclasses import dataclass
from pathlib import Path
from typing import Optional

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
