# 📥 Cómo instalar Whisper y el modelo mediano

## ✅ Resumen
Este documento explica paso a paso cómo instalar Whisper y descargar el modelo mediano para tu proyecto.

---

## 📋 Requisitos previos

### 1. **Python instalado**
- Asegúrate de tener Python 3.8 o superior
- Verifica con: `python --version`

### 2. **pip actualizado**
```bash
python -m pip install --upgrade pip
```

---

## 🔧 Instalación de Whisper

### Paso 1: Instalar openai-whisper

Abre tu terminal/PowerShell en la carpeta del proyecto y ejecuta:

```bash
pip install openai-whisper
```

### Paso 2: Instalar NumPy (si no lo tienes)

```bash
pip install numpy
```

### Paso 3: **IMPORTANTE - Instalar ffmpeg en Windows**

Whisper requiere **ffmpeg** para procesar audio. Hay varias formas de instalarlo:

#### **Opción A: Con Chocolatey (Recomendado)**

Si tienes Chocolatey instalado:
```bash
choco install ffmpeg
```

#### **Opción B: Manual**

1. Ve a: https://ffmpeg.org/download.html
2. Descarga la versión para Windows (builds by BtbN o gyan.dev)
3. Extrae el archivo ZIP
4. Copia la carpeta `bin` que contiene `ffmpeg.exe`
5. Añade la ruta de la carpeta `bin` al PATH del sistema:
   - Busca "Variables de entorno" en Windows
   - En "Variables del sistema", selecciona `Path` y haz clic en "Editar"
   - Haz clic en "Nuevo" y añade la ruta completa a la carpeta `bin`
   - Ejemplo: `C:\ffmpeg\bin`
6. **Reinicia** tu terminal/PowerShell

#### **Verificar instalación de ffmpeg**

```bash
ffmpeg -version
```

Si ves la versión de ffmpeg, está correctamente instalado.

---

## 📦 Descarga del modelo mediano

### ¿Cómo se descarga el modelo?

**¡Buenas noticias!** No necesitas hacer nada adicional. El modelo mediano se descarga **automáticamente** la primera vez que lo uses.

### ¿Cuándo se descarga?

La primera vez que ejecutes tu aplicación y uses la transcripción, Whisper descargará el modelo automáticamente.

### ¿Cuánto tarda?

- **Tamaño del modelo medium:** ~1.5 GB
- **Tiempo de descarga:** Depende de tu conexión a internet (5-15 minutos aprox.)
- **Solo se descarga UNA VEZ**

### Proceso de descarga

Cuando ejecutes tu aplicación por primera vez:

1. Inicias la grabación
2. Verás un mensaje: `"Cargando modelo Whisper medium..."`
3. Whisper descarga el modelo en segundo plano
4. El modelo se guarda en cache para usos futuros
5. La próxima vez que uses la app, el modelo ya estará disponible

### ¿Dónde se guarda el modelo?

Whisper guarda los modelos en la carpeta cache del sistema:

- **Windows:** `C:\Users\<TuUsuario>\.cache\whisper\`
- **Linux/Mac:** `~/.cache/whisper/`

Puedes revisar esta carpeta para ver si el modelo está descargado.

---

## 🧪 Prueba de instalación

### Script de prueba rápido

Crea un archivo `test_whisper_instalacion.py` en la raíz de tu proyecto:

```python
import whisper
import sys

print("🔍 Verificando instalación de Whisper...")
print(f"Python: {sys.version}")

try:
    print("\n📥 Descargando/Cargando modelo 'medium'...")
    print("⚠️ Si es la primera vez, esto puede tardar varios minutos (~1.5GB)")
    
    modelo = whisper.load_model("medium")
    
    print("\n✅ ¡Modelo cargado correctamente!")
    print(f"📊 Información del modelo: {type(modelo)}")
    print("\n🎉 Whisper está correctamente instalado y listo para usar.")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nPosibles soluciones:")
    print("1. Verifica que ffmpeg esté instalado: ffmpeg -version")
    print("2. Reinstala whisper: pip uninstall openai-whisper && pip install openai-whisper")
    print("3. Verifica tu conexión a internet para descargar el modelo")
