# src/themes/theme_cyberpunk.py

import flet as ft

PRIMARY_COLOR = "#36CACC"
SECONDARY_COLOR = "#CB1F5A"
BACKGROUND_COLOR = "#21303B"
SURFACE_COLOR = "#327987"
ERROR_COLOR = "#D3CACE"
ON_BACKGROUND_COLOR = "#D3CACE"
ON_SURFACE_COLOR = "#FFFFFF"

def get_cyberpunk_theme() -> ft.Theme:
    # Creamos un objeto ColorScheme con tus colores
    scheme = ft.ColorScheme(
        primary=PRIMARY_COLOR,
        secondary=SECONDARY_COLOR,
        background=BACKGROUND_COLOR,
        surface=SURFACE_COLOR,
        error=ERROR_COLOR,
        on_background=ON_BACKGROUND_COLOR,
        on_surface=ON_SURFACE_COLOR,
        # Si quieres también on_primary, on_secondary, etc. agrégalos aquí
    )
    
    # Retornamos Theme usando color_scheme
    return ft.Theme(
        color_scheme=scheme,
        # Opcionalmente, si quieres un seed particular:
        # color_scheme_seed=ft.Colors.from_hex(PRIMARY_COLOR),
        # use_material3=True,   # si deseas Material 3
    )
