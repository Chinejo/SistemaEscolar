"""
Paquete de vistas.
Cada vista representa una pantalla completa de la aplicación.
"""

from ui.main_window import MainWindow

from .base import BaseView
from .materias_view import MateriasView, build_materias_view
from .planes_view import PlanesView, build_planes_view
from .anios_view import AniosView, build_anios_view
from .divisiones_view import DivisionesView, build_divisiones_view
from .profesores_view import ProfesoresView, build_profesores_view
from .turnos_view import TurnosView, build_turnos_view
from .horarios_view import HorariosCursoView, HorariosProfesorView, build_horarios_curso_view, build_horarios_profesor_view

__all__ = [
	"BaseView",
	"MateriasView",
	"build_materias_view",
	"PlanesView",
	"build_planes_view",
	"AniosView",
	"build_anios_view",
	"DivisionesView",
	"build_divisiones_view",
	"ProfesoresView",
	"build_profesores_view",
	"TurnosView",
	"build_turnos_view",
	"HorariosCursoView",
	"build_horarios_curso_view",
	"HorariosProfesorView",
	"build_horarios_profesor_view",
	"register_views",
]


def register_views(app: MainWindow) -> None:
	"""Registra todas las vistas disponibles en la ventana principal."""
	app.register_view("materias", build_materias_view)
	app.register_view("planes", build_planes_view)
	app.register_view("anios", build_anios_view)
	app.register_view("divisiones", build_divisiones_view)
	app.register_view("profesores", build_profesores_view)
	app.register_view("turnos", build_turnos_view)
	app.register_view("horarios_curso", build_horarios_curso_view)
	app.register_view("horarios_profesor", build_horarios_profesor_view)
