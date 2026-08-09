"""
Adim 2 — Muzik (MusicGen / facebook, ACIK KAYNAK, ucretsiz): stil prompt -> enstrumantal WAV.
transformers ile calisir; Actions CPU'da yavas ama ucretsiz (public repo = sinirsiz Actions dakikasi).
"""
import tempfile
from . import config

def uret(stil_prompt: str, saniye: int = None) -> str:
    saniye = saniye or config.SES_SANIYE
    import torch, scipy.io.wavfile as wav
    from transformers import AutoProcessor, MusicgenForConditionalGeneration
    proc = AutoProcessor.from_pretrained(config.MUSICGEN_MODEL)
    model = MusicgenForConditionalGeneration.from_pretrained(config.MUSICGEN_MODEL)
    inputs = proc(text=[stil_prompt], padding=True, return_tensors="pt")
    max_new = int(saniye * 50)  # MusicGen ~50 token/sn
    with torch.no_grad():
        ses = model.generate(**inputs, max_new_tokens=max_new, do_sample=True, guidance_scale=3.0)
    sr = model.config.audio_encoder.sampling_rate
    out = tempfile.mktemp(suffix=".wav")
    wav.write(out, rate=sr, data=ses[0, 0].numpy())
    return out
