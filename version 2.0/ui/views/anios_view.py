"""Vista para gestionar cursos/años de cada plan de estudio."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from models.anio import Anio
from models.plan import Plan
from services import ValidationError
from ui.components import crear_treeview, recargar_treeview
from ui.main_window import MainWindow
from ui.views.base import BaseView
from utils import bind_enter, center_window, focus_entry, get_first_selection


class AniosView(BaseView):
    """Permite administrar los cursos asociados a un plan y sus materias."""

    def __init__(self, master: tk.Misc, app: MainWindow) -> None:  # type: ignore[override]
        super().__init__(master, app, title="Gestión de cursos por plan")
        self.anio_service = app.anio_service
        self.plan_service = app.plan_service

        self._planes: list[Plan] = []
        self._anios: list[Anio] = []
        self._selected_plan_id: int | None = None
        self._selected_anio_id: int | None = None

        self._plan_var = tk.StringVar()
        self._nombre_var = tk.StringVar()

        self._build_layout()
        self.refresh()

    # ------------------------------------------------------------------
    # Construcción de UI
    # ------------------------------------------------------------------
    def _build_layout(self) -> None:
        selector = ttk.Frame(self)
        selector.pack(fill="x", pady=(0, 10))
        ttk.Label(selector, text="Plan de estudio:").grid(row=0, column=0, padx=5, pady=2, sticky="e")
        self._plan_combobox = ttk.Combobox(selector, textvariable=self._plan_var, state="readonly", width=40)
        self._plan_combobox.grid(row=0, column=1, padx=5, pady=2, sticky="w")
        self._plan_combobox.bind("<<ComboboxSelected>>", self._on_plan_selected)

        resumen = ttk.Frame(self)
        resumen.pack(fill="x", pady=(0, 8))
        self._total_label = ttk.Label(resumen, text="Total de cursos: 0")
        self._total_label.pack(side="left")

        tabla = ttk.Frame(self)
        tabla.pack(fill="both", expand=True)
        self._tree = crear_treeview(tabla, ("nombre",), ("Nombre del curso",), height=12)
        self._tree.bind("<<TreeviewSelect>>", self._on_tree_select)

        formulario = ttk.Frame(self)
        formulario.pack(fill="x", pady=12)
        ttk.Label(formulario, text="Nombre del curso:").grid(row=0, column=0, padx=5, pady=2, sticky="e")
        self._nombre_entry = ttk.Entry(formulario, textvariable=self._nombre_var, width=40)
        self._nombre_entry.grid(row=0, column=1, padx=5, pady=2, sticky="w")

        botones = ttk.Frame(self)
        botones.pack(pady=6)
        ttk.Button(botones, text="Agregar", command=self._agregar).grid(row=0, column=0, padx=5)
        ttk.Button(botones, text="Editar", command=self._editar).grid(row=0, column=1, padx=5)
        ttk.Button(botones, text="Eliminar", command=self._eliminar).grid(row=0, column=2, padx=5)
        ttk.Button(botones, text="Materias del curso", command=self._abrir_asignacion_materias).grid(row=0, column=3, padx=5)

        bind_enter(self._nombre_entry, self._agregar)
        focus_entry(self._nombre_entry)

    # ------------------------------------------------------------------
    # Datos y refresco
    # ------------------------------------------------------------------
    def refresh(self) -> None:
        seleccion_anterior = self._plan_var.get()
        self._planes = sorted(self.plan_service.listar(), key=lambda plan: (plan.nombre or "").lower())
        opciones = [plan.nombre or "" for plan in self._planes]
        self._plan_combobox["values"] = opciones
        if seleccion_anterior and seleccion_anterior in opciones:
            self._plan_var.set(seleccion_anterior)
        elif opciones:
            self._plan_var.set(opciones[0])
        else:
            self._plan_var.set("")
        self._on_plan_selected()
        self.set_status("Cursos por plan actualizados")

    def _load_anios(self) -> None:
        if self._selected_plan_id is None:
            self._anios = []
            self._selected_anio_id = None
            self._nombre_var.set("")
            recargar_treeview(self._tree, [], ["nombre"])
            self._total_label.config(text="Total de cursos: 0")
            return
        self._anios = self.anio_service.listar_por_plan(self._selected_plan_id)
        filas = [
            {
                "id": anio.id,
                "nombre": anio.nombre or "",
            }
            for anio in self._anios
        ]
        recargar_treeview(self._tree, filas, ["nombre"])
        self._selected_anio_id = None
        self._nombre_var.set("")
        self._total_label.config(text=f"Total de cursos: {len(self._anios)}")

    # ------------------------------------------------------------------
    # Eventos
    # ------------------------------------------------------------------
    def _on_plan_selected(self, _event: tk.Event | None = None) -> None:
        nombre = self._plan_var.get()
        plan = next((p for p in self._planes if (p.nombre or "") == nombre), None)
        self._selected_plan_id = plan.id if plan and plan.id is not None else None
        self._load_anios()

    def _on_tree_select(self, _event: tk.Event) -> None:
        seleccion = get_first_selection(self._tree)
        if seleccion is None:
            self._selected_anio_id = None
            self._nombre_var.set("")
            return
        self._selected_anio_id = int(seleccion)
        anio = next((a for a in self._anios if a.id == self._selected_anio_id), None)
        if anio:
            self._nombre_var.set(anio.nombre or "")

    # ------------------------------------------------------------------
    # Acciones CRUD
    # ------------------------------------------------------------------
    def _require_plan(self) -> int | None:
        if self._selected_plan_id is None:
            self.show_error("Seleccione un plan de estudio para continuar.")
            return None
        return self._selected_plan_id

    def _agregar(self) -> None:
        plan_id = self._require_plan()
        if plan_id is None:
            return
        nombre = self._nombre_var.get()
        try:
            self.anio_service.crear(nombre, plan_id)
        except ValidationError as exc:
            self.show_error(str(exc))
            return
        except Exception as exc:  # pragma: no cover
            self.show_error(str(exc))
            return
        self.show_info("Curso creado correctamente.")
        self._load_anios()

    def _editar(self) -> None:
        if self._selected_anio_id is None:
            self.show_error("Seleccione un curso para editar.")
            return
        nombre = self._nombre_var.get()
        try:
            self.anio_service.actualizar(self._selected_anio_id, nombre)
        except ValidationError as exc:
            self.show_error(str(exc))
            return
        except Exception as exc:  # pragma: no cover
            self.show_error(str(exc))
            return
        self.show_info("Curso actualizado correctamente.")
        self._load_anios()

    def _eliminar(self) -> None:
        if self._selected_anio_id is None:
            self.show_error("Seleccione un curso para eliminar.")
            return
        if not self.ask_yes_no("¿Desea eliminar el curso seleccionado?"):
            return
        try:
            self.anio_service.eliminar(self._selected_anio_id)
        except ValidationError as exc:
            self.show_error(str(exc))
            return
        except Exception as exc:  # pragma: no cover
            self.show_error(str(exc))
            return
        self.show_info("Curso eliminado.")
        self._load_anios()

    # ------------------------------------------------------------------
    # Gestión de materias asociadas
    # ------------------------------------------------------------------
    def _abrir_asignacion_materias(self) -> None:
        if self._selected_anio_id is None:
            self.show_error("Seleccione un curso para gestionar sus materias.")
            return
        plan_id = self._require_plan()
        if plan_id is None:
            return
        anio = next((a for a in self._anios if a.id == self._selected_anio_id), None)
        if anio is None:
            self.show_error("No se pudo obtener el curso seleccionado.")
            return

        dialog = tk.Toplevel(self)
        dialog.title("Materias del curso")
        dialog.configure(padx=12, pady=12)
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()
        dialog.focus_set()
        center_window(dialog, 520, 480)

        ttk.Label(
            dialog,
            text=f"Materias asociadas a {anio.nombre or ''}",
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

        def materias_asignadas() -> list[dict]:
            return self.anio_service.obtener_materias(self._selected_anio_id or 0)

        def cargar_asignadas() -> None:
            filas = [
                {
                    "id": registro.get("id"),
                    "nombre": registro.get("nombre", ""),
                    "horas": registro.get("horas_semanales", 0),
                }
                for registro in materias_asignadas()
            ]
            recargar_treeview(tree, filas, ["nombre", "horas"])

        def materias_disponibles() -> list[str]:
            asignadas = {registro.get("id") for registro in materias_asignadas()}
            plan_materias = self.plan_service.obtener_materias(plan_id)
            return sorted(
                [registro.get("nombre", "") for registro in plan_materias if registro.get("id") not in asignadas],
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
            if not nombre_materia:
                self.show_error("Seleccione una obligación válida.")
                return
            plan_materias = self.plan_service.obtener_materias(plan_id)
            materia = next((m for m in plan_materias if m.get("nombre") == nombre_materia), None)
            if materia is None:
                self.show_error("Seleccione una obligación válida.")
                return
            try:
                self.anio_service.agregar_materia(self._selected_anio_id, materia.get("id"))
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
            if not self.ask_yes_no("¿Quitar la obligación seleccionada del curso?"):
                return
            try:
                self.anio_service.quitar_materia(self._selected_anio_id, int(seleccion))
            except Exception as exc:  # pragma: no cover
                self.show_error(str(exc))
                return
            cargar_asignadas()
            cb_materia.config(values=materias_disponibles())

        ttk.Button(botones, text="Agregar obligación", command=agregar_materia).grid(row=0, column=0, padx=5)
        ttk.Button(botones, text="Quitar obligación", command=quitar_materia).grid(row=0, column=1, padx=5)

        bind_enter(cb_materia, agregar_materia)
        dialog.bind("<Escape>", lambda _event: dialog.destroy())


def build_anios_view(container: tk.Misc, app: MainWindow) -> AniosView:
    """Factory para registrar la vista en la ventana principal."""
    return AniosView(container, app)
