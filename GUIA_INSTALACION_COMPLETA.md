# 📦 GUÍA DE INSTALACIÓN COMPLETA - Paso a Paso
## Para configurar el proyecto en otro PC

**FECHA:** 14 de febrero de 2026  
**SISTEMA:** Windows  
**PROYECTO:** Inperia con transcripción Whisper

---

## 📝 RESUMEN RÁPIDO

Lo que necesitas instalar:
1. Python 3.8 o superior
2. Dependencias Python (openai-whisper, PyQt5, etc.)
3. ffmpeg
4. El modelo Whisper se descarga automáticamente

**Tiempo estimado:** 30-45 minutos (incluye descargas)

---

# 🚀 INSTALACIÓN PASO A PASO

## PASO 1: Verificar Python

### 1.1. Comprobar si Python está instalado

Abre PowerShell o CMD y ejecuta:

```bash
python --version
```

**Resultado esperado:** `Python 3.8.x` o superior

### 1.2. Si NO tienes Python instalado

1. Ve a: https://www.python.org/downloads/
2. Descarga Python 3.11 o superior
3. Durante la instalación, **MARCA LA CASILLA**: ✅ "Add Python to PATH"
4. Instala con opciones por defecto
5. Reinicia el terminal
6. Verifica de nuevo: `python --version`

---

## PASO 2: Clonar/Copiar el proyecto

### 2.1. Si usas Git

```bash
# Navega a donde quieras el proyecto
cd C:\Users\TuUsuario\Documentos

# Clona el repositorio (si está en Git)
git clone <URL_DEL_REPOSITORIO>
cd Inperia
```

### 2.2. Si copias manualmente

1. Copia toda la carpeta del proyecto a tu nuevo PC
2. Navega a la carpeta en el terminal:

```bash
cd "C:\ruta\a\tu\proyecto\Inperia"
```

---

## PASO 3: Actualizar pip

```bash
python -m pip install --upgrade pip
```

---

## PASO 4: Instalar dependencias Python

### 4.1. Si tienes archivo `requirements.txt`

```bash
pip install -r requirements.txt
```

### 4.2. Si NO tienes `requirements.txt`, instala manualmente:

Copia y pega estos comandos uno por uno:

```bash
# Whisper y dependencias de audio
pip install openai-whisper

# PyQt5 para la interfaz gráfica
pip install PyQt5

# PyAudio para grabación de audio
pip install pyaudio

# Otras dependencias comunes
pip install numpy
pip install sounddevice
```

**NOTA:** Si `pyaudio` da error en Windows, usa:

```bash
pip install pipwin
pipwin install pyaudio
```

O descarga el wheel desde: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

---

## PASO 5: Instalar ffmpeg (CRÍTICO)

### Opción A: Con Chocolatey (MÁS FÁCIL)

#### 5.1. Instalar Chocolatey (si no lo tienes)

1. Abre PowerShell **como Administrador**
2. Ejecuta:

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

3. Cierra y abre PowerShell de nuevo

#### 5.2. Instalar ffmpeg con Chocolatey

```powershell
choco install ffmpeg
```

#### 5.3. Verificar instalación

```bash
ffmpeg -version
```

---

### Opción B: Instalación Manual de ffmpeg

#### 5.1. Descargar ffmpeg

1. Ve a: https://github.com/BtbN/FFmpeg-Builds/releases
2. Descarga: `ffmpeg-master-latest-win64-gpl.zip`
3. Extrae el archivo ZIP

#### 5.2. Añadir al PATH

