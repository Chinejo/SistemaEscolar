"""Repositorio para turnos."""
from __future__ import annotations

from typing import List, Optional

from database.connection import get_connection
from models.turno import Turno
from repositories.base_repository import BaseRepository


class TurnoRepository(BaseRepository):
    """Gestiona turnos, asociaciones con planes y espacios horarios."""

    def __init__(self) -> None:
        super().__init__("turno")

    def crear(self, nombre: str) -> None:
        self.create(["nombre"], [nombre])

    def obtener_todos(self) -> List[Turno]:
        registros = self.find_all(["id", "nombre"])
        return [Turno.from_dict(registro) for registro in registros]

    def actualizar(self, turno_id: int, nombre: str) -> None:
        self.update(turno_id, ["nombre"], [nombre])

    def eliminar(self, turno_id: int) -> None:
        self.delete(turno_id)

    def agregar_plan(self, turno_id: int, plan_id: int) -> None:
        with get_connection() as connection:
            connection.execute(
                "INSERT INTO turno_plan (turno_id, plan_id) VALUES (?, ?)",
                (turno_id, plan_id),
            )

    def quitar_plan(self, turno_id: int, plan_id: int) -> None:
        with get_connection() as connection:
            connection.execute(
                "DELETE FROM turno_plan WHERE turno_id=? AND plan_id=?",
                (turno_id, plan_id),
            )

    def obtener_planes(self, turno_id: int) -> List[dict]:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT DISTINCT p.id, p.nombre
                FROM plan_estudio p
                JOIN turno_plan tp ON tp.plan_id = p.id
                WHERE tp.turno_id=?
                """,
                (turno_id,),
            )
            return [dict(row) for row in cursor.fetchall()]

    def obtener_espacio_hora(self, turno_id: int, espacio: int) -> Optional[dict]:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT id, hora_inicio, hora_fin
                FROM turno_espacio_hora
                WHERE turno_id=? AND espacio=?
                """,
                (turno_id, espacio),
            )
            row = cursor.fetchone()
            return dict(row) if row else None

    def set_espacio_hora(self, turno_id: int, espacio: int, hora_inicio: str, hora_fin: str) -> None:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO turno_espacio_hora (turno_id, espacio, hora_inicio, hora_fin)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(turno_id, espacio)
                DO UPDATE SET hora_inicio=excluded.hora_inicio, hora_fin=excluded.hora_fin
                """,
                (turno_id, espacio, hora_inicio, hora_fin),
            )

    def eliminar_espacio_hora(self, turno_id: int, espacio: int) -> None:
        with get_connection() as connection:
            connection.execute(
                "DELETE FROM turno_espacio_hora WHERE turno_id=? AND espacio=?",
                (turno_id, espacio),
            )
