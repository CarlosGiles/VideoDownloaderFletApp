# src/main.py

import flet as ft
import os

# Scripts de descarga
from scripts.download_single import download_single_video
from scripts.download_playlist import download_playlist
from scripts.download_only_audio import download_audio_only

# Configuración de códecs
from scripts.codecs_config import (
    VIDEO_CODECS, AUDIO_CODECS,
    DEFAULT_VIDEO_CODEC, DEFAULT_AUDIO_CODEC
)

# Tema
from themes.theme_cyberpunk import get_cyberpunk_theme

# Componentes personalizados
from components.btn import PrimaryButton
from components.check import AudioOnlyCheckbox

def main(page: ft.Page):
    page.adaptive = True
    page.bgcolor = "#21303B"
    cyberpunk = get_cyberpunk_theme()
    page.dark_theme = cyberpunk

    page.title = "Flet Downloader"
    page.window_width = 800
    page.window_height = 600

    # Campos de texto
    single_url_field = ft.TextField(label="URL de Video", width=700)
    playlist_url_field = ft.TextField(label="URL de Lista de Reproducción", width=700)
    output_folder_field = ft.TextField(label="Carpeta de destino", width=500, read_only=True)
    cookies_file_field = ft.TextField(label="Archivo de Cookies (opcional)", width=500, read_only=True)

    # Checkbox para indicar SOLO AUDIO
    audio_only_check = AudioOnlyCheckbox()

    # Códecs
    video_codec_dropdown = ft.Dropdown(
        label="Códec de Video",
        width=200,
        value=DEFAULT_VIDEO_CODEC,  # "auto"
        options=[ft.dropdown.Option(v) for v in VIDEO_CODECS],
    )
    audio_codec_dropdown = ft.Dropdown(
        label="Códec de Audio",
        width=200,
        value=DEFAULT_AUDIO_CODEC,  # "auto"
        options=[ft.dropdown.Option(a) for a in AUDIO_CODECS],
    )

    # Log
    log_output = ft.Text(value="", selectable=True, expand=True)
    def log_message(msg: str):
        log_output.value += msg + "\n"
        page.update()

    # Pickers
    dir_picker = ft.FilePicker(on_result=lambda e: pick_folder_result(e))
    file_picker = ft.FilePicker(on_result=lambda e: pick_cookies_result(e))
    page.overlay.append(dir_picker)
    page.overlay.append(file_picker)

    def pick_folder_result(e: ft.FilePickerResultEvent):
        if e.path:
            output_folder_field.value = e.path
            page.update()

    def pick_cookies_result(e: ft.FilePickerResultEvent):
        if e.files:
            cookies_file_field.value = e.files[0].path
            page.update()

    pick_folder_button = ft.ElevatedButton(
        text="Seleccionar carpeta",
        icon=ft.Icons.FOLDER_OPEN,
        on_click=lambda _: dir_picker.get_directory_path()
    )
    pick_cookies_button = ft.ElevatedButton(
        text="Seleccionar cookies",
        icon=ft.Icons.FILE_OPEN,
        on_click=lambda _: file_picker.pick_files(allow_multiple=False)
    )

    # --- Botones de descarga ---
    def download_single_click(e):
        url = single_url_field.value.strip()
        folder = output_folder_field.value.strip()
        cookies = cookies_file_field.value.strip() or None

        chosen_video_codec = video_codec_dropdown.value
        chosen_audio_codec = audio_codec_dropdown.value

        if not url:
            log_message("Falta la URL del video.")
            return
        if not folder:
            log_message("Falta la carpeta de destino.")
            return

        try:
            if audio_only_check.value:
                # SOLO AUDIO
                log_message(f"[VIDEO SINGLE] Modo SOLO AUDIO => {url}")
                download_audio_only(
                    video_url=url,
                    output_folder=folder,
                    cookies_file=cookies,
                    audio_codec=chosen_audio_codec
                )
                log_message("Descarga de solo audio (video único) completada.\n")
            else:
                # VIDEO + AUDIO NORMAL
                log_message(f"Iniciando descarga de video: {url}")
                download_single_video(
                    video_url=url,
                    output_folder=folder,
                    cookies_file=cookies,
                    video_codec=chosen_video_codec,
                    audio_codec=chosen_audio_codec,
                )
                log_message("Descarga completada.\n")

        except Exception as ex:
            log_message(f"Error al descargar: {ex}\n")

    def download_playlist_click(e):
        url = playlist_url_field.value.strip()
        folder = output_folder_field.value.strip()
        cookies = cookies_file_field.value.strip() or None

        chosen_video_codec = video_codec_dropdown.value
        chosen_audio_codec = audio_codec_dropdown.value

        if not url:
            log_message("Falta la URL de la playlist.")
            return
        if not folder:
            log_message("Falta la carpeta de destino.")
            return

        try:
            if audio_only_check.value:
                # SOLO AUDIO (playlist)
                log_message(f"[PLAYLIST] Modo SOLO AUDIO => {url}")
                download_audio_only(
                    video_url=url,              # YT-DLP permite un playlist URL en 'download_audio_only'
                    output_folder=folder,
                    cookies_file=cookies,
                    audio_codec=chosen_audio_codec
                )
                log_message("Descarga de solo audio (playlist) finalizada.\n")
            else:
                # VIDEO + AUDIO (playlist)
                log_message(f"Iniciando descarga de playlist: {url}")
                download_playlist(
                    playlist_url=url,
                    output_folder=folder,
                    cookies_file=cookies,
                    log_file="descargas_registradas.txt",
                    video_codec=chosen_video_codec,
                    audio_codec=chosen_audio_codec,
                )
                log_message("Descarga de la playlist finalizada.\n")

        except Exception as ex:
            log_message(f"Error en la playlist: {ex}\n")

    btn_download_single = ft.ElevatedButton(
        text="Descargar Video",
        icon=ft.Icons.DOWNLOAD,
        on_click=download_single_click
    )

    btn_download_playlist = ft.ElevatedButton(
        text="Descargar Playlist",
        icon=ft.Icons.DOWNLOAD,
        on_click=download_playlist_click
    )

    # Checkbox para indicar SOLO AUDIO
    audio_only_check = AudioOnlyCheckbox(label="Descargar solo audio")

    # Ejemplo: botón con tu componente PrimaryButton (opcional).
    btn_primario = PrimaryButton(text="Botón Demo", icon=ft.Icons.STAR, on_click=lambda e: log_message("¡Botón primario presionado!"))

    # Interfaz
    page.add(
        ft.Column(
            controls=[
                ft.Text("Descargador de YT con Flet", style="headlineMedium"),
                single_url_field,
                playlist_url_field,
                ft.Row([output_folder_field, pick_folder_button]),
                ft.Row([cookies_file_field, pick_cookies_button]),
                ft.Row([
                    video_codec_dropdown,
                    audio_codec_dropdown,
                    # Nota: Separa la selección de códec de video/audio
                    # de los botones, para que el usuario defina primero qué desea.
                ]),
                ft.Row([
                    btn_download_single,
                    btn_download_playlist,
                    # Checkbox "Solo audio" al lado del botón de playlist (y sirve también para single).
                    audio_only_check,
                    btn_primario
                ]),
                ft.Text("Log de eventos:"),
                log_output
            ],
            expand=True,
        )
    )

    page.update()

if __name__ == "__main__":
    ft.app(target=main)
