"""
Adım 5 — Montaj (ffmpeg): sahne kliplerini tek videoda birleştirir.
Her klibi hedef çözünürlüğe ölçekler/pad'ler, sonra birleştirir. GPU gerekmez (CPU runner yeter).
"""
import os, subprocess, tempfile
from . import config

def _normalize(girdi: str) -> str:
    cikti = tempfile.mktemp(suffix=".mp4")
    vf = (f"scale={config.GENISLIK}:{config.YUKSEKLIK}:force_original_aspect_ratio=decrease,"
          f"pad={config.GENISLIK}:{config.YUKSEKLIK}:(ow-iw)/2:(oh-ih)/2,setsar=1")
    subprocess.run(
        ["ffmpeg", "-y", "-i", girdi, "-vf", vf, "-r", "30",
         "-c:v", "libx264", "-c:a", "aac", "-ar", "44100", cikti],
        check=True, capture_output=True)
    return cikti

def birlestir(klip_yollari: list, cikti_yolu: str) -> str:
    normal = [_normalize(k) for k in klip_yollari]
    liste = tempfile.mktemp(suffix=".txt")
    with open(liste, "w") as f:
        for n in normal:
            f.write(f"file '{n}'\n")
    os.makedirs(os.path.dirname(cikti_yolu) or ".", exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", liste,
         "-c:v", "libx264", "-c:a", "aac", cikti_yolu],
        check=True, capture_output=True)
    return cikti_yolu
