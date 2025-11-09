"""Repositorio para divisiones."""
from __future__ import annotations

from typing import List

from database.connection import get_connection
from models.division import Division
from repositories.base_repository import BaseRepository


class DivisionRepository(BaseRepository):
    """Gestiona divisiones asociadas a turno, plan y anio."""

    def __init__(self) -> None:
        super().__init__("division")

    def crear(self, nombre: str, turno_id: int, plan_id: int, anio_id: int) -> None:
        self.create(["nombre", "turno_id", "plan_id", "anio_id"], [nombre, turno_id, plan_id, anio_id])

    def obtener_todas(self) -> List[Division]:
        registros = self.find_all(["id", "nombre", "turno_id", "plan_id", "anio_id"])
        return [Division.from_dict(registro) for registro in registros]

    def actualizar(self, division_id: int, nombre: str) -> None:
        self.update(division_id, ["nombre"], [nombre])

    def eliminar(self, division_id: int) -> None:
        self.delete(division_id)
