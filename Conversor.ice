module Conversor
{
    exception UnidadInvalidaException
    {
        string mensaje;
    };

    interface ConversorUnidades
    {
        double convertirTemperatura(double valor, string desde, string hasta)
            throws UnidadInvalidaException;

        double convertirLongitud(double valor, string desde, string hasta)
            throws UnidadInvalidaException;

        double convertirPeso(double valor, string desde, string hasta)
            throws UnidadInvalidaException;

        double convertirVelocidad(double valor, string desde, string hasta)
            throws UnidadInvalidaException;

        string unidadesDisponibles(string categoria)
            throws UnidadInvalidaException;
    };
};