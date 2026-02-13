"""
Script de diagnóstico para verificar el micrófono
"""
import pyaudio
import sounddevice as sd

print("=" * 60)
print("DIAGNÓSTICO DEL MICRÓFONO")
print("=" * 60)

# 1. Verificar dispositivos con sounddevice
print("\n1. DISPOSITIVOS DISPONIBLES (sounddevice):")
print("-" * 60)
try:
    devices = sd.query_devices()
    print(devices)
    
    # Mostrar dispositivo de entrada por defecto
    default_input = sd.query_devices(kind='input')
    print("\nDispositivo de ENTRADA por defecto:")
    print(default_input)
except Exception as e:
    print(f"❌ Error al consultar dispositivos con sounddevice: {e}")

# 2. Verificar dispositivos con PyAudio
print("\n2. DISPOSITIVOS DISPONIBLES (PyAudio):")
print("-" * 60)
try:
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    
    print(f"Total de dispositivos encontrados: {numdevices}\n")
    
    input_devices = []
    for i in range(0, numdevices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        if device_info.get('maxInputChannels') > 0:
            input_devices.append((i, device_info))
            print(f"[{i}] {device_info.get('name')}")
            print(f"    - Canales de entrada: {device_info.get('maxInputChannels')}")
            print(f"    - Sample Rate: {device_info.get('defaultSampleRate')}")
            print()
    
    if not input_devices:
        print("⚠️ NO SE ENCONTRARON DISPOSITIVOS DE ENTRADA")
    
    # Obtener dispositivo por defecto
    try:
        default_device = p.get_default_input_device_info()
        print(f"Dispositivo de entrada por defecto: {default_device.get('name')}")
    except Exception as e:
        print(f"❌ No hay dispositivo de entrada por defecto: {e}")
    
    p.terminate()
    
except Exception as e:
    print(f"❌ Error al consultar dispositivos con PyAudio: {e}")

# 3. Intentar abrir un stream de audio
print("\n3. PRUEBA DE ACCESO AL MICRÓFONO:")
print("-" * 60)
try:
    p = pyaudio.PyAudio()
    
    print("Intentando abrir stream de audio...")
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=4000
    )
    
    print("✅ Stream abierto correctamente!")
    print("Grabando 2 segundos de audio...")
    
    # Leer algunos frames para verificar
    for i in range(0, int(16000 / 4000 * 2)):
        data = stream.read(4000, exception_on_overflow=False)
        print(f"Frame {i+1}: {len(data)} bytes leídos")
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    print("✅ MICRÓFONO FUNCIONA CORRECTAMENTE")
    
except Exception as e:
    print(f"❌ ERROR al acceder al micrófono: {e}")
    print("\nPOSIBLES CAUSAS:")
    print("1. Permisos de micrófono no otorgados en Windows")
    print("2. No hay micrófono conectado")
    print("3. El micrófono está siendo usado por otra aplicación")
    print("4. Drivers de audio no instalados correctamente")

print("\n" + "=" * 60)
print("FIN DEL DIAGNÓSTICO")
print("=" * 60)
