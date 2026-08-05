"""Adim 3 — Gorsel (Pollinations.ai, UCRETSIZ, anahtarsiz): prompt -> PNG."""
import tempfile, time, urllib.parse, requests
from . import config

def uret(prompt: str) -> str:
    tam = f"{prompt}, {config.STIL}"
    url = ("https://image.pollinations.ai/prompt/" + urllib.parse.quote(tam)
           + f"?width={config.GENISLIK}&height={config.YUKSEKLIK}&nologo=true"
           + f"&model={config.GORSEL_MODEL}&seed={config.KARAKTER_SEED}")
    son = None
    for _ in range(4):
        try:
            r = requests.get(url, timeout=240)
            if r.status_code == 200 and len(r.content) > 1000:
                out = tempfile.mktemp(suffix=".png")
                open(out, "wb").write(r.content)
                return out
            son = f"HTTP {r.status_code}"
        except Exception as e:
            son = str(e)
        time.sleep(6)
    raise RuntimeError(f"Pollinations gorsel uretilemedi: {son}")
