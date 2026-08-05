"""
Adim 3 — Gorsel (Pollinations.ai, UCRETSIZ): prompt -> PNG.
Cok yollu: (1) anahtarsiz varsayilan, (2) anahtarsiz turbo, (3) POLLINATIONS_KEY varsa gen/flux.
Anahtarsiz genelde yeter; servis dalgalanirsa enter.pollinations.ai'den ucretsiz anahtar eklenebilir.
"""
import tempfile, time, urllib.parse, requests
from . import config

def _dene(url, headers=None, tekrar=3):
    for _ in range(tekrar):
        try:
            r = requests.get(url, headers=headers or {}, timeout=240)
            ct = r.headers.get("content-type", "")
            if r.status_code == 200 and len(r.content) > 1000 and not ct.startswith("text"):
                out = tempfile.mktemp(suffix=".png"); open(out, "wb").write(r.content); return out
        except Exception:
            pass
        time.sleep(5)
    return None

def uret(prompt: str) -> str:
    q = urllib.parse.quote(f"{prompt}, {config.STIL}")
    w, h, seed = config.GENISLIK, config.YUKSEKLIK, config.KARAKTER_SEED
    adaylar = [
        (f"https://image.pollinations.ai/prompt/{q}?width={w}&height={h}&nologo=true&seed={seed}", None),
        (f"https://image.pollinations.ai/prompt/{q}?width={w}&height={h}&nologo=true&seed={seed}&model=turbo", None),
    ]
    if config.POLLINATIONS_KEY:
        adaylar.append((f"https://gen.pollinations.ai/image/{q}?width={w}&height={h}&seed={seed}&model=flux",
                        {"Authorization": f"Bearer {config.POLLINATIONS_KEY}"}))
    for url, hdr in adaylar:
        yol = _dene(url, hdr)
        if yol:
            return yol
    raise RuntimeError("Pollinations gorsel uretilemedi (tum yollar basarisiz)")
