# src/download_playlist.py

"""
- ignoreerrors=True para que yt-dlp salte errores y continúe con los demás videos.
- Mantenemos un archivo de registro descargas_registradas.txt para evitar descargas duplicadas.
- cookiefile se asigna si el usuario selecciona uno.
- Descarga una playlist de YouTube y remuxea o re-encodea (si es necesario) a los códecs
especificados. Por defecto: H.264 (video) + AAC (audio), en contenedor MP4.
"""
import os
import yt_dlp
import logging

from .codecs_config import (
    FFMPEG_VIDEO_LIBS, FFMPEG_AUDIO_LIBS,
    DEFAULT_VIDEO_CODEC, DEFAULT_AUDIO_CODEC,
    is_auto
)

def download_playlist(
    playlist_url: str,
    output_folder: str,
    cookies_file: str = None,
    log_file: str = "descargas_registradas.txt",
    video_codec: str = DEFAULT_VIDEO_CODEC,
    audio_codec: str = DEFAULT_AUDIO_CODEC,
):
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Leemos IDs descargados
    descargados = set()
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            descargados = {line.strip() for line in f if line.strip()}

    # Decidir remux vs re-encode
    if is_auto(video_codec, audio_codec):
        # REMUX
        postprocessors = [
            {
                "key": "FFmpegVideoRemuxer",
                "preferedformat": "mp4"
            }
        ]
        download_format = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]"
        postprocessor_args = []
    else:
        # RE-ENCODE
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
        "ignoreerrors": True,
        "postprocessors": postprocessors
    }

    if postprocessor_args:
        ydl_opts["postprocessor_args"] = postprocessor_args

    if cookies_file:
        ydl_opts["cookiefile"] = cookies_file

    logging.info(f"Iniciando descarga de playlist con video_codec={video_codec}, audio_codec={audio_codec}")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(playlist_url, download=False)
            if not info:
                raise ValueError("No se pudo extraer info de la playlist.")
            videos = info.get("entries", [])
            if not videos:
                raise ValueError("No se encontraron videos en la lista.")

            for video in videos:
                if not video:
                    continue
                video_id = video.get("id")
                video_title = video.get("title") or "Desconocido"
                video_url = video.get("webpage_url")
                if not video_id or not video_url:
                    logging.warning(f"Video inválido: {video_title}")
                    continue

                if video_id in descargados:
                    logging.info(f"Ya descargado, se omite: {video_title}")
                    continue

                try:
                    logging.info(f"Descargando: {video_title}")
                    ydl.download([video_url])
                    with open(log_file, "a", encoding="utf-8") as f:
                        f.write(f"{video_id}\n")
                    logging.info(f"Descargado con éxito: {video_title}")
                except Exception as e:
                    logging.error(f"Error en {video_title}: {e}")

            logging.info("Descarga de la playlist completada.")
        except Exception as e:
            logging.exception(f"Error general en la playlist: {e}")
