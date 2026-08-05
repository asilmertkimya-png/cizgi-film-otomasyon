"""
Adim 3 — Gorsel (Gemini 2.5 Flash Image / "Nano Banana", UCRETSIZ katman): prompt -> PNG.
Zaten elimizdeki GEMINI_API_KEY'i kullanir; ek servis/uyelik gerekmez. REST ile cagirir.
"""
import base64, tempfile, time, requests
from . import config

_MODELLER = ["gemini-2.5-flash-image", "gemini-2.5-flash-image-preview",
             "gemini-2.0-flash-preview-image-generation"]

def _cagir(model, prompt):
    url = (f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
           f"?key={config.GEMINI_API_KEY}")
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}}
    r = requests.post(url, json=body, timeout=180)
    if r.status_code != 200:
        return None, f"HTTP {r.status_code}: {r.text[:160]}"
    for part in r.json().get("candidates", [{}])[0].get("content", {}).get("parts", []):
        inline = part.get("inlineData") or part.get("inline_data")
        if inline and inline.get("data"):
            out = tempfile.mktemp(suffix=".png")
            open(out, "wb").write(base64.b64decode(inline["data"]))
            return out, None
    return None, "yanitta gorsel yok"

def uret(prompt: str) -> str:
    tam = f"{prompt}, {config.STIL}, vertical 9:16 portrait composition, centered subject"
    son = None
    for model in _MODELLER:
        for _ in range(2):
            yol, hata = _cagir(model, tam)
            if yol:
                return yol
            son = f"{model}: {hata}"
            if hata and "HTTP 404" in hata:
                break   # bu model yok, sonrakine gec
            time.sleep(4)
    raise RuntimeError(f"Gemini gorsel uretilemedi: {son}")
