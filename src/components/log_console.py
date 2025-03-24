# src/components/log_console.py

"""
Este módulo define un Logging Handler que redirige los mensajes de logging
a un control de texto en Flet, de modo que el usuario pueda verlos en la
interfaz gráfica.
"""

import logging
import flet as ft

class FletLogHandler(logging.Handler):
    """
    Handler personalizado para redirigir los logs de Python
    a un componente de Flet (por ejemplo, ft.Text o ft.TextField).

    Atributos:
    ----------
    text_control : ft.Control
        Control de Flet donde se mostrarán los logs (ej: ft.Text o ft.TextField).
    page : ft.Page
        Página de Flet donde se actualiza el contenido del 'text_control'.
    """

    def __init__(self, text_control: ft.Control, page: ft.Page):
        """
        Constructor del FletLogHandler.

        Parámetros:
        -----------
        text_control : ft.Control
            Instancia de un control de Flet (ft.Text, ft.TextField, etc.)
            en el que se insertarán los mensajes de log.
        page : ft.Page
            Página de Flet que se actualizará tras cada mensaje.
        """
        super().__init__()
        self.text_control = text_control
        self.page = page
        # Configura el formato de los mensajes (fecha, nivel y mensaje).
        self.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )

    def emit(self, record: logging.LogRecord):
        """
        Emite el mensaje de log hacia el control de Flet.
        Cada vez que se llama un 'logging.info()', 'logging.error()', etc.,
        este método inserta el texto en 'self.text_control'.
        """
        try:
            # Formatear el mensaje usando Formatter
            msg = self.format(record)
            # Agregar el texto con salto de línea
            self.text_control.value += msg + "\n"
            # Refrescar la página para que el usuario vea el cambio
            self.page.update()
        except Exception:
            self.handleError(record)
