"""Adim 2 — Ses (edge-tts, UCRETSIZ): metin -> Turkce neural seste MP3. Anahtar gerekmez."""
import asyncio, tempfile, edge_tts
from . import config

def _voice(karakter):
    if not karakter:
        return config.SES_ERKEK
    return config.SES_KADIN if (sum(map(ord, karakter)) % 2) else config.SES_ERKEK

def uret(metin: str, karakter: str = None) -> str:
    out = tempfile.mktemp(suffix=".mp3")
    async def _g():
        await edge_tts.Communicate(metin, _voice(karakter)).save(out)
    asyncio.run(_g())
    return out
