"""
Adım 6 — YouTube yükleme (opsiyonel). Actions'ta başsız (headless) çalışması için
OAuth refresh token kullanır. YUKLE=1 ve YOUTUBE_* secret'ları gerekir.
"""
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from . import config

def youtube(video_yolu: str, baslik: str, aciklama: str, etiketler: list) -> str:
    creds = Credentials(
        token=None,
        refresh_token=config.YOUTUBE_REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=config.YOUTUBE_CLIENT_ID,
        client_secret=config.YOUTUBE_CLIENT_SECRET,
        scopes=["https://www.googleapis.com/auth/youtube.upload"],
    )
    yt = build("youtube", "v3", credentials=creds)
    istek = yt.videos().insert(
        part="snippet,status",
        body={
            "snippet": {"title": baslik[:100], "description": aciklama, "tags": etiketler},
            "status": {"privacyStatus": "private", "selfDeclaredMadeForKids": False},
        },
        media_body=MediaFileUpload(video_yolu, resumable=True),
    )
    cevap = istek.execute()
    return cevap["id"]
