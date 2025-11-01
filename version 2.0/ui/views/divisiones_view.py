"""Vista para gestionar divisiones/cursos finales (turno + plan + año)."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from models.division import Division
from models.plan import Plan
from models.anio import Anio
from models.turno import Turno
from services import ValidationError
from ui.components import crear_treeview, recargar_treeview
from ui.main_window import MainWindow
from ui.views.base import BaseView
from utils import bind_enter, focus_entry, get_first_selection


class DivisionesView(BaseView):
    """Permite crear y administrar divisiones académicas."""

    def __init__(self, master: tk.Misc, app: MainWindow) -> None:  # type: ignore[override]
        super().__init__(master, app, title="Gestión de divisiones")
        self.division_service = app.division_service
        self.plan_service = app.plan_service
        self.anio_service = app.anio_service
        self.turno_service = app.turno_service

        self._divisiones: list[Division] = []
        self._planes: list[Plan] = []
        self._anios_por_plan: dict[int, list[Anio]] = {}
        self._turnos: list[Turno] = []
        self._selected_id: int | None = None

        self._filtro_turno = tk.StringVar(value="Todos")
        self._filtro_plan = tk.StringVar(value="Todos")
        self._nombre_var = tk.StringVar()
        self._turno_var = tk.StringVar()
        self._plan_var = tk.StringVar()
        self._anio_var = tk.StringVar()

        self._build_layout()
        self.refresh()

    # ------------------------------------------------------------------
    # Construcción de UI
    # ------------------------------------------------------------------
    def _build_layout(self) -> None:
        filtros = ttk.Frame(self)
        filtros.pack(fill="x", pady=(0, 10))

        ttk.Label(filtros, text="Filtro turno:").grid(row=0, column=0, padx=5, pady=2)
        self._combo_filtro_turno = ttk.Combobox(filtros, textvariable=self._filtro_turno, state="readonly", width=20)
        self._combo_filtro_turno.grid(row=0, column=1, padx=5, pady=2)
        self._combo_filtro_turno.bind("<<ComboboxSelected>>", lambda _e: self._apply_filters())

        ttk.Label(filtros, text="Filtro plan:").grid(row=0, column=2, padx=5, pady=2)
        self._combo_filtro_plan = ttk.Combobox(filtros, textvariable=self._filtro_plan, state="readonly", width=20)
        self._combo_filtro_plan.grid(row=0, column=3, padx=5, pady=2)
        self._combo_filtro_plan.bind("<<ComboboxSelected>>", lambda _e: self._apply_filters())

        tabla = ttk.Frame(self)
        tabla.pack(fill="both", expand=True)
        self._tree = crear_treeview(
            tabla,
            ("nombre", "turno", "plan", "anio"),
            ("División", "Turno", "Plan", "Curso"),
            height=12,
        )
        self._tree.bind("<<TreeviewSelect>>", self._on_tree_select)

        formulario = ttk.LabelFrame(self, text="Datos de la división")
        formulario.pack(fill="x", pady=12)

        ttk.Label(formulario, text="Nombre:").grid(row=0, column=0, padx=5, pady=4, sticky="e")
        self._entry_nombre = ttk.Entry(formulario, textvariable=self._nombre_var, width=30)
        self._entry_nombre.grid(row=0, column=1, padx=5, pady=4, sticky="w")

        ttk.Label(formulario, text="Turno:").grid(row=1, column=0, padx=5, pady=4, sticky="e")
        self._combo_turno = ttk.Combobox(formulario, textvariable=self._turno_var, state="readonly", width=28)
        self._combo_turno.grid(row=1, column=1, padx=5, pady=4, sticky="w")
        self._combo_turno.bind("<<ComboboxSelected>>", self._on_form_plan_reset)

        ttk.Label(formulario, text="Plan:").grid(row=2, column=0, padx=5, pady=4, sticky="e")
        self._combo_plan = ttk.Combobox(formulario, textvariable=self._plan_var, state="readonly", width=28)
        self._combo_plan.grid(row=2, column=1, padx=5, pady=4, sticky="w")
        self._combo_plan.bind("<<ComboboxSelected>>", self._on_form_plan_change)

        ttk.Label(formulario, text="Curso/Año:").grid(row=3, column=0, padx=5, pady=4, sticky="e")
        self._combo_anio = ttk.Combobox(formulario, textvariable=self._anio_var, state="readonly", width=28)
        self._combo_anio.grid(row=3, column=1, padx=5, pady=4, sticky="w")

        botones = ttk.Frame(self)
        botones.pack(pady=6)
        ttk.Button(botones, text="Agregar", command=self._agregar).grid(row=0, column=0, padx=5)
        ttk.Button(botones, text="Editar", command=self._editar).grid(row=0, column=1, padx=5)
        ttk.Button(botones, text="Eliminar", command=self._eliminar).grid(row=0, column=2, padx=5)

        bind_enter(self._entry_nombre, self._agregar)
        focus_entry(self._entry_nombre)

    # ------------------------------------------------------------------
    # Datos y refresco
    # ------------------------------------------------------------------
    def refresh(self) -> None:
        self._divisiones = self.division_service.listar()
        self._turnos = sorted(self.turno_service.listar(), key=lambda t: (t.nombre or "").lower())
        self._planes = sorted(self.plan_service.listar(), key=lambda p: (p.nombre or "").lower())
        self._anios_por_plan = {
            plan.id or 0: self.anio_service.listar_por_plan(plan.id or 0)
            for plan in self._planes
        }
        self._selected_id = None
        self._nombre_var.set("")
        self._turno_var.set("")
        self._plan_var.set("")
        self._anio_var.set("")

        self._populate_filters()
        self._populate_form_comboboxes()
        self._apply_filters()
        self.set_status("Divisiones actualizadas")

    def _populate_filters(self) -> None:
        turno_values = ["Todos"] + [turno.nombre or "" for turno in self._turnos]
        plan_values = ["Todos"] + [plan.nombre or "" for plan in self._planes]
        self._combo_filtro_turno["values"] = turno_values
        self._combo_filtro_plan["values"] = plan_values
        if self._filtro_turno.get() not in turno_values:
            self._filtro_turno.set("Todos")
        if self._filtro_plan.get() not in plan_values:
            self._filtro_plan.set("Todos")

    def _populate_form_comboboxes(self) -> None:
        self._combo_turno["values"] = [turno.nombre or "" for turno in self._turnos]
        self._combo_plan["values"] = [plan.nombre or "" for plan in self._planes]
        self._combo_anio["values"] = []

    # ------------------------------------------------------------------
    # Filtros y selección
    # ------------------------------------------------------------------
    def _apply_filters(self) -> None:
        turno_filtro = self._filtro_turno.get().strip().lower()
        plan_filtro = self._filtro_plan.get().strip().lower()
        visibles = list(self._divisiones)
        if turno_filtro and turno_filtro != "todos":
            visibles = [div for div in visibles if self._lookup_turno_nombre(div.turno_id).lower() == turno_filtro]
        if plan_filtro and plan_filtro != "todos":
            visibles = [div for div in visibles if self._lookup_plan_nombre(div.plan_id).lower() == plan_filtro]

        filas = [
            {
                "id": division.id,
                "nombre": division.nombre or "",
                "turno": self._lookup_turno_nombre(division.turno_id),
                "plan": self._lookup_plan_nombre(division.plan_id),
                "anio": self._lookup_anio_nombre(division.plan_id, division.anio_id),
            }
            for division in visibles
        ]
        recargar_treeview(self._tree, filas, ["nombre", "turno", "plan", "anio"])

    def _lookup_turno_nombre(self, turno_id: int | None) -> str:
        turno = next((t for t in self._turnos if t.id == turno_id), None)
        return turno.nombre or "" if turno else ""

    def _lookup_plan_nombre(self, plan_id: int | None) -> str:
        plan = next((p for p in self._planes if p.id == plan_id), None)
        return plan.nombre or "" if plan else ""

    def _lookup_anio_nombre(self, plan_id: int | None, anio_id: int | None) -> str:
        if plan_id is None:
            return ""
        registros = self._anios_por_plan.get(plan_id, [])
        anio = next((a for a in registros if a.id == anio_id), None)
        return anio.nombre or "" if anio else ""

    def _on_tree_select(self, _event: tk.Event) -> None:
        seleccion = get_first_selection(self._tree)
        if seleccion is None:
            self._selected_id = None
            self._nombre_var.set("")
            self._turno_var.set("")
            self._plan_var.set("")
            self._anio_var.set("")
            return
        self._selected_id = int(seleccion)
        division = next((d for d in self._divisiones if d.id == self._selected_id), None)
        if division is None:
            return
        self._nombre_var.set(division.nombre or "")
        self._turno_var.set(self._lookup_turno_nombre(division.turno_id))
        self._plan_var.set(self._lookup_plan_nombre(division.plan_id))
        self._update_anio_combobox_for_plan(division.plan_id)
        self._anio_var.set(self._lookup_anio_nombre(division.plan_id, division.anio_id))

    def _on_form_plan_reset(self, _event: tk.Event) -> None:
        # Si cambia el turno no reseteamos plan ni año, pero limpiamos selección actual
        self._selected_id = None

    def _on_form_plan_change(self, _event: tk.Event) -> None:
        plan_nombre = self._plan_var.get()
        plan = next((p for p in self._planes if (p.nombre or "") == plan_nombre), None)
        plan_id = plan.id if plan and plan.id is not None else None
        self._update_anio_combobox_for_plan(plan_id)

    def _update_anio_combobox_for_plan(self, plan_id: int | None) -> None:
        if plan_id is None:
            self._combo_anio["values"] = []
            self._anio_var.set("")
            return
        registros = self._anios_por_plan.get(plan_id, [])
        opciones = [anio.nombre or "" for anio in registros]
        self._combo_anio["values"] = opciones
        if self._anio_var.get() not in opciones:
            self._anio_var.set("")

    # ------------------------------------------------------------------
    # Acciones CRUD
    # ------------------------------------------------------------------
    def _resolve_turno(self) -> Turno | None:
        nombre = self._turno_var.get()
        return next((turno for turno in self._turnos if (turno.nombre or "") == nombre), None)

    def _resolve_plan(self) -> Plan | None:
        nombre = self._plan_var.get()
        return next((plan for plan in self._planes if (plan.nombre or "") == nombre), None)

    def _resolve_anio(self, plan_id: int | None) -> Anio | None:
        nombre = self._anio_var.get()
        registros = self._anios_por_plan.get(plan_id or 0, [])
        return next((anio for anio in registros if (anio.nombre or "") == nombre), None)

    def _agregar(self) -> None:
        turno = self._resolve_turno()
        plan = self._resolve_plan()
        anio = self._resolve_anio(plan.id if plan else None)
        if turno is None or plan is None or anio is None:
            self.show_error("Seleccione turno, plan y curso válidos.")
            return
        nombre = self._nombre_var.get()
        try:
            self.division_service.crear(nombre, turno.id, plan.id, anio.id)
        except ValidationError as exc:
            self.show_error(str(exc))
            return
        except Exception as exc:  # pragma: no cover
            self.show_error(str(exc))
            return
        self.show_info("División creada correctamente.")
        self.refresh()

    def _editar(self) -> None:
        if self._selected_id is None:
            self.show_error("Seleccione una división para editar.")
            return
        nombre = self._nombre_var.get()
        try:
            self.division_service.actualizar_nombre(self._selected_id, nombre)
        except ValidationError as exc:
            self.show_error(str(exc))
            return
        except Exception as exc:  # pragma: no cover
            self.show_error(str(exc))
            return
        self.show_info("División actualizada correctamente.")
        self.refresh()

    def _eliminar(self) -> None:
        if self._selected_id is None:
            self.show_error("Seleccione una división para eliminar.")
            return
        if not self.ask_yes_no("¿Desea eliminar la división seleccionada?"):
            return
        try:
            self.division_service.eliminar(self._selected_id)
        except ValidationError as exc:
            self.show_error(str(exc))
            return
        except Exception as exc:  # pragma: no cover
            self.show_error(str(exc))
            return
        self.show_info("División eliminada.")
        self.refresh()


def build_divisiones_view(container: tk.Misc, app: MainWindow) -> DivisionesView:
    """Factory para registrar la vista en la ventana principal."""
    return DivisionesView(container, app)
