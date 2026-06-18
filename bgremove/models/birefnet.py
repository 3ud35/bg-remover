import numpy as np
from PIL import Image
from bgremove.models.base import BackgroundModel
import torch
from transformers import AutoModelForImageSegmentation
from torchvision import transforms

class BiRefNetModel(BackgroundModel):
    name = "birefnet"

    def __init__(self):
        self.model = None
        self.device = None
        self.transform = None

    def load(self, device: str) -> None:
        if self.model is not None:
            return

        if device == "auto":
            self.device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
        else:
            self.device = device
            
        try:
            self.model = AutoModelForImageSegmentation.from_pretrained(
                "ZhengPeng7/BiRefNet", trust_remote_code=True
            )
            self.model.to(self.device)
            self.model.eval()
            
            self.transform = transforms.Compose([
                transforms.Resize((1024, 1024)),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ])
        except Exception as e:
            raise RuntimeError(f"Failed to load BiRefNet model: {e}")

    def predict_alpha(self, image: Image.Image) -> np.ndarray:
        if self.model is None:
            raise RuntimeError("Model not loaded. Call load() first.")
            
        orig_size = image.size
        img_rgb = image.convert("RGB")
        input_tensor = self.transform(img_rgb).unsqueeze(0).to(self.device)
        
        # Cast input to match model dtype
        model_dtype = next(self.model.parameters()).dtype
        input_tensor = input_tensor.to(dtype=model_dtype)

        with torch.no_grad():
            preds = self.model(input_tensor)[-1].sigmoid().cpu()
            
        pred = preds[0].squeeze()
        pred_img = transforms.ToPILImage()(pred)
        pred_img = pred_img.resize(orig_size, resample=Image.Resampling.BILINEAR)
        return np.array(pred_img, dtype=np.float32) / 255.0
