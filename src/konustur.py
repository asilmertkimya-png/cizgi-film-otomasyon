"""
Adim 4 — Konusturma / lip-sync (fal.ai / SadTalker): gorsel + ses -> konusan klip (MP4).
Gorsel ve sesi fal'a yukler, URL verir; sonucu indirir.
Uyari: cizgi yuzde iyi calisan modeli onceden test et (SadTalker/Wav2Lip/LatentSync).
"""
import fal_client
from . import config
from .utils import indir

def uret(gorsel_yolu: str, ses_yolu: str) -> str:
    img_url = fal_client.upload_file(gorsel_yolu)
    aud_url = fal_client.upload_file(ses_yolu)
    sonuc = fal_client.subscribe(config.MODEL_LIPSYNC, arguments={
        "source_image_url": img_url,
        "driven_audio_url": aud_url,
    }, with_logs=False)
    video = sonuc.get("video")
    url = video.get("url") if isinstance(video, dict) else video
    return indir(url, ".mp4")
