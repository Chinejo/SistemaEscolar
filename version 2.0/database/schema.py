"""Inicialización del esquema de base de datos."""
from __future__ import annotations

import sqlite3
from typing import Iterable

from database.connection import get_connection


def _execute_statements(cursor: sqlite3.Cursor, statements: Iterable[str]) -> None:
    """Ejecuta un conjunto de sentencias SQL secuencialmente."""
    for statement in statements:
        cursor.execute(statement)


def init_db() -> None:
    """Crea tablas y restricciones necesarias si aún no existen."""
    connection = get_connection()
    cursor = connection.cursor()

    statements = (
        """
        CREATE TABLE IF NOT EXISTS plan_estudio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS materia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL,
            horas_semanales INTEGER NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS anio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            plan_id INTEGER,
            FOREIGN KEY(plan_id) REFERENCES plan_estudio(id),
            UNIQUE(nombre, plan_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS anio_materia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            anio_id INTEGER,
            materia_id INTEGER,
            FOREIGN KEY(anio_id) REFERENCES anio(id),
            FOREIGN KEY(materia_id) REFERENCES materia(id),
            UNIQUE(anio_id, materia_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS plan_materia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plan_id INTEGER,
            materia_id INTEGER,
            FOREIGN KEY(plan_id) REFERENCES plan_estudio(id),
            FOREIGN KEY(materia_id) REFERENCES materia(id),
            UNIQUE(plan_id, materia_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS turno (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS turno_plan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            turno_id INTEGER,
            plan_id INTEGER,
            FOREIGN KEY(turno_id) REFERENCES turno(id),
            FOREIGN KEY(plan_id) REFERENCES plan_estudio(id),
            UNIQUE(turno_id, plan_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS division (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            turno_id INTEGER,
            plan_id INTEGER,
            anio_id INTEGER,
            FOREIGN KEY(turno_id) REFERENCES turno(id),
            FOREIGN KEY(plan_id) REFERENCES plan_estudio(id),
            FOREIGN KEY(anio_id) REFERENCES anio(id),
            UNIQUE(nombre, turno_id, plan_id, anio_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS profesor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS profesor_materia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profesor_id INTEGER,
            materia_id INTEGER,
            banca_horas INTEGER NOT NULL,
            FOREIGN KEY(profesor_id) REFERENCES profesor(id),
            FOREIGN KEY(materia_id) REFERENCES materia(id),
            UNIQUE(profesor_id, materia_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS profesor_turno (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profesor_id INTEGER,
            turno_id INTEGER,
            FOREIGN KEY(profesor_id) REFERENCES profesor(id),
            FOREIGN KEY(turno_id) REFERENCES turno(id),
            UNIQUE(profesor_id, turno_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS horario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            division_id INTEGER,
            dia TEXT,
            espacio INTEGER,
            hora_inicio TEXT,
            hora_fin TEXT,
            materia_id INTEGER,
            profesor_id INTEGER,
            turno_id INTEGER,
            FOREIGN KEY(division_id) REFERENCES division(id),
            FOREIGN KEY(materia_id) REFERENCES materia(id),
            FOREIGN KEY(profesor_id) REFERENCES profesor(id),
            FOREIGN KEY(turno_id) REFERENCES turno(id),
            UNIQUE(division_id, dia, espacio)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS turno_espacio_hora (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            turno_id INTEGER,
            espacio INTEGER,
            hora_inicio TEXT,
            hora_fin TEXT,
            FOREIGN KEY(turno_id) REFERENCES turno(id),
            UNIQUE(turno_id, espacio)
        )
        """,
    )

    _execute_statements(cursor, statements)

    try:
        cursor.execute(
            "ALTER TABLE horario ADD COLUMN turno_id INTEGER REFERENCES turno(id)"
        )
    except sqlite3.OperationalError:
        pass

    connection.commit()
    connection.close()
