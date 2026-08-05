"""Küçük yardımcılar."""
import os, tempfile, requests

def indir(url: str, uzanti: str) -> str:
    """Bir URL'yi geçici bir dosyaya indirir, yerel yolu döner."""
    r = requests.get(url, timeout=300)
    r.raise_for_status()
    fd, yol = tempfile.mkstemp(suffix=uzanti)
    with os.fdopen(fd, "wb") as f:
        f.write(r.content)
    return yol

def as_file(deger, uzanti: str) -> str:
    """Replicate çıktısı URL (str) ya da dosya-benzeri olabilir; her ikisini de yerel yola çevirir."""
    if isinstance(deger, str) and deger.startswith("http"):
        return indir(deger, uzanti)
    # replicate FileOutput nesnesi ise .url ya da read() olabilir
    url = getattr(deger, "url", None)
    if url:
        return indir(url, uzanti)
    fd, yol = tempfile.mkstemp(suffix=uzanti)
    with os.fdopen(fd, "wb") as f:
        f.write(deger.read() if hasattr(deger, "read") else bytes(deger))
    return yol
