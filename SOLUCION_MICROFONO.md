# GUIA DE SOLUCION DE PROBLEMAS DEL MICROFONO

## Si el volumen sigue bajo despues de ajustarlo:

1. **Actualizar drivers de audio:**
   - Presiona Windows + X → Administrador de dispositivos
   - Expande "Entradas y salidas de audio"
   - Click derecho en "Microphone (Realtek Audio)" → Actualizar controlador
   - Selecciona "Buscar controladores automaticamente"

2. **Reinstalar drivers Realtek:**
   - Ve a la pagina del fabricante de tu portatil/placa base
   - Descarga los drivers de audio Realtek mas recientes
   - Instalelos

3. **Verificar en el BIOS/UEFI:**
   - Reinicia el PC
   - Entra al BIOS (F2, F10, DEL o Supr al iniciar)
   - Busca configuracion de audio
   - Asegurate de que el microfono integrado este HABILITADO

4. **Probar con microfono externo:**
   - Conecta un microfono USB o por jack 3.5mm externo
   - Si funciona, el microfono integrado puede estar dañado

5. **Verificar aplicaciones que bloquean el micro:**
   - Cierra: Discord, Zoom, Teams, Skype, OBS, etc.
   - Estas aplicaciones a veces "capturan" el microfono

## Si Windows NO detecta ningun microfono:

1. El microfono puede estar deshabilitado:
   - Panel de control → Sonido → Grabar
   - Click derecho en el area blanca → "Mostrar dispositivos deshabilitados"
   - Si aparece, click derecho → Habilitar

2. Driver corrupto:
   - Administrador de dispositivos → Entradas y salidas de audio
   - Click derecho en Realtek → Desinstalar dispositivo
   - Reiniciar (Windows reinstalara el driver automaticamente)

## Comandos para diagnostico avanzado:

Ejecutar en PowerShell como administrador:

# Listar dispositivos de audio
Get-AudioDevice -List

# Verificar servicios de audio
Get-Service -Name "Audiosrv" | Select-Object Status, StartType
