# src/components/btn.py

import flet as ft

def PrimaryButton(text: str, on_click=None, icon=None, bgcolor=None, color=None, style=None):
    """
    Botón principal reutilizable.
    - Param 'text' define el texto del botón.
    - Param 'on_click' recibe la función que se ejecutará al hacer clic.
    """
    return ft.ElevatedButton(
        text=text,
        on_click=on_click,
        bgcolor=bgcolor,
        color=color,
        icon=icon,
        style=style,
    )
