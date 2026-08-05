"""
Adım 4 — Konuşturma / lip-sync (Replicate): görsel + ses -> konuşan klip (MP4).
Uyarı: bazı modeller gerçek yüz için eğitilmiştir; çizgi yüzde iyi çalışanı önceden test et
(Wav2Lip / SadTalker / LivePortrait). Model seçimini MODEL_LIPSYNC ile değiştir.
"""
import replicate
from . import config
from .utils import as_file

def uret(gorsel_yolu: str, ses_yolu: str) -> str:
    cikti = replicate.run(
        config.MODEL_LIPSYNC,
        input={
            "source_image": open(gorsel_yolu, "rb"),
            "driven_audio": open(ses_yolu, "rb"),
        },
    )
    return as_file(cikti, ".mp4")
