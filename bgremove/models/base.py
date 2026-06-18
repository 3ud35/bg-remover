from typing import Protocol
from PIL import Image
import numpy as np

class BackgroundModel(Protocol):
    name: str

    def load(self, device: str) -> None:
        ...

    def predict_alpha(self, image: Image.Image) -> np.ndarray:
        ...
