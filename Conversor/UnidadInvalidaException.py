# Copyright (c) ZeroC, Inc.

# slice2py version 3.8.1

from __future__ import annotations
import IcePy

from Ice.UserException import UserException

from dataclasses import dataclass


@dataclass
class UnidadInvalidaException(UserException):
    """
    Notes
    -----
        The Slice compiler generated this exception dataclass from Slice exception ``::Conversor::UnidadInvalidaException``.
    """
    mensaje: str = ""

    _ice_id = "::Conversor::UnidadInvalidaException"

_Conversor_UnidadInvalidaException_t = IcePy.defineException(
    "::Conversor::UnidadInvalidaException",
    UnidadInvalidaException,
    (),
    None,
    (("mensaje", (), IcePy._t_string, False, 0),))

setattr(UnidadInvalidaException, '_ice_type', _Conversor_UnidadInvalidaException_t)

__all__ = ["UnidadInvalidaException", "_Conversor_UnidadInvalidaException_t"]
