# Inperia

## Instalación

1. **Instalar las dependencias de Python:**

Puedes instalar todas las librerías necesarias con el siguiente comando:

```bash
pip install -r requirements.txt
```

O si prefieres instalarlas manualmente, aquí tienes la lista:
```bash
pip install PyQt5 bcrypt sounddevice PyAudio vosk openai-whisper numpy reportlab
```

2. **Modelos Adicionales (Vosk y Whisper):**

- **Vosk:** Es necesario descargar el modelo de lenguaje de Vosk (por ejemplo, `vosk-model-es-0.42`) desde [https://alphacephei.com/vosk/models](https://alphacephei.com/vosk/models) y colocarlo en la carpeta correspondiente.
- **Whisper (LLM):** Whisper descargará los modelos necesarios (como el modelo 'medium' o el que tengas configurado) automáticamente la primera vez que se ejecute una transcripción, pero requiere conexión a Internet.

_Nota: Asegúrate de tener instalados los compiladores necesarios en Windows o descargar el instalador precompilado (Wheel) en caso de experimentar problemas al instalar `PyAudio` o `bcrypt`._
