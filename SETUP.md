# 🔄 Conversor de Unidades Remoto - Guía de Ejecución

## Arquitectura

```
┌──────────────┐          ┌─────────────────┐          ┌──────────────┐
│   Frontend   │ ◄────────┤   Flask Server  │ ◄────────┤  ICE Server  │
│ (HTML/CSS/JS)│ HTTP:5000 │   (web_server)  │ ICE:10000│ (server.py)  │
└──────────────┘          └─────────────────┘          └──────────────┘
```

## Instalación

Ya hemos instalado Flask. Si necesitas instalar dependencias adicionales:

```bash
pip install flask
```

### Instalar ngrok (macOS)

```bash
brew install ngrok
```

Luego inicia sesión y configura tu token (una sola vez):

```bash
ngrok config add-authtoken <TU_TOKEN>
```

## Ejecución (3 terminales)

### Terminal 1: Servidor ICE (puerto 10000)
```bash
python3 server.py
```
Deberías ver:
```
Servidor escuchando en puerto 10000... (Ctrl+C para detener)
```

### Terminal 2: Servidor Flask (puerto 5000)
```bash
python3 web_server.py
```
Deberías ver:
```
✅ Conectado al servidor ICE en puerto 10000
🌐 Servidor Flask escuchando en http://localhost:5000
```

### Terminal 3: Acceso a la web
Abre tu navegador en:
```
http://localhost:5000
```

## Ejecución con URL pública (ngrok)

Mantén corriendo `server.py` y `web_server.py`, y abre una tercera terminal para ngrok:

### Terminal 3: Túnel ngrok hacia Flask (puerto 5000)
```bash
ngrok http 5000
```

ngrok mostrará una URL pública como:
```
https://xxxx-xx-xx-xx-xx.ngrok-free.app
```

Comparte esa URL para acceder al frontend desde internet.

## Endpoints API disponibles

### POST /api/convert
Convierte unidades:
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

### GET /api/unidades/<categoria>
Obtiene unidades disponibles:
```
GET /api/unidades/temperatura
```

Respuesta:
```json
{
  "unidades": "celsius, fahrenheit, kelvin"
}
```

### GET /api/status
Verifica estado de conexión:
```json
{
  "connected": true,
  "servidor": "localhost:10000"
}
```

## Troubleshooting

### "Error: Servidor ICE desconectado"
- Asegúrate de que `python3 server.py` está ejecutándose en terminal 1
- Verifica que el puerto 10000 no está en uso: `netstat -an | grep 10000`

### Puerto 5000 en uso
```bash
lsof -i :5000
kill -9 <PID>
```

### Variantes de ejecución

**Con debug desactivado:**
```bash
python3 web_server.py
# Y cambiar en web_server.py: app.run(debug=False, ...)
```

**Acceso remoto (no solo localhost):**
```bash
python3 web_server.py
# Y cambiar: app.run(host='0.0.0.0', port=5000)
```

## Archivos importantes

- `server.py` - Servidor ICE (conversiones remotas)
- `web_server.py` - Servidor Flask + API endpoints (NUEVO)
- `frontend/index.html` - Interfaz web
- `frontend/app.js` - Lógica frontend (modificado para usar API)
- `frontend/style.css` - Estilos (modificado con animación de carga)
- `Conversor.ice` - Definición de interfaces ICE
- `Conversor/` - Módulos Python generados por slice2py

## Flujo de una conversión

1. Usuario ingresa valor en frontend
2. `app.js` envía HTTP POST a `/api/convert`
3. `web_server.py` recibe y llama a `servidor.py` vía ICE
4. `server.py` realiza la conversión matemática
5. Respuesta regresa: ICE → Flask → Frontend
6. resultado se muestra en pantalla

---

¡Listo para usar! 🚀
