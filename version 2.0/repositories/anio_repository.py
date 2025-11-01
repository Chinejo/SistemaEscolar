"""Repositorio para anios dentro de un plan."""
from __future__ import annotations

from typing import List

from database.connection import db_operation, get_connection
from models.anio import Anio
from repositories.base_repository import BaseRepository


class AnioRepository(BaseRepository):
    """Gestiona anios y sus materias asociadas."""

    def __init__(self) -> None:
        super().__init__("anio")

    def crear(self, nombre: str, plan_id: int) -> None:
        self.create(["nombre", "plan_id"], [nombre, plan_id])

    def obtener_por_plan(self, plan_id: int) -> List[Anio]:
        registros = self._obtener(
            "SELECT id, nombre, plan_id FROM anio WHERE plan_id=? ORDER BY nombre COLLATE NOCASE",
            (plan_id,),
        )
        return [Anio.from_dict(registro) for registro in registros]

    def actualizar(self, anio_id: int, nombre: str) -> None:
        self.update(anio_id, ["nombre"], [nombre])

    def eliminar(self, anio_id: int) -> None:
        self.delete(anio_id)

    def agregar_materia(self, anio_id: int, materia_id: int) -> None:
        with get_connection() as connection:
            connection.execute(
                "INSERT INTO anio_materia (anio_id, materia_id) VALUES (?, ?)",
                (anio_id, materia_id),
            )

    def quitar_materia(self, anio_id: int, materia_id: int) -> None:
        with get_connection() as connection:
            connection.execute(
                "DELETE FROM anio_materia WHERE anio_id=? AND materia_id=?",
                (anio_id, materia_id),
            )

    def obtener_materias(self, anio_id: int) -> List[dict]:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT m.id, m.nombre, m.horas_semanales
                FROM anio_materia am
                JOIN materia m ON am.materia_id = m.id
                WHERE am.anio_id=?
                """,
                (anio_id,),
            )
            return [dict(row) for row in cursor.fetchall()]

    @db_operation
    def _obtener(self, connection, query: str, params: tuple[int, ...]) -> List[dict]:
        cursor = connection.cursor()
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
