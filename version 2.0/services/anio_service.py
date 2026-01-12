"""Servicios de negocio para años dentro de un plan de estudios."""
from __future__ import annotations

from typing import List

from models.anio import Anio
from repositories.anio_repository import AnioRepository
from services.validation_service import (
    ValidationError,
    ValidationService,
    is_foreign_key_constraint_error,
    is_unique_constraint_error,
)


class AnioService:
    """Gestiona años académicos y sus asociaciones con materias."""

    def __init__(
        self,
        repository: AnioRepository | None = None,
        validator: ValidationService | None = None,
    ) -> None:
        self._repository = repository or AnioRepository()
        self._validator = validator or ValidationService()

    def listar_por_plan(self, plan_id: object) -> List[Anio]:
        """Obtiene los años pertenecientes a un plan de estudio."""
        plan_int = self._validator.require_id(plan_id, "plan")
        return self._repository.obtener_por_plan(plan_int)

    def crear(self, nombre: object, plan_id: object) -> None:
        """Registra un año dentro de un plan, validando duplicados."""
        nombre_normalizado = self._validator.require_text(
            nombre,
            "nombre del año",
            "Ingrese un nombre válido para el año.",
        )
        plan_int = self._validator.require_id(plan_id, "plan")
        try:
            self._repository.crear(nombre_normalizado, plan_int)
        except Exception as exc:  # pragma: no cover
            if is_unique_constraint_error(exc, "anio.nombre"):
                raise ValidationError("Ya existe un año con ese nombre en el plan seleccionado.") from exc
            raise

    def actualizar(self, anio_id: object, nombre: object) -> None:
        """Actualiza el nombre de un año existente."""
        anio_int = self._validator.require_id(anio_id, "año")
        nombre_normalizado = self._validator.require_text(
            nombre,
            "nombre del año",
            "Ingrese un nombre válido para el año.",
        )
        try:
            self._repository.actualizar(anio_int, nombre_normalizado)
        except Exception as exc:  # pragma: no cover
            if is_unique_constraint_error(exc, "anio.nombre"):
                raise ValidationError("Ya existe un año con ese nombre en el plan seleccionado.") from exc
            raise

    def eliminar(self, anio_id: object) -> None:
        """Elimina un año siempre que no tenga dependencias."""
        anio_int = self._validator.require_id(anio_id, "año")
        try:
            self._repository.eliminar(anio_int)
        except Exception as exc:  # pragma: no cover
            if is_foreign_key_constraint_error(exc):
                raise ValidationError("No se puede eliminar el año porque está asociado a otras entidades.") from exc
            raise

    def agregar_materia(self, anio_id: object, materia_id: object) -> None:
        """Asocia una materia a un año."""
        anio_int = self._validator.require_id(anio_id, "año")
        materia_int = self._validator.require_id(materia_id, "materia")
        try:
            self._repository.agregar_materia(anio_int, materia_int)
        except Exception as exc:  # pragma: no cover
            if is_unique_constraint_error(exc, "anio_materia.anio_id"):
                raise ValidationError("La materia ya está asignada al año seleccionado.") from exc
            raise

    def quitar_materia(self, anio_id: object, materia_id: object) -> None:
        """Desasocia una materia de un año."""
        anio_int = self._validator.require_id(anio_id, "año")
        materia_int = self._validator.require_id(materia_id, "materia")
        self._repository.quitar_materia(anio_int, materia_int)

    def obtener_materias(self, anio_id: object) -> List[dict]:
        """Devuelve las materias asignadas a un año."""
        anio_int = self._validator.require_id(anio_id, "año")
        return self._repository.obtener_materias(anio_int)
