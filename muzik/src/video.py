"""Adim 3 — Muzik video (ffmpeg): ses + baslik + sozler -> dalga formu gorselli lyric video (MP4)."""
import os, subprocess, tempfile, glob
from . import config

def _sure(ses):
    r = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
                        "-of","default=nw=1:nk=1",ses], capture_output=True, text=True)
    try: return float(r.stdout.strip())
    except ValueError: return float(config.SES_SANIYE)

def _ts(t):
    h=int(t//3600); m=int(t%3600//60); s=t-3600*h-60*m
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".",",")

def _srt(sozler, sure, yol):
    n=max(1,len(sozler)); pay=sure/n
    with open(yol,"w",encoding="utf-8") as f:
        for i,dize in enumerate(sozler):
            f.write(f"{i+1}\n{_ts(i*pay)} --> {_ts((i+1)*pay)}\n{dize}\n\n")

def _font():
    p="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    if os.path.exists(p): return p
    c=glob.glob("/usr/share/fonts/**/DejaVuSans-Bold.ttf",recursive=True)
    return c[0] if c else p

def uret(ses, baslik, sozler, cikti):
    sure=_sure(ses)
    srt=tempfile.mktemp(suffix=".srt"); _srt(sozler,sure,srt)
    bfile=tempfile.mktemp(suffix=".txt"); open(bfile,"w",encoding="utf-8").write(baslik)
    W,H,F=config.GENISLIK,config.YUKSEKLIK,config.FPS; font=_font()
    fc=(f"[1:a]showwaves=s={W}x480:mode=cline:rate={F}:colors={config.DALGA_RENK}[wv];"
        f"[0:v][wv]overlay=(W-w)/2:(H-h)/2[bgw];"
        f"[bgw]drawtext=fontfile={font}:textfile={bfile}:fontcolor=white:fontsize=70:"
        f"x=(w-text_w)/2:y=180:box=1:boxcolor=0x00000099:boxborderw=24[t];"
        f"[t]subtitles={srt}:force_style='FontName=DejaVu Sans,Fontsize=15,Bold=1,"
        f"PrimaryColour=&H00FFFFFF&,OutlineColour=&H00000000&,BorderStyle=1,Outline=3,Alignment=2,MarginV=380'[v]")
    os.makedirs(os.path.dirname(cikti) or ".",exist_ok=True)
    subprocess.run(["ffmpeg","-y","-f","lavfi","-i",f"color=c={config.BG_RENK}:s={W}x{H}:d={sure}",
        "-i",ses,"-filter_complex",fc,"-map","[v]","-map","1:a","-t",f"{sure}","-r",str(F),
        "-c:v","libx264","-pix_fmt","yuv420p","-c:a","aac","-shortest",cikti],
        check=True, capture_output=True)
    return cikti
