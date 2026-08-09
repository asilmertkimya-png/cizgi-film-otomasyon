"""Adim 1 — Soz + konsept (Gemini): tema -> baslik, POP muzik stili, sozler, etiket, aciklama."""
import json, time, google.generativeai as genai
from . import config

PROMPT = """Sen hit POP sarkilar yazan bir soz yazari ve muzik yonetmenisin. Asagidaki TEMA icin
Turkce, akilda kalan, catchy, enerjik bir POP sarki uret. TEMA: {tema}

Kurallar: nakarati (chorus) tekrar eden, siddetli/dokunakli 10-14 kisa dize; kufur yok. Ayrica
muzik icin INGILIZCE kisa bir stil tarifi ver: modern upbeat pop, catchy hook, danceable,
bright synths, punchy drums, energetic (enstrumantal, vokalsiz). Yaniti SADECE tek satirlik gecerli
JSON ver, kod blogu ekleme:
{{"baslik":"kisa cekici baslik","stil":"modern upbeat pop instrumental, catchy, danceable, bright synths, punchy drums",
"sozler":["dize1","..."],"etiketler":["pop","e2","e3","e4","e5"],"aciklama":"2-3 cumle youtube aciklamasi"}}"""

def uret(tema: str) -> dict:
    genai.configure(api_key=config.GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")
    son = None
    for _ in range(3):
        try:
            cevap = model.generate_content(PROMPT.format(tema=tema))
            metin = cevap.text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            return json.loads(metin)
        except Exception as e:
            son = str(e); print(f"    sozyaz tekrar (429/hata): {son[:80]}"); time.sleep(20)
    raise RuntimeError(f"Soz uretilemedi: {son}")
