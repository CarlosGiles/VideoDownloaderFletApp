# src/codecs_config.py

VIDEO_CODECS = [
    "auto",
    "h264",
    "h265",
    "vp9",
    "av1",
    "mpeg4"
]

AUDIO_CODECS = [
    "auto",
    "aac",
    "mp3",
    "wav",
    "flac",
    "opus",
    "m4a"
]

DEFAULT_VIDEO_CODEC = "auto"
DEFAULT_AUDIO_CODEC = "auto"

FFMPEG_VIDEO_LIBS = {
    "h264": "libx264",
    "h265": "libx265",
    "vp9":  "libvpx-vp9",
    "av1":  "libaom-av1",
    "mpeg4": "mpeg4"
}
FFMPEG_AUDIO_LIBS = {
    "aac":  "aac",
    "mp3":  "libmp3lame",
    "wav":  "pcm_s16le",
    "flac": "flac",
    "opus": "libopus",
    "m4a":  "aac"  # Normalmente produce .m4a con codec AAC
}

def is_auto(video_codec: str, audio_codec: str) -> bool:
    """
    Retorna True si AMBOS códecs son 'auto',
    indicando que se hará un remux en lugar de recodificar.
    """
    return (video_codec == "auto") and (audio_codec == "auto")
