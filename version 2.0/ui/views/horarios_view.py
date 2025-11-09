"""Vistas para gestionar horarios por curso y por profesor."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from config import DIAS_SEMANA
from models.anio import Anio
from models.division import Division
from models.plan import Plan
from models.profesor import Profesor
from models.turno import Turno
from services import ValidationError
from ui.components import crear_treeview, recargar_treeview
from ui.main_window import MainWindow
from ui.views.base import BaseView
from utils import bind_enter, focus_entry, get_first_selection


_ESPACIOS = tuple(str(numero) for numero in range(1, 9))


class HorariosCursoView(BaseView):
    """Permite asignar horarios a divisiones desde la perspectiva del curso."""

    def __init__(self, master: tk.Misc, app: MainWindow) -> None:  # type: ignore[override]
        super().__init__(master, app, title="Gestión de horarios por curso")
        self.horario_service = app.horario_service
        self.division_service = app.division_service
        self.plan_service = app.plan_service
        self.anio_service = app.anio_service
        self.turno_service = app.turno_service
        self.profesor_service = app.profesor_service

        self._divisiones: list[Division] = []
        self._turnos: list[Turno] = []
        self._planes_por_id: dict[int, Plan] = {}
        self._divisiones_por_turno: dict[int, list[Division]] = {}
        self._materias_plan: dict[int, list[dict]] = {}
        self._anios_plan: dict[int, list[Anio]] = {}
        self._profesores_por_turno: dict[int, list[dict]] = {}
        self._horarios_actuales: list[dict] = []
        self._materia_map: dict[str, int | None] = {}
        self._profesor_map: dict[str, int | None] = {}
        self._division_display_map: dict[str, Division] = {}

        self._selected_division: Division | None = None
        self._selected_horario_id: int | None = None

        self._turno_var = tk.StringVar()
        self._division_var = tk.StringVar()
        self._dia_var = tk.StringVar(value=DIAS_SEMANA[0])
        self._espacio_var = tk.StringVar(value=_ESPACIOS[0])
        self._materia_var = tk.StringVar()
        self._profesor_var = tk.StringVar()
        self._hora_inicio_var = tk.StringVar()
        self._hora_fin_var = tk.StringVar()
        self._plan_label_var = tk.StringVar()
        self._anio_label_var = tk.StringVar()

        self._build_layout()
        self.refresh()

    # ------------------------------------------------------------------
    # Construcción de UI
    # ------------------------------------------------------------------
    def _build_layout(self) -> None:
        selector = ttk.Frame(self)
        selector.pack(fill="x", pady=(0, 10))

        ttk.Label(selector, text="Turno:").grid(row=0, column=0, padx=5, pady=2)
        self._combo_turno = ttk.Combobox(selector, textvariable=self._turno_var, state="readonly", width=25)
        self._combo_turno.grid(row=0, column=1, padx=5, pady=2)
        self._combo_turno.bind("<<ComboboxSelected>>", self._on_turno_changed)

        ttk.Label(selector, text="División:").grid(row=0, column=2, padx=5, pady=2)
        self._combo_division = ttk.Combobox(selector, textvariable=self._division_var, state="readonly", width=35)
        self._combo_division.grid(row=0, column=3, padx=5, pady=2)
        self._combo_division.bind("<<ComboboxSelected>>", self._on_division_changed)

        tabla = ttk.Frame(self)
        tabla.pack(fill="both", expand=True)
        self._tree = crear_treeview(
            tabla,
            ("dia", "espacio", "materia", "profesor", "inicio", "fin"),
            ("Día", "Espacio", "Materia", "Profesor", "Inicio", "Fin"),
            height=12,
        )
        self._tree.bind("<<TreeviewSelect>>", self._on_tree_select)

        detalle = ttk.LabelFrame(self, text="Nueva asignación")
        detalle.pack(fill="x", pady=12)

        ttk.Label(detalle, text="Plan:").grid(row=0, column=0, padx=5, pady=3, sticky="e")
        ttk.Label(detalle, textvariable=self._plan_label_var).grid(row=0, column=1, padx=5, pady=3, sticky="w")
        ttk.Label(detalle, text="Curso:").grid(row=0, column=2, padx=5, pady=3, sticky="e")
        ttk.Label(detalle, textvariable=self._anio_label_var).grid(row=0, column=3, padx=5, pady=3, sticky="w")

        ttk.Label(detalle, text="Día:").grid(row=1, column=0, padx=5, pady=3, sticky="e")
        self._combo_dia = ttk.Combobox(detalle, textvariable=self._dia_var, values=DIAS_SEMANA, state="readonly", width=18)
        self._combo_dia.grid(row=1, column=1, padx=5, pady=3, sticky="w")

        ttk.Label(detalle, text="Espacio:").grid(row=1, column=2, padx=5, pady=3, sticky="e")
        self._combo_espacio = ttk.Combobox(detalle, textvariable=self._espacio_var, values=_ESPACIOS, state="readonly", width=8)
        self._combo_espacio.grid(row=1, column=3, padx=5, pady=3, sticky="w")

        ttk.Label(detalle, text="Materia:").grid(row=2, column=0, padx=5, pady=3, sticky="e")
        self._combo_materia = ttk.Combobox(detalle, textvariable=self._materia_var, state="readonly", width=28)
        self._combo_materia.grid(row=2, column=1, padx=5, pady=3, sticky="w")

        ttk.Label(detalle, text="Profesor:").grid(row=2, column=2, padx=5, pady=3, sticky="e")
        self._combo_profesor = ttk.Combobox(detalle, textvariable=self._profesor_var, state="readonly", width=28)
        self._combo_profesor.grid(row=2, column=3, padx=5, pady=3, sticky="w")

        ttk.Label(detalle, text="Hora inicio:").grid(row=3, column=0, padx=5, pady=3, sticky="e")
        self._entry_inicio = ttk.Entry(detalle, textvariable=self._hora_inicio_var, width=12)
        self._entry_inicio.grid(row=3, column=1, padx=5, pady=3, sticky="w")

        ttk.Label(detalle, text="Hora fin:").grid(row=3, column=2, padx=5, pady=3, sticky="e")
        self._entry_fin = ttk.Entry(detalle, textvariable=self._hora_fin_var, width=12)
        self._entry_fin.grid(row=3, column=3, padx=5, pady=3, sticky="w")

        botones = ttk.Frame(self)
        botones.pack(pady=6)
        ttk.Button(botones, text="Agregar", command=self._agregar).grid(row=0, column=0, padx=5)
        ttk.Button(botones, text="Eliminar", command=self._eliminar).grid(row=0, column=1, padx=5)

        bind_enter(self._entry_inicio, self._agregar)
        focus_entry(self._entry_inicio)

    # ------------------------------------------------------------------
    # Datos y refresco
    # ------------------------------------------------------------------
    def refresh(self) -> None:
        self._divisiones = sorted(self.division_service.listar(), key=lambda d: (d.nombre or "").lower())
        self._turnos = sorted(self.turno_service.listar(), key=lambda t: (t.nombre or "").lower())
        self._planes_por_id = {plan.id or 0: plan for plan in self.plan_service.listar()}
        self._materias_plan.clear()
        self._anios_plan.clear()
        self._profesores_por_turno.clear()
        self._divisiones_por_turno = {}
        for division in self._divisiones:
            turno_id = division.turno_id or 0
            self._divisiones_por_turno.setdefault(turno_id, []).append(division)
            if division.plan_id and division.plan_id not in self._anios_plan:
                self._anios_plan[division.plan_id] = self.anio_service.listar_por_plan(division.plan_id)

        # Ordenar divisiones por nombre dentro de cada turno
        for divisiones in self._divisiones_por_turno.values():
            divisiones.sort(key=lambda d: (d.nombre or "").lower())

        turno_nombres = [turno.nombre or "" for turno in self._turnos]
        self._combo_turno["values"] = turno_nombres
        if turno_nombres:
            self._turno_var.set(turno_nombres[0])
        else:
            self._turno_var.set("")

        self._update_division_options()
        self.set_status("Horarios por curso actualizados")

    def _update_division_options(self) -> None:
        turno = self._resolve_turno(self._turno_var.get())
        if turno is None:
            self._combo_division["values"] = []
            self._division_var.set("")
            self._selected_division = None
            self._clear_form()
            recargar_treeview(self._tree, [], ["dia", "espacio", "materia", "profesor", "inicio", "fin"])
            return

        opciones = []
        self._division_display_map: dict[str, Division] = {}
        for division in self._divisiones_por_turno.get(turno.id or 0, []):
            plan_nombre = self._lookup_plan_nombre(division.plan_id)
            etiqueta = f"{division.nombre or ''} ({plan_nombre})"
            opciones.append(etiqueta)
            self._division_display_map[etiqueta] = division

        self._combo_division["values"] = opciones
        if opciones:
            self._division_var.set(opciones[0])
        else:
            self._division_var.set("")
        self._on_division_changed()

    def _clear_form(self) -> None:
        self._plan_label_var.set("")
        self._anio_label_var.set("")
        self._combo_materia["values"] = []
        self._combo_profesor["values"] = []
        self._materia_var.set("")
        self._profesor_var.set("")
        self._hora_inicio_var.set("")
        self._hora_fin_var.set("")
        self._materia_map = {}
        self._profesor_map = {}
        self._selected_horario_id = None

    def _load_materias_for_plan(self, plan_id: int | None) -> None:
        if plan_id is None:
            self._combo_materia["values"] = []
            self._materia_map = {}
            self._materia_var.set("")
            return
        if plan_id not in self._materias_plan:
            self._materias_plan[plan_id] = self.plan_service.obtener_materias(plan_id)
        materias = self._materias_plan.get(plan_id, [])
        self._materia_map = {registro.get("nombre", ""): registro.get("id") for registro in materias}
        valores = sorted(self._materia_map.keys(), key=str.lower)
        self._combo_materia["values"] = valores
        if valores:
            self._materia_var.set(valores[0])
        else:
            self._materia_var.set("")

    def _load_profesores_for_turno(self, turno_id: int | None) -> None:
        if turno_id is None:
            self._combo_profesor["values"] = []
            self._profesor_map = {}
            self._profesor_var.set("")
            return
        if turno_id not in self._profesores_por_turno:
            self._profesores_por_turno[turno_id] = self.profesor_service.obtener_por_turno(turno_id)
        profesores = self._profesores_por_turno.get(turno_id, [])
        self._profesor_map = {registro.get("nombre", ""): registro.get("id") for registro in profesores}
        valores = sorted(self._profesor_map.keys(), key=str.lower)
        self._combo_profesor["values"] = valores
        if valores:
            self._profesor_var.set(valores[0])
        else:
            self._profesor_var.set("")

    # ------------------------------------------------------------------
    # Eventos
    # ------------------------------------------------------------------
    def _on_turno_changed(self, _event: tk.Event | None = None) -> None:
        self._update_division_options()

    def _on_division_changed(self, _event: tk.Event | None = None) -> None:
        etiqueta = self._division_var.get()
        division = self._division_display_map.get(etiqueta) if hasattr(self, "_division_display_map") else None
        self._selected_division = division
        if division is None or division.id is None:
            self._clear_form()
            recargar_treeview(self._tree, [], ["dia", "espacio", "materia", "profesor", "inicio", "fin"])
            return

        plan_nombre = self._lookup_plan_nombre(division.plan_id)
        self._plan_label_var.set(plan_nombre)
        self._anio_label_var.set(self._lookup_anio_nombre(division))
        self._load_materias_for_plan(division.plan_id)
        self._load_profesores_for_turno(division.turno_id)
        self._reload_horarios()

    def _reload_horarios(self) -> None:
        if self._selected_division is None or self._selected_division.id is None:
            self._horarios_actuales = []
            recargar_treeview(self._tree, [], ["dia", "espacio", "materia", "profesor", "inicio", "fin"])
            return
        self._horarios_actuales = self.horario_service.obtener_por_division(self._selected_division.id)
        filas = [
            {
                "id": registro.get("id"),
                "dia": registro.get("dia", ""),
                "espacio": registro.get("espacio", ""),
                "materia": registro.get("materia", ""),
                "profesor": registro.get("profesor", ""),
                "inicio": registro.get("hora_inicio", ""),
                "fin": registro.get("hora_fin", ""),
            }
            for registro in self._horarios_actuales
        ]
        recargar_treeview(self._tree, filas, ["dia", "espacio", "materia", "profesor", "inicio", "fin"])
        self._selected_horario_id = None

    def _on_tree_select(self, _event: tk.Event) -> None:
        seleccion = get_first_selection(self._tree)
        self._selected_horario_id = int(seleccion) if seleccion else None

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _resolve_turno(self, nombre: str) -> Turno | None:
        return next((turno for turno in self._turnos if (turno.nombre or "") == nombre), None)

    def _lookup_plan_nombre(self, plan_id: int | None) -> str:
        if plan_id is None:
            return ""
        plan = self._planes_por_id.get(plan_id)
        return plan.nombre or "" if plan else ""

    def _lookup_anio_nombre(self, division: Division) -> str:
        if division.anio_id is None or division.plan_id is None:
            return ""
        anios = self._anios_plan.get(division.plan_id)
        if anios is None:
            anios = self.anio_service.listar_por_plan(division.plan_id)
            self._anios_plan[division.plan_id] = anios
        registro = next((anio for anio in anios if anio.id == division.anio_id), None)
        return registro.nombre or "" if registro else ""

    # ------------------------------------------------------------------
    # Acciones
    # ------------------------------------------------------------------
    def _agregar(self) -> None:
        division = self._selected_division
        if division is None or division.id is None:
            self.show_error("Seleccione una división para asignar un horario.")
            return
        dia = self._dia_var.get()
        espacio = self._espacio_var.get()
        materia_id = self._materia_map.get(self._materia_var.get()) if hasattr(self, "_materia_map") else None
        profesor_id = self._profesor_map.get(self._profesor_var.get()) if hasattr(self, "_profesor_map") else None
        try:
            self.horario_service.crear_para_division(
                division.id,
                dia,
                espacio,
                hora_inicio=self._hora_inicio_var.get().strip() or None,
                hora_fin=self._hora_fin_var.get().strip() or None,
                materia_id=materia_id,
                profesor_id=profesor_id,
                turno_id=division.turno_id,
            )
        except ValidationError as exc:
            self.show_error(str(exc))
            return
        except Exception as exc:  # pragma: no cover
            self.show_error(str(exc))
            return
        self.show_info("Horario asignado correctamente.")
        self._reload_horarios()

    def _eliminar(self) -> None:
        if self._selected_horario_id is None:
            self.show_error("Seleccione un horario para eliminar.")
            return
        if not self.ask_yes_no("¿Desea eliminar el horario seleccionado?"):
            return
        try:
            self.horario_service.eliminar(self._selected_horario_id)
        except Exception as exc:  # pragma: no cover
            self.show_error(str(exc))
            return
        self.show_info("Horario eliminado.")
        self._reload_horarios()


class HorariosProfesorView(BaseView):
    """Permite administrar horarios desde la perspectiva del profesor."""

    def __init__(self, master: tk.Misc, app: MainWindow) -> None:  # type: ignore[override]
        super().__init__(master, app, title="Gestión de horarios por profesor")
        self.horario_service = app.horario_service
        self.profesor_service = app.profesor_service
        self.turno_service = app.turno_service
        self.division_service = app.division_service
        self.plan_service = app.plan_service

        self._profesores: list[Profesor] = []
        self._turnos: list[Turno] = []
        self._divisiones: list[Division] = []
        self._divisiones_por_turno: dict[int, list[Division]] = {}
        self._horarios_actuales: list[dict] = []
        self._materias_por_profesor: dict[int, list[dict]] = {}
        self._division_map: dict[str, Division | None] = {"": None}
        self._materia_map: dict[str, int | None] = {}

        self._selected_profesor: Profesor | None = None
        self._selected_turno: Turno | None = None
        self._selected_horario_id: int | None = None

        self._profesor_var = tk.StringVar()
        self._turno_var = tk.StringVar()
        self._dia_var = tk.StringVar(value=DIAS_SEMANA[0])
        self._espacio_var = tk.StringVar(value=_ESPACIOS[0])
        self._division_var = tk.StringVar()
        self._materia_var = tk.StringVar()
        self._hora_inicio_var = tk.StringVar()
        self._hora_fin_var = tk.StringVar()

        self._build_layout()
        self.refresh()

    def _build_layout(self) -> None:
        selector = ttk.Frame(self)
        selector.pack(fill="x", pady=(0, 10))

        ttk.Label(selector, text="Profesor:").grid(row=0, column=0, padx=5, pady=2)
        self._combo_profesor = ttk.Combobox(selector, textvariable=self._profesor_var, state="readonly", width=30)
        self._combo_profesor.grid(row=0, column=1, padx=5, pady=2)
        self._combo_profesor.bind("<<ComboboxSelected>>", self._on_profesor_changed)

        ttk.Label(selector, text="Turno:").grid(row=0, column=2, padx=5, pady=2)
        self._combo_turno = ttk.Combobox(selector, textvariable=self._turno_var, state="readonly", width=20)
        self._combo_turno.grid(row=0, column=3, padx=5, pady=2)
        self._combo_turno.bind("<<ComboboxSelected>>", self._on_turno_changed)

        tabla = ttk.Frame(self)
        tabla.pack(fill="both", expand=True)
        self._tree = crear_treeview(
            tabla,
            ("dia", "espacio", "division", "materia", "inicio", "fin"),
            ("Día", "Espacio", "División", "Materia", "Inicio", "Fin"),
            height=12,
        )
        self._tree.bind("<<TreeviewSelect>>", self._on_tree_select)

        detalle = ttk.LabelFrame(self, text="Nueva asignación")
        detalle.pack(fill="x", pady=12)

        ttk.Label(detalle, text="Día:").grid(row=0, column=0, padx=5, pady=3, sticky="e")
        self._combo_dia = ttk.Combobox(detalle, textvariable=self._dia_var, values=DIAS_SEMANA, state="readonly", width=18)
        self._combo_dia.grid(row=0, column=1, padx=5, pady=3, sticky="w")

        ttk.Label(detalle, text="Espacio:").grid(row=0, column=2, padx=5, pady=3, sticky="e")
        self._combo_espacio = ttk.Combobox(detalle, textvariable=self._espacio_var, values=_ESPACIOS, state="readonly", width=8)
        self._combo_espacio.grid(row=0, column=3, padx=5, pady=3, sticky="w")

        ttk.Label(detalle, text="División (opcional):").grid(row=1, column=0, padx=5, pady=3, sticky="e")
        self._combo_division = ttk.Combobox(detalle, textvariable=self._division_var, state="readonly", width=30)
        self._combo_division.grid(row=1, column=1, padx=5, pady=3, sticky="w")

        ttk.Label(detalle, text="Materia (opcional):").grid(row=1, column=2, padx=5, pady=3, sticky="e")
        self._combo_materia = ttk.Combobox(detalle, textvariable=self._materia_var, state="readonly", width=28)
        self._combo_materia.grid(row=1, column=3, padx=5, pady=3, sticky="w")

        ttk.Label(detalle, text="Hora inicio:").grid(row=2, column=0, padx=5, pady=3, sticky="e")
        self._entry_inicio = ttk.Entry(detalle, textvariable=self._hora_inicio_var, width=12)
        self._entry_inicio.grid(row=2, column=1, padx=5, pady=3, sticky="w")

        ttk.Label(detalle, text="Hora fin:").grid(row=2, column=2, padx=5, pady=3, sticky="e")
        self._entry_fin = ttk.Entry(detalle, textvariable=self._hora_fin_var, width=12)
        self._entry_fin.grid(row=2, column=3, padx=5, pady=3, sticky="w")

        botones = ttk.Frame(self)
        botones.pack(pady=6)
        ttk.Button(botones, text="Agregar", command=self._agregar).grid(row=0, column=0, padx=5)
        ttk.Button(botones, text="Eliminar", command=self._eliminar).grid(row=0, column=1, padx=5)

        bind_enter(self._entry_inicio, self._agregar)
        focus_entry(self._entry_inicio)

    # ------------------------------------------------------------------
    # Datos y refresco
    # ------------------------------------------------------------------
    def refresh(self) -> None:
        self._profesores = sorted(self.profesor_service.listar(), key=lambda p: (p.nombre or "").lower())
        self._turnos = sorted(self.turno_service.listar(), key=lambda t: (t.nombre or "").lower())
        self._divisiones = sorted(self.division_service.listar(), key=lambda d: (d.nombre or "").lower())
        self._divisiones_por_turno = {}
        for division in self._divisiones:
            self._divisiones_por_turno.setdefault(division.turno_id or 0, []).append(division)
        for divisiones in self._divisiones_por_turno.values():
            divisiones.sort(key=lambda d: (d.nombre or "").lower())

        profesor_nombres = [profesor.nombre or "" for profesor in self._profesores]
        self._combo_profesor["values"] = profesor_nombres
        if profesor_nombres:
            self._profesor_var.set(profesor_nombres[0])
        else:
            self._profesor_var.set("")

        turno_nombres = [turno.nombre or "" for turno in self._turnos]
        self._combo_turno["values"] = turno_nombres
        if turno_nombres:
            self._turno_var.set(turno_nombres[0])
        else:
            self._turno_var.set("")
        self._selected_turno = self._resolve_turno(self._turno_var.get())

        self._on_profesor_changed()
        self.set_status("Horarios por profesor actualizados")

    # ------------------------------------------------------------------
    # Eventos
    # ------------------------------------------------------------------
    def _on_profesor_changed(self, _event: tk.Event | None = None) -> None:
        self._selected_profesor = self._resolve_profesor(self._profesor_var.get())
        self._materias_por_profesor_cache()
        self._reload_materias()
        self._reload_divisiones()
        self._reload_horarios()

    def _on_turno_changed(self, _event: tk.Event | None = None) -> None:
        self._selected_turno = self._resolve_turno(self._turno_var.get())
        self._reload_divisiones()
        self._reload_horarios()

    def _on_tree_select(self, _event: tk.Event) -> None:
        seleccion = get_first_selection(self._tree)
        self._selected_horario_id = int(seleccion) if seleccion else None

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _resolve_profesor(self, nombre: str) -> Profesor | None:
        return next((prof for prof in self._profesores if (prof.nombre or "") == nombre), None)

    def _resolve_turno(self, nombre: str) -> Turno | None:
        return next((turno for turno in self._turnos if (turno.nombre or "") == nombre), None)

    def _materias_por_profesor_cache(self) -> None:
        if self._selected_profesor is None or self._selected_profesor.id is None:
            return
        profesor_id = self._selected_profesor.id
        if profesor_id not in self._materias_por_profesor:
            self._materias_por_profesor[profesor_id] = self.profesor_service.obtener_banca(profesor_id)

    def _reload_materias(self) -> None:
        if self._selected_profesor is None or self._selected_profesor.id is None:
            self._combo_materia["values"] = [""]
            self._materia_map = {}
            self._materia_var.set("")
            return
        registros = self._materias_por_profesor.get(self._selected_profesor.id, [])
        self._materia_map = {registro.get("materia", ""): registro.get("materia_id") or registro.get("id") for registro in registros}
        valores = sorted([nombre for nombre in self._materia_map if nombre], key=str.lower)
        valores.insert(0, "")
        self._combo_materia["values"] = valores
        if self._materia_var.get() not in valores:
            self._materia_var.set("")

    def _reload_divisiones(self) -> None:
        turno_id = self._selected_turno.id if self._selected_turno and self._selected_turno.id is not None else None
        opciones = [""]
        self._division_map = {"": None}
        if turno_id is not None:
            for division in self._divisiones_por_turno.get(turno_id, []):
                etiqueta = division.nombre or ""
                opciones.append(etiqueta)
                self._division_map[etiqueta] = division
        self._combo_division["values"] = opciones
        if self._division_var.get() not in opciones:
            self._division_var.set("")

    def _reload_horarios(self) -> None:
        if (
            self._selected_profesor is None
            or self._selected_profesor.id is None
            or self._selected_turno is None
            or self._selected_turno.id is None
        ):
            self._horarios_actuales = []
            recargar_treeview(self._tree, [], ["dia", "espacio", "division", "materia", "inicio", "fin"])
            return
        self._horarios_actuales = self.horario_service.obtener_por_profesor(
            self._selected_profesor.id,
            self._selected_turno.id,
        )
        filas = [
            {
                "id": registro.get("id"),
                "dia": registro.get("dia", ""),
                "espacio": registro.get("espacio", ""),
                "division": registro.get("division", ""),
                "materia": registro.get("materia", ""),
                "inicio": registro.get("hora_inicio", ""),
                "fin": registro.get("hora_fin", ""),
            }
            for registro in self._horarios_actuales
        ]
        recargar_treeview(self._tree, filas, ["dia", "espacio", "division", "materia", "inicio", "fin"])
        self._selected_horario_id = None

    # ------------------------------------------------------------------
    # Acciones
    # ------------------------------------------------------------------
    def _agregar(self) -> None:
        if self._selected_profesor is None or self._selected_profesor.id is None:
            self.show_error("Seleccione un profesor.")
            return
        if self._selected_turno is None or self._selected_turno.id is None:
            self.show_error("Seleccione un turno.")
            return
        division = self._division_map.get(self._division_var.get()) if hasattr(self, "_division_map") else None
        division_id = division.id if division and division.id is not None else None
        materia_id = None
        if hasattr(self, "_materia_map"):
            materia_id = self._materia_map.get(self._materia_var.get())
        try:
            self.horario_service.crear_para_profesor(
                self._selected_profesor.id,
                self._selected_turno.id,
                self._dia_var.get(),
                self._espacio_var.get(),
                hora_inicio=self._hora_inicio_var.get().strip() or None,
                hora_fin=self._hora_fin_var.get().strip() or None,
                division_id=division_id,
                materia_id=materia_id,
            )
        except ValidationError as exc:
            self.show_error(str(exc))
            return
        except Exception as exc:  # pragma: no cover
            self.show_error(str(exc))
            return
        self.show_info("Horario asignado correctamente.")
        self._reload_horarios()

    def _eliminar(self) -> None:
        if self._selected_horario_id is None:
            self.show_error("Seleccione un horario para eliminar.")
            return
        if not self.ask_yes_no("¿Desea eliminar el horario seleccionado?"):
            return
        try:
            self.horario_service.eliminar(self._selected_horario_id)
        except Exception as exc:  # pragma: no cover
            self.show_error(str(exc))
            return
        self.show_info("Horario eliminado.")
        self._reload_horarios()


def build_horarios_curso_view(container: tk.Misc, app: MainWindow) -> HorariosCursoView:
    """Factory para registrar la vista de horarios por curso."""
    return HorariosCursoView(container, app)


def build_horarios_profesor_view(container: tk.Misc, app: MainWindow) -> HorariosProfesorView:
    """Factory para registrar la vista de horarios por profesor."""
    return HorariosProfesorView(container, app)
