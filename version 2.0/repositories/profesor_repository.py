"""Repositorio para profesores."""
from __future__ import annotations

from typing import List

from database.connection import db_operation, get_connection
from models.profesor import Profesor
from repositories.base_repository import BaseRepository


class ProfesorRepository(BaseRepository):
    """Gestiona profesores, turnos asignados y banca de materias."""

    def __init__(self) -> None:
        super().__init__("profesor")

    def crear(self, nombre: str) -> None:
        self.create(["nombre"], [nombre])

    def obtener_todos(self) -> List[Profesor]:
        registros = self.find_all(["id", "nombre"])
        return [Profesor.from_dict(registro) for registro in registros]

    def actualizar(self, profesor_id: int, nombre: str) -> None:
        self.update(profesor_id, ["nombre"], [nombre])

    @db_operation
    def eliminar(self, connection, profesor_id: int) -> None:
        connection.execute("DELETE FROM profesor_turno WHERE profesor_id=?", (profesor_id,))
        connection.execute("DELETE FROM profesor_materia WHERE profesor_id=?", (profesor_id,))
        connection.execute("DELETE FROM profesor WHERE id=?", (profesor_id,))

    def asignar_turno(self, profesor_id: int, turno_id: int) -> None:
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO profesor_turno (profesor_id, turno_id) VALUES (?, ?)",
                (profesor_id, turno_id),
            )
            connection.commit()
        except Exception as exc:
            connection.rollback()
            raise Exception("El profesor ya tiene asignado ese turno.") from exc
        finally:
            connection.close()

    def quitar_turno(self, profesor_id: int, turno_id: int) -> None:
        with get_connection() as connection:
            connection.execute(
                "DELETE FROM profesor_turno WHERE profesor_id=? AND turno_id=?",
                (profesor_id, turno_id),
            )

    def obtener_turnos(self, profesor_id: int) -> List[dict]:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT t.id, t.nombre
                FROM profesor_turno pt
                JOIN turno t ON pt.turno_id = t.id
                WHERE pt.profesor_id=?
                """,
                (profesor_id,),
            )
            return [dict(row) for row in cursor.fetchall()]

    def obtener_por_turno(self, turno_id: int) -> List[dict]:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT p.id, p.nombre
                FROM profesor p
                JOIN profesor_turno pt ON p.id = pt.profesor_id
                WHERE pt.turno_id=?
                """,
                (turno_id,),
            )
            return [dict(row) for row in cursor.fetchall()]

    def asignar_banca(self, profesor_id: int, materia_id: int, banca_horas: int) -> None:
        try:
            with get_connection() as connection:
                connection.execute(
                    """
                    INSERT INTO profesor_materia (profesor_id, materia_id, banca_horas)
                    VALUES (?, ?, ?)
                    """,
                    (profesor_id, materia_id, banca_horas),
                )
        except Exception as exc:
            raise Exception("El profesor ya tiene esa materia asignada.") from exc

    def obtener_banca(self, profesor_id: int) -> List[dict]:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT pm.id, m.nombre, pm.banca_horas
                FROM profesor_materia pm
                JOIN materia m ON pm.materia_id = m.id
                WHERE pm.profesor_id=?
                """,
                (profesor_id,),
            )
            return [dict(row) for row in cursor.fetchall()]

    def actualizar_banca(self, relacion_id: int, banca_horas: int) -> None:
        with get_connection() as connection:
            connection.execute(
                "UPDATE profesor_materia SET banca_horas=? WHERE id=?",
                (banca_horas, relacion_id),
            )

    def eliminar_banca(self, relacion_id: int) -> None:
        with get_connection() as connection:
            connection.execute(
                "DELETE FROM profesor_materia WHERE id=?",
                (relacion_id,),
            )
