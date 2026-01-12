"""Clases base para modelos de datos."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Mapping, Type, TypeVar

T = TypeVar("T", bound="BaseModel")


@dataclass
class BaseModel:
    """Proporciona serialización simple a diccionarios."""

    id: int | None = None

    def to_dict(self) -> Dict[str, Any]:
        """Devuelve los campos del modelo en formato diccionario."""
        return asdict(self)

    @classmethod
    def from_dict(cls: Type[T], data: Mapping[str, Any]) -> T:
        """Crea una instancia a partir de un mapeo de datos."""
        return cls(**data)
