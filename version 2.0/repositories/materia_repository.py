"""Repositorio de materias."""
from __future__ import annotations

from typing import List

from models.materia import Materia
from repositories.base_repository import BaseRepository


class MateriaRepository(BaseRepository):
    """Gestiona operaciones de persistencia para materias."""

    def __init__(self) -> None:
        super().__init__("materia")

    def crear(self, nombre: str, horas_semanales: int) -> None:
        self.create(["nombre", "horas_semanales"], [nombre, horas_semanales])

    def obtener_todas(self) -> List[Materia]:
        registros = self.find_all(["id", "nombre", "horas_semanales"])
        return [Materia.from_dict(registro) for registro in registros]

    def actualizar(self, materia_id: int, nombre: str, horas_semanales: int) -> None:
        self.update(materia_id, ["nombre", "horas_semanales"], [nombre, horas_semanales])

    def eliminar(self, materia_id: int) -> None:
        self.delete(materia_id)
