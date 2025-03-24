# theme_cyberpunk.py

import flet as ft

def get_cyberpunk_theme() -> ft.Theme:
    return ft.Theme(
        color_scheme=ft.ColorScheme(
            primary="#36CACC",#36CACC
            secondary="#CB1F5A",
            background="#D3CACE",
            surface="#327987",
            error="#CB1F5A",
            on_background="#D3CACE",
            #on_surface="#21303B",
            # Si quieres on_primary, on_secondary, etc. agrégalos
        )
    )
