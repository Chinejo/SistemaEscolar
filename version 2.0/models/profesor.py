"""Modelo de profesor."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from models.base import BaseModel


@dataclass
class Profesor(BaseModel):
    """Representa a un profesor o agente docente."""

    nombre: Optional[str] = None
