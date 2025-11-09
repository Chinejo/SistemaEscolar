"""Servicios de negocio para materias."""
from __future__ import annotations

from typing import List

from models.materia import Materia
from repositories.materia_repository import MateriaRepository
from services.validation_service import (
    ValidationError,
    ValidationService,
    is_foreign_key_constraint_error,
    is_unique_constraint_error,
)


class MateriaService:
    """Encapsula la logica de negocio asociada a materias."""

    def __init__(
        self,
        repository: MateriaRepository | None = None,
        validator: ValidationService | None = None,
    ) -> None:
        self._repository = repository or MateriaRepository()
        self._validator = validator or ValidationService()

    def listar(self) -> List[Materia]:
        """Devuelve todas las materias registradas."""
        return self._repository.obtener_todas()

    def crear(self, nombre: object, horas_semanales: object) -> None:
        """Crea una materia validando nombre y horas permitidas."""
        nombre_normalizado = self._validator.require_text(nombre, "nombre de la materia", "Ingrese un nombre valido.")
        horas = self._validator.require_non_negative_int(
            horas_semanales,
            "horas semanales",
            message="Ingrese un numero valido para las horas semanales.",
        )
        self._validator.validar_limite_horas(horas, minimo=0)
        try:
            self._repository.crear(nombre_normalizado, horas)
        except Exception as exc:  # pragma: no cover - pasa mensajes del repositorio
            if is_unique_constraint_error(exc, "materia.nombre"):
                raise ValidationError("Ya existe una materia con ese nombre.") from exc
            raise

    def actualizar(self, materia_id: object, nombre: object, horas_semanales: object) -> None:
        """Actualiza datos de una materia existente."""
        materia_int = self._validator.require_id(materia_id, "materia")
        nombre_normalizado = self._validator.require_text(nombre, "nombre de la materia", "Ingrese un nombre valido.")
        horas = self._validator.require_non_negative_int(
            horas_semanales,
            "horas semanales",
            message="Ingrese un numero valido para las horas semanales.",
        )
        self._validator.validar_limite_horas(horas, minimo=0)
        try:
            self._repository.actualizar(materia_int, nombre_normalizado, horas)
        except Exception as exc:  # pragma: no cover
            if is_unique_constraint_error(exc, "materia.nombre"):
                raise ValidationError("Ya existe una materia con ese nombre.") from exc
            raise

    def eliminar(self, materia_id: object) -> None:
        """Elimina una materia si no esta referenciada."""
        materia_int = self._validator.require_id(materia_id, "materia")
        try:
            self._repository.eliminar(materia_int)
        except Exception as exc:  # pragma: no cover
            if is_foreign_key_constraint_error(exc):
                raise ValidationError(
                    "No se puede eliminar la materia porque esta en uso en horarios u otros registros.",
                ) from exc
            raise
