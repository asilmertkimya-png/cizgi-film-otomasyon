# Cizgi Film Otomasyonu — BEDAVA otonom taslak surum

Tamamen ucretsiz, anahtarsiz (Gemini haric) ve GPU'suz calisan taslak hat. Arkadaşa demo icin.
Ucretli/kaliteli surumde ses klonlama (ElevenLabs), FLUX+LoRA gorsel ve lip-sync eklenecek.

## Ucretsiz yigin
1. **Senaryo** — Gemini (ucretsiz katman) `src/senaryo.py`
2. **Ses** — edge-tts, Turkce neural, anahtarsiz `src/ses.py`
3. **Gorsel** — Pollinations.ai, anahtarsiz `src/gorsel.py`
4. **Montaj** — ffmpeg: her sahne gorsel+ses+altyazi (Ken Burns), sonra birlestir `src/montaj.py`
   (Lip-sync YOK — ucretli surumde eklenecek.)
5. **Yukleme** — YouTube API (opsiyonel) `src/yukle.py`

## Kurulum
- Tek gerekli secret: `GEMINI_API_KEY` (aistudio.google.com, ucretsiz).
- Kuyruk: `data/fikirler.json` (sive + fikir; durum 'yeni' -> islenir -> 'hazir').
- Calistir: Actions -> **Cizgi Film Uret** -> Run. Cikti: `cikti/bolum.mp4` (artifact).

## Notlar
- Karakter tutarliligi icin sabit `KARAKTER_SEED` + ortak `STIL`. Tam tutarlilik ucretli LoRA ile.
- Ucretsiz servisler ara sira yavas/limit olabilir; tekrar denemeler kod icinde var.
