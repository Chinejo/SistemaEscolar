"""Vista para gestionar materias u obligaciones institucionales."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from models.materia import Materia
from ui.components import crear_treeview, recargar_treeview
from ui.main_window import MainWindow
from ui.views.base import BaseView
from utils import bind_enter, focus_entry, get_first_selection


class MateriasView(BaseView):
    """Permite listar, crear, editar y eliminar materias."""

    def __init__(self, master: tk.Misc, app: MainWindow) -> None:  # type: ignore[override]
        super().__init__(master, app, title="Gestión de Materias/Obligaciones")
        self.service = app.materia_service

        self._records: list[Materia] = []
        self._selected_id: int | None = None

        self._filter_var = tk.StringVar()
        self._nombre_var = tk.StringVar()
        self._horas_var = tk.StringVar()

        self._build_layout()
        self.refresh()

    # ------------------------------------------------------------------
    # Construcción de UI
    # ------------------------------------------------------------------
    def _build_layout(self) -> None:
        resumen_frame = ttk.Frame(self)
        resumen_frame.pack(fill="x", pady=(0, 10))

        self._total_materias = ttk.Label(resumen_frame, text="Total de materias: 0")
        self._total_materias.pack(side="left", padx=(0, 15))
        self._total_horas = ttk.Label(resumen_frame, text="Total de horas: 0")
        self._total_horas.pack(side="left")

        filtro_frame = ttk.Frame(self)
        filtro_frame.pack(fill="x", pady=(0, 12))
        ttk.Label(filtro_frame, text="Filtro por nombre:").pack(side="left")
        entrada_filtro = ttk.Entry(filtro_frame, textvariable=self._filter_var, width=40)
        entrada_filtro.pack(side="left", padx=(6, 0))
        self._filter_var.trace_add("write", lambda *_: self._apply_filter())

        tabla_frame = ttk.Frame(self)
        tabla_frame.pack(fill="both", expand=True)
        self._tree = crear_treeview(
            tabla_frame,
            ("nombre", "horas"),
            ("Nombre", "Horas semanales"),
            height=12,
        )
        self._tree.bind("<<TreeviewSelect>>", self._on_tree_select)

        formulario = ttk.Frame(self)
        formulario.pack(fill="x", pady=12)
        ttk.Label(formulario, text="Nombre:").grid(row=0, column=0, padx=5, pady=2, sticky="e")
        self._nombre_entry = ttk.Entry(formulario, textvariable=self._nombre_var, width=40)
        self._nombre_entry.grid(row=0, column=1, padx=5, pady=2, sticky="w")
        ttk.Label(formulario, text="Horas semanales:").grid(row=0, column=2, padx=5, pady=2, sticky="e")
        self._horas_entry = ttk.Entry(formulario, textvariable=self._horas_var, width=8)
        self._horas_entry.grid(row=0, column=3, padx=5, pady=2, sticky="w")

        botones = ttk.Frame(self)
        botones.pack(pady=5)
        btn_agregar = ttk.Button(botones, text="Agregar", command=self._agregar)
        btn_agregar.grid(row=0, column=0, padx=5)
        ttk.Button(botones, text="Editar", command=self._editar).grid(row=0, column=1, padx=5)
        ttk.Button(botones, text="Eliminar", command=self._eliminar).grid(row=0, column=2, padx=5)

        bind_enter(self._nombre_entry, self._agregar)
        bind_enter(self._horas_entry, self._agregar)
        focus_entry(self._nombre_entry)

    # ------------------------------------------------------------------
    # Datos y refresco
    # ------------------------------------------------------------------
    def refresh(self) -> None:
        self._records = sorted(self.service.listar(), key=lambda m: (m.nombre or "").lower())
        self._selected_id = None
        self._nombre_var.set("")
        self._horas_var.set("")
        self._apply_filter()
        self.set_status("Materias actualizadas")

    def _apply_filter(self) -> None:
        filtro = self._filter_var.get().strip().lower()
        if filtro:
            visibles = [m for m in self._records if filtro in (m.nombre or "").lower()]
        else:
            visibles = list(self._records)

        total_horas = sum(m.horas_semanales or 0 for m in visibles)
        self._total_materias.config(text=f"Total de materias: {len(visibles)}")
        self._total_horas.config(text=f"Total de horas: {total_horas}")

        filas = [
            {
                "id": m.id,
                "nombre": m.nombre or "",
                "horas": m.horas_semanales or 0,
            }
            for m in visibles
        ]
        recargar_treeview(self._tree, filas, ["nombre", "horas"])

    # ------------------------------------------------------------------
    # Eventos
    # ------------------------------------------------------------------
    def _on_tree_select(self, _event: tk.Event) -> None:
        seleccion = get_first_selection(self._tree)
        if not seleccion:
            self._selected_id = None
            self._nombre_var.set("")
            self._horas_var.set("")
            return

        self._selected_id = int(seleccion)
        materia = next((m for m in self._records if m.id == self._selected_id), None)
        if materia:
            self._nombre_var.set(materia.nombre or "")
            self._horas_var.set(str(materia.horas_semanales or 0))

    # ------------------------------------------------------------------
    # Acciones
    # ------------------------------------------------------------------
    def _agregar(self) -> None:
        nombre = self._nombre_var.get()
        horas = self._horas_var.get()
        try:
            self.service.crear(nombre, horas)
        except Exception as exc:  # pragma: no cover - muestra mensaje al usuario
            self.show_error(str(exc))
            return
        self.show_info("Materia creada correctamente.")
        self.refresh()

    def _editar(self) -> None:
        if self._selected_id is None:
            self.show_error("Seleccione una materia para editar.")
            return
        nombre = self._nombre_var.get()
        horas = self._horas_var.get()
        try:
            self.service.actualizar(self._selected_id, nombre, horas)
        except Exception as exc:  # pragma: no cover
            self.show_error(str(exc))
            return
        self.show_info("Materia actualizada correctamente.")
        self.refresh()

    def _eliminar(self) -> None:
        if self._selected_id is None:
            self.show_error("Seleccione una materia para eliminar.")
            return
        if not self.ask_yes_no("¿Desea eliminar la materia seleccionada?"):
            return
        try:
            self.service.eliminar(self._selected_id)
        except Exception as exc:  # pragma: no cover
            self.show_error(str(exc))
            return
        self.show_info("Materia eliminada.")
        self.refresh()


def build_materias_view(container: tk.Misc, app: MainWindow) -> MateriasView:
    """Factory utilizado por la ventana principal para registrar la vista."""
    return MateriasView(container, app)
