"""Wrappers comunes sobre las validaciones de negocio."""
from __future__ import annotations

from services.validation_service import ValidationError, ValidationService

__all__ = [
    "ValidationError",
    "require_text",
    "require_positive_int",
    "require_non_negative_int",
    "require_id",
    "optional_id",
    "optional_time",
]

_validator = ValidationService()


def require_text(value: object | None, field_name: str, message: str | None = None) -> str:
    """Normaliza y valida que un texto no esté vacío."""
    return _validator.require_text(value, field_name, message)


def require_positive_int(
    value: object,
    field_name: str,
    *,
    allow_zero: bool = False,
    message: str | None = None,
) -> int:
    """Valida un entero positivo y permite reutilizar la lógica en formularios."""
    return _validator.require_positive_int(value, field_name, allow_zero=allow_zero, message=message)


def require_non_negative_int(value: object, field_name: str, *, message: str | None = None) -> int:
    """Valida un entero mayor o igual que cero."""
    return _validator.require_non_negative_int(value, field_name, message=message)


def require_id(value: object, field_name: str) -> int:
    """Valida un identificador interno (entero positivo)."""
    return _validator.require_id(value, field_name)


def optional_id(value: object | None, field_name: str) -> int | None:
    """Convierte un identificador opcional a entero o ``None``."""
    return _validator.optional_id(value, field_name)


def optional_time(value: object | None, field_name: str) -> str | None:
    """Valida el formato de hora ``HH:MM`` permitiendo cadenas vacías."""
    return _validator.optional_time(value, field_name)
