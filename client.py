import sys
import Ice       # Libreria principal de ZeroC ICE
import Conversor # Modulo generado automaticamente por slice2py

def main():
    # Inicializar el runtime de ICE (igual que en el servidor)
    with Ice.initialize(sys.argv) as communicator:

        # Crear un proxy: referencia al objeto remoto en el servidor
        # Formato: "NombreObjeto:protocolo -h host -p puerto"
        base = communicator.stringToProxy(
            "ConversorUnidades:default -h localhost -p 10000"
        )

        # Hacer un cast al tipo especifico del proxy
        # checkedCast verifica en el servidor que el objeto es del tipo correcto
        # Si el servidor no responde o el tipo no coincide, retorna None
        conversor = Conversor.ConversorUnidadesPrx.checkedCast(base)

        if not conversor:
            raise RuntimeError("No se pudo obtener el proxy del servidor.")

        try:
            # Cada llamada a continuacion es una llamada REMOTA via ICE
            # El cliente serializa los parametros, los envia por TCP al servidor,
            # el servidor ejecuta la logica y devuelve el resultado

            print("=== TEMPERATURA ===")
            r = conversor.convertirTemperatura(100, "celsius", "fahrenheit")
            print(f"100 celsius -> fahrenheit: {r:.4f}")

            r = conversor.convertirTemperatura(0, "celsius", "kelvin")
            print(f"0 celsius -> kelvin: {r:.4f}")

            r = conversor.convertirTemperatura(98.6, "fahrenheit", "celsius")
            print(f"98.6 fahrenheit -> celsius: {r:.4f}")

            print("\n=== LONGITUD ===")
            r = conversor.convertirLongitud(1, "mi", "km")
            print(f"1 mi -> km: {r:.4f}")

            r = conversor.convertirLongitud(100, "ft", "m")
            print(f"100 ft -> m: {r:.4f}")

            r = conversor.convertirLongitud(5, "km", "m")
            print(f"5 km -> m: {r:.4f}")

            print("\n=== PESO ===")
            r = conversor.convertirPeso(70, "kg", "lb")
            print(f"70 kg -> lb: {r:.4f}")

            r = conversor.convertirPeso(1, "lb", "g")
            print(f"1 lb -> g: {r:.4f}")

            print("\n=== VELOCIDAD ===")
            r = conversor.convertirVelocidad(120, "kmh", "mph")
            print(f"120 kmh -> mph: {r:.4f}")

            r = conversor.convertirVelocidad(60, "mph", "ms")
            print(f"60 mph -> ms: {r:.4f}")

            print("\n=== UNIDADES DISPONIBLES ===")
            for cat in ["temperatura", "longitud", "peso", "velocidad"]:
                print(f"{cat}: {conversor.unidadesDisponibles(cat)}")

        # Capturar excepciones ICE definidas en el Slice
        # Estas viajan serializadas desde el servidor hasta el cliente
        except Conversor.UnidadInvalidaException as e:
            print(f"Error de conversion: {e.mensaje}")

if __name__ == "__main__":
    main()