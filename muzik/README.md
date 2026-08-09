# Muzik Otomasyonu — BEDAVA otonom AI muzik + soz + yayin

Tema listesinden, elini surmeden: Gemini sozu yazar, MusicGen (acik kaynak) enstrumantal
muzigi uretir, ffmpeg dalga-formu gorselli lyric video yapar, YouTube'a yukler. Hepsi ucretsiz,
GitHub Actions'ta otonom (public repo = sinirsiz Actions dakikasi). Tek gerekli secret: GEMINI_API_KEY.

## Yigin
1. **Soz + konsept** — Gemini `src/sozyaz.py` (baslik, muzik stili, sozler, etiket, aciklama)
2. **Muzik** — MusicGen (facebook/musicgen-small, acik kaynak, enstrumantal) `src/muzik.py`
3. **Video** — ffmpeg: koyu arka plan + dalga formu + baslik + akan sozler `src/video.py`
4. **Yukleme** — YouTube API (opsiyonel) `src/yukle.py`

Kuyruk: `data/fikirler.json` (tema; durum 'yeni' -> islenir -> 'hazir'). Cikti: `cikti/parca.mp4`.

## Kurulum
- Secret: `GEMINI_API_KEY` (aistudio.google.com, ucretsiz). YouTube icin YOUTUBE_* + vars YUKLE=1.
- Calistir: Actions -> **Muzik Uret** -> Run. Dikey 1080x1920, ~30 sn (Shorts uyumlu).

## Notlar
- MusicGen ENSTRUMANTAL uretir (vokal yok); sozler ekranda gorunur. Vokalli "soylenen" sarki
  ileride ucretli MiniMax Music / ElevenLabs Music API'siyle eklenebilir (motor degistirmek kolay).
- CPU'da muzik uretimi birkac dakika surer; public repo'da Actions dakikasi ucretsiz/sinirsiz.
- Parca uzunlugu SES_SANIYE ile ayarlanir (varsayilan 30 sn).
