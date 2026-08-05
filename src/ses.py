"""
Adım 2 — Ses (Replicate / XTTS): metin + şiveli ses örneği -> klonlanmış seste WAV.
Not: Tam otonom yol budur. En OTANTİK şive için RVC (sesten-sese) tercih et:
gerçek kişi repliği şiveyle söyler, RVC modeli karakter sesine çevirir.
"""
import replicate
from . import config
from .utils import as_file

def uret(replik: str, ses_ornegi: str = None) -> str:
    ses_ornegi = ses_ornegi or config.SES_ORNEGI
    cikti = replicate.run(
        config.MODEL_SES,
        input={
            "text": replik,
            "language": config.DIL,
            "speaker": open(ses_ornegi, "rb") if not ses_ornegi.startswith("http") else ses_ornegi,
        },
    )
    return as_file(cikti, ".wav")
