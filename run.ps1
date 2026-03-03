$GREEN = "Green"
$BLUE = "Cyan"
$YELLOW = "Yellow"

Write-Host "🚀 Iniciando Conversor de Unidades..." -ForegroundColor $BLUE
Write-Host ""

# Validar que estamos en la carpeta raíz
if (-not (Test-Path "backend")) {
    Write-Host "⚠️  Por favor ejecuta este script desde la raíz del proyecto" -ForegroundColor $YELLOW
    exit 1
}

# Terminal 1: ICE Server
Write-Host "[1/3] Levantando ICE Server en puerto 10000" -ForegroundColor $GREEN
$iceProcess = Start-Process python3 -ArgumentList "backend/server.py" -PassThru
Write-Host "ICE PID: $($iceProcess.Id)" -ForegroundColor $BLUE
Start-Sleep -Seconds 3

# Terminal 2: Flask Server
Write-Host "[2/3] Levantando Flask Server en puerto 5000" -ForegroundColor $GREEN
$flaskProcess = Start-Process python3 -ArgumentList "backend/web_server.py" -PassThru
Write-Host "Flask PID: $($flaskProcess.Id)" -ForegroundColor $BLUE
Start-Sleep -Seconds 2

# Terminal 3: ngrok (opcional)
Write-Host ""
Write-Host "[3/3] ¿Quieres levantar ngrok para acceso remoto? (s/n)" -ForegroundColor $GREEN
$response = Read-Host

if ($response -eq "s" -or $response -eq "S") {
    Write-Host "Levantando ngrok en puerto 5000..." -ForegroundColor $BLUE
    & ngrok http 5000
} else {
    Write-Host "✅ Servidores activos:" -ForegroundColor $BLUE
    Write-Host "   - ICE Server: http://localhost:10000" -ForegroundColor $BLUE
    Write-Host "   - Web App: http://localhost:5000" -ForegroundColor $BLUE
    Write-Host "Presiona Ctrl+C para detener" -ForegroundColor $YELLOW
    
    # Esperar a que se cierren los procesos
    $iceProcess.WaitForExit()
    $flaskProcess.WaitForExit()
}
