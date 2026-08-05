"""
Merkezi ayarlar. Gizli anahtarlar ortam degiskeninden (GitHub Secrets) okunur.
Saglayici: fal.ai — acik kaynak modelleri API ile calistirir (Replicate alternatifi).
fal_client, FAL_KEY ortam degiskenini otomatik okur.
"""
import os

# --- Gizli anahtarlar ---
FAL_KEY        = os.environ.get("FAL_KEY", "")          # fal.ai API anahtari
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# YouTube yukleme (opsiyonel; YUKLE=1 ise gerekir)
YOUTUBE_CLIENT_ID     = os.environ.get("YOUTUBE_CLIENT_ID", "")
YOUTUBE_CLIENT_SECRET = os.environ.get("YOUTUBE_CLIENT_SECRET", "")
YOUTUBE_REFRESH_TOKEN = os.environ.get("YOUTUBE_REFRESH_TOKEN", "")

# --- Davranis ---
YUKLE      = os.environ.get("YUKLE", "0") == "1"
GENISLIK   = int(os.environ.get("GENISLIK", "1080"))   # montaj hedef cozunurluk (dikey Shorts)
YUKSEKLIK  = int(os.environ.get("YUKSEKLIK", "1920"))
DIL        = os.environ.get("DIL", "tr")
GORSEL_BOYUT  = os.environ.get("GORSEL_BOYUT", "portrait_16_9")  # fal FLUX en-boy (9:16 dikey)
KARAKTER_LORA = os.environ.get("KARAKTER_LORA", "")    # egitilmis karakter LoRA URL'si. Bos ise temel FLUX.
LORA_GUC   = float(os.environ.get("LORA_GUC", "1.0"))

# Siveyi konusan kisinin temiz ses ornegi (klonlama referansi). URL ya da repo ici yol.
SES_ORNEGI = os.environ.get("SES_ORNEGI", "data/ses_ornegi.wav")

# --- fal.ai model referanslari ---
MODEL_SES     = os.environ.get("MODEL_SES",     "fal-ai/f5-tts")     # zero-shot ses klonlama
# Not: Turkce/sive zayif gelirse MODEL_SES'i Turkce'si guclu bir modelle degistir
# (or. fal-ai/minimax/speech-02-turbo ya da fal uzerindeki ElevenLabs) - tek satir degisiklik.
MODEL_GORSEL  = os.environ.get("MODEL_GORSEL",  "fal-ai/flux-lora")  # FLUX + LoRA
MODEL_LIPSYNC = os.environ.get("MODEL_LIPSYNC", "fal-ai/sadtalker")  # gorsel+ses -> konusan klip

def dogrula():
    eksik = [k for k, v in {"FAL_KEY": FAL_KEY, "GEMINI_API_KEY": GEMINI_API_KEY}.items() if not v]
    if eksik:
        raise SystemExit(f"Eksik ortam degiskeni: {', '.join(eksik)}")
