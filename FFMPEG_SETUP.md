# Configuración de FFmpeg para VideoDownloader

## Problema

El error `ERROR: You have requested merging of multiple formats but ffmpeg is not installed` ocurre porque `yt-dlp` necesita FFmpeg para combinar streams de video y audio de alta calidad.

## Solución Implementada

### 1. Detección Automática de FFmpeg

El sistema ahora detecta automáticamente FFmpeg en las siguientes ubicaciones:
- `C:\ffmpeg\bin`
- `C:\Program Files\ffmpeg\bin`
- `C:\Program Files (x86)\ffmpeg\bin`
- `%USERPROFILE%\ffmpeg\bin`
- `%USERPROFILE%\AppData\Local\ffmpeg\bin`
- PATH del sistema

### 2. Configuración Automática

El código ahora configura automáticamente `yt-dlp` para usar FFmpeg cuando está disponible:

```python
from scripts.ffmpeg_utils import configure_ffmpeg_for_ydl, is_ffmpeg_available

# En las funciones de descarga:
ydl_opts = configure_ffmpeg_for_ydl(ydl_opts)

if not is_ffmpeg_available():
    print("Advertencia: FFmpeg no disponible. Usando formatos alternativos...")
    ydl_opts["format"] = "best[ext=mp4]/best"
    ydl_opts["postprocessors"] = []
```

### 3. Modo Fallback

Si FFmpeg no está disponible, el sistema automáticamente:
- Cambia a formatos pre-combinados (`best[ext=mp4]/best`)
- Desactiva los postprocesadores que requieren FFmpeg
- Muestra advertencias informativas al usuario

## Instalación de FFmpeg

### Opción 1: Chocolatey (Recomendada)
```powershell
# Instalar Chocolatey si no lo tienes
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Instalar FFmpeg
choco install ffmpeg
```

### Opción 2: Descarga Manual
1. Descargar FFmpeg desde https://www.gyan.dev/ffmpeg/builds/
2. Extraer a `C:\ffmpeg`
3. Añadir `C:\ffmpeg\bin` al PATH del sistema

### Opción 3: Configuración Temporal del PATH
```powershell
# Para la sesión actual de PowerShell
$env:PATH += ";C:\ffmpeg\bin"

# Para verificar
ffmpeg -version
```

## Verificación

Usa el script de prueba incluido:
```bash
python test_ffmpeg.py
```

## Notas Técnicas

- **Formatos Soportados**: Con FFmpeg disponible, se pueden descargar formatos de alta calidad (1080p+, 4K) que requieren combinar streams separados de video y audio.
- **Sin FFmpeg**: Se limita a formatos pre-combinados, generalmente de menor calidad (720p max en la mayoría de casos).
- **Detección Automática**: El sistema verifica FFmpeg al inicio de cada descarga y ajusta automáticamente el comportamiento.

## Solución de Problemas

1. **FFmpeg no detectado pero está instalado:**
   - Verificar que `ffmpeg.exe` esté en la ruta especificada
   - Probar ejecutar `ffmpeg -version` manualmente
   - Reiniciar la terminal después de modificar el PATH

2. **Descargas lentas o de baja calidad:**
   - Instalar FFmpeg para acceder a formatos de alta calidad
   - Verificar conexión a internet
   - Considerar usar diferentes servidores de descarga

3. **Errores de permisos:**
   - Ejecutar como administrador si es necesario
   - Verificar permisos de escritura en la carpeta de destino