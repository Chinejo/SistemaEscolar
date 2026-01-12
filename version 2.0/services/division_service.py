"""Servicios de negocio para divisiones o cursos."""
from __future__ import annotations

from typing import List

from models.division import Division
from repositories.division_repository import DivisionRepository
from services.validation_service import (
    ValidationError,
    ValidationService,
    is_foreign_key_constraint_error,
    is_unique_constraint_error,
)


class DivisionService:
    """Gestiona divisiones vinculadas a turno, plan y año."""

    def __init__(
        self,
        repository: DivisionRepository | None = None,
        validator: ValidationService | None = None,
    ) -> None:
        self._repository = repository or DivisionRepository()
        self._validator = validator or ValidationService()

    def listar(self) -> List[Division]:
        """Devuelve todas las divisiones registradas."""
        return self._repository.obtener_todas()

    def crear(self, nombre: object, turno_id: object, plan_id: object, anio_id: object) -> None:
        """Registra una división validando sus claves foráneas y duplicados."""
        nombre_normalizado = self._validator.require_text(
            nombre,
            "nombre de la división",
            "Ingrese un nombre válido para la división.",
        )
        turno_int = self._validator.require_id(turno_id, "turno")
        plan_int = self._validator.require_id(plan_id, "plan")
        anio_int = self._validator.require_id(anio_id, "año")
        try:
            self._repository.crear(nombre_normalizado, turno_int, plan_int, anio_int)
        except Exception as exc:  # pragma: no cover
            if is_unique_constraint_error(exc, "division.nombre") or is_unique_constraint_error(exc, "division.turno_id"):
                raise ValidationError(
                    "Ya existe una división con el mismo nombre para el turno, plan y año seleccionados.",
                ) from exc
            if is_foreign_key_constraint_error(exc):
                raise ValidationError("Los valores seleccionados para turno, plan o año no son válidos.") from exc
            raise

    def actualizar_nombre(self, division_id: object, nombre: object) -> None:
        """Actualiza el nombre de una división existente."""
        division_int = self._validator.require_id(division_id, "división")
        nombre_normalizado = self._validator.require_text(
            nombre,
            "nombre de la división",
            "Ingrese un nombre válido para la división.",
        )
        try:
            self._repository.actualizar(division_int, nombre_normalizado)
        except Exception as exc:  # pragma: no cover
            if is_unique_constraint_error(exc, "division.nombre"):
                raise ValidationError("Ya existe una división con ese nombre.") from exc
            raise

    def eliminar(self, division_id: object) -> None:
        """Elimina una división siempre que no tenga horarios asociados."""
        division_int = self._validator.require_id(division_id, "división")
        try:
            self._repository.eliminar(division_int)
        except Exception as exc:  # pragma: no cover
            if is_foreign_key_constraint_error(exc):
                raise ValidationError("No se puede eliminar la división porque está en uso.") from exc
            raise
