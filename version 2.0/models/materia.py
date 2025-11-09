"""Modelo de materia u obligacion academica."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from models.base import BaseModel


@dataclass
class Materia(BaseModel):
    """Representa una materia con su carga horaria semanal."""

    nombre: Optional[str] = None
    horas_semanales: Optional[int] = None
