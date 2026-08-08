"""
Orkestrator (bedava surum): kuyruktan bir bolum al, ucretsiz hatti calistir.
senaryo (Gemini) -> her sahne: ses (edge-tts) + gorsel (Pollinations) + sahne klibi (ffmpeg) -> birlestir -> (ops.) yukle
"""
import json, os, pathlib, time
from . import config, senaryo, ses, gorsel, montaj, yukle

KUYRUK = pathlib.Path("data/fikirler.json")

def sirdaki(veri):
    for b in veri["bolumler"]:
        if b.get("durum", "yeni") == "yeni":
            return b
    return None

def main():
    config.dogrula()
    veri = json.loads(KUYRUK.read_text(encoding="utf-8"))
    bolum = sirdaki(veri)
    if not bolum:
        print("Islenecek 'yeni' bolum yok."); return

    print(f"Bolum: {bolum['fikir']} | sive: {bolum['sive']}")
    kurgu = senaryo.uret(bolum["fikir"], bolum["sive"])
    print(f"Senaryo: {kurgu['baslik']} ({len(kurgu['sahneler'])} sahne)")

    klipler = []
    for i, s in enumerate(kurgu["sahneler"], 1):
        print(f"  Sahne {i}: ses");    a = ses.uret(s["replik"], s.get("karakter"))
        print(f"  Sahne {i}: gorsel"); g = gorsel.uret(s["gorsel"])
        print(f"  Sahne {i}: montaj"); klipler.append(montaj.sahne_klip(g, a, s["replik"]))
        time.sleep(6)  # RPM: sahneler arasi kucuk bekleme

    os.makedirs("cikti", exist_ok=True)
    final = montaj.birlestir(klipler, "cikti/bolum.mp4")
    print(f"Final video: {final}")

    if config.YUKLE:
        vid = yukle.youtube(final, kurgu["baslik"], kurgu.get("ozet", ""), kurgu.get("etiketler", []))
        print(f"YouTube'a yuklendi: https://youtu.be/{vid}")

    bolum["durum"] = "hazir"; bolum["baslik"] = kurgu["baslik"]
    KUYRUK.write_text(json.dumps(veri, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Kuyruk guncellendi (durum=hazir).")

if __name__ == "__main__":
    main()
