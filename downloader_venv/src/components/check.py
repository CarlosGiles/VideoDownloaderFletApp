# src/components/check.py

import flet as ft

def AudioOnlyCheckbox(on_change=None, label=None, label_color=None):
    """
    Checkbox para indicar que se desea descargar solo la pista de audio.
    :param on_change: función que se ejecuta cuando cambia el estado del checkbox.
    """
    return ft.Checkbox(
        label=label,
        value=False,        # Por defecto desmarcado
        on_change=on_change, # Evento que se dispara al marcar/desmarcar
        label_style=ft.TextStyle(color=label_color) if label_color else None
    )
