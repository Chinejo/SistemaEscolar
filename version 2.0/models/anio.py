"""Modelo de anio dentro de un plan."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from models.base import BaseModel


@dataclass
class Anio(BaseModel):
    """Representa un anio perteneciente a un plan de estudio."""

    nombre: Optional[str] = None
    plan_id: Optional[int] = None
