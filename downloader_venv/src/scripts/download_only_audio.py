# src/scripts/download_only_audio.py

import os
import yt_dlp
from .codecs_config import (
    FFMPEG_AUDIO_LIBS,
    DEFAULT_AUDIO_CODEC,
    is_auto
)

def download_audio_only(
    video_url: str,
    output_folder: str,
    cookies_file: str = None,
    audio_codec: str = DEFAULT_AUDIO_CODEC
):
    """
    Descarga únicamente la pista de audio de un video/playlist y la convierte
    al códec deseado (mp3, opus, etc.) si no es 'auto'.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Configuramos el "format" para audio
    download_format = "bestaudio/best"

    # Decidimos el códec final en base a 'audio_codec'
    # Usamos el postprocessor "FFmpegExtractAudio" con 'preferredcodec'.
    if is_auto("", audio_codec):
        # "auto" => extraemos audio sin recodificar, pero normalmente
        #          se convierte a un formato de audio final, p.e. .m4a
        postprocessors = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "m4a",
                "preferredquality": "192"
            }
        ]
    else:
        # Si el usuario escoge un códec (mp3, opus, etc.)
        # lo indicamos en "preferredcodec"
        # No es un re-encode a mano, sino que 'yt_dlp' hace la conversión final.
        postprocessors = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": audio_codec,
                "preferredquality": "192"
            }
        ]

    ydl_opts = {
        "outtmpl": os.path.join(output_folder, "%(title)s.%(ext)s"),
        "format": download_format,
        "socket_timeout": 60,
        "postprocessors": postprocessors,
    }

    if cookies_file:
        ydl_opts["cookiefile"] = cookies_file

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"[Solo audio] Descargando {video_url} con códec '{audio_codec}'...")
        ydl.download([video_url])
        print("[Solo audio] Descarga completada.")
