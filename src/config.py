"""
Merkezi ayarlar. Tüm gizli anahtarlar ortam değişkeninden (GitHub Secrets) okunur.
Replicate model sürümleri ZAMANLA DEĞİŞİR — replicate.com'da güncel sürümü bulup
aşağıdaki ortam değişkenleriyle sabitle (pinle). Varsayılanlar yalnızca örnektir.
"""
import os

# --- Gizli anahtarlar (GitHub Secrets / .env) ---
REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN", "")
GEMINI_API_KEY      = os.environ.get("GEMINI_API_KEY", "")

# YouTube yükleme (opsiyonel; YUKLE=1 ise gerekir)
YOUTUBE_CLIENT_ID     = os.environ.get("YOUTUBE_CLIENT_ID", "")
YOUTUBE_CLIENT_SECRET = os.environ.get("YOUTUBE_CLIENT_SECRET", "")
YOUTUBE_REFRESH_TOKEN = os.environ.get("YOUTUBE_REFRESH_TOKEN", "")

# --- Davranış ---
YUKLE      = os.environ.get("YUKLE", "0") == "1"      # 1 ise YouTube'a yükler
GENISLIK   = int(os.environ.get("GENISLIK", "1080"))  # dikey Shorts: 1080x1920
YUKSEKLIK  = int(os.environ.get("YUKSEKLIK", "1920"))
DIL        = os.environ.get("DIL", "tr")
EN_BOY     = os.environ.get("EN_BOY", "9:16")        # FLUX en-boy orani (dikey Shorts)
KARAKTER_LORA = os.environ.get("KARAKTER_LORA", "")  # egitilmis karakter LoRA (HF/Replicate/CivitAI URL). Bos ise temel FLUX.
LORA_GUC   = float(os.environ.get("LORA_GUC", "1.0"))

# Şiveyi konuşan kişinin temiz ses örneği (XTTS klonlama için). URL ya da repo içi yol.
SES_ORNEGI = os.environ.get("SES_ORNEGI", "data/ses_ornegi.wav")

# --- Replicate model referansları (owner/model:version) ---
# Bunları replicate.com'da GÜNCEL sürümle sabitle. Aşağıdakiler yalnızca başlangıç örneği.
MODEL_SES      = os.environ.get("MODEL_SES",      "lucataco/xtts-v2")          # metin->ses (klon) [SABIT]
MODEL_GORSEL   = os.environ.get("MODEL_GORSEL",   "black-forest-labs/flux-dev-lora")  # FLUX + LoRA [SABIT]
MODEL_LIPSYNC  = os.environ.get("MODEL_LIPSYNC",  "cjwbw/sadtalker")            # görsel+ses->konuşan klip [SABIT]

def dogrula():
    eksik = [k for k, v in {
        "REPLICATE_API_TOKEN": REPLICATE_API_TOKEN,
        "GEMINI_API_KEY": GEMINI_API_KEY,
    }.items() if not v]
    if eksik:
        raise SystemExit(f"Eksik ortam değişkeni: {', '.join(eksik)}")
