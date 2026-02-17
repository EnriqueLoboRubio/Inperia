# 🚀 INSTALACIÓN RÁPIDA - OTRO PC

## 📋 RESUMEN EN 3 PASOS

### 1️⃣ INSTALACIONES BÁSICAS

```bash
# Verificar Python (3.8+)
python --version

# Actualizar pip
python -m pip install --upgrade pip
```

---

### 2️⃣ INSTALAR TODO

```bash
# Dependencias Python
pip install openai-whisper PyQt5 pyaudio numpy sounddevice

# ffmpeg (PowerShell como Administrador)
choco install ffmpeg
```

---

### 3️⃣ DESCARGAR MODELO Y PROBAR

```bash
# Descargar modelo Whisper (~1.5GB) - Tarda 5-15 min
python test_whisper_instalacion.py

# Ejecutar aplicación
python main.py
```

---

## 🎯 ORDEN DE INSTALACIÓN

1. **Python** → https://www.python.org/downloads/
2. **Chocolatey** (para ffmpeg) → Ver abajo
3. **Dependencias Python** → `pip install ...`
4. **ffmpeg** → `choco install ffmpeg`
5. **Modelo Whisper** → Se descarga automáticamente

---

## 💻 INSTALAR CHOCOLATEY

**PowerShell como Administrador:**

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

---

## ✅ VERIFICACIÓN

```bash
# Verificar Python
python --version

# Verificar ffmpeg
ffmpeg -version

# Ver paquetes instalados
pip list
```

Busca: `openai-whisper`, `PyQt5`, `pyaudio`, `numpy`, `torch`

---

## ⚠️ SI ALGO FALLA

### pyaudio no instala:
```bash
pip install pipwin
pipwin install pyaudio
```

### ffmpeg no se reconoce:
1. Reinicia el terminal
2. Verifica PATH del sistema
3. Ver `INSTALAR_FFMPEG.md`

### Modelo no se descarga:
- Verifica conexión a internet
- Necesitas 2GB libres en disco
- Reinténtalo

---

## 📂 ARCHIVOS IMPORTANTES

- ✅ `transcripcionWhisper.py` - Nuevo módulo
- ✅ `pantalla_preguntas.py` - Modificado
- ✅ `ventana_detalle_edit_pregunta_interno.py` - Modificado
- ✅ `test_whisper_instalacion.py` - Script de prueba

---

## 📚 DOCUMENTACIÓN COMPLETA

- **`GUIA_INSTALACION_COMPLETA.md`** ← Guía paso a paso detallada
- **`COMANDOS_INSTALACION.txt`** ← Solo comandos para copiar
- **`INSTALAR_FFMPEG.md`** ← Guía completa de ffmpeg
- **`INSTALACION_WHISPER.md`** ← Guía completa de Whisper

---

## ⏱️ TIEMPO ESTIMADO

- Python: 5 min
- Chocolatey: 2 min
- Dependencias: 5-10 min
- ffmpeg: 3 min
- **Modelo Whisper: 5-15 min** ⚠️
- **TOTAL: 20-35 min**

---

## 💾 ESPACIO NECESARIO

- Dependencias Python: ~300 MB
- ffmpeg: ~100 MB
- **Modelo Whisper: ~1.5 GB**
- **TOTAL: ~2 GB**

---

## 🎉 ¡LISTO PARA USAR!

Una vez instalado todo, tu aplicación transcribirá con **Whisper** que es:
- ✅ Más preciso que Vosk
- ✅ Mejor con acentos
- ✅ Mejor con ruido de fondo
- ⚠️ Un poco más lento (2-3 segundos)
