"""
Bedava, otonom AI muzik + soz + yayin sistemi ayarlari.
Yigin: Gemini (soz/konsept) + MusicGen (acik kaynak enstrumantal) + ffmpeg (muzik-video) + YouTube.
Tek gerekli secret: GEMINI_API_KEY (ucretsiz). Muzik ve video ucretsiz/anahtarsiz.
"""
import os

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# YouTube (opsiyonel; YUKLE=1 ise gerekir)
YOUTUBE_CLIENT_ID     = os.environ.get("YOUTUBE_CLIENT_ID", "")
YOUTUBE_CLIENT_SECRET = os.environ.get("YOUTUBE_CLIENT_SECRET", "")
YOUTUBE_REFRESH_TOKEN = os.environ.get("YOUTUBE_REFRESH_TOKEN", "")
YUKLE = os.environ.get("YUKLE", "0") == "1"

# Video
GENISLIK  = int(os.environ.get("GENISLIK", "1080"))
YUKSEKLIK = int(os.environ.get("YUKSEKLIK", "1920"))
FPS       = int(os.environ.get("FPS", "30"))
BG_RENK   = os.environ.get("BG_RENK", "0x0b1e3a")     # koyu gradyan taban
DALGA_RENK= os.environ.get("DALGA_RENK", "0x4fd1ff|0x9b5cff")

# Muzik (MusicGen, acik kaynak; Actions'ta CPU'da calisir)
MUSICGEN_MODEL = os.environ.get("MUSICGEN_MODEL", "facebook/musicgen-small")
SES_SANIYE     = int(os.environ.get("SES_SANIYE", "30"))   # parca uzunlugu (~30s tek uretim)

def dogrula():
    if not GEMINI_API_KEY:
        raise SystemExit("Eksik ortam degiskeni: GEMINI_API_KEY")
