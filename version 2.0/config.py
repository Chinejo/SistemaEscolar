"""Configuración global de la aplicación."""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Final, Sequence


def get_base_path() -> str:
    """Obtiene la ruta base de la aplicación, compatible con ejecutables PyInstaller."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


_BASE_PATH: Final[Path] = Path(get_base_path())
_DEFAULT_DB_NAME: Final[str] = "horarios.db"

_ENV_DB_PATH = os.getenv("HORARIOS_DB_PATH")

if _ENV_DB_PATH:
    DB_PATH: Final[Path] = Path(_ENV_DB_PATH).resolve()
    DB_DIR: Final[Path] = DB_PATH.parent
    DB_NAME: Final[str] = DB_PATH.name
else:
    DB_DIR: Final[Path] = _BASE_PATH
    DB_NAME: Final[str] = _DEFAULT_DB_NAME
    DB_PATH: Final[Path] = DB_DIR / DB_NAME

DIAS_SEMANA: Final[Sequence[str]] = (
    "Lunes",
    "Martes",
    "Miercoles",
    "Jueves",
    "Viernes",
)


def ensure_directories() -> None:
    """Crea los directorios necesarios para almacenar la base de datos."""
    DB_DIR.mkdir(parents=True, exist_ok=True)


ensure_directories()
