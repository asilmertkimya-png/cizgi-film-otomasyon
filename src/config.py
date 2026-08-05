"""
Bedava otonom surum ayarlari (taslak/demo).
Ucretsiz yigin: Gemini (senaryo) + edge-tts (ses) + Pollinations (gorsel) + ffmpeg (montaj).
Tek gerekli secret: GEMINI_API_KEY (ucretsiz katman). Diger servisler anahtarsiz.
"""
import os

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# YouTube yukleme (opsiyonel; YUKLE=1 ise gerekir)
YOUTUBE_CLIENT_ID     = os.environ.get("YOUTUBE_CLIENT_ID", "")
YOUTUBE_CLIENT_SECRET = os.environ.get("YOUTUBE_CLIENT_SECRET", "")
YOUTUBE_REFRESH_TOKEN = os.environ.get("YOUTUBE_REFRESH_TOKEN", "")
YUKLE = os.environ.get("YUKLE", "0") == "1"

GENISLIK  = int(os.environ.get("GENISLIK", "1080"))   # dikey Shorts
YUKSEKLIK = int(os.environ.get("YUKSEKLIK", "1920"))
FPS       = int(os.environ.get("FPS", "30"))

# Ses (edge-tts, ucretsiz Turkce neural sesler)
SES_ERKEK = os.environ.get("SES_ERKEK", "tr-TR-AhmetNeural")
SES_KADIN = os.environ.get("SES_KADIN", "tr-TR-EmelNeural")

# Gorsel (Pollinations.ai, ucretsiz, anahtarsiz)
POLLINATIONS_KEY = os.environ.get("POLLINATIONS_KEY", "")  # opsiyonel; ucretsiz anahtar (enter.pollinations.ai)
GORSEL_MODEL  = os.environ.get("GORSEL_MODEL", "flux")
KARAKTER_SEED = int(os.environ.get("KARAKTER_SEED", "4242"))  # sabit seed -> daha tutarli karakter
STIL = os.environ.get("STIL",
    "cute 2D cartoon, flat colors, thick outlines, children's storybook style, simple background, no text")

def dogrula():
    if not GEMINI_API_KEY:
        raise SystemExit("Eksik ortam degiskeni: GEMINI_API_KEY")
