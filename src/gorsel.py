"""
Adim 3 — Gorsel: prompt -> PNG.
Oncelik: POLLINATIONS_KEY varsa Pollinations/Flux (Gemini'den bagimsiz ucretsiz kota).
Yedek: Gemini 2.5 Flash Image (429 durumunda kisa backoff).
"""
import base64, tempfile, time, urllib.parse, requests
from . import config

def _pollinations(prompt):
    if not config.POLLINATIONS_KEY:
        return None
    q = urllib.parse.quote(prompt)
    url = (f"https://gen.pollinations.ai/image/{q}"
           f"?width={config.GENISLIK}&height={config.YUKSEKLIK}&seed={config.KARAKTER_SEED}&model=flux")
    hdr = {"Authorization": f"Bearer {config.POLLINATIONS_KEY}"}
    for _ in range(3):
        try:
            r = requests.get(url, headers=hdr, timeout=240)
            ct = r.headers.get("content-type", "")
            if r.status_code == 200 and len(r.content) > 1000 and not ct.startswith("text"):
                out = tempfile.mktemp(suffix=".png"); open(out, "wb").write(r.content); return out
            print(f"    pollinations: HTTP {r.status_code}")
        except Exception as e:
            print(f"    pollinations hata: {str(e)[:80]}")
        time.sleep(5)
    return None

def _gemini(prompt):
    url = ("https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent"
           f"?key={config.GEMINI_API_KEY}")
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}}
    for deneme in range(3):
        try:
            r = requests.post(url, json=body, timeout=180)
        except Exception as e:
            print(f"    gemini hata: {str(e)[:80]}"); time.sleep(8); continue
        if r.status_code == 200:
            for part in r.json().get("candidates", [{}])[0].get("content", {}).get("parts", []):
                inline = part.get("inlineData") or part.get("inline_data")
                if inline and inline.get("data"):
                    out = tempfile.mktemp(suffix=".png")
                    open(out, "wb").write(base64.b64decode(inline["data"])); return out
            print("    gemini: yanitta gorsel yok"); return None
        if r.status_code == 429:
            print(f"    gemini 429 hiz/kota limiti ({deneme+1}/3)"); time.sleep(30); continue
        print(f"    gemini HTTP {r.status_code}: {r.text[:100]}"); return None
    return None

def uret(prompt: str) -> str:
    tam = f"{prompt}, {config.STIL}, vertical 9:16 portrait composition, centered subject"
    yol = _pollinations(tam) or _gemini(tam)
    if yol:
        return yol
    raise RuntimeError("Gorsel uretilemedi (Pollinations anahtari yok/basarisiz VE Gemini kota/429).")
