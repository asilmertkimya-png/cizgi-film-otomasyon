"""
Adim 3 — Gorsel (Gemini 2.5 Flash Image / "Nano Banana", UCRETSIZ katman): prompt -> PNG.
Mevcut GEMINI_API_KEY'i kullanir. 429 (hiz limiti) durumunda bekleyip tekrar dener.
"""
import base64, tempfile, time, requests
from . import config

_MODELLER = ["gemini-2.5-flash-image"]

def _cagir(model, prompt):
    url = (f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
           f"?key={config.GEMINI_API_KEY}")
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}}
    try:
        r = requests.post(url, json=body, timeout=180)
    except Exception as e:
        return None, str(e), 0
    if r.status_code != 200:
        return None, f"HTTP {r.status_code}: {r.text[:120]}", r.status_code
    for part in r.json().get("candidates", [{}])[0].get("content", {}).get("parts", []):
        inline = part.get("inlineData") or part.get("inline_data")
        if inline and inline.get("data"):
            out = tempfile.mktemp(suffix=".png")
            open(out, "wb").write(base64.b64decode(inline["data"]))
            return out, None, 200
    return None, "yanitta gorsel yok", 200

def uret(prompt: str) -> str:
    tam = f"{prompt}, {config.STIL}, vertical 9:16 portrait composition, centered subject"
    hatalar = []
    for model in _MODELLER:
        for deneme in range(6):
            yol, hata, st = _cagir(model, tam)
            if yol:
                return yol
            if st == 429:
                print(f"    429 hiz limiti ({model}) -> 35sn bekle ({deneme+1}/6)")
                time.sleep(35); continue
            hatalar.append(f"[{model}] {hata}")
            break
        else:
            hatalar.append(f"[{model}] 429 (limit asilamadi)")
    raise RuntimeError("Gemini gorsel uretilemedi -> " + " || ".join(hatalar))
