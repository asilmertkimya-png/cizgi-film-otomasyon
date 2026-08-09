"""
Adim 2 — Muzik. Once fal MiniMax Music (VOKALLI sarki, ~$0.035, max 60sn, max 400 karakter soz).
Faturalama/kredi yoksa veya hata olursa UCRETSIZ MusicGen enstrumantale duser (hat hep bir cikti verir).
"""
import os, tempfile, requests
from . import config

def _minimax(stil, sozler):
    if not config.FAL_KEY:
        print("    FAL_KEY yok -> MiniMax atlaniyor")
        return None
    os.environ["FAL_KEY"] = config.FAL_KEY
    try:
        import fal_client
        soz = "\n".join(sozler) if isinstance(sozler, list) else (sozler or "")
        soz = soz[:380]  # MiniMax soz limiti ~400 karakter
        prompt = f"{stil}\n##\n{soz}\n##"
        r = fal_client.subscribe("fal-ai/minimax-music", arguments={"prompt": prompt}, with_logs=False)
        ses = r.get("audio")
        url = ses.get("url") if isinstance(ses, dict) else ses
        if url:
            out = tempfile.mktemp(suffix=".mp3")
            open(out, "wb").write(requests.get(url, timeout=300).content)
            print("    MiniMax VOKAL sarki uretildi")
            return out
        print(f"    MiniMax yanitinda ses yok: {str(r)[:120]}")
    except Exception as e:
        print(f"    MiniMax basarisiz (faturalama/kredi?): {str(e)[:140]}")
    return None

def _musicgen(stil, saniye):
    import torch, scipy.io.wavfile as wav
    from transformers import AutoProcessor, MusicgenForConditionalGeneration
    proc = AutoProcessor.from_pretrained(config.MUSICGEN_MODEL)
    model = MusicgenForConditionalGeneration.from_pretrained(config.MUSICGEN_MODEL)
    inputs = proc(text=[stil], padding=True, return_tensors="pt")
    with torch.no_grad():
        ses = model.generate(**inputs, max_new_tokens=int(saniye*50), do_sample=True, guidance_scale=3.0)
    sr = model.config.audio_encoder.sampling_rate
    out = tempfile.mktemp(suffix=".wav")
    wav.write(out, rate=sr, data=ses[0, 0].numpy())
    return out

def uret(stil, sozler=None, saniye=None):
    yol = _minimax(stil, sozler)
    if yol:
        return yol
    print("    -> ucretsiz MusicGen enstrumantale dusuluyor")
    return _musicgen(stil, saniye or config.SES_SANIYE)
