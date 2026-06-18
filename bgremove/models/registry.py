from bgremove.models.base import BackgroundModel

PRIMARY_MODELS = ["birefnet"]

_model_cache = {}

def get_model(name: str, device: str) -> BackgroundModel:
    if name in _model_cache:
        return _model_cache[name]
        
    if name == "birefnet":
        from bgremove.models.birefnet import BiRefNetModel
        model = BiRefNetModel()
        model.load(device)
        _model_cache[name] = model
        return model
    else:
        raise ValueError(f"Model {name} not found in registry")
