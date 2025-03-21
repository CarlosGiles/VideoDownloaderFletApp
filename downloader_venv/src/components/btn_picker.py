# src/components/btn_picker.py

import flet as ft

def FolderPickerButton(text: str = "Seleccionar carpeta",
                       icon=ft.icons.FOLDER_OPEN,
                       picker_control: ft.FilePicker = None,
                       bgcolor=None, color=None, style=None
):
    """
    Botón reutilizable para abrir el diálogo de selección de carpeta.
    :param text: Texto del botón.
    :param icon: Ícono para el botón (por defecto, ft.icons.FOLDER_OPEN).
    :param picker_control: Instancia de ft.FilePicker configurada en main.py
                           para recibir la ruta de la carpeta seleccionada.
    :param bgcolor: Color de fondo del botón.
    :param color: Color del texto del botón.
    :param style: Estilo adicional para el botón.
    """
    return ft.ElevatedButton(text=text,
                             icon=icon,
                             bgcolor=bgcolor,
                             color=color,
                             style=style,
                             on_click=lambda _: picker_control.get_directory_path()
    )

def CookiesPickerButton(text: str = "Seleccionar cookies",
                        icon=ft.icons.FILE_OPEN,
                        picker_control: ft.FilePicker = None,
                        bgcolor=None, color=None, style=None
    
):
    """
    Botón reutilizable para abrir el diálogo de selección de archivo de cookies.
    :param text: Texto del botón.
    :param icon: Ícono para el botón (por defecto, ft.icons.FILE_OPEN).
    :param picker_control: Instancia de ft.FilePicker configurada en main.py
                           para recibir el archivo de cookies seleccionado.
    """
    return ft.ElevatedButton(text=text,
                             icon=icon,
                             on_click=lambda _: picker_control.pick_files(allow_multiple=False),
                             bgcolor=bgcolor, color=color, style=style
    )
