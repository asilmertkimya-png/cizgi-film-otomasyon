"""
Orkestrator: kuyruktan bir tema al, ucretsiz muzik hattini calistir.
soz+konsept (Gemini) -> muzik (MusicGen) -> muzik video (ffmpeg) -> (ops.) YouTube upload.
"""
import json, os, pathlib
from . import config, sozyaz, muzik, video, yukle

KUYRUK = pathlib.Path("data/fikirler.json")

def sirdaki(v):
    for p in v["parcalar"]:
        if p.get("durum","yeni")=="yeni": return p
    return None

def main():
    config.dogrula()
    v=json.loads(KUYRUK.read_text(encoding="utf-8"))
    p=sirdaki(v)
    if not p: print("Islenecek 'yeni' tema yok."); return
    print(f"Tema: {p['tema']}")
    k=sozyaz.uret(p["tema"])
    print(f"Sarki: {k['baslik']} | stil: {k['stil']}")
    print("Muzik uretiliyor (MusicGen, CPU'da birkac dakika surebilir)...")
    ses=muzik.uret(k["stil"], k["sozler"])
    os.makedirs("cikti",exist_ok=True)
    final=video.uret(ses,k["baslik"],k["sozler"],"cikti/parca.mp4")
    print(f"Video hazir: {final}")
    if config.YUKLE:
        vid=yukle.youtube(final,k["baslik"],k.get("aciklama",""),k.get("etiketler",[]))
        print(f"YouTube'a yuklendi: https://youtu.be/{vid}")
    p["durum"]="hazir"; p["baslik"]=k["baslik"]
    KUYRUK.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding="utf-8")
    print("Kuyruk guncellendi (durum=hazir).")

if __name__=="__main__": main()
