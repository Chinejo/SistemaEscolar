"""Modelo de plan de estudio."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from models.base import BaseModel


@dataclass
class Plan(BaseModel):
    """Representa un plan de estudios."""

    nombre: Optional[str] = None
