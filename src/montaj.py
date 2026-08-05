"""
Adim 4+5 — Montaj (ffmpeg, UCRETSIZ, CPU): her sahne = gorsel + ses + altyazi (Ken Burns yavas zoom),
sonra tum sahneler birlestirilir. Lip-sync yok (ucretli surumde eklenir); taslak icin gorsel+ses+yazi akar.
"""
import os, subprocess, tempfile, textwrap
from . import config

def _sure(ses: str) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", ses], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 2.0

def _ts(t: float) -> str:
    h = int(t // 3600); m = int(t % 3600 // 60); s = t - 3600*h - 60*m
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")

def _srt(metin: str, sure: float, yol: str):
    sar = "\n".join(textwrap.wrap(metin, 30)) or metin
    open(yol, "w", encoding="utf-8").write(f"1\n{_ts(0)} --> {_ts(sure)}\n{sar}\n")

def sahne_klip(gorsel: str, ses: str, metin: str) -> str:
    sure = _sure(ses) + 0.3
    srt = tempfile.mktemp(suffix=".srt"); _srt(metin, sure, srt)
    out = tempfile.mktemp(suffix=".mp4")
    W, H, F = config.GENISLIK, config.YUKSEKLIK, config.FPS
    kare = int(sure * F)
    fc = (f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
          f"zoompan=z='min(1+0.0007*on,1.15)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
          f"d={kare}:s={W}x{H}:fps={F},"
          f"subtitles={srt}:force_style='Fontsize=14,Bold=1,PrimaryColour=&H00FFFFFF&,"
          f"OutlineColour=&H00000000&,BorderStyle=1,Outline=3,Shadow=1,Alignment=2,MarginV=90'[v]")
    subprocess.run(["ffmpeg", "-y", "-loop", "1", "-t", f"{sure}", "-i", gorsel, "-i", ses,
                    "-filter_complex", fc, "-map", "[v]", "-map", "1:a", "-r", str(F),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", out],
                   check=True, capture_output=True)
    return out

def birlestir(klipler: list, cikti: str) -> str:
    liste = tempfile.mktemp(suffix=".txt")
    with open(liste, "w") as f:
        for k in klipler:
            f.write(f"file '{k}'\n")
    os.makedirs(os.path.dirname(cikti) or ".", exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", liste,
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", cikti],
                   check=True, capture_output=True)
    return cikti
