"""Utilidades de validacion y normalizacion para la capa de servicios."""
from __future__ import annotations

import re
from typing import Iterable, Mapping, Optional

from config import DIAS_SEMANA

__all__ = [
    "ValidationError",
    "ValidationService",
    "is_unique_constraint_error",
    "is_foreign_key_constraint_error",
]


class ValidationError(ValueError):
    """Representa errores de validacion dentro de la logica de negocio."""


class ValidationService:
    """Centraliza validaciones comunes reutilizadas por los servicios."""

    _TIME_PATTERN = re.compile(r"^(?:[01]\d|2[0-3]):[0-5]\d$")

    @staticmethod
    def sanitize_text(value: object | None) -> str:
        """Devuelve una cadena sin espacios iniciales ni finales."""
        if isinstance(value, str):
            return value.strip()
        return ""

    def require_text(self, value: object | None, field_name: str, message: str | None = None) -> str:
        """Exige una cadena no vacia y la devuelve normalizada."""
        text = self.sanitize_text(value)
        if not text:
            raise ValidationError(message or f'El campo "{field_name}" es obligatorio.')
        return text

    def require_int(self, value: object, field_name: str, *, message: str | None = None) -> int:
        """Convierte la entrada en entero valido."""
        if isinstance(value, bool):
            raise ValidationError(message or f'Ingrese un valor numerico para "{field_name}".')
        if isinstance(value, int):
            return value
        text = self.sanitize_text(value)
        if not text or not re.fullmatch(r"-?\d+", text):
            raise ValidationError(message or f'Ingrese un valor numerico para "{field_name}".')
        return int(text)

    def require_positive_int(
        self,
        value: object,
        field_name: str,
        *,
        allow_zero: bool = False,
        message: str | None = None,
    ) -> int:
        """Obtiene un entero y valida que sea positivo (o cero si se permite)."""
        number = self.require_int(value, field_name)
        if allow_zero:
            if number < 0:
                raise ValidationError(message or f'El valor de "{field_name}" no puede ser negativo.')
        else:
            if number <= 0:
                raise ValidationError(message or f'El valor de "{field_name}" debe ser mayor que cero.')
        return number

    def require_non_negative_int(
        self,
        value: object,
        field_name: str,
        *,
        message: str | None = None,
    ) -> int:
        """Valida y devuelve un entero mayor o igual a cero."""
        return self.require_positive_int(value, field_name, allow_zero=True, message=message)

    def optional_int(
        self,
        value: object | None,
        field_name: str,
        *,
        allow_zero: bool = False,
    ) -> Optional[int]:
        """Devuelve un entero opcional, aceptando cadenas vacias como None."""
        if value is None:
            return None
        if isinstance(value, int) and not isinstance(value, bool):
            return self.require_positive_int(value, field_name, allow_zero=allow_zero)
        text = self.sanitize_text(value)
        if not text:
            return None
        return self.require_positive_int(value, field_name, allow_zero=allow_zero)

    def require_id(self, value: object, field_name: str) -> int:
        """Valida un identificador positivo."""
        return self.require_positive_int(value, field_name, allow_zero=False)

    def optional_id(self, value: object | None, field_name: str) -> Optional[int]:
        """Convierte un identificador opcional a entero o None."""
        return self.optional_int(value, field_name, allow_zero=False)

    def normalize_day(self, value: object, *, message: str | None = None) -> str:
        """Normaliza y valida un dia de la semana segun configuracion."""
        day = self.require_text(value, "dia", message=message or "Seleccione un dia.")
        for option in DIAS_SEMANA:
            if option.lower() == day.lower():
                return option
        raise ValidationError(message or f'Dia invalido: {day}.')

    def normalize_espacio(
        self,
        value: object,
        *,
        max_espacios: int | None = 8,
        message: str | None = None,
    ) -> int:
        """Valida un numero de espacio dentro del rango permitido."""
        espacio = self.require_positive_int(value, "espacio", allow_zero=False)
        if max_espacios is not None and espacio > max_espacios:
            raise ValidationError(message or f'El espacio debe estar entre 1 y {max_espacios}.')
        return espacio

    def optional_time(self, value: object | None, field_name: str) -> Optional[str]:
        """Normaliza un valor de hora en formato HH:MM, aceptando None."""
        text = self.sanitize_text(value)
        if not text:
            return None
        if not self._TIME_PATTERN.match(text):
            raise ValidationError(f'Ingrese una hora valida para "{field_name}" (HH:MM).')
        return text

    def ensure_time_order(
        self,
        hora_inicio: Optional[str],
        hora_fin: Optional[str],
        *,
        message: str | None = None,
    ) -> None:
        """Verifica que la hora de inicio sea menor a la hora de fin."""
        if hora_inicio and hora_fin and hora_inicio >= hora_fin:
            raise ValidationError(message or "La hora de inicio debe ser menor que la hora de fin.")

    def validar_conflicto_horario(
        self,
        registros: Iterable[Mapping[str, object]],
        dia: str,
        espacio: int,
        *,
        message: str,
    ) -> None:
        """Detecta conflictos de horario para un dia y espacio dados."""
        dia_objetivo = dia.lower()
        for registro in registros:
            registro_dia = str(registro.get("dia", "")).lower()
            try:
                registro_espacio = int(registro.get("espacio", -1))
            except (TypeError, ValueError):
                continue
            if registro_dia == dia_objetivo and registro_espacio == espacio:
                raise ValidationError(message)

    def validar_espacio_ocupado(
        self,
        registros_division: Iterable[Mapping[str, object]],
        dia: str,
        espacio: int,
    ) -> None:
        """Valida que una division no tenga un horario duplicado."""
        self.validar_conflicto_horario(
            registros_division,
            dia,
            espacio,
            message="Ya existe un horario asignado para la division en ese dia y espacio.",
        )

    def validar_disponibilidad_profesor(
        self,
        horarios_profesor: Iterable[Mapping[str, object]],
        dia: str,
        espacio: int,
    ) -> None:
        """Confirma que el profesor no tenga otro compromiso en el mismo turno."""
        self.validar_conflicto_horario(
            horarios_profesor,
            dia,
            espacio,
            message="El profesor ya tiene un horario asignado en este dia y espacio en este turno.",
        )

    def validar_limite_horas(
        self,
        horas: int,
        *,
        minimo: int = 0,
        maximo: Optional[int] = None,
        message: str | None = None,
    ) -> int:
        """Garantiza que las horas se encuentren dentro del rango permitido."""
        if horas < minimo:
            raise ValidationError(message or f'Las horas deben ser al menos {minimo}.')
        if maximo is not None and horas > maximo:
            raise ValidationError(message or f'Las horas deben ser como maximo {maximo}.')
        return horas


def is_unique_constraint_error(error: Exception, constraint_target: str | None = None) -> bool:
    """Detecta errores de restriccion UNIQUE opcionalmente filtrando por columna."""
    message = str(error)
    if "UNIQUE constraint failed" not in message:
        return False
    if constraint_target is None:
        return True
    return constraint_target in message


def is_foreign_key_constraint_error(error: Exception, constraint_target: str | None = None) -> bool:
    """Detecta errores de claves foraneas opcionalmente filtrando por tabla."""
    message = str(error)
    if "FOREIGN KEY constraint failed" not in message:
        return False
    if constraint_target is None:
        return True
    return constraint_target in message
