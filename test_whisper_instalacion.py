import whisper
import sys

print("🔍 Verificando instalación de Whisper...")
print(f"Python: {sys.version}")

try:
    print("\n📥 Descargando/Cargando modelo 'medium'...")
    print("⚠️ Si es la primera vez, esto puede tardar varios minutos (~1.5GB)")
    print("   El modelo se descargará automáticamente desde internet.")
    print("   Ubicación: C:\\Users\\<TuUsuario>\\.cache\\whisper\\")
    
    modelo = whisper.load_model("medium")
    
    print("\n✅ ¡Modelo cargado correctamente!")
    print(f"📊 Información del modelo: {type(modelo)}")
    print("\n🎉 Whisper está correctamente instalado y listo para usar.")
    print("\n📂 El modelo ha sido descargado y guardado en cache.")
    print("   La próxima vez que uses la aplicación, cargará mucho más rápido.")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nPosibles soluciones:")
    print("1. Verifica que ffmpeg esté instalado: ffmpeg -version")
    print("2. Reinstala whisper: pip uninstall openai-whisper && pip install openai-whisper")
    print("3. Verifica tu conexión a internet para descargar el modelo")
    print("4. Asegúrate de tener al menos 2GB de espacio libre en disco")
