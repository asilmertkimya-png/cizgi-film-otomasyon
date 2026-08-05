"""
Adim 3 — Gorsel (fal.ai / FLUX-LoRA): prompt -> karakter gorseli (PNG).
KARAKTER_LORA ayarliysa egitilmis LoRA uygulanir; bos ise temel FLUX.
"""
import fal_client
from . import config
from .utils import indir

def uret(prompt: str) -> str:
    args = {
        "prompt": prompt,
        "image_size": config.GORSEL_BOYUT,   # or. "portrait_16_9" (dikey)
        "num_images": 1,
    }
    if config.KARAKTER_LORA:
        args["loras"] = [{"path": config.KARAKTER_LORA, "scale": config.LORA_GUC}]
    sonuc = fal_client.subscribe(config.MODEL_GORSEL, arguments=args, with_logs=False)
    return indir(sonuc["images"][0]["url"], ".png")
