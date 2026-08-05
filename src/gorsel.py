"""
Adım 3 — Görsel (Replicate / FLUX): prompt -> karakter görseli (PNG).
FLUX 'aspect_ratio' bekler (SDXL gibi genişlik/yükseklik değil).
Karakter tutarlılığı için KARAKTER_LORA ayarlandığında eğitilmiş LoRA uygulanır;
boşsa temel FLUX ile üretir (LoRA'yı sonra eğitip env'e ekleyebilirsin).
"""
import replicate
from . import config
from .utils import as_file

def uret(prompt: str) -> str:
    girdi = {
        "prompt": prompt,
        "aspect_ratio": config.EN_BOY,   # örn "9:16" (dikey Shorts)
        "num_outputs": 1,
        "output_format": "png",
    }
    if config.KARAKTER_LORA:
        girdi["lora_weights"] = config.KARAKTER_LORA
        girdi["lora_scale"] = config.LORA_GUC
    cikti = replicate.run(config.MODEL_GORSEL, input=girdi)
    ilk = cikti[0] if isinstance(cikti, (list, tuple)) else cikti
    return as_file(ilk, ".png")
