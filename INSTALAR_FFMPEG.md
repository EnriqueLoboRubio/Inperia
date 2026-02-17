# ⚠️ IMPORTANTE: Instalar ffmpeg

## 🚨 NECESARIO PARA QUE FUNCIONE WHISPER

ffmpeg es un requisito **OBLIGATORIO** para que Whisper funcione.

---

## 🪟 Instalación en Windows

### Opción 1: Con Chocolatey (MÁS FÁCIL)

Si tienes Chocolatey instalado, abre PowerShell como Administrador y ejecuta:

```powershell
choco install ffmpeg
```

Luego **reinicia** tu terminal o IDE.

---

### Opción 2: Instalación Manual

#### Paso 1: Descargar ffmpeg

Ve a una de estas páginas:
- https://github.com/BtbN/FFmpeg-Builds/releases
- https://www.gyan.dev/ffmpeg/builds/

Descarga la versión "**ffmpeg-release-full.7z**" o "**ffmpeg-git-full.7z**"

#### Paso 2: Extraer el archivo

1. Extrae el archivo descargado (necesitarás 7-Zip o WinRAR)
2. Obtendrás una carpeta llamada `ffmpeg-xxxxx`
3. Dentro encontrarás una carpeta `bin` con `ffmpeg.exe`

#### Paso 3: Añadir al PATH

**Método visual:**
1. Copia la ruta completa de la carpeta `bin`
   - Ejemplo: `C:\ffmpeg\bin`
2. Presiona `Windows + R`
3. Escribe: `sysdm.cpl` y presiona Enter
4. Ve a la pestaña **"Opciones avanzadas"**
5. Haz clic en **"Variables de entorno"**
6. En "Variables del sistema", busca `Path` y haz clic en **"Editar"**
7. Haz clic en **"Nuevo"**
8. Pega la ruta de la carpeta `bin` (ejemplo: `C:\ffmpeg\bin`)
9. Haz clic en **"Aceptar"** en todas las ventanas
10. **REINICIA** tu terminal/PowerShell/IDE

**Método por comando (PowerShell como Administrador):**
```powershell
# Reemplaza C:\ffmpeg\bin con tu ruta real
$env:Path += ";C:\ffmpeg\bin"
[System.Environment]::SetEnvironmentVariable("Path", $env:Path, [System.EnvironmentVariableTarget]::Machine)
```

#### Paso 4: Verificar

**REINICIA** tu terminal o IDE, luego ejecuta:

```bash
ffmpeg -version
```

Si ves la versión de ffmpeg, ¡está instalado correctamente! ✅

---

## 🐧 Instalación en Linux

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install ffmpeg
```

### Fedora
```bash
sudo dnf install ffmpeg
```

### Arch Linux
```bash
sudo pacman -S ffmpeg
```

---

## 🍎 Instalación en macOS

### Con Homebrew
```bash
brew install ffmpeg
```

---

## ✅ Verificación

Ejecuta en tu terminal:

```bash
ffmpeg -version
```

**Salida esperada:**
```
ffmpeg version x.x.x ...
```

Si ves esto, ✅ **ffmpeg está correctamente instalado**.

---

## 🆘 Problemas comunes

### "ffmpeg no se reconoce como comando"

**Causas:**
1. No reiniciaste el terminal/IDE después de la instalación
2. La ruta no se añadió correctamente al PATH
3. La instalación falló

**Soluciones:**
1. **Reinicia** tu terminal/IDE (importante)
2. Verifica que la carpeta `bin` esté en el PATH del sistema
3. Reinstala ffmpeg

### "No tengo permisos para instalar"

**Solución:** Ejecuta PowerShell/Terminal como Administrador

### "Chocolatey no está instalado"

**Solución:** Usa la opción manual o instala Chocolatey desde: https://chocolatey.org/install

---

## 📊 Después de instalar

Una vez instalado ffmpeg:

1. ✅ Reinicia tu terminal/IDE
2. ✅ Verifica con: `ffmpeg -version`
3. ✅ Ejecuta el script de prueba: `python test_whisper_instalacion.py`
4. ✅ Prueba tu aplicación con el micrófono

---

## 🎯 ¿Por qué es necesario ffmpeg?

Whisper usa ffmpeg para:
- Convertir formatos de audio
- Procesar archivos de audio
- Decodificar streams de audio

**Sin ffmpeg, Whisper dará error al intentar transcribir.**

---

## 💡 Consejo

Si trabajas en varios proyectos de audio/video, ffmpeg es una herramienta muy útil de tener instalada globalmente en tu sistema.

---

**Una vez instalado y verificado, estarás listo para usar Whisper! 🎉**
