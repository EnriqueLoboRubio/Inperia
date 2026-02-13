"""
Script simple de prueba de micrófono
"""
import pyaudio

print("=" * 60)
print("PRUEBA DE MICROFONO")
print("=" * 60)

try:
    p = pyaudio.PyAudio()
    
    print("\nAbriendo stream de audio...")
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=4000
    )
    
    print("OK - Stream abierto correctamente!")
    print("Grabando 2 segundos de audio...")
    
    # Leer algunos frames para verificar
    for i in range(0, int(16000 / 4000 * 2)):
        data = stream.read(4000, exception_on_overflow=False)
        print(f"Frame {i+1}: {len(data)} bytes leidos")
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    print("\n*** MICROFONO FUNCIONA CORRECTAMENTE ***")
    
except Exception as e:
    print(f"\nERROR al acceder al microfono: {e}")
    print("\nPOSIBLES CAUSAS:")
    print("1. Permisos de microfono no otorgados en Windows")
    print("2. No hay microfono conectado")
    print("3. El microfono esta siendo usado por otra aplicacion")

print("=" * 60)
