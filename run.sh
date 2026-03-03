#!/bin/bash

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Iniciando Conversor de Unidades...${NC}"
echo ""

# Validar que estamos en la carpeta raíz del proyecto
if [ ! -d "backend" ]; then
    echo -e "${YELLOW}⚠️  Por favor ejecuta este script desde la raíz del proyecto${NC}"
    exit 1
fi

# Función para limpiar procesos al salir
cleanup() {
    echo -e "${YELLOW}\n⏹️  Deteniendo servidores...${NC}"
    kill $ICE_PID $FLASK_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Terminal 1: ICE Server
echo -e "${GREEN}[1/3] Levantando ICE Server en puerto 10000${NC}"
cd backend
python3 server.py &
ICE_PID=$!
echo -e "${BLUE}ICE PID: $ICE_PID${NC}"

# Esperar a que ICE esté listo
sleep 3

# Terminal 2: Flask Server
echo -e "${GREEN}[2/3] Levantando Flask Server en puerto 5000${NC}"
python3 web_server.py &
FLASK_PID=$!
echo -e "${BLUE}Flask PID: $FLASK_PID${NC}"
cd ..

# Esperar a que Flask esté listo
sleep 2

# Terminal 3: ngrok (opcional)
echo ""
echo -e "${GREEN}[3/3] ¿Quieres levantar ngrok para acceso remoto? (s/n)${NC}"
read -r response
if [[ "$response" =~ ^[Ss]$ ]]; then
    echo -e "${BLUE}Levantando ngrok en puerto 5000...${NC}"
    ngrok http 5000
else
    echo -e "${BLUE}✅ Servidores activos:${NC}"
    echo -e "   - ICE Server: http://localhost:10000"
    echo -e "   - Web App: http://localhost:5000"
    echo -e "${YELLOW}Presiona Ctrl+C para detener${NC}"
    wait
fi