1. Copia la carpeta extraída a: `C:\ffmpeg\`
2. La carpeta `bin` debe estar en: `C:\ffmpeg\bin\`
3. Añadir al PATH:
   - Presiona `Windows + R`
   - Escribe: `sysdm.cpl` → Enter
   - Pestaña **"Opciones avanzadas"**
   - **"Variables de entorno"**
   - En "Variables del sistema" → Busca `Path` → **"Editar"**
   - **"Nuevo"** → Pega: `C:\ffmpeg\bin`
   - **"Aceptar"** en todas las ventanas
   - **REINICIA EL TERMINAL**

#### 5.3. Verificar

```bash
ffmpeg -version
```

---

## PASO 6: Verificar instalación

### 6.1. Ejecutar script de prueba

```bash
python test_whisper_instalacion.py
```

**Esto hará:**
- ✅ Verifica que Whisper esté instalado
- ✅ **Descarga el modelo "medium" (~1.5GB)** ← Tarda varios minutos
- ✅ Confirma que todo funciona

**IMPORTANTE:** La primera vez que ejecutes esto, descargará el modelo Whisper medium (~1.5GB). Esto puede tardar 5-15 minutos dependiendo de tu conexión a internet.

### 6.2. Salida esperada

```
🔍 Verificando instalación de Whisper...
Python: 3.x.x

📥 Descargando/Cargando modelo 'medium'...
⚠️ Si es la primera vez, esto puede tardar varios minutos (~1.5GB)

✅ ¡Modelo cargado correctamente!
📊 Información del modelo: <class 'whisper.model.Whisper'>

🎉 Whisper está correctamente instalado y listo para usar.
```

---

## PASO 7: Probar la aplicación

### 7.1. Ejecutar la aplicación

```bash
# Según cómo se ejecute tu aplicación, puede ser:
python main.py

# O si tienes un archivo específico:
python "main GUI.py"
```

### 7.2. Probar la grabación

1. Abre la aplicación
2. Haz clic en el botón de micrófono 🎤
3. Habla algo
4. Verifica que transcribe correctamente

---

# 📋 COMANDOS COMPLETOS (RESUMEN)

Aquí tienes todos los comandos en orden, listos para copiar y pegar:

```bash
# 1. Verificar Python
python --version

# 2. Ir a la carpeta del proyecto
cd "C:\ruta\a\tu\proyecto\Inperia"

# 3. Actualizar pip
python -m pip install --upgrade pip

# 4. Instalar dependencias
pip install openai-whisper
pip install PyQt5
pip install pyaudio
pip install numpy
pip install sounddevice

# 5. Instalar ffmpeg (con Chocolatey)
# Abre PowerShell como Administrador:
choco install ffmpeg

# 6. Verificar ffmpeg
ffmpeg -version

# 7. Probar instalación y descargar modelo
python test_whisper_instalacion.py

# 8. Ejecutar aplicación
python main.py
```

---

# 📦 CREAR ARCHIVO requirements.txt

Para facilitar instalaciones futuras, crea un archivo `requirements.txt`:

### En el PC actual (donde ya funciona):

```bash
pip freeze > requirements.txt
```

### En el nuevo PC:

```bash
pip install -r requirements.txt
```

**Esto instalará todas las dependencias automáticamente.**

---

# 🔍 VERIFICACIÓN DE DEPENDENCIAS

Ejecuta este comando para ver qué tienes instalado:

```bash
pip list
```

**Busca estas librerías:**
- ✅ `openai-whisper`
- ✅ `PyQt5`
- ✅ `pyaudio`
- ✅ `numpy`
- ✅ `torch`
- ✅ `sounddevice`

---

# 🗂️ ESTRUCTURA DE ARCHIVOS NECESARIOS

Asegúrate de copiar estos archivos al nuevo PC:

```
Inperia/
├── main.py
├── main GUI.py
├── requirements.txt (si existe)
├── test_whisper_instalacion.py
├── assets/
│   ├── micro.png
│   ├── pausa.png
│   ├── play.png
│   └── ...
├── gui/
│   ├── pantalla_preguntas.py (modificado para Whisper)
│   ├── ventana_detalle_edit_pregunta_interno.py (modificado)
│   └── ...
├── utils/
│   ├── transcripcionWhisper.py (NUEVO)
│   └── ...
├── db/
├── controllers/
├── models/
└── data/
    └── grabaciones/
