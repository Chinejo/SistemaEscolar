"""Modelo de turno."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from models.base import BaseModel


@dataclass
class Turno(BaseModel):
    """Representa un turno disponible para cursado."""

    nombre: Optional[str] = None
