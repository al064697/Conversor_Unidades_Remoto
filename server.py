import sys
import Ice       # Libreria principal de ZeroC ICE
import Conversor # Modulo generado automaticamente por slice2py desde Conversor.ice

# Implementacion del servant (objeto remoto)
# Hereda de Conversor.ConversorUnidades que fue generado por slice2py
class ConversorUnidadesImpl(Conversor.ConversorUnidades):

    """
    ------------------------------------------------------------------
    TEMPERATURA
        Parametros:
            valor: numero a convertir
            desde: unidad origen  (celsius, fahrenheit, kelvin)
            hasta: unidad destino (celsius, fahrenheit, kelvin)
            current: objeto ICE con info de la llamada remota (obligatorio en servants)
    ------------------------------------------------------------------
    """

    def convertirTemperatura(self, valor, desde, hasta, current=None):
        unidades = {"celsius", "fahrenheit", "kelvin"}
        desde, hasta = desde.lower(), hasta.lower()
        self._validar(desde, hasta, unidades, "temperatura")

        # Estrategia: convertir primero a Celsius como unidad base,
        # luego de Celsius a la unidad destino
        if desde == "fahrenheit":
            en_celsius = (valor - 32) * 5 / 9
        elif desde == "kelvin":
            en_celsius = valor - 273.15
        else:
            en_celsius = valor  # ya esta en Celsius

        if hasta == "fahrenheit":
            return en_celsius * 9 / 5 + 32
        elif hasta == "kelvin":
            return en_celsius + 273.15
        return en_celsius  # destino es Celsius

    def convertirLongitud(self, valor, desde, hasta, current=None):
        """
        LONGITUD
        Unidades: m (metros), km (kilometros), mi (millas), ft (pies)
        Estrategia: convertir a metros como unidad base
        """
        unidades = {"m", "km", "mi", "ft"}
        desde, hasta = desde.lower(), hasta.lower()
        self._validar(desde, hasta, unidades, "longitud")

        # Factor de conversion a metros para cada unidad
        a_metros = {"m": 1.0, "km": 1000.0, "mi": 1609.344, "ft": 0.3048}

        # valor -> metros -> unidad destino
        return valor * a_metros[desde] / a_metros[hasta]

    def convertirPeso(self, valor, desde, hasta, current=None):
        """
        PESO / MASA
        Unidades: kg (kilogramos), lb (libras), g (gramos)
        Estrategia: convertir a kg como unidad base
        """
        unidades = {"kg", "lb", "g"}
        desde, hasta = desde.lower(), hasta.lower()
        self._validar(desde, hasta, unidades, "peso")

        # Factor de conversion a kilogramos para cada unidad
        a_kg = {"kg": 1.0, "lb": 0.453592, "g": 0.001}

        # valor -> kg -> unidad destino
        return valor * a_kg[desde] / a_kg[hasta]

    def convertirVelocidad(self, valor, desde, hasta, current=None):
        """
        VELOCIDAD
        Unidades: kmh (km/hora), mph (millas/hora), ms (metros/segundo)
        Estrategia: convertir a m/s como unidad base
        """
        unidades = {"kmh", "mph", "ms"}
        desde, hasta = desde.lower(), hasta.lower()
        self._validar(desde, hasta, unidades, "velocidad")

        # Factor de conversion a metros/segundo para cada unidad
        a_ms = {"ms": 1.0, "kmh": 1/3.6, "mph": 0.44704}

        # valor -> m/s -> unidad destino
        return valor * a_ms[desde] / a_ms[hasta]

    def unidadesDisponibles(self, categoria, current=None):
        """
        UNIDADES DISPONIBLES
        Retorna un string con las unidades validas para una categoria dada
        """
        catalogo = {
            "temperatura": "celsius, fahrenheit, kelvin",
            "longitud":    "m, km, mi, ft",
            "peso":        "kg, lb, g",
            "velocidad":   "kmh, mph, ms",
        }
        cat = categoria.lower()
        if cat not in catalogo:
            # Lanzar excepcion ICE definida en el archivo Conversor.ice
            ex = Conversor.UnidadInvalidaException()
            ex.mensaje = f"Categoria '{categoria}' no existe. Disponibles: {', '.join(catalogo)}"
            raise ex
        return catalogo[cat]

    def _validar(self, desde, hasta, validas, categoria):
        """
        HELPER PRIVADO: valida que las unidades origen y destino sean validas
        Si alguna no lo es, lanza UnidadInvalidaException (definida en Slice)
        """
        errores = []
        if desde not in validas:
            errores.append(f"Unidad origen '{desde}' no valida para {categoria}.")
        if hasta not in validas:
            errores.append(f"Unidad destino '{hasta}' no valida para {categoria}.")
        if errores:
            # Construir y lanzar la excepcion ICE con mensaje descriptivo
            ex = Conversor.UnidadInvalidaException()
            ex.mensaje = " ".join(errores) + f" Validas: {', '.join(sorted(validas))}"
            raise ex


def main():
    """
    MAIN: inicializa y arranca el servidor ICE
    """
    # Ice.initialize arranca el runtime de ICE y procesa argumentos de linea
    # de comandos (como --Ice.Trace.Network=2 para debug)
    with Ice.initialize(sys.argv) as communicator:

        # Crear el Object Adapter: componente que recibe llamadas remotas
        # y las despacha al servant correcto
        # "default -p 10000" indica protocolo TCP en puerto 10000
        adapter = communicator.createObjectAdapterWithEndpoints(
            "ConversorAdapter", "default -p 10000"
        )

        # Instanciar el servant (la implementacion real de la interfaz)
        servant = ConversorUnidadesImpl()

        # Registrar el servant en el adapter con un nombre/identidad
        # Los clientes usaran este nombre para localizar el objeto remoto
        adapter.add(servant, Ice.stringToIdentity("ConversorUnidades"))

        # Activar el adapter: empieza a aceptar conexiones entrantes
        adapter.activate()

        print("Servidor escuchando en puerto 10000... (Ctrl+C para detener)")

        # Bloquear el hilo principal hasta recibir una señal de shutdown
        communicator.waitForShutdown()


if __name__ == "__main__":
    main()