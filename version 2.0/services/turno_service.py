"""Servicios de negocio para turnos."""
from __future__ import annotations

from typing import List, Optional

from models.turno import Turno
from repositories.turno_repository import TurnoRepository
from services.validation_service import (
    ValidationError,
    ValidationService,
    is_foreign_key_constraint_error,
    is_unique_constraint_error,
)


class TurnoService:
    """Gestiona la lógica de negocio asociada a turnos."""

    def __init__(
        self,
        repository: TurnoRepository | None = None,
        validator: ValidationService | None = None,
    ) -> None:
        self._repository = repository or TurnoRepository()
        self._validator = validator or ValidationService()

    def listar(self) -> List[Turno]:
        """Devuelve todos los turnos registrados."""
        return self._repository.obtener_todos()

    def crear(self, nombre: object) -> None:
        """Crea un turno validando duplicados."""
        nombre_normalizado = self._validator.require_text(
            nombre,
            "nombre del turno",
            "Ingrese un nombre válido para el turno.",
        )
        try:
            self._repository.crear(nombre_normalizado)
        except Exception as exc:  # pragma: no cover - reproduce mensaje del repositorio
            if is_unique_constraint_error(exc, "turno.nombre"):
                raise ValidationError("Ya existe un turno con ese nombre.") from exc
            raise

    def actualizar(self, turno_id: object, nombre: object) -> None:
        """Actualiza el nombre de un turno existente."""
        turno_int = self._validator.require_id(turno_id, "turno")
        nombre_normalizado = self._validator.require_text(
            nombre,
            "nombre del turno",
            "Ingrese un nombre válido para el turno.",
        )
        try:
            self._repository.actualizar(turno_int, nombre_normalizado)
        except Exception as exc:  # pragma: no cover
            if is_unique_constraint_error(exc, "turno.nombre"):
                raise ValidationError("Ya existe un turno con ese nombre.") from exc
            raise

    def eliminar(self, turno_id: object) -> None:
        """Elimina un turno asegurando que no tenga dependencias."""
        turno_int = self._validator.require_id(turno_id, "turno")
        try:
            self._repository.eliminar(turno_int)
        except Exception as exc:  # pragma: no cover
            if is_foreign_key_constraint_error(exc):
                raise ValidationError("No se puede eliminar el turno porque está en uso.") from exc
            raise

    def agregar_plan(self, turno_id: object, plan_id: object) -> None:
        """Asocia un plan de estudio a un turno."""
        turno_int = self._validator.require_id(turno_id, "turno")
        plan_int = self._validator.require_id(plan_id, "plan de estudio")
        try:
            self._repository.agregar_plan(turno_int, plan_int)
        except Exception as exc:  # pragma: no cover
            raise ValidationError("El plan ya está asignado a este turno.") from exc

    def quitar_plan(self, turno_id: object, plan_id: object) -> None:
        """Quita un plan de estudio previamente asociado a un turno."""
        turno_int = self._validator.require_id(turno_id, "turno")
        plan_int = self._validator.require_id(plan_id, "plan de estudio")
        self._repository.quitar_plan(turno_int, plan_int)

    def obtener_planes(self, turno_id: object) -> List[dict]:
        """Devuelve los planes asociados a un turno."""
        turno_int = self._validator.require_id(turno_id, "turno")
        return self._repository.obtener_planes(turno_int)

    def obtener_espacio_hora(self, turno_id: object, espacio: object) -> Optional[dict]:
        """Obtiene la configuración de horas para un espacio determinado."""
        turno_int = self._validator.require_id(turno_id, "turno")
        espacio_int = self._validator.normalize_espacio(espacio, max_espacios=None)
        return self._repository.obtener_espacio_hora(turno_int, espacio_int)

    def set_espacio_hora(
        self,
        turno_id: object,
        espacio: object,
        hora_inicio: object | None,
        hora_fin: object | None,
    ) -> None:
        """Configura el horario de un espacio; lo elimina si ambas horas están vacías."""
        turno_int = self._validator.require_id(turno_id, "turno")
        espacio_int = self._validator.normalize_espacio(espacio, max_espacios=None)
        hora_inicio_norm = self._validator.optional_time(hora_inicio, "hora de inicio")
        hora_fin_norm = self._validator.optional_time(hora_fin, "hora de fin")
        self._validator.ensure_time_order(hora_inicio_norm, hora_fin_norm)

        if hora_inicio_norm is None and hora_fin_norm is None:
            self._repository.eliminar_espacio_hora(turno_int, espacio_int)
        else:
            self._repository.set_espacio_hora(turno_int, espacio_int, hora_inicio_norm, hora_fin_norm)

    def eliminar_espacio_hora(self, turno_id: object, espacio: object) -> None:
        """Elimina la configuración de horas de un espacio específico."""
        turno_int = self._validator.require_id(turno_id, "turno")
        espacio_int = self._validator.normalize_espacio(espacio, max_espacios=None)
        self._repository.eliminar_espacio_hora(turno_int, espacio_int)
