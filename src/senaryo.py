"""
Adım 1 — Senaryo (Gemini): fikir + şive -> yapılandırılmış bölüm JSON'u.
Çıktı: {baslik, ozet, etiketler[], sahneler:[{karakter, replik, gorsel}]}
"""
import json, google.generativeai as genai
from . import config

PROMPT = """Sen genel izleyiciye ve cocuklara uygun, {sive} sivesiyle konusan cizgi film \
karakterleri icin senaryo yazan bir yazarsin. Asagidaki FIKIR icin yaklasik 45-60 saniyelik, \
eglenceli ve sicak bir cizgi film bolumu kurgula. FIKIR: {fikir}

Diyaloglar {sive} yoresinin agzina, kelime ve deyimlerine uygun olsun; komik ama nazik, \
kesinlikle kufur/kaba icerik olmasin, cocuk dostu kalsin. Bolumu 4-6 sahneye bol. Her sahne \
icin: konusan karakterin adi, {sive} sivesindeki replik, ve o sahnenin INGILIZCE gorsel tarifi \
(cartoon stili, sahnede yazi yok, ana karakter her sahnede tutarli). Yaniti SADECE gecerli JSON \
ver, kod blogu ekleme:
{{"baslik":"...","ozet":"...","etiketler":["e1","e2","e3","e4","e5"],
"sahneler":[{{"karakter":"...","replik":"...","gorsel":"cartoon english description, consistent character, no text"}}]}}"""

def uret(fikir: str, sive: str) -> dict:
    genai.configure(api_key=config.GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")
    cevap = model.generate_content(PROMPT.format(fikir=fikir, sive=sive))
    metin = cevap.text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(metin)
