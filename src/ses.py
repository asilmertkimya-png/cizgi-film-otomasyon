"""
Adim 2 — Ses (fal.ai / F5-TTS): metin + referans ses -> klonlanmis seste WAV.
Referans sesi fal'a yukler, URL alir; sonucu yerel dosyaya indirir.
Not: Turkce/sive kalitesi zayifsa MODEL_SES'i degistir (config.py).
"""
import fal_client
from . import config
from .utils import indir

def _ses_url(sonuc: dict) -> str:
    for anahtar in ("audio_url", "audio"):
        deger = sonuc.get(anahtar)
        if isinstance(deger, dict):
            return deger.get("url")
        if isinstance(deger, str):
            return deger
    raise RuntimeError(f"Ses cikti URL'si bulunamadi: {sonuc}")

def uret(replik: str, ses_ornegi: str = None) -> str:
    ses_ornegi = ses_ornegi or config.SES_ORNEGI
    ref_url = ses_ornegi if ses_ornegi.startswith("http") else fal_client.upload_file(ses_ornegi)
    sonuc = fal_client.subscribe(config.MODEL_SES, arguments={
        "gen_text": replik,
        "ref_audio_url": ref_url,
        "model_type": "F5-TTS",
        "remove_silence": True,
    }, with_logs=False)
    return indir(_ses_url(sonuc), ".wav")
