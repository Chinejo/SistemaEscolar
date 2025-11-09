"""Servicios de negocio para la asignacion de horarios."""
from __future__ import annotations

from typing import List

from repositories.horario_repository import HorarioRepository
from services.validation_service import (
    ValidationError,
    ValidationService,
    is_unique_constraint_error,
)


class HorarioService:
    """Orquesta validaciones y persistencia para horarios."""

    def __init__(
        self,
        repository: HorarioRepository | None = None,
        validator: ValidationService | None = None,
    ) -> None:
        self._repository = repository or HorarioRepository()
        self._validator = validator or ValidationService()

    def crear_para_division(
        self,
        division_id: object,
        dia: object,
        espacio: object,
        hora_inicio: object | None = None,
        hora_fin: object | None = None,
        materia_id: object | None = None,
        profesor_id: object | None = None,
        turno_id: object | None = None,
        *,
        max_espacios: int | None = 8,
    ) -> None:
        """Crea un horario asociado a una division, validando conflictos previos."""
        division_int = self._validator.require_id(division_id, "division")
        dia_normalizado = self._validator.normalize_day(dia)
        espacio_int = self._validator.normalize_espacio(espacio, max_espacios=max_espacios)
        hora_inicio_norm = self._validator.optional_time(hora_inicio, "hora de inicio")
        hora_fin_norm = self._validator.optional_time(hora_fin, "hora de fin")
        self._validator.ensure_time_order(hora_inicio_norm, hora_fin_norm)
        materia_int = self._validator.optional_id(materia_id, "materia")
        profesor_int = self._validator.optional_id(profesor_id, "profesor")
        turno_int = self._validator.optional_id(turno_id, "turno")

        existentes = self._repository.obtener_por_division(division_int)
        self._validator.validar_espacio_ocupado(existentes, dia_normalizado, espacio_int)

        if profesor_int is not None and turno_int is not None:
            horarios_profesor = self._repository.obtener_por_profesor(profesor_int, turno_int)
            self._validator.validar_disponibilidad_profesor(horarios_profesor, dia_normalizado, espacio_int)

        try:
            self._repository.crear(
                division_int,
                dia_normalizado,
                espacio_int,
                hora_inicio_norm,
                hora_fin_norm,
                materia_int,
                profesor_int,
                turno_int,
            )
        except Exception as exc:  # pragma: no cover
            if is_unique_constraint_error(exc, "horario.division_id"):
                raise ValidationError(
                    "Ya existe un horario asignado para la division en ese dia y espacio.",
                ) from exc
            raise ValidationError(str(exc)) from exc

    def crear_para_profesor(
        self,
        profesor_id: object,
        turno_id: object,
        dia: object,
        espacio: object,
        hora_inicio: object | None = None,
        hora_fin: object | None = None,
        division_id: object | None = None,
        materia_id: object | None = None,
        *,
        max_espacios: int | None = 8,
    ) -> None:
        """Crea un horario desde la perspectiva de un profesor."""
        profesor_int = self._validator.require_id(profesor_id, "profesor")
        turno_int = self._validator.require_id(turno_id, "turno")
        dia_normalizado = self._validator.normalize_day(dia)
        espacio_int = self._validator.normalize_espacio(espacio, max_espacios=max_espacios)
        hora_inicio_norm = self._validator.optional_time(hora_inicio, "hora de inicio")
        hora_fin_norm = self._validator.optional_time(hora_fin, "hora de fin")
        self._validator.ensure_time_order(hora_inicio_norm, hora_fin_norm)
        division_int = self._validator.optional_id(division_id, "division")
        materia_int = self._validator.optional_id(materia_id, "materia")

        horarios_profesor = self._repository.obtener_por_profesor(profesor_int, turno_int)
        self._validator.validar_disponibilidad_profesor(horarios_profesor, dia_normalizado, espacio_int)

        if division_int is not None:
            existentes_division = self._repository.obtener_por_division(division_int)
            self._validator.validar_espacio_ocupado(existentes_division, dia_normalizado, espacio_int)

        try:
            self._repository.crear_para_profesor(
                profesor_int,
                turno_int,
                dia_normalizado,
                espacio_int,
                hora_inicio_norm,
                hora_fin_norm,
                division_int,
                materia_int,
            )
        except Exception as exc:  # pragma: no cover
            raise ValidationError(str(exc)) from exc

    def obtener_por_division(self, division_id: object) -> List[dict]:
        """Obtiene los horarios cargados para una division."""
        division_int = self._validator.require_id(division_id, "division")
        return self._repository.obtener_por_division(division_int)

    def obtener_por_profesor(self, profesor_id: object, turno_id: object) -> List[dict]:
        """Recupera los horarios asignados a un profesor en un turno."""
        profesor_int = self._validator.require_id(profesor_id, "profesor")
        turno_int = self._validator.require_id(turno_id, "turno")
        return self._repository.obtener_por_profesor(profesor_int, turno_int)

    def eliminar(self, horario_id: object) -> None:
        """Elimina un horario por su identificador."""
        horario_int = self._validator.require_id(horario_id, "horario")
        self._repository.eliminar(horario_int)
