# src/download_single.py

"""
- Se crea la carpeta de destino si no existe.
- Se configura yt_dlp.YoutubeDL con formato MP4, mejor calidad disponible y tiempo de espera de socket extendido.
- Si se proporciona cookies_file, se configura "cookiefile": cookies_file.
- Descarga un único video de YouTube y lo re-encodea (si es necesario) a los códecs
especificados. Por defecto: H.264 (video) + AAC (audio), en contenedor MP4.
- Toma en cuenta si ambos códecs son 'auto' para hacer un remux rápido.
"""

import os
import yt_dlp
from .codecs_config import (
    FFMPEG_VIDEO_LIBS, FFMPEG_AUDIO_LIBS,
    DEFAULT_VIDEO_CODEC, DEFAULT_AUDIO_CODEC,
    is_auto
)

def download_single_video(
    video_url: str,
    output_folder: str,
    cookies_file: str = None,
    video_codec: str = DEFAULT_VIDEO_CODEC,
    audio_codec: str = DEFAULT_AUDIO_CODEC,
):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Si ambos códecs son 'auto', usamos un "remux" rápido.
    if is_auto(video_codec, audio_codec):
        # REMUX -> no re-encode, solo unimos streams en MP4
        postprocessors = [
            {
                "key": "FFmpegVideoRemuxer",
                "preferedformat": "mp4"
            }
        ]
        # Force preferir mp4 con h264+aac (si está disponible), sino fallback a lo mejor que haya
        # El /best[ext=mp4] te cacha un mp4 con audio+video si existe
        download_format = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]"
    else:
        # RE-ENCODE -> forzamos h264/aac, etc.
        ffmpeg_video_codec = FFMPEG_VIDEO_LIBS.get(video_codec, "libx264")
        ffmpeg_audio_codec = FFMPEG_AUDIO_LIBS.get(audio_codec, "aac")
        postprocessors = [
            {
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4",
            }
        ]
        postprocessor_args = [
            "-c:v", ffmpeg_video_codec,
            "-c:a", ffmpeg_audio_codec
        ]
        download_format = "bestvideo+bestaudio/best"

    ydl_opts = {
        "outtmpl": os.path.join(output_folder, "%(title)s.%(ext)s"),
        "format": download_format,
        "merge_output_format": "mp4",
        "socket_timeout": 60,
        "postprocessors": postprocessors
    }

    # Si recodificamos, añadimos los postprocessor_args
    if not is_auto(video_codec, audio_codec):
        ydl_opts["postprocessor_args"] = postprocessor_args

    if cookies_file:
        ydl_opts["cookiefile"] = cookies_file

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"Descargando (single) con códec_video={video_codec} códec_audio={audio_codec}: {video_url}")
        ydl.download([video_url])
        print("Descarga completada.")
