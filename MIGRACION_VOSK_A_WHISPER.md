# Migración de Vosk a Whisper para Transcripción

## 📋 Resumen
Este documento explica cómo migrar de **Vosk** a **Whisper** (modelo mediano) para la transcripción de audio en el proyecto Inperia.

## 🔄 Diferencias principales entre Vosk y Whisper

| Aspecto | Vosk | Whisper |
|---------|------|---------|
| **Velocidad** | Muy rápido (tiempo real) | Más lento (procesa por lotes) |
| **Precisión** | Buena | Excelente |
| **Tamaño modelo** | ~50MB (español pequeño) | ~1.5GB (medium) |
| **Dependencias** | Vosk | OpenAI Whisper, ffmpeg |
| **Transcripción** | Stream en tiempo real | Por lotes (cada X segundos) |
| **Idiomas** | Requiere modelo específico | Multi-idioma en un solo modelo |

## 📝 Pasos para la migración

### 1. Instalar dependencias

Primero, instala Whisper y sus dependencias:

```bash
pip install openai-whisper numpy
```

**IMPORTANTE**: Whisper también requiere `ffmpeg`. En Windows:
- Descarga ffmpeg desde: https://ffmpeg.org/download.html
- Extrae y añade la carpeta `bin` al PATH del sistema
- O instala con chocolatey: `choco install ffmpeg`

### 2. Archivo creado: `transcripcionWhisper.py`

Ya se ha creado el archivo `utils/transcripcionWhisper.py` que:
- Mantiene la **misma interfaz** que `transcripcionVosk.py`
- Usa las mismas señales PyQt5: `texto_signal`, `error_signal`, `parcial_signal`
- Funciona de forma similar para facilitar la migración

### 3. Modificar los archivos que usan la transcripción

Necesitas actualizar estos archivos para usar el nuevo módulo:

#### Archivo 1: `gui/pantalla_preguntas.py`
**Cambio en línea 9:**
```python
# ANTES:
from utils.transcripcionVosk import HiloTranscripcion

# DESPUÉS:
from utils.transcripcionWhisper import HiloTranscripcion
```

#### Archivo 2: `gui/ventana_detalle_edit_pregunta_interno.py`
**Cambio en línea 8:**
```python
# ANTES:
from utils.transcripcionVosk import HiloTranscripcion

# DESPUÉS:
from utils.transcripcionWhisper import HiloTranscripcion
```

### 4. Actualizar la inicialización del hilo de transcripción

**IMPORTANTE**: El constructor ha cambiado.

#### Con Vosk (ANTES):
```python
self.hilo_transcripcion = HiloTranscripcion(
    ruta_modelo="utils/vosk-es",  # Ruta al modelo Vosk
    archivo_salida="grabacion.wav"
)
```

#### Con Whisper (DESPUÉS):
```python
self.hilo_transcripcion = HiloTranscripcion(
    modelo_nombre="medium",  # Tamaño del modelo: tiny, base, small, medium, large
    archivo_salida="grabacion.wav",
    idioma="es"  # Código de idioma
)
```

### 5. Modelos disponibles de Whisper

Whisper tiene varios tamaños de modelo:

| Modelo | Tamaño | Calidad | Velocidad | Recomendado para |
|--------|--------|---------|-----------|------------------|
| `tiny` | ~39 MB | Baja | Muy rápido | Pruebas rápidas |
| `base` | ~74 MB | Media | Rápido | Uso ligero |
| `small` | ~244 MB | Buena | Moderado | Buen equilibrio |
| **`medium`** | ~1.5 GB | Muy buena | Lento | **Producción (recomendado)** |
| `large` | ~2.9 GB | Excelente | Muy lento | Máxima calidad |

**La primera vez que uses un modelo, Whisper lo descargará automáticamente.**

### 6. Consideraciones importantes

#### ⚡ Rendimiento
- **Whisper es más lento** que Vosk, especialmente en CPU
- La transcripción parcial se hace cada 3 segundos (configurable)
- Para mejor rendimiento, considera usar GPU si está disponible

#### 🎯 Precisión
- Whisper es **significativamente más preciso** que Vosk
- Maneja mejor acentos y ruido de fondo
- Funciona bien con español de diferentes regiones

