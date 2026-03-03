# Copyright (c) ZeroC, Inc.

# slice2py version 3.8.1

from __future__ import annotations
import IcePy

from Conversor.ConversorUnidades_forward import _Conversor_ConversorUnidadesPrx_t

from Conversor.UnidadInvalidaException import _Conversor_UnidadInvalidaException_t

from Ice.Object import Object

from Ice.ObjectPrx import ObjectPrx
from Ice.ObjectPrx import checkedCast
from Ice.ObjectPrx import checkedCastAsync
from Ice.ObjectPrx import uncheckedCast

from Ice.OperationMode import OperationMode

from abc import ABC
from abc import abstractmethod

from typing import TYPE_CHECKING
from typing import overload

if TYPE_CHECKING:
    from Ice.Current import Current
    from collections.abc import Awaitable
    from collections.abc import Sequence


class ConversorUnidadesPrx(ObjectPrx):
    """
    Notes
    -----
        The Slice compiler generated this proxy class from Slice interface ``::Conversor::ConversorUnidades``.
    """

    def convertirTemperatura(self, valor: float, desde: str, hasta: str, context: dict[str, str] | None = None) -> float:
        return ConversorUnidades._op_convertirTemperatura.invoke(self, ((valor, desde, hasta), context))

    def convertirTemperaturaAsync(self, valor: float, desde: str, hasta: str, context: dict[str, str] | None = None) -> Awaitable[float]:
        return ConversorUnidades._op_convertirTemperatura.invokeAsync(self, ((valor, desde, hasta), context))

    def convertirLongitud(self, valor: float, desde: str, hasta: str, context: dict[str, str] | None = None) -> float:
        return ConversorUnidades._op_convertirLongitud.invoke(self, ((valor, desde, hasta), context))

    def convertirLongitudAsync(self, valor: float, desde: str, hasta: str, context: dict[str, str] | None = None) -> Awaitable[float]:
        return ConversorUnidades._op_convertirLongitud.invokeAsync(self, ((valor, desde, hasta), context))

    def convertirPeso(self, valor: float, desde: str, hasta: str, context: dict[str, str] | None = None) -> float:
        return ConversorUnidades._op_convertirPeso.invoke(self, ((valor, desde, hasta), context))

    def convertirPesoAsync(self, valor: float, desde: str, hasta: str, context: dict[str, str] | None = None) -> Awaitable[float]:
        return ConversorUnidades._op_convertirPeso.invokeAsync(self, ((valor, desde, hasta), context))

    def convertirVelocidad(self, valor: float, desde: str, hasta: str, context: dict[str, str] | None = None) -> float:
        return ConversorUnidades._op_convertirVelocidad.invoke(self, ((valor, desde, hasta), context))

    def convertirVelocidadAsync(self, valor: float, desde: str, hasta: str, context: dict[str, str] | None = None) -> Awaitable[float]:
        return ConversorUnidades._op_convertirVelocidad.invokeAsync(self, ((valor, desde, hasta), context))

    def unidadesDisponibles(self, categoria: str, context: dict[str, str] | None = None) -> str:
        return ConversorUnidades._op_unidadesDisponibles.invoke(self, ((categoria, ), context))

    def unidadesDisponiblesAsync(self, categoria: str, context: dict[str, str] | None = None) -> Awaitable[str]:
        return ConversorUnidades._op_unidadesDisponibles.invokeAsync(self, ((categoria, ), context))

    @staticmethod
    def checkedCast(
        proxy: ObjectPrx | None,
        facet: str | None = None,
        context: dict[str, str] | None = None
    ) -> ConversorUnidadesPrx | None:
        return checkedCast(ConversorUnidadesPrx, proxy, facet, context)

    @staticmethod
    def checkedCastAsync(
        proxy: ObjectPrx | None,
        facet: str | None = None,
        context: dict[str, str] | None = None
    ) -> Awaitable[ConversorUnidadesPrx | None ]:
        return checkedCastAsync(ConversorUnidadesPrx, proxy, facet, context)

    @overload
    @staticmethod
    def uncheckedCast(proxy: ObjectPrx, facet: str | None = None) -> ConversorUnidadesPrx:
        ...

    @overload
    @staticmethod
    def uncheckedCast(proxy: None, facet: str | None = None) -> None:
        ...

    @staticmethod
    def uncheckedCast(proxy: ObjectPrx | None, facet: str | None = None) -> ConversorUnidadesPrx | None:
        return uncheckedCast(ConversorUnidadesPrx, proxy, facet)

    @staticmethod
    def ice_staticId() -> str:
        return "::Conversor::ConversorUnidades"

