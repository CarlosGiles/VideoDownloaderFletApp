# src/download_single.py

"""
Se crea la carpeta de destino si no existe.
Se configura yt_dlp.YoutubeDL con formato MP4, mejor calidad disponible y tiempo de espera de socket extendido.
Si se proporciona cookies_file, se configura "cookiefile": cookies_file.
Descarga un único video de YouTube y lo re-encodea (si es necesario) a los códecs
especificados. Por defecto: H.264 (video) + AAC (audio), en contenedor MP4.
"""

import os
import yt_dlp
from codecs_config import (
    FFMPEG_VIDEO_LIBS, FFMPEG_AUDIO_LIBS,
    DEFAULT_VIDEO_CODEC, DEFAULT_AUDIO_CODEC
)


def download_single_video(
    video_url: str,
    output_folder: str,
    cookies_file: str = None,
    video_codec: str = DEFAULT_VIDEO_CODEC,
    audio_codec: str = DEFAULT_AUDIO_CODEC,
):
    """
    Descarga un único video de YouTube y lo re-encodea (si es necesario) a los códecs
    especificados. Por defecto: H.264 (video) + AAC (audio), en contenedor MP4.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Si el usuario escribe un códec que no está en el mapping, caemos a h264/aac
    ffmpeg_video_codec = FFMPEG_VIDEO_LIBS.get(video_codec, "libx264")
    ffmpeg_audio_codec = FFMPEG_AUDIO_LIBS.get(audio_codec, "aac")

    # Postprocessors para que combine video+audio en .mp4 y re-encodee con ffmpeg
    postprocessors = [
        {
            "key": "FFmpegVideoConvertor",
            "preferedformat": "mp4",
        }
    ]
    # Forzamos la recodificación de audio y video en FFmpeg (puede tardar más)
    postprocessor_args = [
        "-c:v", ffmpeg_video_codec,
        "-c:a", ffmpeg_audio_codec
    ]

    ydl_opts = {
        "outtmpl": os.path.join(output_folder, "%(title)s.%(ext)s"),
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "socket_timeout": 60,
        "postprocessors": postprocessors,
        "postprocessor_args": postprocessor_args
    }

    if cookies_file:
        ydl_opts["cookiefile"] = cookies_file

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"Descargando video: {video_url}")
        try:
            ydl.download([video_url])
            print(f"Descarga completada: {video_url}")
        except Exception as e:
            print(f"Error al descargar {video_url}: {e}")
            raise
