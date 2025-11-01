"""Repositorio base con operaciones CRUD genericas."""
from __future__ import annotations

from typing import Iterable, List, Mapping, Sequence

from database.connection import db_operation


class BaseRepository:
    """Proporciona operaciones CRUD para tablas SQLite."""

    def __init__(self, table: str, id_field: str = "id") -> None:
        self.table = table
        self.id_field = id_field

    @db_operation
    def create(self, connection, fields: Sequence[str], values: Sequence[object]) -> None:
        placeholders = ",".join(["?"] * len(values))
        fields_str = ",".join(fields)
        connection.execute(
            f"INSERT INTO {self.table} ({fields_str}) VALUES ({placeholders})",
            values,
        )

    @db_operation
    def find_all(self, connection, fields: Sequence[str]) -> List[Mapping[str, object]]:
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT {','.join(fields)} FROM {self.table}"
        )
        rows = cursor.fetchall()
        return [dict(zip(fields, row)) for row in rows]

    @db_operation
    def find_by_id(self, connection, record_id: int, fields: Sequence[str]) -> Mapping[str, object] | None:
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT {','.join(fields)} FROM {self.table} WHERE {self.id_field} = ?",
            (record_id,),
        )
        row = cursor.fetchone()
        return dict(zip(fields, row)) if row else None

    @db_operation
    def update(self, connection, record_id: int, fields: Sequence[str], values: Sequence[object]) -> None:
        sets = ",".join(f"{field}=?" for field in fields)
        connection.execute(
            f"UPDATE {self.table} SET {sets} WHERE {self.id_field}=?",
            (*values, record_id),
        )

    @db_operation
    def delete(self, connection, record_id: int) -> None:
        connection.execute(
            f"DELETE FROM {self.table} WHERE {self.id_field}=?",
            (record_id,),
        )
