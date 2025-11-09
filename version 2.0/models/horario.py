"""Modelo de horario asignado."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from models.base import BaseModel


@dataclass
class Horario(BaseModel):
    """Representa un bloque horario para una division o profesor."""

    division_id: Optional[int] = None
    dia: Optional[str] = None
    espacio: Optional[int] = None
    hora_inicio: Optional[str] = None
    hora_fin: Optional[str] = None
    materia_id: Optional[int] = None
    profesor_id: Optional[int] = None
    turno_id: Optional[int] = None
