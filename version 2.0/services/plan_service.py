"""Servicios de negocio para planes de estudio."""
from __future__ import annotations

from typing import List

from models.plan import Plan
from repositories.plan_repository import PlanRepository
from services.validation_service import (
    ValidationError,
    ValidationService,
    is_foreign_key_constraint_error,
    is_unique_constraint_error,
)


class PlanService:
    """Gestiona la lógica de negocio asociada a los planes de estudio."""

    def __init__(
        self,
        repository: PlanRepository | None = None,
        validator: ValidationService | None = None,
    ) -> None:
        self._repository = repository or PlanRepository()
        self._validator = validator or ValidationService()

    def listar(self) -> List[Plan]:
        """Devuelve los planes registrados."""
        return self._repository.obtener_todos()

    def crear(self, nombre: object) -> None:
        """Registra un plan de estudio evitando duplicados."""
        nombre_normalizado = self._validator.require_text(
            nombre,
            "nombre del plan",
            "Ingrese un nombre válido para el plan de estudio.",
        )
        try:
            self._repository.crear(nombre_normalizado)
        except Exception as exc:  # pragma: no cover - propaga mensajes del repositorio
            if is_unique_constraint_error(exc, "plan_estudio.nombre"):
                raise ValidationError("Ya existe un plan de estudio con ese nombre.") from exc
            raise

    def actualizar(self, plan_id: object, nombre: object) -> None:
        """Actualiza el nombre de un plan existente."""
        plan_int = self._validator.require_id(plan_id, "plan")
        nombre_normalizado = self._validator.require_text(
            nombre,
            "nombre del plan",
            "Ingrese un nombre válido para el plan de estudio.",
        )
        try:
            self._repository.actualizar(plan_int, nombre_normalizado)
        except Exception as exc:  # pragma: no cover
            if is_unique_constraint_error(exc, "plan_estudio.nombre"):
                raise ValidationError("Ya existe un plan de estudio con ese nombre.") from exc
            raise

    def eliminar(self, plan_id: object) -> None:
        """Elimina un plan siempre que no tenga dependencias."""
        plan_int = self._validator.require_id(plan_id, "plan")
        try:
            self._repository.eliminar(plan_int)
        except Exception as exc:  # pragma: no cover
            if is_foreign_key_constraint_error(exc):
                raise ValidationError("No se puede eliminar el plan porque está en uso en otras entidades.") from exc
            raise

    def agregar_materia(self, plan_id: object, materia_id: object) -> None:
        """Asocia una materia a un plan de estudio."""
        plan_int = self._validator.require_id(plan_id, "plan")
        materia_int = self._validator.require_id(materia_id, "materia")
        try:
            self._repository.agregar_materia(plan_int, materia_int)
        except Exception as exc:  # pragma: no cover
            if is_unique_constraint_error(exc, "plan_materia.plan_id"):
                raise ValidationError("La materia ya está asignada al plan seleccionado.") from exc
            raise

    def quitar_materia(self, plan_id: object, materia_id: object) -> None:
        """Elimina la asociación entre un plan y una materia."""
        plan_int = self._validator.require_id(plan_id, "plan")
        materia_int = self._validator.require_id(materia_id, "materia")
        self._repository.quitar_materia(plan_int, materia_int)

    def obtener_materias(self, plan_id: object) -> List[dict]:
        """Devuelve las materias asociadas a un plan de estudio."""
        plan_int = self._validator.require_id(plan_id, "plan")
        return self._repository.obtener_materias(plan_int)
