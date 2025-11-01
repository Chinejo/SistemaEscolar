"""Modelo de division o curso."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from models.base import BaseModel


@dataclass
class Division(BaseModel):
    """Representa una division asociada a turno, plan y anio."""

    nombre: Optional[str] = None
    turno_id: Optional[int] = None
    plan_id: Optional[int] = None
    anio_id: Optional[int] = None
