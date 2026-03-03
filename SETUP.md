# Guía completa de ejecución y uso (Windows + macOS)

Esta guía cubre instalación, ejecución, uso diario, pruebas básicas y publicación con ngrok para que el proyecto sea portable entre Windows y macOS.

## 1) Estructura del proyecto

```text
Conversor_Unidades_Remoto-1/
├── backend/
│   ├── __init__.py
│   ├── Conversor.ice
│   ├── server.py
│   ├── web_server.py
│   └── client.py
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── style.css
├── Conversor/                  # stubs ICE generados por slice2py
├── requirements.txt
└── SETUP.md
```

## 2) Requisitos

- Python 3.10 o 3.11 recomendado
- pip actualizado
- Acceso a terminal
- Dependencias Python del archivo `requirements.txt`

## 3) Crear entorno virtual e instalar dependencias

### macOS (Terminal / zsh)

```bash
cd /ruta/al/proyecto/Conversor_Unidades_Remoto-1
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Windows (PowerShell)

```powershell
cd C:\ruta\al\proyecto\Conversor_Unidades_Remoto-1
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Si PowerShell bloquea scripts:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### Windows (CMD)

```bat
cd C:\ruta\al\proyecto\Conversor_Unidades_Remoto-1
py -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4) Ejecución automática (recomendado)

Ejecuta todo automáticamente con un solo comando:

### macOS/Linux

**Primer setup (una sola vez):**

```bash
cd /ruta/al/proyecto/Conversor_Unidades_Remoto-1
source .venv/bin/activate
chmod +x run.sh
```

**Ejecutar:**

```bash
./run.sh
```

**Qué esperar:**
```
🚀 Iniciando Conversor de Unidades...

[1/3] Levantando ICE Server en puerto 10000
ICE PID: 12345
[2/3] Levantando Flask Server en puerto 5000
Flask PID: 12346
[3/3] ¿Quieres levantar ngrok para acceso remoto? (s/n)
```

Si respondés `n`, verás:
```
✅ Servidores activos:
   - ICE Server: http://localhost:10000
   - Web App: http://localhost:5000
Presiona Ctrl+C para detener
```

**Luego abre en navegador:**
- http://localhost:5000

### Windows (PowerShell)

**Primer setup (una sola vez):**

```powershell
cd C:\ruta\al\proyecto\Conversor_Unidades_Remoto-1
.\.venv\Scripts\Activate.ps1
```

**Ejecutar:**

```powershell
powershell -ExecutionPolicy Bypass -File run.ps1
```

**Qué esperar:** (igual que macOS)

**Luego abre en navegador:**
- http://localhost:5000

### Activar ngrok (opcional)

Si en la pregunta respondés `s`:

```
✅ Levantando ngrok en puerto 5000...
```

Verás una salida como:
```
Forwarding https://abc-123-def.ngrok-free.app -> http://localhost:5000
```

Comparte esa URL con quien quieras para que acceda remotamente.

## 5) Ejecutar la app completa (modo manual)

La app usa 2 procesos:

1. Servidor ICE (puerto 10000)
2. Servidor web Flask (puerto 5000 por defecto)

### Ejecución desde carpeta `backend`

#### Terminal 1: ICE

```bash
cd backend
python3 server.py
```

#### Terminal 2: Web Flask

```bash
cd backend
python3 web_server.py
```

Luego abre:

- http://localhost:5000

## 6) Configuración por variables de entorno (host/puerto/debug)

El servidor web soporta:

- `HOST` (default `localhost`)
- `PORT` (default `5000`)
- `DEBUG` (default `true`)

### macOS

```bash
HOST=0.0.0.0 PORT=8080 DEBUG=true python backend/web_server.py
```

### Windows PowerShell

```powershell
$env:HOST="0.0.0.0"
$env:PORT="8080"
$env:DEBUG="true"
python backend/web_server.py
```

### Windows CMD

```bat
set HOST=0.0.0.0
set PORT=8080
set DEBUG=true
python backend\web_server.py
```

## 7) Uso funcional de la app (frontend)

- Selecciona categoría: temperatura, longitud, peso, velocidad
- Ingresa valor numérico
- Selecciona unidades origen/destino
- Usa botón swap para intercambiar unidades
- Convierte con botón o en tiempo real al cambiar valor/unidades
- Revisa historial reciente y recarga conversiones al hacer click
- Cambia tema en selector: `Auto`, `Dark`, `Light`

## 8) Endpoints API disponibles

### `POST /api/convert`

Body:

```json
{
  "categoria": "temperatura",
  "valor": 32,
  "desde": "fahrenheit",
  "hasta": "celsius"
}
```

Respuesta:

```json
{
  "resultado": 0.0
}
```

### `GET /api/unidades/<categoria>`

Ejemplo: `GET /api/unidades/temperatura`

```json
{
  "unidades": "celsius, fahrenheit, kelvin"
}
```

### `GET /api/status`

```json
{
  "connected": true,
  "servidor": "localhost:10000"
}
```

## 9) Exponer por internet con ngrok (opcional)

### Instalar ngrok

#### macOS

```bash
brew install ngrok
```

#### Windows (winget)

```powershell
winget install ngrok.ngrok
```

#### Windows (choco, opcional)

```powershell
choco install ngrok
```

### Configurar token (una sola vez)

```bash
ngrok config add-authtoken TU_TOKEN
```

### Levantar túnel

Con el web server ya corriendo en `5000` (desde carpeta `backend`):

**Terminal 3 (desde carpeta principal del proyecto):**

```bash
ngrok http 5000
```

Comparte la URL `https://...ngrok-free.app`.

## 10) Cliente de prueba por terminal

Para validar llamadas ICE sin frontend:

```bash
python backend/client.py
```

## 11) Regenerar stubs ICE (si editas `Conversor.ice`)

> Solo necesario si cambias la interfaz.

```bash
slice2py backend/Conversor.ice
```

Esto actualiza el paquete `Conversor/` usado por servidor y cliente.

## 12) Troubleshooting (Windows + macOS)

### Error: no conecta al servidor ICE

- Verifica que `backend/server.py` esté corriendo
- Verifica puerto 10000

macOS:

```bash
lsof -i :10000
```

Windows (PowerShell):

```powershell
netstat -ano | findstr :10000
```

### Puerto 5000 ocupado

macOS:

```bash
lsof -i :5000
```

Windows:

```powershell
netstat -ano | findstr :5000
```

### Dependencia `zeroc-ice` falla al instalar

- Actualiza pip: `python -m pip install --upgrade pip`
- Usa Python 3.10/3.11
- Reinstala en entorno virtual limpio

### Cambios de frontend no se ven

- Hard reload del navegador (`Ctrl+F5` en Windows, `Cmd+Shift+R` en macOS)

## 13) Flujo recomendado de trabajo

1. Activar venv: `source .venv/bin/activate` (macOS) o `.\.venv\Scripts\Activate.ps1` (Windows)
2. **Terminal 1 (ICE Server):** `cd backend && python3 server.py`
3. **Terminal 2 (Web Server):** `cd backend && python3 web_server.py`
4. Probar en navegador: http://localhost:5000
5. **(Opcional) Terminal 3 (ngrok):** `ngrok http 5000`

---

Con esta estructura y guía, el proyecto queda preparado para uso portable en macOS y Windows.
