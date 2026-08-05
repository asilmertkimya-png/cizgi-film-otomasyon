"""
Orkestratör: kuyruktan bir bölüm alır ve tüm hattı çalıştırır.
Fikir kuyruğu: data/fikirler.json  (durum: "yeni" olan ilk kayıt işlenir)
Akış: senaryo -> (her sahne: ses + görsel + konuşturma) -> montaj -> (opsiyonel) yükleme
"""
import json, os, pathlib
from . import config, senaryo, ses, gorsel, konustur, montaj, yukle

KUYRUK = pathlib.Path("data/fikirler.json")

def sirdaki_bolum(veri):
    for b in veri["bolumler"]:
        if b.get("durum", "yeni") == "yeni":
            return b
    return None

def main():
    config.dogrula()
    veri = json.loads(KUYRUK.read_text(encoding="utf-8"))
    bolum = sirdaki_bolum(veri)
    if not bolum:
        print("İşlenecek 'yeni' bölüm yok. Çıkılıyor.")
        return

    print(f"Bölüm: {bolum['fikir']}  | şive: {bolum['sive']}")
    kurgu = senaryo.uret(bolum["fikir"], bolum["sive"])
    print(f"Senaryo hazır: {kurgu['baslik']} ({len(kurgu['sahneler'])} sahne)")

    klipler = []
    for i, sahne in enumerate(kurgu["sahneler"], 1):
        print(f"  Sahne {i}: ses...");        s = ses.uret(sahne["replik"])
        print(f"  Sahne {i}: görsel...");     g = gorsel.uret(sahne["gorsel"])
        print(f"  Sahne {i}: konuşturma..."); k = konustur.uret(g, s)
        klipler.append(k)

    os.makedirs("cikti", exist_ok=True)
    final = montaj.birlestir(klipler, "cikti/bolum.mp4")
    print(f"Final video: {final}")

    if config.YUKLE:
        vid = yukle.youtube(final, kurgu["baslik"], kurgu["ozet"], kurgu["etiketler"])
        print(f"YouTube'a yüklendi (private): https://youtu.be/{vid}")

    bolum["durum"] = "hazir"
    bolum["baslik"] = kurgu["baslik"]
    KUYRUK.write_text(json.dumps(veri, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Kuyruk güncellendi (durum=hazir).")

if __name__ == "__main__":
    main()
