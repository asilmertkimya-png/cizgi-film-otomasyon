"""
Adım 3 — Görsel (Replicate / SDXL veya FLUX): prompt -> karakter görseli (PNG).
Karakter tutarlılığı için MODEL_GORSEL'i, kendi eğittiğin karakter-LoRA modeline ayarla.
"""
import replicate
from . import config
from .utils import as_file

def uret(prompt: str) -> str:
    cikti = replicate.run(
        config.MODEL_GORSEL,
        input={
            "prompt": prompt,
            "width": config.GENISLIK,
            "height": config.YUKSEKLIK,
            "num_outputs": 1,
        },
    )
    ilk = cikti[0] if isinstance(cikti, (list, tuple)) else cikti
    return as_file(ilk, ".png")
