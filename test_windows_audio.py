"""
Test para verificar la configuracion del microfono en Windows
"""
import pyaudio
import wave
import os
import time

print("=" * 70)
print("DIAGNOSTICO COMPLETO DEL MICROFONO EN WINDOWS")
print("=" * 70)

# 1. Listar todos los dispositivos
print("\n1. DISPOSITIVOS DE AUDIO DETECTADOS:")
print("-" * 70)

p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

print(f"Total de dispositivos: {numdevices}\n")

dispositivos_entrada = []
for i in range(0, numdevices):
    device_info = p.get_device_info_by_host_api_device_index(0, i)
    max_input = device_info.get('maxInputChannels')
    
    if max_input > 0:
        dispositivos_entrada.append(i)
        nombre = device_info.get('name')
        sample_rate = device_info.get('defaultSampleRate')
        print(f"[{i}] {nombre}")
        print(f"    Canales entrada: {max_input}")
        print(f"    Tasa de muestreo: {sample_rate} Hz")
        print()

if not dispositivos_entrada:
    print("*** PROBLEMA: No se detectaron dispositivos de entrada ***")
    print("\nSOLUCIONES:")
    print("1. Conecta un microfono externo (USB o por jack)")
    print("2. Activa el microfono integrado en el BIOS/UEFI")
    print("3. Actualiza los drivers de audio desde el Administrador de dispositivos")
    p.terminate()
    exit(1)

# 2. Verificar dispositivo por defecto
print("\n2. DISPOSITIVO DE ENTRADA POR DEFECTO:")
print("-" * 70)
try:
    default_input = p.get_default_input_device_info()
    print(f"Nombre: {default_input.get('name')}")
    print(f"Index: {default_input.get('index')}")
    print(f"Canales: {default_input.get('maxInputChannels')}")
    print(f"Sample Rate: {default_input.get('defaultSampleRate')} Hz")
    dispositivo_usar = default_input.get('index')
except Exception as e:
    print(f"ERROR: No hay dispositivo por defecto configurado")
    print(f"Detalles: {e}")
    print("\nUsando el primer dispositivo disponible...")
    dispositivo_usar = dispositivos_entrada[0]

# 3. Intentar grabar 3 segundos de audio
print(f"\n3. PRUEBA DE GRABACION (3 segundos):")
print("-" * 70)
print("SE VA A GRABAR 3 SEGUNDOS DE AUDIO.")
print("!!! HABLA AHORA PARA PROBAR EL MICROFONO !!!")
print("Di por ejemplo: 'Hola, esta es una prueba del microfono'")
print()

archivo_prueba = "prueba_microfono.wav"

try:
    # Configurar stream
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    DURACION = 3
    
    print(f"Usando dispositivo [{dispositivo_usar}]")
    print("Iniciando grabacion...")
    
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        input_device_index=dispositivo_usar,
        frames_per_buffer=CHUNK
    )
    
    frames = []
    
    for i in range(0, int(RATE / CHUNK * DURACION)):
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)
        
        # Mostrar progreso
        segundo_actual = (i + 1) * CHUNK / RATE
        print(f"Grabando... {segundo_actual:.1f}s / {DURACION}s", end='\r')
    
    print("\nGrabacion finalizada!                    ")
    
    stream.stop_stream()
    stream.close()
    
    # Guardar archivo WAV
    wf = wave.open(archivo_prueba, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    print(f"\n*** EXITO: Audio guardado en '{archivo_prueba}' ***")
    print(f"Tamano del archivo: {os.path.getsize(archivo_prueba)} bytes")
    
    # Verificar que no sea silencio total
    import struct
    total_samples = len(b''.join(frames)) // 2  # 2 bytes por sample (paInt16)
    samples = struct.unpack(f'{total_samples}h', b''.join(frames))
    max_amplitud = max(abs(s) for s in samples)
    
    print(f"Amplitud maxima detectada: {max_amplitud}")
    
    if max_amplitud < 100:
        print("\n!!! ADVERTENCIA: Amplitud muy baja !!!")
        print("El microfono graba pero casi no detecta sonido.")
        print("\nPOSIBLES CAUSAS:")
        print("1. El microfono esta en MUTE en Windows")
        print("2. El volumen del microfono esta muy bajo")
        print("3. El microfono esta defectuoso")
        print("\nCOMO SOLUCIONARLO:")
        print("- Click derecho en el icono de volumen > Sonidos")
        print("- Ve a la pestana 'Grabar'")
        print("- Selecciona tu microfono > Propiedades > Niveles")
        print("- Sube el volumen del microfono a 80-100")
    elif max_amplitud > 100:
        print(f"\n*** MICROFONO FUNCIONA CORRECTAMENTE ***")
        print(f"Se detecto audio con buena amplitud.")
        print(f"\nPuedes reproducir el archivo '{archivo_prueba}' para verificar.")
    
except Exception as e:
    print(f"\n*** ERROR AL GRABAR: {e} ***")
    print("\nPOSIBLES CAUSAS:")
    print("1. PERMISOS: Windows bloquea el acceso al microfono")
    print("2. OCUPADO: Otra aplicacion esta usando el microfono")
    print("3. DRIVER: Los drivers de audio estan corruptos")
    print("\nSOLUCIONES:")
    print("\nA) Verificar permisos en Windows 10/11:")
    print("   1. Abre Configuracion de Windows")
    print("   2. Ve a: Privacidad y seguridad > Microfono")
    print("   3. Activa 'Acceso al microfono'")
    print("   4. Activa 'Permitir que las apps accedan al microfono'")
    print("   5. Activa 'Permitir que las apps de escritorio accedan al microfono'")
    print("\nB) Cerrar otras aplicaciones que usen el micro:")
    print("   - Discord, Skype, Teams, Zoom, etc.")
    print("\nC) Actualizar/Reinstalar drivers de audio:")
    print("   - Administrador de dispositivos > Entradas y salidas de audio")
    print("   - Click derecho en el microfono > Actualizar controlador")

p.terminate()

print("\n" + "=" * 70)
print("FIN DEL DIAGNOSTICO")
print("=" * 70)
