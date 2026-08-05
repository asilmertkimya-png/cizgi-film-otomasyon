# Çizgi Film Otomasyonu (açık kaynak, GitHub Actions + Replicate)

Şiveli konuşan çizgi film karakterleriyle kısa video üreten uçtan uca hat.
**GitHub Actions** orkestratördür; ağır (GPU'lu) işleri **Replicate** üzerindeki
**açık kaynak modeller** yapar. Video baytları Actions'a girmez — her adım bir URL/dosya döndürür.

## Akış
1. **Senaryo** — Gemini: fikir + şive → sahne/diyalog/görsel-prompt JSON'u (`src/senaryo.py`)
2. **Ses** — Replicate/XTTS (klon) veya RVC (sesten-sese, en otantik şive) (`src/ses.py`)
3. **Görsel** — Replicate/SDXL veya FLUX + karakter LoRA (tutarlılık) (`src/gorsel.py`)
4. **Konuşturma** — Replicate lip-sync: SadTalker/Wav2Lip/LivePortrait (`src/konustur.py`)
5. **Montaj** — ffmpeg ile sahneleri birleştir (CPU) (`src/montaj.py`)
6. **Yükleme** — YouTube API (opsiyonel) (`src/yukle.py`)

Kuyruk: `data/fikirler.json` — `durum: "yeni"` olan ilk bölüm işlenir, biter `durum: "hazir"` olur.

## Kurulum
1. Bu klasörü bir GitHub reposuna koy (private önerilir).
2. **Secrets** ekle (Settings → Secrets and variables → Actions):
   - `REPLICATE_API_TOKEN`, `GEMINI_API_KEY`
   - (yükleme için) `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN`
   - **Variables**: `YUKLE` = `1` (yüklemeyi açmak için)
3. **Bir kerelik hazırlık:**
   - **Ses:** şiveyi konuşan kişiden temiz ~30 sn kayıt → `data/ses_ornegi.wav` (XTTS klonu) ya da RVC modeli.
   - **Karakter:** karakterin 10-20 görseliyle Replicate'te bir **LoRA eğit** → çıkan model slug'ını `MODEL_GORSEL`'e yaz. Böylece her bölümde aynı yüz.
4. **Model sürümlerini sabitle:** `MODEL_SES / MODEL_GORSEL / MODEL_LIPSYNC` değerlerini
   replicate.com'daki **güncel sürümle** (`owner/model:version`) gir. Varsayılanlar sadece örnek.

## Çalıştırma
- Elle: Actions sekmesi → **Cizgi Film Uret** → Run.
- Dış tetik (Make vb.): `repository_dispatch` ile `event_type: "uret"` gönder (bilim senaryondaki desenle aynı).
- Zamanlı: `uret.yml` içindeki `schedule` bloğunu aç.
- Yerel test: `.env.example` → `.env`, sonra `pip install -r requirements.txt && python -m src.main`.

## Önemli notlar
- **Çizgi yüz uyarısı:** lip-sync modellerinin çoğu gerçek yüz için eğitilmiştir. Bağlamadan önce
  Wav2Lip / SadTalker / LivePortrait'i bir örnek çizgi karakterle Hugging Face/Replicate'te
  ücretsiz dene, en iyisini `MODEL_LIPSYNC` yap.
- **Şive kalitesi:** en otantik yol RVC (gerçek şiveli performansı karakter sesine çevirir, yarı-otonom).
  XTTS tam otonomdur ama yeni metinde şive standarda kayabilir.
- **Maliyet:** Replicate saniyelik ücretlendirir; en ağır adım lip-sync'tir. Aboneliksiz, kullandıkça öde.
- Bu iskelet, sen anahtarları ve model sürümlerini girdikten sonra çalışır; uçtan uca test için
  Replicate/Gemini anahtarların gerekir.
