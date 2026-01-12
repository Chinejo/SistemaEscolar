"""
Paquete de servicios.
Contiene la lógica de negocio y validaciones de la aplicación.
"""

from .validation_service import (
	ValidationError,
	ValidationService,
	is_foreign_key_constraint_error,
	is_unique_constraint_error,
)
from .anio_service import AnioService
from .division_service import DivisionService
from .horario_service import HorarioService
from .materia_service import MateriaService
from .plan_service import PlanService
from .profesor_service import ProfesorService
from .turno_service import TurnoService

__all__ = [
	"ValidationError",
	"ValidationService",
	"is_unique_constraint_error",
	"is_foreign_key_constraint_error",
	"AnioService",
	"DivisionService",
	"HorarioService",
	"MateriaService",
	"PlanService",
	"ProfesorService",
	"TurnoService",
]