```

**NOTA:** NO necesitas copiar:
- ❌ `utils/vosk-es/` (ya no se usa)
- ❌ `__pycache__/` (se regenera automáticamente)
- ❌ `.git/` (si no usas control de versiones)

---

# ⚠️ PROBLEMAS COMUNES Y SOLUCIONES

## Error: "No module named 'PyQt5'"

```bash
pip install PyQt5
```

## Error: "No module named 'pyaudio'"

```bash
# Opción 1:
pip install pyaudio

# Opción 2 (si opción 1 falla en Windows):
pip install pipwin
pipwin install pyaudio
```

## Error: "ffmpeg not found"

1. Reinstala ffmpeg
2. Verifica que esté en el PATH
3. **REINICIA** el terminal/IDE
4. Verifica: `ffmpeg -version`

## Error: "No module named 'whisper'"

```bash
pip install openai-whisper
```

## El modelo Whisper no se descarga

1. Verifica tu conexión a internet
2. Verifica que tienes al menos 2GB de espacio libre
3. Desactiva temporalmente firewall/antivirus
4. Reintenta: `python test_whisper_instalacion.py`

## La transcripción es muy lenta

Cambia el modelo a `"small"` en los archivos:
- `gui/pantalla_preguntas.py` línea ~238
- `gui/ventana_detalle_edit_pregunta_interno.py` línea ~268

Busca:
```python
modelo_nombre="medium",
```

Cambia a:
```python
modelo_nombre="small",
```

---

# ✅ CHECKLIST DE INSTALACIÓN

Marca cada paso cuando lo completes:

- [ ] Python 3.8+ instalado y verificado
- [ ] Proyecto copiado/clonado al nuevo PC
- [ ] pip actualizado
- [ ] openai-whisper instalado
- [ ] PyQt5 instalado
- [ ] pyaudio instalado
- [ ] numpy instalado
- [ ] sounddevice instalado
- [ ] ffmpeg instalado y en PATH
- [ ] Terminal reiniciado después de instalar ffmpeg
- [ ] `test_whisper_instalacion.py` ejecutado exitosamente
- [ ] Modelo Whisper descargado (~1.5GB)
- [ ] Aplicación ejecutada correctamente
- [ ] Grabación con micrófono probada y funcionando

---

# 📊 TAMAÑOS DE DESCARGA

Para que sepas cuánto espacio y tiempo necesitas:

| Item | Tamaño | Tiempo estimado |
|------|--------|-----------------|
| Python 3.11 | ~25 MB | 2-5 min |
| openai-whisper + deps | ~300 MB | 3-10 min |
| ffmpeg | ~100 MB | 2-5 min |
| Modelo Whisper medium | **~1.5 GB** | **5-15 min** |
| **TOTAL** | **~2 GB** | **15-35 min** |

**Espacio en disco necesario:** Mínimo 3-4 GB libres

---

# 🎯 ORDEN RECOMENDADO

1. **Primero:** Python
2. **Segundo:** ffmpeg
3. **Tercero:** Dependencias Python (openai-whisper, PyQt5, etc.)
4. **Cuarto:** Modelo Whisper (se descarga automáticamente)
5. **Quinto:** Probar la aplicación

---

# 📞 AYUDA ADICIONAL

Si tienes problemas, consulta:
- `INSTALACION_WHISPER.md` - Guía detallada de Whisper
- `INSTALAR_FFMPEG.md` - Guía detallada de ffmpeg
- `MIGRACION_VOSK_A_WHISPER.md` - Detalles técnicos

---

# 🎉 ¡LISTO!

Una vez completados todos los pasos, tu aplicación estará funcionando en el nuevo PC con transcripción Whisper.

**Recuerda:** La primera vez que uses la grabación, puede tardar unos segundos más porque está cargando el modelo desde cache.
