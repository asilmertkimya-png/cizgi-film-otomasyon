"""Adim 4 — YouTube yukleme (opsiyonel). Actions'ta basiz calismak icin OAuth refresh token kullanir."""
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from . import config

def youtube(video_yolu, baslik, aciklama, etiketler):
    creds = Credentials(token=None, refresh_token=config.YOUTUBE_REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=config.YOUTUBE_CLIENT_ID, client_secret=config.YOUTUBE_CLIENT_SECRET,
        scopes=["https://www.googleapis.com/auth/youtube.upload"])
    yt = build("youtube","v3",credentials=creds)
    istek = yt.videos().insert(part="snippet,status",
        body={"snippet":{"title":baslik[:100],"description":aciklama,"tags":etiketler},
              "status":{"privacyStatus":"private","selfDeclaredMadeForKids":False}},
        media_body=MediaFileUpload(video_yolu, resumable=True))
    return istek.execute()["id"]
