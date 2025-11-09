"""Vista para gestionar planes de estudio."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from models.plan import Plan
from models.materia import Materia
from services import ValidationError
from ui.components import crear_treeview, recargar_treeview
from ui.main_window import MainWindow
from ui.views.base import BaseView
from utils import bind_enter, center_window, focus_entry, get_first_selection


class PlanesView(BaseView):
    """Permite gestionar planes de estudio y asociar sus materias."""

    def __init__(self, master: tk.Misc, app: MainWindow) -> None:  # type: ignore[override]
        super().__init__(master, app, title="Gestión de planes de estudio")
        self.service = app.plan_service
        self.materia_service = app.materia_service

        self._planes: list[Plan] = []
        self._materias: list[Materia] = []
        self._selected_id: int | None = None

        self._filter_var = tk.StringVar()
        self._nombre_var = tk.StringVar()

        self._build_layout()
        self.refresh()

    # ------------------------------------------------------------------
    # Construcción de UI
    # ------------------------------------------------------------------
    def _build_layout(self) -> None:
        resumen = ttk.Frame(self)
        resumen.pack(fill="x", pady=(0, 10))
        self._total_label = ttk.Label(resumen, text="Total de planes: 0")
        self._total_label.pack(side="left")

        filtro = ttk.Frame(self)
        filtro.pack(fill="x", pady=(0, 12))
        ttk.Label(filtro, text="Filtro por nombre:").grid(row=0, column=0, padx=5, pady=2)
        ttk.Entry(filtro, textvariable=self._filter_var, width=30).grid(row=0, column=1, padx=5, pady=2)

        tabla = ttk.Frame(self)
        tabla.pack(fill="both", expand=True)
        self._tree = crear_treeview(tabla, ("nombre",), ("Nombre",), height=12)
        self._tree.bind("<<TreeviewSelect>>", self._on_tree_select)

        formulario = ttk.Frame(self)
        formulario.pack(fill="x", pady=12)
        ttk.Label(formulario, text="Nombre:").grid(row=0, column=0, padx=5, pady=2, sticky="e")
        self._nombre_entry = ttk.Entry(formulario, textvariable=self._nombre_var, width=40)
        self._nombre_entry.grid(row=0, column=1, padx=5, pady=2, sticky="w")

        botones = ttk.Frame(self)
        botones.pack(pady=6)
        ttk.Button(botones, text="Agregar", command=self._agregar).grid(row=0, column=0, padx=5)
        ttk.Button(botones, text="Editar", command=self._editar).grid(row=0, column=1, padx=5)
        ttk.Button(botones, text="Eliminar", command=self._eliminar).grid(row=0, column=2, padx=5)
        ttk.Button(botones, text="Materias del plan", command=self._abrir_asignacion_materias).grid(row=0, column=3, padx=5)

        bind_enter(self._nombre_entry, self._agregar)
        focus_entry(self._nombre_entry)
        self._filter_var.trace_add("write", lambda *_: self._apply_filter())

    # ------------------------------------------------------------------
    # Datos y refresco
    # ------------------------------------------------------------------
    def refresh(self) -> None:
        self._planes = sorted(self.service.listar(), key=lambda plan: (plan.nombre or "").lower())
        self._materias = sorted(self.materia_service.listar(), key=lambda materia: (materia.nombre or "").lower())
        self._selected_id = None
        self._nombre_var.set("")
        self._apply_filter()
        self.set_status("Planes actualizados")

    def _apply_filter(self) -> None:
        filtro = self._filter_var.get().strip().lower()
        if filtro:
            visibles = [plan for plan in self._planes if filtro in (plan.nombre or "").lower()]
        else:
            visibles = list(self._planes)

        filas = [
            {
                "id": plan.id,
                "nombre": plan.nombre or "",
            }
            for plan in visibles
        ]
        recargar_treeview(self._tree, filas, ["nombre"])
        self._total_label.config(text=f"Total de planes: {len(visibles)}")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _get_plan(self) -> Plan | None:
        if self._selected_id is None:
            return None
        return next((plan for plan in self._planes if plan.id == self._selected_id), None)

    # ------------------------------------------------------------------
    # Eventos
    # ------------------------------------------------------------------
    def _on_tree_select(self, _event: tk.Event) -> None:
        seleccion = get_first_selection(self._tree)
        if seleccion is None:
            self._selected_id = None
            self._nombre_var.set("")
            return

        self._selected_id = int(seleccion)
        plan = self._get_plan()
        if plan:
            self._nombre_var.set(plan.nombre or "")

    # ------------------------------------------------------------------
    # Acciones CRUD
    # ------------------------------------------------------------------
    def _agregar(self) -> None:
        nombre = self._nombre_var.get()
        try:
            self.service.crear(nombre)
        except ValidationError as exc:
            self.show_error(str(exc))
            return
        except Exception as exc:  # pragma: no cover
            self.show_error(str(exc))
            return

        self.show_info("Plan creado correctamente.")
        self.refresh()

    def _editar(self) -> None:
        if self._selected_id is None:
            self.show_error("Seleccione un plan para editar.")
            return
        nombre = self._nombre_var.get()
        try:
            self.service.actualizar(self._selected_id, nombre)
        except ValidationError as exc:
            self.show_error(str(exc))
            return
        except Exception as exc:  # pragma: no cover
            self.show_error(str(exc))
            return

        self.show_info("Plan actualizado correctamente.")
        self.refresh()

    def _eliminar(self) -> None:
        if self._selected_id is None:
            self.show_error("Seleccione un plan para eliminar.")
            return
        if not self.ask_yes_no("¿Desea eliminar el plan seleccionado?"):
            return
        try:
            self.service.eliminar(self._selected_id)
        except ValidationError as exc:
            self.show_error(str(exc))
            return
        except Exception as exc:  # pragma: no cover
            self.show_error(str(exc))
            return

        self.show_info("Plan eliminado.")
        self.refresh()

    # ------------------------------------------------------------------
    # Gestión de materias asociadas
    # ------------------------------------------------------------------
    def _abrir_asignacion_materias(self) -> None:
        plan = self._get_plan()
        if plan is None or plan.id is None:
            self.show_error("Seleccione un plan para gestionar sus materias.")
            return

        dialog = tk.Toplevel(self)
        dialog.title("Materias del plan")
        dialog.configure(padx=12, pady=12)
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()
        dialog.focus_set()
        center_window(dialog, 520, 480)

        ttk.Label(
            dialog,
            text=f"Materias asociadas a {plan.nombre or ''}",
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="w", pady=(0, 8))

        tabla_frame = ttk.Frame(dialog)
        tabla_frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(tabla_frame, columns=("nombre", "horas"), show="headings", height=10)
        tree.heading("nombre", text="Obligación")
        tree.heading("horas", text="Horas semanales")
        tree.column("nombre", anchor="w", width=320)
        tree.column("horas", anchor="center", width=120)
        tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        tabla_frame.grid_rowconfigure(0, weight=1)
        tabla_frame.grid_columnconfigure(0, weight=1)

        def cargar_asignadas() -> None:
            registros = self.service.obtener_materias(plan.id or 0)
            filas = [
                {
                    "id": registro.get("id"),
                    "nombre": registro.get("nombre", ""),
                    "horas": registro.get("horas_semanales", 0),
                }
                for registro in registros
            ]
            recargar_treeview(tree, filas, ["nombre", "horas"])

        def materias_disponibles() -> list[str]:
            asignadas = {registro.get("id") for registro in self.service.obtener_materias(plan.id or 0)}
            return sorted(
                [materia.nombre or "" for materia in self._materias if materia.id not in asignadas],
                key=str.lower,
            )

        cargar_asignadas()

        formulario = ttk.Frame(dialog)
        formulario.pack(fill="x", pady=10)
        ttk.Label(formulario, text="Agregar obligación:").grid(row=0, column=0, padx=5, pady=2)
        materia_var = tk.StringVar()
        cb_materia = ttk.Combobox(
            formulario,
            textvariable=materia_var,
            values=materias_disponibles(),
            state="readonly",
            width=35,
        )
        cb_materia.grid(row=0, column=1, padx=5, pady=2, sticky="w")

        botones = ttk.Frame(dialog)
        botones.pack(pady=5)

        def agregar_materia() -> None:
            nombre_materia = materia_var.get()
            materia = next((m for m in self._materias if (m.nombre or "") == nombre_materia), None)
            if materia is None or materia.id is None:
                self.show_error("Seleccione una obligación válida.")
                return
            try:
                self.service.agregar_materia(plan.id, materia.id)
            except ValidationError as exc:
                self.show_error(str(exc))
                return
            except Exception as exc:  # pragma: no cover
                self.show_error(str(exc))
                return
            materia_var.set("")
            cargar_asignadas()
            cb_materia.config(values=materias_disponibles())

        def quitar_materia() -> None:
            seleccion = get_first_selection(tree)
            if seleccion is None:
                self.show_error("Seleccione una obligación para quitar.")
                return
            if not self.ask_yes_no("¿Quitar la obligación seleccionada del plan?"):
                return
            try:
                self.service.quitar_materia(plan.id, int(seleccion))
            except Exception as exc:  # pragma: no cover
                self.show_error(str(exc))
                return
            cargar_asignadas()
            cb_materia.config(values=materias_disponibles())

        ttk.Button(botones, text="Agregar obligación", command=agregar_materia).grid(row=0, column=0, padx=5)
        ttk.Button(botones, text="Quitar obligación", command=quitar_materia).grid(row=0, column=1, padx=5)

        bind_enter(cb_materia, agregar_materia)
        dialog.bind("<Escape>", lambda _event: dialog.destroy())


def build_planes_view(container: tk.Misc, app: MainWindow) -> PlanesView:
    """Factory para registrar la vista de planes."""
    return PlanesView(container, app)
