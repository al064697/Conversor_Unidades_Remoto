# Importaciones necesarias
import sys  # Para acceder a argumentos del sistema y salir del programa
import Ice  # Framework de ZeroC Ice para comunicación remota

# Configuración del path para importar el código generado por slice2py
sys.path.insert(0, "generated")
import Conversor_ice as Slice  # type: ignore  # Módulo generado desde Conversor.ice

def main():
    """
    Función principal del cliente que se conecta al servidor de conversión.
    Realiza conversiones de unidades de forma remota.
    """
    # Variable para almacenar el comunicador Ice
    communicator = None
    
    try:
        # 1. Inicializar el comunicador Ice
        # Crea una conexión con el middleware Ice
        communicator = Ice.initialize(sys.argv)
        
        # 2. Crear el proxy al objeto remoto
        # El proxy es una representación local del objeto servidor
        # Formato: "identificador:protocolo -h host -p puerto"
        base = communicator.stringToProxy(
            "conversor:default -h localhost -p 10000"
        )
        
        # 3. Hacer el cast al tipo específico (Conversor)
        # Verifica que el objeto remoto sea del tipo esperado
        # checkedCast lanza una excepción si el tipo no coincide
        conversor = Slice.ConversorPrx.checkedCast(base)
        
        # 4. Verificar que el cast fue exitoso
        if not conversor:
            raise RuntimeError("Proxy inválido: no es un objeto Conversor")
        
        # Mensaje de bienvenida
        print("=" * 50)
        print("Cliente de conversión de unidades")
        print("Conectado al servidor en localhost:10000")
        print("=" * 50)
        
        # 5. Realizar conversiones remotas
        # Cada llamada se envía al servidor a través de la red
        
        # Conversión de temperatura
        celsius = 25.0
        fahrenheit = conversor.celciusAFahrenheit(celsius)
        print(f"\n{celsius}°C = {fahrenheit:.2f}°F")
        
        # Conversión de distancia
        km = 10.0
        millas = conversor.kilometrosAMillas(km)
        print(f"{km} km = {millas:.2f} millas")
        
        # Conversión de peso
        kg = 70.0
        libras = conversor.kgALibras(kg)
        print(f"{kg} kg = {libras:.2f} libras")
        
        print("\n" + "=" * 50)
        print("Conversiones completadas exitosamente")
        print("=" * 50)
        
    except Ice.ConnectionRefusedException:
        # Error cuando el servidor no está en ejecución
        print("Error: No se pudo conectar al servidor.")
        print("Asegúrate de que el servidor esté ejecutándose.")
        return 1
        
    except Exception as e:
        # Captura cualquier otro error
        print(f"Error durante la ejecución del cliente: {e}")
        return 1
        
    finally:
        # Bloque que siempre se ejecuta
        # Limpia los recursos de Ice para evitar fugas de memoria
        if communicator:
            communicator.destroy()
    
    return 0  # Código de salida 0 indica éxito

# Punto de entrada del programa
# Solo se ejecuta si el script se corre directamente
if __name__ == "__main__":
    # sys.exit() termina el programa con el código de retorno de main()
    sys.exit(main())

