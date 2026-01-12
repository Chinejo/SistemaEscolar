"""Pruebas integradas sobre la capa de servicios."""
from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

# Configurar base de datos temporal antes de importar módulos del proyecto
_PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

_TEMP_DIR = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
os.environ["HORARIOS_DB_PATH"] = str(Path(_TEMP_DIR.name) / "test_horarios.db")

from database.schema import init_db  # noqa: E402
from services import ValidationError  # noqa: E402
from services.anio_service import AnioService  # noqa: E402
from services.division_service import DivisionService  # noqa: E402
from services.horario_service import HorarioService  # noqa: E402
from services.materia_service import MateriaService  # noqa: E402
from services.plan_service import PlanService  # noqa: E402
from services.profesor_service import ProfesorService  # noqa: E402
from services.turno_service import TurnoService  # noqa: E402


def reset_database() -> None:
    """Recrea la base de datos temporal para cada prueba."""
    db_path = Path(os.environ["HORARIOS_DB_PATH"])
    if db_path.exists():
        db_path.unlink()
    init_db()


class ServiceIntegrationTests(unittest.TestCase):
    """Escenarios de integración que ejercitan múltiples servicios."""

    def setUp(self) -> None:
        reset_database()
        self.materia_service = MateriaService()
        self.plan_service = PlanService()
        self.turno_service = TurnoService()
        self.anio_service = AnioService()
        self.division_service = DivisionService()
        self.profesor_service = ProfesorService()
        self.horario_service = HorarioService()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _crear_materia(self, nombre: str = "Matematica", horas: int = 5):
        self.materia_service.crear(nombre, horas)
        return self.materia_service.listar()[0]

    def _crear_plan(self, nombre: str = "Plan 2025"):
        self.plan_service.crear(nombre)
        return self.plan_service.listar()[0]

    def _crear_turno(self, nombre: str = "Mañana"):
        self.turno_service.crear(nombre)
        return self.turno_service.listar()[0]

    def _crear_anio(self, nombre: str, plan_id: int):
        self.anio_service.crear(nombre, plan_id)
        return self.anio_service.listar_por_plan(plan_id)[0]

    def _crear_division(self, nombre: str, turno_id: int, plan_id: int, anio_id: int):
        self.division_service.crear(nombre, turno_id, plan_id, anio_id)
        return self.division_service.listar()[0]

    def _crear_profesor(self, nombre: str = "Juan Perez"):
        self.profesor_service.crear(nombre)
        return self.profesor_service.listar()[0]

    # ------------------------------------------------------------------
    # Casos de prueba
    # ------------------------------------------------------------------
    def test_crear_materia_y_detectar_duplicado(self) -> None:
        materia = self._crear_materia("Historia", 4)
        self.assertEqual("Historia", materia.nombre)
        with self.assertRaises(ValidationError):
            self.materia_service.crear("Historia", 4)

    def test_flujo_completo_horario(self) -> None:
        materia = self._crear_materia("Biologia", 3)
        plan = self._crear_plan("Plan Ciencias")
        turno = self._crear_turno("Tarde")
        self.assertIsNotNone(materia.id)
        self.assertIsNotNone(plan.id)
        self.assertIsNotNone(turno.id)

        self.turno_service.agregar_plan(turno.id, plan.id)
        self.plan_service.agregar_materia(plan.id, materia.id)
        anio = self._crear_anio("1ro", plan.id)
        division = self._crear_division("1A", turno.id, plan.id, anio.id)
        profesor = self._crear_profesor("Maria Lopez")
        self.assertIsNotNone(anio.id)
        self.assertIsNotNone(division.id)
        self.assertIsNotNone(profesor.id)

        self.profesor_service.asignar_turno(profesor.id, turno.id)
        self.profesor_service.asignar_banca(profesor.id, materia.id, 3)

        self.horario_service.crear_para_division(
            division.id,
            "Lunes",
            "1",
            hora_inicio="08:00",
            hora_fin="09:00",
            materia_id=materia.id,
            profesor_id=profesor.id,
            turno_id=turno.id,
        )

        with self.assertRaises(ValidationError):
            self.horario_service.crear_para_division(
                division.id,
                "Lunes",
                "1",
                materia_id=materia.id,
                profesor_id=profesor.id,
                turno_id=turno.id,
            )

        horarios_curso = self.horario_service.obtener_por_division(division.id)
        self.assertEqual(1, len(horarios_curso))
        self.assertEqual("Biologia", horarios_curso[0]["materia"])
        self.assertEqual("Maria Lopez", horarios_curso[0]["profesor"])

        horarios_profesor = self.horario_service.obtener_por_profesor(profesor.id, turno.id)
        self.assertEqual(1, len(horarios_profesor))

        with self.assertRaises(ValidationError):
            self.horario_service.crear_para_profesor(
                profesor.id,
                turno.id,
                "Lunes",
                "1",
                division_id=division.id,
            )

        total_banca = self.profesor_service.calcular_horas_asignadas(profesor.id)
        self.assertEqual(4, total_banca)


if __name__ == "__main__":
    unittest.main()
