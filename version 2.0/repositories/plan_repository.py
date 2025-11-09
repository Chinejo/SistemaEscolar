"""Repositorio para planes de estudio."""
from __future__ import annotations

from typing import List

from database.connection import get_connection
from models.plan import Plan
from repositories.base_repository import BaseRepository


class PlanRepository(BaseRepository):
    """Gestiona planes de estudio y sus materias asociadas."""

    def __init__(self) -> None:
        super().__init__("plan_estudio")

    def crear(self, nombre: str) -> None:
        self.create(["nombre"], [nombre])

    def obtener_todos(self) -> List[Plan]:
        registros = self.find_all(["id", "nombre"])
        return [Plan.from_dict(registro) for registro in registros]

    def actualizar(self, plan_id: int, nombre: str) -> None:
        self.update(plan_id, ["nombre"], [nombre])

    def eliminar(self, plan_id: int) -> None:
        self.delete(plan_id)

    def agregar_materia(self, plan_id: int, materia_id: int) -> None:
        with get_connection() as connection:
            connection.execute(
                "INSERT INTO plan_materia (plan_id, materia_id) VALUES (?, ?)",
                (plan_id, materia_id),
            )

    def quitar_materia(self, plan_id: int, materia_id: int) -> None:
        with get_connection() as connection:
            connection.execute(
                "DELETE FROM plan_materia WHERE plan_id=? AND materia_id=?",
                (plan_id, materia_id),
            )

    def obtener_materias(self, plan_id: int) -> List[dict]:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT m.id, m.nombre, m.horas_semanales
                FROM plan_materia pm
                JOIN materia m ON pm.materia_id = m.id
                WHERE pm.plan_id=?
                """,
                (plan_id,),
            )
            return [dict(row) for row in cursor.fetchall()]
