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

## 4) Ejecutar la app completa (modo local)

La app usa 2 procesos:

1. Servidor ICE (puerto 10000)
2. Servidor web Flask (puerto 5000 por defecto)

### Ejecución única desde backend

#### Terminal 1: ICE

```bash
python backend/server.py
```

#### Terminal 2: Web Flask

```bash
python backend/web_server.py
```

Luego abre:

- http://localhost:5000

## 5) Configuración por variables de entorno (host/puerto/debug)

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

## 6) Uso funcional de la app (frontend)

- Selecciona categoría: temperatura, longitud, peso, velocidad
- Ingresa valor numérico
- Selecciona unidades origen/destino
- Usa botón swap para intercambiar unidades
- Convierte con botón o en tiempo real al cambiar valor/unidades
- Revisa historial reciente y recarga conversiones al hacer click
- Cambia tema en selector: `Auto`, `Dark`, `Light`

## 7) Endpoints API disponibles

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

## 8) Exponer por internet con ngrok (opcional)

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

Con el web server ya corriendo en `5000`:

```bash
ngrok http 5000
```

Comparte la URL `https://...ngrok-free.app`.

## 9) Cliente de prueba por terminal

Para validar llamadas ICE sin frontend:

```bash
python backend/client.py
```

## 10) Regenerar stubs ICE (si editas `Conversor.ice`)

> Solo necesario si cambias la interfaz.

```bash
slice2py backend/Conversor.ice
```

Esto actualiza el paquete `Conversor/` usado por servidor y cliente.

## 11) Troubleshooting (Windows + macOS)

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

## 12) Flujo recomendado de trabajo

1. Activar venv
2. Ejecutar `python backend/server.py`
3. Ejecutar `python backend/web_server.py`
4. Probar en navegador
5. (Opcional) abrir ngrok

---

Con esta estructura y guía, el proyecto queda preparado para uso portable en macOS y Windows.
