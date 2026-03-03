# Importaciones necesarias
import sys  # Para acceder a argumentos del sistema y salir del programa
import Ice  # Framework de ZeroC Ice para comunicación remota

# Configuración del path para importar el código generado por slice2py
# Insert en posición 0 para que tenga prioridad en la búsqueda de módulos
sys.path.insert(0, "generated")
import Conversor_ice as Slice  # type: ignore  # Módulo generado desde Conversor.ice

class ConversorI(Slice.Conversor):
    """
    Implementación del servidor de conversión de unidades.
    Hereda de la interfaz Conversor definida en el archivo .ice
    """
    
    def celciusAFahrenheit(self, celsius, current=None):
        """
        Convierte grados Celsius a Fahrenheit
        Args:
            celsius: Temperatura en grados Celsius
            current: Contexto de Ice (requerido por el framework)
        Returns:
            Temperatura en grados Fahrenheit
        """
        return (celsius * 9.0 / 5.0) + 32.0
    
    def kilometrosAMillas(self, km, current=None):
        """
        Convierte kilómetros a millas
        Args:
            km: Distancia en kilómetros
            current: Contexto de Ice (requerido por el framework)
        Returns:
            Distancia en millas
        """
        return km * 0.621371
    
    def kgALibras(self, kg, current=None):
        """
        Convierte kilogramos a libras
        Args:
            kg: Peso en kilogramos
            current: Contexto de Ice (requerido por el framework)
        Returns:
            Peso en libras
        """
        return kg * 2.20462

def main():
    """
    Función principal que inicia el servidor Ice.
    Configura y mantiene el servidor en ejecución hasta que se interrumpa.
    """
    # Variable para almacenar el comunicador Ice
    # Se inicializa en None para poder verificar en el finally
    communicator = None
    
    try:
        # 1. Inicializar el comunicador Ice
        # El comunicador es el punto de entrada principal de Ice
        # sys.argv permite pasar configuraciones desde la línea de comandos
        communicator = Ice.initialize(sys.argv)
        
        # 2. Crear un adaptador de objetos
        # El adaptador es responsable de recibir peticiones de los clientes
        # "ConversorAdapter" es el nombre del adaptador
        # "default -p 10000" configura el endpoint TCP en el puerto 10000
        adapter = communicator.createObjectAdapterWithEndpoints(
            "ConversorAdapter",  # Nombre del adaptador
            "default -p 10000"   # Protocolo y puerto
        )
        
        # 3. Crear el objeto sirviente
        # Este objeto implementa la lógica de negocio (las conversiones)
        servant = ConversorI()
        
        # 4. Agregar el sirviente al adaptador
        # stringToIdentity("conversor") crea un identificador único
        # Los clientes usarán este identificador para conectarse
        adapter.add(servant, communicator.stringToIdentity("conversor"))
        
        # 5. Activar el adaptador
        # Cuando se activa, el adaptador empieza a escuchar peticiones
        # Sin esto, el servidor no recibirá ninguna llamada
        adapter.activate()
        
        # Mensajes informativos para el usuario
        print("=" * 50)
        print("Servidor de conversión de unidades iniciado")
        print("Puerto: 10000")
        print("Identificador: conversor")
        print("=" * 50)
        print("Presiona Ctrl+C para detener el servidor")
        
        # 6. Mantener el servidor en ejecución
        # waitForShutdown() bloquea el programa hasta que se reciba una señal de apagado
        # El servidor procesa peticiones en este estado
        communicator.waitForShutdown()
        
    except KeyboardInterrupt:
        # Captura Ctrl+C para cerrar el servidor de forma ordenada
        print("\nServidor detenido por el usuario")
        
    except Exception as e:
        # Captura cualquier otro error durante la inicialización o ejecución
        print(f"Error al iniciar el servidor: {e}")
        return 1  # Código de salida 1 indica error
        
    finally:
        # Bloque que siempre se ejecuta, haya o no error
        # Limpia los recursos de Ice para evitar fugas de memoria
        if communicator:
            communicator.destroy()
    
    return 0  # Código de salida 0 indica éxito

# Punto de entrada del programa
# Solo se ejecuta si el script se corre directamente (no si se importa)
if __name__ == "__main__":
    # sys.exit() termina el programa con el código de retorno de main()
    sys.exit(main())