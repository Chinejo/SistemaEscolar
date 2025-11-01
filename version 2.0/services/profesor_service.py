"""Servicios de negocio para profesores."""
from __future__ import annotations

from typing import Dict, List

from models.profesor import Profesor
from repositories.profesor_repository import ProfesorRepository
from services.validation_service import (
    ValidationError,
    ValidationService,
    is_foreign_key_constraint_error,
    is_unique_constraint_error,
)


class ProfesorService:
    """Gestiona profesores, turnos y banca de materias."""

    def __init__(
        self,
        repository: ProfesorRepository | None = None,
        validator: ValidationService | None = None,
    ) -> None:
        self._repository = repository or ProfesorRepository()
        self._validator = validator or ValidationService()

    def listar(self) -> List[Profesor]:
        """Retorna la coleccion de profesores."""
        return self._repository.obtener_todos()

    def crear(self, nombre: object) -> None:
        """Crea un profesor evitando duplicados."""
        nombre_normalizado = self._validator.require_text(nombre, "nombre del profesor", "Ingrese un nombre valido.")
        try:
            self._repository.crear(nombre_normalizado)
        except Exception as exc:  # pragma: no cover
            if is_unique_constraint_error(exc, "profesor.nombre"):
                raise ValidationError("Ya existe un profesor con ese nombre.") from exc
            raise

    def actualizar(self, profesor_id: object, nombre: object) -> None:
        """Actualiza el nombre de un profesor."""
        profesor_int = self._validator.require_id(profesor_id, "profesor")
        nombre_normalizado = self._validator.require_text(nombre, "nombre del profesor", "Ingrese un nombre valido.")
        try:
            self._repository.actualizar(profesor_int, nombre_normalizado)
        except Exception as exc:  # pragma: no cover
            if is_unique_constraint_error(exc, "profesor.nombre"):
                raise ValidationError("Ya existe un profesor con ese nombre.") from exc
            raise

    def eliminar(self, profesor_id: object) -> None:
        """Elimina un profesor si no tiene horario asociado."""
        profesor_int = self._validator.require_id(profesor_id, "profesor")
        try:
            self._repository.eliminar(profesor_int)
        except Exception as exc:  # pragma: no cover
            if is_foreign_key_constraint_error(exc):
                raise ValidationError("No se puede eliminar el profesor porque tiene horarios asignados.") from exc
            raise

    def asignar_turno(self, profesor_id: object, turno_id: object) -> None:
        """Asigna un turno a un profesor validando duplicados."""
        profesor_int = self._validator.require_id(profesor_id, "profesor")
        turno_int = self._validator.require_id(turno_id, "turno")
        try:
            self._repository.asignar_turno(profesor_int, turno_int)
        except Exception as exc:  # pragma: no cover
            raise ValidationError(str(exc)) from exc

    def quitar_turno(self, profesor_id: object, turno_id: object) -> None:
        """Quita un turno previamente asignado."""
        profesor_int = self._validator.require_id(profesor_id, "profesor")
        turno_int = self._validator.require_id(turno_id, "turno")
        self._repository.quitar_turno(profesor_int, turno_int)

    def obtener_turnos(self, profesor_id: object) -> List[Dict[str, object]]:
        """Obtiene los turnos asociados a un profesor."""
        profesor_int = self._validator.require_id(profesor_id, "profesor")
        return self._repository.obtener_turnos(profesor_int)

    def obtener_por_turno(self, turno_id: object) -> List[Dict[str, object]]:
        """Lista profesores disponibles para un turno."""
        turno_int = self._validator.require_id(turno_id, "turno")
        return self._repository.obtener_por_turno(turno_int)

    def asignar_banca(self, profesor_id: object, materia_id: object, banca_horas: object) -> None:
        """Relaciona un profesor con una materia y sus horas de banca."""
        profesor_int = self._validator.require_id(profesor_id, "profesor")
        materia_int = self._validator.require_id(materia_id, "materia")
        horas = self._validator.require_non_negative_int(
            banca_horas,
            "banca de horas",
            message="Ingrese un numero valido para la banca de horas.",
        )
        self._validator.validar_limite_horas(horas, minimo=0)
        try:
            self._repository.asignar_banca(profesor_int, materia_int, horas)
        except Exception as exc:  # pragma: no cover
            raise ValidationError(str(exc)) from exc

    def obtener_banca(self, profesor_id: object) -> List[Dict[str, object]]:
        """Devuelve las materias con banca asignada a un profesor."""
        profesor_int = self._validator.require_id(profesor_id, "profesor")
        return self._repository.obtener_banca(profesor_int)

    def actualizar_banca(self, relacion_id: object, banca_horas: object) -> None:
        """Modifica las horas asignadas a una relacion profesor-materia."""
        relacion_int = self._validator.require_id(relacion_id, "relacion")
        horas = self._validator.require_non_negative_int(
            banca_horas,
            "banca de horas",
            message="Ingrese un numero valido para la banca de horas.",
        )
        self._validator.validar_limite_horas(horas, minimo=0)
        self._repository.actualizar_banca(relacion_int, horas)

    def eliminar_banca(self, relacion_id: object) -> None:
        """Quita una materia de la banca del profesor."""
        relacion_int = self._validator.require_id(relacion_id, "relacion")
        self._repository.eliminar_banca(relacion_int)

    def calcular_horas_asignadas(self, profesor_id: object) -> int:
        """Calcula la suma de horas de banca para un profesor."""
        profesor_int = self._validator.require_id(profesor_id, "profesor")
        banca = self._repository.obtener_banca(profesor_int)
        total = 0
        for registro in banca:
            try:
                total += int(registro.get("banca_horas", 0))
            except (TypeError, ValueError):
                continue
        return total
