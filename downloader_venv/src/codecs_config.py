# src/codecs_config.py

# Listas de códecs de video y audio disponibles
VIDEO_CODECS = [
    "h264",   
    "h265",   
    "vp9",
    "av1",
    "mpeg4"   
]

AUDIO_CODECS = [
    "aac",
    "mp3",
    "wav",
    "flac",
    "opus",
    "m4a"
]

# Valores por defecto (forzaremos H.264 + AAC)
DEFAULT_VIDEO_CODEC = "h264"
DEFAULT_AUDIO_CODEC = "aac"

# Opcional: Mapear "códec" de la UI a la librería interna de FFmpeg
# (cuando se quiera re-encodear con -c:v y -c:a)
FFMPEG_VIDEO_LIBS = {
    "h264": "libx264",
    "h265": "libx265",
    "vp9":  "libvpx-vp9",
    "av1":  "libaom-av1",
    "mpeg4": "mpeg4"   # FFmpeg nativo
}

FFMPEG_AUDIO_LIBS = {
    "aac":  "aac",
    "mp3":  "libmp3lame",
    "wav":  "pcm_s16le",
    "flac": "flac",
    "opus": "libopus",
    "m4a":  "aac"  # Normalmente "m4a" se produce con "aac"
}
