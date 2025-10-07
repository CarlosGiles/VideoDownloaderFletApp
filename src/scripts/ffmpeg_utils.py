# src/scripts/ffmpeg_utils.py

"""
Utilidades para verificar y configurar FFmpeg en el sistema.
Busca FFmpeg en ubicaciones comunes de Windows y configura yt-dlp para usarlo.
"""

import os
import shutil
import subprocess
from typing import Optional

# Ubicaciones comunes donde FFmpeg podría estar instalado en Windows
COMMON_FFMPEG_PATHS = [
    r"C:\ffmpeg\bin",
    r"C:\Program Files\ffmpeg\bin", 
    r"C:\Program Files (x86)\ffmpeg\bin",
    os.path.expanduser(r"~\ffmpeg\bin"),
    os.path.expanduser(r"~\AppData\Local\ffmpeg\bin"),
]

def find_ffmpeg_executable() -> Optional[str]:
    """
    Busca el ejecutable de FFmpeg en el sistema.
    
    Returns:
        str: Ruta completa al ejecutable de ffmpeg si se encuentra, None si no.
    """
    # Primero verificar si está en PATH
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        return ffmpeg_path
    
    # Si no está en PATH, buscar en ubicaciones comunes
    for path in COMMON_FFMPEG_PATHS:
        ffmpeg_exe = os.path.join(path, "ffmpeg.exe")
        if os.path.isfile(ffmpeg_exe):
            try:
                # Verificar que el ejecutable funciona
                result = subprocess.run(
                    [ffmpeg_exe, "-version"], 
                    capture_output=True, 
                    text=True, 
                    timeout=5
                )
                if result.returncode == 0:
                    return ffmpeg_exe
            except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
                continue
    
    return None

def configure_ffmpeg_for_ydl(ydl_opts: dict) -> dict:
    """
    Configura las opciones de yt-dlp para usar FFmpeg si está disponible.
    
    Args:
        ydl_opts: Diccionario de opciones para yt-dlp
        
    Returns:
        dict: Opciones actualizadas con configuración de FFmpeg
    """
    ffmpeg_path = find_ffmpeg_executable()
    
    if ffmpeg_path:
        # Si encontramos FFmpeg, configurar yt-dlp para usarlo
        ffmpeg_dir = os.path.dirname(ffmpeg_path)
        ydl_opts["ffmpeg_location"] = ffmpeg_dir
        print(f"FFmpeg encontrado en: {ffmpeg_path}")
    else:
        print("Advertencia: FFmpeg no encontrado. Las descargas de alta calidad podrían fallar.")
        print("Instala FFmpeg o asegúrate de que esté en tu PATH del sistema.")
    
    return ydl_opts

def is_ffmpeg_available() -> bool:
    """
    Verifica si FFmpeg está disponible en el sistema.
    
    Returns:
        bool: True si FFmpeg está disponible, False si no.
    """
    return find_ffmpeg_executable() is not None

def get_ffmpeg_info() -> dict:
    """
    Obtiene información sobre la instalación de FFmpeg.
    
    Returns:
        dict: Información sobre FFmpeg (ruta, versión, disponible)
    """
    ffmpeg_path = find_ffmpeg_executable()
    
    info = {
        "available": ffmpeg_path is not None,
        "path": ffmpeg_path,
        "version": None
    }
    
    if ffmpeg_path:
        try:
            result = subprocess.run(
                [ffmpeg_path, "-version"], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            if result.returncode == 0:
                # Extraer la versión de la primera línea
                first_line = result.stdout.split('\n')[0]
                if "version" in first_line:
                    info["version"] = first_line
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            pass
    
    return info