#### 💾 Almacenamiento
- El modelo `medium` ocupa ~1.5GB en disco
- Se almacena en cache: `~/.cache/whisper/` (Linux/Mac) o `%USERPROFILE%\.cache\whisper\` (Windows)

#### 🔊 Transcripción en tiempo real
- Vosk transcribe **palabra por palabra** en tiempo real
- Whisper transcribe **por lotes cada X segundos** (configurado en 3 segundos)
- La experiencia del usuario puede sentirse menos "instantánea"

### 7. Optimizaciones opcionales

#### Ajustar frecuencia de transcripción parcial
En `transcripcionWhisper.py`, línea 38:
```python
self.PARTIAL_DURATION = 3  # Cambiar a 2 para actualizar cada 2 segundos
```

#### Usar modelo más pequeño para desarrollo
Durante desarrollo, puedes usar `small` o `base` para más velocidad:
```python
self.hilo_transcripcion = HiloTranscripcion(
    modelo_nombre="small",  # Más rápido que medium
    archivo_salida="grabacion.wav",
    idioma="es"
)
```

#### Habilitar GPU (opcional, requiere CUDA)
Si tienes GPU NVIDIA con CUDA:
```bash
pip install openai-whisper[gpu]
```

Luego en `transcripcionWhisper.py`, cambia `fp16=False` a `fp16=True` en las líneas de transcripción.

## 🧪 Prueba de migración

### Prueba básica
1. Asegúrate de que las dependencias estén instaladas
2. Cambia los imports como se indica arriba
3. Ejecuta la aplicación
4. Prueba la funcionalidad de transcripción

### Script de prueba rápido
Puedes crear un archivo `test_whisper.py` para probar:

```python
from utils.transcripcionWhisper import HiloTranscripcion
from PyQt5.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)

def on_texto(texto):
    print(f"TEXTO FINAL: {texto}")

def on_parcial(texto):
    print(f"Parcial: {texto}")

def on_error(error):
    print(f"ERROR: {error}")

hilo = HiloTranscripcion(modelo_nombre="medium", idioma="es")
hilo.texto_signal.connect(on_texto)
hilo.parcial_signal.connect(on_parcial)
hilo.error_signal.connect(on_error)
hilo.start()

print("Grabando... Presiona Ctrl+C para detener")
try:
    app.exec_()
except KeyboardInterrupt:
    hilo.detener()
    hilo.wait()
```

## 📊 Comparación de resultados esperados

### Vosk
- ✅ Muy rápido, transcripción instantánea
- ⚠️ Puede tener errores con acentos o ruido
- ✅ Funciona bien en equipos antiguos

### Whisper (medium)
- ✅ Muy preciso, menos errores
- ✅ Mejor con ruido de fondo
- ⚠️ Más lento (retraso de ~3 segundos)
- ⚠️ Requiere más recursos

## 🔙 Volver a Vosk

Si necesitas volver a Vosk, simplemente:
1. Cambia los imports de vuelta a `transcripcionVosk`
2. Ajusta el constructor para usar `ruta_modelo` en lugar de `modelo_nombre`

## ✅ Checklist de migración

- [ ] Instalar `openai-whisper` y `numpy`
- [ ] Instalar `ffmpeg` (Windows)
- [ ] Crear archivo `transcripcionWhisper.py` (✓ ya creado)
- [ ] Actualizar import en `gui/pantalla_preguntas.py`
- [ ] Actualizar import en `gui/ventana_detalle_edit_pregunta_interno.py`
- [ ] Actualizar inicialización del HiloTranscripcion
- [ ] Probar la aplicación
- [ ] Verificar que la transcripción funciona correctamente

## 🆘 Solución de problemas

### Error: "No module named 'whisper'"
```bash
pip install openai-whisper
```

### Error: "ffmpeg not found"
- Instala ffmpeg y añádelo al PATH del sistema
- Reinicia el terminal/IDE después de instalarlo

### La transcripción es muy lenta
- Usa un modelo más pequeño (`small` o `base`)
- Considera usar GPU si está disponible
- Aumenta `PARTIAL_DURATION` para actualizar menos frecuentemente

### El modelo no se descarga
- Verifica tu conexión a internet
- El modelo se descarga automáticamente la primera vez
- Puede tardar varios minutos (model medium ~1.5GB)

## 📚 Recursos adicionales

- Documentación oficial de Whisper: https://github.com/openai/whisper
- Modelos disponibles: https://github.com/openai/whisper#available-models-and-languages
- Paper de investigación: https://cdn.openai.com/papers/whisper.pdf
