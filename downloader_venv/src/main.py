# src/main.py

import flet as ft
import os

from download_single import download_single_video
from download_playlist import download_playlist
from codecs_config import (
    VIDEO_CODECS, AUDIO_CODECS,
    DEFAULT_VIDEO_CODEC, DEFAULT_AUDIO_CODEC
)

def main(page: ft.Page):
    page.title = "Descargador de YouTube con Flet"
    page.window_width = 800
    page.window_height = 600

    # Campos
    single_url_field = ft.TextField(label="URL de Video", width=500)
    playlist_url_field = ft.TextField(label="URL de Lista de Reproducción", width=500)
    output_folder_field = ft.TextField(label="Carpeta de destino", width=500, read_only=True)
    cookies_file_field = ft.TextField(label="Archivo de Cookies (opcional)", width=500, read_only=True)

    # DropDown para video
    video_codec_dropdown = ft.Dropdown(
        label="Códec de Video",
        width=200,
        value=DEFAULT_VIDEO_CODEC,  # valor por defecto
        options=[ft.dropdown.Option(v) for v in VIDEO_CODECS],
    )
    # DropDown para audio
    audio_codec_dropdown = ft.Dropdown(
        label="Códec de Audio",
        width=200,
        value=DEFAULT_AUDIO_CODEC,  # valor por defecto
        options=[ft.dropdown.Option(a) for a in AUDIO_CODECS],
    )

    # Text para log
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
        icon=ft.icons.FOLDER_OPEN,
        on_click=lambda _: dir_picker.get_directory_path()
    )
    pick_cookies_button = ft.ElevatedButton(
        text="Seleccionar cookies",
        icon=ft.icons.FILE_OPEN,
        on_click=lambda _: file_picker.pick_files(allow_multiple=False)
    )

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
        icon=ft.icons.DOWNLOAD,
        on_click=download_single_click
    )
    btn_download_playlist = ft.ElevatedButton(
        text="Descargar Playlist",
        icon=ft.icons.DOWNLOAD,
        on_click=download_playlist_click
    )

    page.add(
        ft.Column(
            controls=[
                ft.Text("Descargador de YouTube con Flet", style="headlineMedium"),
                single_url_field,
                playlist_url_field,
                ft.Row([output_folder_field, pick_folder_button]),
                ft.Row([cookies_file_field, pick_cookies_button]),
                ft.Row([video_codec_dropdown, audio_codec_dropdown]),
                ft.Row([btn_download_single, btn_download_playlist]),
                ft.Text("Log de eventos:"),
                log_output
            ],
            expand=True,
        )
    )
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
