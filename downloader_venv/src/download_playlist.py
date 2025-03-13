# src/download_playlist.py

"""
ignoreerrors=True para que yt-dlp salte errores y continúe con los demás videos.
Mantenemos un archivo de registro descargas_registradas.txt para evitar descargas duplicadas.
cookiefile se asigna si el usuario selecciona uno.
"""

import os
import yt_dlp
import logging

from codecs_config import (
    FFMPEG_VIDEO_LIBS, FFMPEG_AUDIO_LIBS,
    DEFAULT_VIDEO_CODEC, DEFAULT_AUDIO_CODEC
)


def download_playlist(
    playlist_url: str,
    output_folder: str,
    cookies_file: str = None,
    log_file: str = "descargas_registradas.txt",
    video_codec: str = DEFAULT_VIDEO_CODEC,
    audio_codec: str = DEFAULT_AUDIO_CODEC,
):
    """
    Descarga todos los videos de una playlist. Re-encodea a los códecs dados (default h264+aac).
    Continúa si algún video falla.
    """
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Cargamos el set de IDs ya descargados
    descargados = set()
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            descargados = {line.strip() for line in f if line.strip()}

    # Verificamos mapeos de ffmpeg
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

    ydl_opts = {
        "outtmpl": os.path.join(output_folder, "%(title)s.%(ext)s"),
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "socket_timeout": 60,
        "ignoreerrors": True,
        "postprocessors": postprocessors,
        "postprocessor_args": postprocessor_args,
    }

    if cookies_file:
        ydl_opts["cookiefile"] = cookies_file

    logging.info(f"Iniciando descarga de playlist: {playlist_url}")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(playlist_url, download=False)
            if not info:
                raise ValueError("No se pudo extraer información de la lista. Verifica la URL o cookies.")
            
            videos = info.get("entries", [])
            if not videos:
                raise ValueError("No se encontraron videos en la lista de reproducción.")
            
            for video in videos:
                if video is None:
                    continue
                video_id = video.get("id")
                video_title = video.get("title") or "TítuloDesconocido"
                video_url = video.get("webpage_url")

                if not video_id or not video_url:
                    logging.warning(f"Video inválido: {video_title} (ID/URL faltante). Se omite.")
                    continue

                if video_id in descargados:
                    logging.info(f"Ya descargado (se ignora): {video_title}")
                    continue

                try:
                    logging.info(f"Descargando: {video_title}")
                    ydl.download([video_url])
                    # Guardamos ID en el log de descargas
                    with open(log_file, "a", encoding="utf-8") as f:
                        f.write(f"{video_id}\n")
                    logging.info(f"Descargado con éxito: {video_title}")
                except yt_dlp.utils.DownloadError as e:
                    logging.error(f"Error al descargar {video_title}: {e}")
                except Exception as ex:
                    logging.exception(f"Excepción inesperada en {video_title}: {ex}")

            logging.info("Descarga de la playlist completada.")
        except Exception as e:
            logging.exception(f"Error al procesar la lista {playlist_url}: {e}")