IcePy.defineProxy("::Conversor::ConversorUnidades", ConversorUnidadesPrx)

class ConversorUnidades(Object, ABC):
    """
    Notes
    -----
        The Slice compiler generated this skeleton class from Slice interface ``::Conversor::ConversorUnidades``.
    """

    _ice_ids: Sequence[str] = ("::Conversor::ConversorUnidades", "::Ice::Object", )
    _op_convertirTemperatura: IcePy.Operation
    _op_convertirLongitud: IcePy.Operation
    _op_convertirPeso: IcePy.Operation
    _op_convertirVelocidad: IcePy.Operation
    _op_unidadesDisponibles: IcePy.Operation

    @staticmethod
    def ice_staticId() -> str:
        return "::Conversor::ConversorUnidades"

    @abstractmethod
    def convertirTemperatura(self, valor: float, desde: str, hasta: str, current: Current) -> float | Awaitable[float]:
        pass

    @abstractmethod
    def convertirLongitud(self, valor: float, desde: str, hasta: str, current: Current) -> float | Awaitable[float]:
        pass

    @abstractmethod
    def convertirPeso(self, valor: float, desde: str, hasta: str, current: Current) -> float | Awaitable[float]:
        pass

    @abstractmethod
    def convertirVelocidad(self, valor: float, desde: str, hasta: str, current: Current) -> float | Awaitable[float]:
        pass

    @abstractmethod
    def unidadesDisponibles(self, categoria: str, current: Current) -> str | Awaitable[str]:
        pass

ConversorUnidades._op_convertirTemperatura = IcePy.Operation(
    "convertirTemperatura",
    "convertirTemperatura",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_double, False, 0), ((), IcePy._t_string, False, 0), ((), IcePy._t_string, False, 0)),
    (),
    ((), IcePy._t_double, False, 0),
    (_Conversor_UnidadInvalidaException_t,))

ConversorUnidades._op_convertirLongitud = IcePy.Operation(
    "convertirLongitud",
    "convertirLongitud",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_double, False, 0), ((), IcePy._t_string, False, 0), ((), IcePy._t_string, False, 0)),
    (),
    ((), IcePy._t_double, False, 0),
    (_Conversor_UnidadInvalidaException_t,))

ConversorUnidades._op_convertirPeso = IcePy.Operation(
    "convertirPeso",
    "convertirPeso",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_double, False, 0), ((), IcePy._t_string, False, 0), ((), IcePy._t_string, False, 0)),
    (),
    ((), IcePy._t_double, False, 0),
    (_Conversor_UnidadInvalidaException_t,))

ConversorUnidades._op_convertirVelocidad = IcePy.Operation(
    "convertirVelocidad",
    "convertirVelocidad",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_double, False, 0), ((), IcePy._t_string, False, 0), ((), IcePy._t_string, False, 0)),
    (),
    ((), IcePy._t_double, False, 0),
    (_Conversor_UnidadInvalidaException_t,))

ConversorUnidades._op_unidadesDisponibles = IcePy.Operation(
    "unidadesDisponibles",
    "unidadesDisponibles",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_string, False, 0),),
    (),
    ((), IcePy._t_string, False, 0),
    (_Conversor_UnidadInvalidaException_t,))

__all__ = ["ConversorUnidades", "ConversorUnidadesPrx", "_Conversor_ConversorUnidadesPrx_t"]
