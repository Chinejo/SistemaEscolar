"""Repositorio para horarios."""
from __future__ import annotations

from typing import List, Optional

from database.connection import get_connection
from repositories.base_repository import BaseRepository


class HorarioRepository(BaseRepository):
    """Gestiona horarios por division y por profesor, aplicando validaciones basicas."""

    def __init__(self) -> None:
        super().__init__("horario")

    def crear(
        self,
        division_id: int,
        dia: str,
        espacio: int,
        hora_inicio: Optional[str],
        hora_fin: Optional[str],
        materia_id: Optional[int],
        profesor_id: Optional[int],
        turno_id: Optional[int] = None,
    ) -> None:
        with get_connection() as connection:
            cursor = connection.cursor()

            if turno_id is None:
                cursor.execute("SELECT turno_id FROM division WHERE id=?", (division_id,))
                row = cursor.fetchone()
                if not row:
                    raise Exception("Division no encontrada.")
                turno_id = row[0]

            if profesor_id is not None:
                cursor.execute(
                    """
                    SELECT 1
                    FROM horario h
                    JOIN division d ON h.division_id = d.id
                    WHERE h.dia=? AND h.espacio=? AND h.profesor_id=? AND d.turno_id=? AND h.division_id != ?
                    """,
                    (dia, espacio, profesor_id, turno_id, division_id),
                )
                if cursor.fetchone():
                    raise Exception(
                        "El profesor ya esta asignado en ese horario en otra division del mismo turno."
                    )

            if profesor_id is not None and materia_id is not None:
                cursor.execute(
                    "SELECT 1 FROM profesor_materia WHERE profesor_id=? AND materia_id=?",
                    (profesor_id, materia_id),
                )
                if not cursor.fetchone():
                    raise Exception("El profesor no tiene asignada la materia seleccionada.")

            cursor.execute(
                """
                INSERT INTO horario (division_id, dia, espacio, hora_inicio, hora_fin, materia_id, profesor_id, turno_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    division_id,
                    dia,
                    espacio,
                    hora_inicio or None,
                    hora_fin or None,
                    materia_id,
                    profesor_id,
                    turno_id,
                ),
            )

            if materia_id is not None:
                cursor.execute(
                    "UPDATE materia SET horas_semanales = horas_semanales + 1 WHERE id=?",
                    (materia_id,),
                )
            if profesor_id is not None and materia_id is not None:
                cursor.execute(
                    """
                    UPDATE profesor_materia
                    SET banca_horas = banca_horas + 1
                    WHERE profesor_id=? AND materia_id=?
                    """,
                    (profesor_id, materia_id),
                )

    def obtener_por_division(self, division_id: int) -> List[dict]:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT h.id, h.dia, h.espacio, h.hora_inicio, h.hora_fin,
                       m.nombre AS materia, p.nombre AS profesor
                FROM horario h
                LEFT JOIN materia m ON h.materia_id = m.id
                LEFT JOIN profesor p ON h.profesor_id = p.id
                WHERE h.division_id=?
                """,
                (division_id,),
            )
            return [dict(row) for row in cursor.fetchall()]

    def eliminar(self, horario_id: int) -> None:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT materia_id, profesor_id FROM horario WHERE id=?",
                (horario_id,),
            )
            row = cursor.fetchone()
            if row:
                materia_id, profesor_id = row
                if materia_id is not None:
                    cursor.execute(
                        "UPDATE materia SET horas_semanales = horas_semanales - 1 WHERE id=?",
                        (materia_id,),
                    )
                if profesor_id is not None and materia_id is not None:
                    cursor.execute(
                        """
                        UPDATE profesor_materia
                        SET banca_horas = banca_horas - 1
                        WHERE profesor_id=? AND materia_id=?
                        """,
                        (profesor_id, materia_id),
                    )
            cursor.execute("DELETE FROM horario WHERE id=?", (horario_id,))

    def crear_para_profesor(
        self,
        profesor_id: int,
        turno_id: int,
        dia: str,
        espacio: int,
        hora_inicio: Optional[str],
        hora_fin: Optional[str],
        division_id: Optional[int] = None,
        materia_id: Optional[int] = None,
    ) -> None:
        with get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute(
                "SELECT 1 FROM profesor_turno WHERE profesor_id=? AND turno_id=?",
                (profesor_id, turno_id),
            )
            if not cursor.fetchone():
                raise Exception("El profesor no esta asignado a este turno.")

            if materia_id is not None:
                cursor.execute(
                    "SELECT 1 FROM profesor_materia WHERE profesor_id=? AND materia_id=?",
                    (profesor_id, materia_id),
                )
                if not cursor.fetchone():
                    raise Exception("El profesor no tiene asignada esta materia.")

            if division_id is not None:
                cursor.execute("SELECT turno_id FROM division WHERE id=?", (division_id,))
                row = cursor.fetchone()
                if not row:
                    raise Exception("Division no encontrada.")
                if row[0] != turno_id:
                    raise Exception("La division no pertenece al turno seleccionado.")
                cursor.execute(
                    """
                    SELECT 1 FROM horario
                    WHERE division_id=? AND dia=? AND espacio=?
                    """,
                    (division_id, dia, espacio),
                )
                if cursor.fetchone():
                    raise Exception(
                        "Ya existe un horario asignado para esta division en este dia y espacio."
                    )

            cursor.execute(
                """
                SELECT 1 FROM horario
                WHERE profesor_id=? AND turno_id=? AND dia=? AND espacio=?
                """,
                (profesor_id, turno_id, dia, espacio),
            )
            if cursor.fetchone():
                raise Exception(
                    "El profesor ya tiene un horario asignado en este dia y espacio en este turno."
                )

            cursor.execute(
                """
                INSERT INTO horario (division_id, dia, espacio, hora_inicio, hora_fin, materia_id, profesor_id, turno_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    division_id,
                    dia,
                    espacio,
                    hora_inicio or None,
                    hora_fin or None,
                    materia_id,
                    profesor_id,
                    turno_id,
                ),
            )

    def obtener_por_profesor(self, profesor_id: int, turno_id: int) -> List[dict]:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT h.id, h.dia, h.espacio, h.hora_inicio, h.hora_fin,
                       m.nombre AS materia, d.nombre AS division
                FROM horario h
                LEFT JOIN materia m ON h.materia_id = m.id
                LEFT JOIN division d ON h.division_id = d.id
                WHERE h.profesor_id=? AND h.turno_id=?
                """,
                (profesor_id, turno_id),
            )
            return [dict(row) for row in cursor.fetchall()]
