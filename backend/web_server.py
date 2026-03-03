"""
Servidor Flask que sirve el frontend estático y proporciona API endpoints
para comunicarse con el servidor ICE en el puerto 10000
"""

import sys
import os
from flask import Flask, render_template, jsonify, request
import Ice

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import Conversor  # Módulo generado por slice2py

FRONTEND_DIR = os.path.join(PROJECT_ROOT, 'frontend')

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')


# ============================================================================
# CLIENTE ICE
# ============================================================================
class ConversorClient:
    """Cliente ICE para comunicarse con el servidor remoto"""

    def __init__(self):
        self.proxy = None
        self.communicator = None

    def connect(self):
        """Conecta con el servidor ICE en puerto 10000"""
        try:
            self.communicator = Ice.initialize(sys.argv)
            base = self.communicator.stringToProxy(
                "ConversorUnidades:default -p 10000"
            )
            self.proxy = Conversor.ConversorUnidadesPrx.checkedCast(base)
            if not self.proxy:
                raise RuntimeError("Servidor ICE no encontrado")
            return True
        except Ice.ConnectionRefusedException:
            print(" No se puede conectar al servidor ICE en puerto 10000")
            return False
        except Exception as e:
            print(f" Error conectando: {e}")
            return False

    def disconnect(self):
        """Cierra la conexión con ICE"""
        if self.communicator:
            try:
                self.communicator.destroy()
            except:
                pass

    def convert_temperatura(self, valor, desde, hasta):
        return self.proxy.convertirTemperatura(valor, desde, hasta)

    def convert_longitud(self, valor, desde, hasta):
        return self.proxy.convertirLongitud(valor, desde, hasta)

    def convert_peso(self, valor, desde, hasta):
        return self.proxy.convertirPeso(valor, desde, hasta)

    def convert_velocidad(self, valor, desde, hasta):
        return self.proxy.convertirVelocidad(valor, desde, hasta)

    def get_unidades_disponibles(self, categoria):
        return self.proxy.unidadesDisponibles(categoria)


# Instancia global del cliente ICE
cliente = ConversorClient()


# ============================================================================
# RUTAS - FRONTEND
# ============================================================================

@app.route('/')
def index():
    """Sirve el archivo index.html"""
    return app.send_static_file('index.html')


@app.route('/<path:filename>')
def serve_static(filename):
    """Sirve archivos estáticos (CSS, JS, etc)"""
    return app.send_static_file(filename)


# ============================================================================
# RUTAS - API
# ============================================================================

@app.route('/api/convert', methods=['POST'])
def api_convert():
    """
    Endpoint para convertir unidades
    Recibe: {categoria, valor, desde, hasta}
    Retorna: {resultado, error}
    """
    try:
        data = request.get_json()
        categoria = data.get('categoria', '').lower()
        valor = float(data.get('valor', 0))
        desde = data.get('desde', '').lower()
        hasta = data.get('hasta', '').lower()

        # Validar que el proxy esté conectado
        if not cliente.proxy:
            return jsonify({'error': 'Servidor ICE desconectado'}), 503

        # Realizar la conversión según la categoría
        if categoria == 'temperatura':
            resultado = cliente.convert_temperatura(valor, desde, hasta)
        elif categoria == 'longitud':
            resultado = cliente.convert_longitud(valor, desde, hasta)
        elif categoria == 'peso':
            resultado = cliente.convert_peso(valor, desde, hasta)
        elif categoria == 'velocidad':
            resultado = cliente.convert_velocidad(valor, desde, hasta)
        else:
            return jsonify({'error': f'Categoría no reconocida: {categoria}'}), 400

        return jsonify({'resultado': resultado})

    except Conversor.UnidadInvalidaException as e:
        return jsonify({'error': f'Unidad inválida: {e.mensaje}'}), 400
    except ValueError as e:
        return jsonify({'error': f'Valor inválido: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Error en servidor: {str(e)}'}), 500


@app.route('/api/unidades/<categoria>', methods=['GET'])
def api_unidades(categoria):
    """
    Endpoint para obtener unidades disponibles
    Retorna: {unidades: "unidad1, unidad2, ..."}
    """
    try:
        if not cliente.proxy:
            return jsonify({'error': 'Servidor ICE desconectado'}), 503

        unidades = cliente.get_unidades_disponibles(categoria)
        return jsonify({'unidades': unidades})

    except Conversor.UnidadInvalidaException as e:
        return jsonify({'error': f'Categoría inválida: {e.mensaje}'}), 400
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500


@app.route('/api/status', methods=['GET'])
def api_status():
    """Retorna el estado de conexión con el servidor ICE"""
    connected = cliente.proxy is not None
    return jsonify({'connected': connected, 'servidor': 'localhost:10000'})


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Ruta no encontrada'}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Error interno del servidor'}), 500


# ============================================================================
# MAIN
# ============================================================================

def main():
    host = os.getenv('HOST', 'localhost')
    port = int(os.getenv('PORT', '5000'))
    debug = os.getenv('DEBUG', 'true').lower() == 'true'

    print(" Iniciando servidor Flask...")

    # Conectar con el servidor ICE
    if cliente.connect():
        print(" Conectado al servidor ICE en puerto 10000")
    else:
        print("  No se pudo conectar al servidor ICE")
        print("   Asegúrate de que el servidor está corriendo: python3 server.py")

    try:
        # Iniciar servidor Flask usando configuración por entorno
        print(f" Servidor Flask escuchando en http://{host}:{port}")
        print(" Para exponerlo con ngrok ejecuta: ngrok http " + str(port))
        app.run(debug=debug, host=host, port=port)
    except KeyboardInterrupt:
        print("\n Deteniendo servidor...")
    finally:
        cliente.disconnect()


if __name__ == '__main__':
    main()