```

Ejecuta el script:
```bash
python test_whisper_instalacion.py
```

---

## 🚀 Modelos disponibles

Whisper tiene varios modelos. Puedes cambiar entre ellos según tus necesidades:

| Modelo | Tamaño | Desempeño | Velocidad | RAM necesaria |
|--------|--------|-----------|-----------|---------------|
| `tiny` | 39 MB | Básico | Muy rápido | ~1 GB |
| `base` | 74 MB | Aceptable | Rápido | ~1 GB |
| `small` | 244 MB | Bueno | Moderado | ~2 GB |
| **`medium`** | **1.5 GB** | **Muy bueno** | **Lento** | **~5 GB** |
| `large` | 2.9 GB | Excelente | Muy lento | ~10 GB |

### Cambiar de modelo

En los archivos ya modificados (`pantalla_preguntas.py` y `ventana_detalle_edit_pregunta_interno.py`), busca esta línea:

```python
self.hilo_grabacion = HiloTranscripcion(
    modelo_nombre="medium",  # <- Cambia aquí
    archivo_salida=ruta_audio_salida,
    idioma="es"
)
```

Cambia `"medium"` por cualquier otro modelo: `"tiny"`, `"base"`, `"small"`, o `"large"`.

---

## ⚡ Optimización (Opcional)

### Usar GPU para más velocidad

Si tienes una tarjeta gráfica NVIDIA con CUDA:

1. Instala PyTorch con soporte CUDA:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

2. En `transcripcionWhisper.py`, cambia `fp16=False` a `fp16=True` en las líneas 123 y 145.

Esto acelerará significativamente la transcripción.

---

## 🆘 Solución de problemas

### Error: "No module named 'whisper'"
**Solución:**
```bash
pip install openai-whisper
```

### Error: "ffmpeg not found"
**Solución:**
1. Instala ffmpeg (ver sección arriba)
2. Añade ffmpeg al PATH del sistema
3. **Reinicia** tu terminal/IDE

### La descarga del modelo falla
**Posibles causas:**
1. **Sin conexión a internet:** Verifica tu conexión
2. **Firewall/Antivirus:** Temporalmente desactiva el firewall
3. **Espacio insuficiente:** Asegúrate de tener al menos 2GB libres

### El modelo se descarga cada vez
**Problema:** La carpeta cache no persiste.
**Solución:** Verifica que la carpeta `C:\Users\<TuUsuario>\.cache\whisper\` exista y tenga permisos de escritura.

### La transcripción es muy lenta
**Soluciones:**
1. Usa un modelo más pequeño (`small` o `base`)
2. Si tienes GPU NVIDIA, activa fp16
3. Reduce la frecuencia de transcripción parcial

---

## ✅ Checklist de instalación

Marca cada paso cuando lo completes:

- [ ] Python 3.8+ instalado
- [ ] pip actualizado
- [ ] `openai-whisper` instalado (`pip install openai-whisper`)
- [ ] `numpy` instalado (`pip install numpy`)
- [ ] `ffmpeg` instalado y en PATH
- [ ] Terminal/IDE reiniciado después de instalar ffmpeg
- [ ] Ejecutado script de prueba `test_whisper_instalacion.py`
- [ ] Modelo descargado correctamente (se verá en la carpeta `.cache/whisper/`)
- [ ] Archivos del proyecto modificados (✅ ya hecho)
- [ ] Primera prueba de transcripción exitosa

---

## 🎯 Próximos pasos

Una vez completada la instalación:

1. **Ejecuta tu aplicación**
2. **Prueba la grabación** con el botón de micrófono
3. **Espera a que descargue el modelo** la primera vez (puede tardar)
4. **Verifica que la transcripción funcione** correctamente

---

## 📚 Recursos adicionales

- **Documentación oficial:** https://github.com/openai/whisper
- **Modelos disponibles:** https://github.com/openai/whisper#available-models-and-languages
- **Paper de investigación:** https://cdn.openai.com/papers/whisper.pdf
- **Instalación de ffmpeg:** https://ffmpeg.org/download.html

---

## 💡 Consejo final

**Para desarrollo/pruebas:** Usa el modelo `small` para probar más rápido.
**Para producción:** Usa el modelo `medium` para mejor calidad.

Puedes cambiar entre modelos fácilmente modificando el parámetro `modelo_nombre` en el código.
