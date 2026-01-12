"""Gestión de conexiones a la base de datos SQLite."""
from __future__ import annotations

import sqlite3
from functools import wraps
from typing import Any, Callable, TypeVar

from config import DB_PATH

T = TypeVar("T")


def get_connection() -> sqlite3.Connection:
    """Devuelve una nueva conexión a la base de datos con row factory por nombre."""
    connection = sqlite3.connect(DB_PATH.as_posix())
    connection.row_factory = sqlite3.Row
    return connection


def db_operation(func: Callable[..., T]) -> Callable[..., T]:
    """Decorador que gestiona apertura, commit y cierre de conexiones SQLite.

    Es compatible tanto con funciones libres como con métodos de instancia.
    Cuando se aplica sobre un método, se inyecta la conexión como segundo
    parámetro (después de ``self``).
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        connection = get_connection()
        try:
            if "." in func.__qualname__ and args:
                new_args = (args[0], connection, *args[1:])
                result = func(*new_args, **kwargs)
            else:
                result = func(connection, *args, **kwargs)
            connection.commit()
            return result
        except sqlite3.IntegrityError as exc:
            connection.rollback()
            raise Exception(str(exc)) from exc
        finally:
            connection.close()

    return wrapper
