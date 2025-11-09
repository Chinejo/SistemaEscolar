"""Vista para gestionar turnos y sus configuraciones."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from models.plan import Plan
from models.turno import Turno
from services import ValidationError
from ui.components import crear_treeview, recargar_treeview
from ui.main_window import MainWindow
from ui.views.base import BaseView
from utils import bind_enter, center_window, focus_entry, get_first_selection


class TurnosView(BaseView):
    """Permite listar turnos, asociar planes y configurar horarios base."""

    def __init__(self, master: tk.Misc, app: MainWindow) -> None:  # type: ignore[override]
        super().__init__(master, app, title="Gestión de turnos")
        self.service = app.turno_service
        self.plan_service = app.plan_service

        self._turnos: list[Turno] = []
        self._planes: list[Plan] = []
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
        self._total_label = ttk.Label(resumen, text="Total de turnos: 0")
        self._total_label.pack(side="left")

        filtro = ttk.Frame(self)
        filtro.pack(fill="x", pady=(0, 12))
        ttk.Label(filtro, text="Filtro por nombre:").grid(row=0, column=0, padx=5, pady=2)
        entrada_filtro = ttk.Entry(filtro, textvariable=self._filter_var, width=30)
        entrada_filtro.grid(row=0, column=1, padx=5, pady=2)

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
        ttk.Button(botones, text="Planes del turno", command=self._abrir_asignacion_planes).grid(row=0, column=3, padx=5)
        ttk.Button(botones, text="Configurar horas", command=self._abrir_configurar_horas).grid(row=0, column=4, padx=5)

        bind_enter(self._nombre_entry, self._agregar)
        focus_entry(self._nombre_entry)
        self._filter_var.trace_add("write", lambda *_: self._apply_filter())

    # ------------------------------------------------------------------
    # Datos y refresco
    # ------------------------------------------------------------------
    def refresh(self) -> None:
        self._turnos = sorted(self.service.listar(), key=lambda turno: (turno.nombre or "").lower())
        self._planes = sorted(self.plan_service.listar(), key=lambda plan: (plan.nombre or "").lower())
        self._selected_id = None
        self._nombre_var.set("")
        self._apply_filter()
        self.set_status("Turnos actualizados")

    def _apply_filter(self) -> None:
        filtro = self._filter_var.get().strip().lower()
        if filtro:
            visibles = [turno for turno in self._turnos if filtro in (turno.nombre or "").lower()]
        else:
            visibles = list(self._turnos)

        filas = [
            {
                "id": turno.id,
                "nombre": turno.nombre or "",
            }
            for turno in visibles
        ]

        recargar_treeview(self._tree, filas, ["nombre"])
        self._total_label.config(text=f"Total de turnos: {len(visibles)}")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _get_turno(self) -> Turno | None:
        if self._selected_id is None:
            return None
        return next((turno for turno in self._turnos if turno.id == self._selected_id), None)

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
        turno = self._get_turno()
        if turno:
            self._nombre_var.set(turno.nombre or "")

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
        except Exception as exc:  # pragma: no cover - mensaje genérico para fallos inesperados
            self.show_error(str(exc))
            return

        self.show_info("Turno creado correctamente.")
        self.refresh()

    def _editar(self) -> None:
        if self._selected_id is None:
            self.show_error("Seleccione un turno para editar.")
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
        self.show_info("Turno actualizado correctamente.")
        self.refresh()

    def _eliminar(self) -> None:
        if self._selected_id is None:
            self.show_error("Seleccione un turno para eliminar.")
            return
        if not self.ask_yes_no("¿Desea eliminar el turno seleccionado?"):
            return
        try:
            self.service.eliminar(self._selected_id)
        except ValidationError as exc:
            self.show_error(str(exc))
            return
        except Exception as exc:  # pragma: no cover
            self.show_error(str(exc))
            return

        self.show_info("Turno eliminado.")
        self.refresh()

    # ------------------------------------------------------------------
    # Gestión de planes asociados
    # ------------------------------------------------------------------
    def _abrir_asignacion_planes(self) -> None:
        turno = self._get_turno()
        if turno is None or turno.id is None:
            self.show_error("Seleccione un turno para gestionar sus planes.")
            return

        dialog = tk.Toplevel(self)
        dialog.title("Planes del turno")
        dialog.configure(padx=12, pady=12)
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()
        dialog.focus_set()
        center_window(dialog, 480, 420)

        ttk.Label(
            dialog,
            text=f"Planes asociados a {turno.nombre or ''}",
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="w", pady=(0, 8))

        tabla_frame = ttk.Frame(dialog)
        tabla_frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(tabla_frame, columns=("nombre",), show="headings", height=8)
        tree.heading("nombre", text="Plan de estudio")
        tree.column("nombre", anchor="w", width=320)
        tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        tabla_frame.grid_rowconfigure(0, weight=1)
        tabla_frame.grid_columnconfigure(0, weight=1)

        def cargar_planes_asociados() -> None:
            registros = self.service.obtener_planes(turno.id or 0)
            filas = [
                {
                    "id": registro.get("id"),
                    "nombre": registro.get("nombre", ""),
                }
                for registro in registros
            ]
            recargar_treeview(tree, filas, ["nombre"])

        def planes_disponibles() -> list[str]:
            asociados = {registro.get("id") for registro in self.service.obtener_planes(turno.id or 0)}
            disponibles = [plan.nombre or "" for plan in self._planes if plan.id not in asociados]
            return sorted(disponibles, key=str.lower)

        cargar_planes_asociados()

        formulario = ttk.Frame(dialog)
        formulario.pack(fill="x", pady=10)
        ttk.Label(formulario, text="Agregar plan:").grid(row=0, column=0, padx=5, pady=2)
        plan_var = tk.StringVar()
        cb_plan = ttk.Combobox(formulario, textvariable=plan_var, values=planes_disponibles(), state="readonly", width=35)
        cb_plan.grid(row=0, column=1, padx=5, pady=2, sticky="w")

        botones = ttk.Frame(dialog)
        botones.pack(pady=5)

        def agregar_plan() -> None:
            nombre_plan = plan_var.get()
            plan = next((p for p in self._planes if (p.nombre or "") == nombre_plan), None)
            if plan is None or plan.id is None:
                self.show_error("Seleccione un plan válido.")
                return
            try:
                self.service.agregar_plan(turno.id, plan.id)
            except ValidationError as exc:
                self.show_error(str(exc))
                return
            except Exception as exc:  # pragma: no cover
                self.show_error(str(exc))
                return
            plan_var.set("")
            cargar_planes_asociados()
            cb_plan.config(values=planes_disponibles())

        def quitar_plan() -> None:
            seleccion = get_first_selection(tree)
            if seleccion is None:
                self.show_error("Seleccione un plan para quitar.")
                return
            if not self.ask_yes_no("¿Quitar el plan seleccionado del turno?"):
                return
            try:
                self.service.quitar_plan(turno.id, int(seleccion))
            except Exception as exc:  # pragma: no cover
                self.show_error(str(exc))
                return
            cargar_planes_asociados()
            cb_plan.config(values=planes_disponibles())

        ttk.Button(botones, text="Agregar plan", command=agregar_plan).grid(row=0, column=0, padx=5)
        ttk.Button(botones, text="Quitar plan", command=quitar_plan).grid(row=0, column=1, padx=5)

        bind_enter(cb_plan, agregar_plan)
        dialog.bind("<Escape>", lambda _event: dialog.destroy())

    # ------------------------------------------------------------------
    # Configuración de horas por espacio
    # ------------------------------------------------------------------
    def _abrir_configurar_horas(self) -> None:
        turno = self._get_turno()
        if turno is None or turno.id is None:
            self.show_error("Seleccione un turno para configurar sus horarios base.")
            return

        dialog = tk.Toplevel(self)
        dialog.title("Configurar horas por espacio")
        dialog.configure(padx=12, pady=12)
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()
        dialog.focus_set()
        center_window(dialog, 380, 520)

        ttk.Label(
            dialog,
            text="Defina las horas de inicio y fin para cada espacio (formato HH:MM).",
            wraplength=320,
        ).pack(anchor="w", pady=(0, 10))

        tabla = ttk.Frame(dialog)
        tabla.pack(fill="both", expand=True)

        entradas: dict[int, tuple[tk.StringVar, tk.StringVar]] = {}
        for idx in range(1, 9):
            datos = self.service.obtener_espacio_hora(turno.id, idx)
            inicio_var = tk.StringVar(value=str(datos.get("hora_inicio", "") if datos else ""))
            fin_var = tk.StringVar(value=str(datos.get("hora_fin", "") if datos else ""))

            fila = ttk.Frame(tabla)
            fila.pack(fill="x", pady=4)
            ttk.Label(fila, text=f"{idx}º espacio:", width=14, anchor="e").pack(side="left", padx=5)
            ttk.Entry(fila, textvariable=inicio_var, width=8).pack(side="left", padx=5)
            ttk.Label(fila, text="a").pack(side="left")
            ttk.Entry(fila, textvariable=fin_var, width=8).pack(side="left", padx=5)

            entradas[idx] = (inicio_var, fin_var)

        botones = ttk.Frame(dialog)
        botones.pack(pady=10)

        def guardar() -> None:
            for espacio, (inicio_var, fin_var) in entradas.items():
                inicio = inicio_var.get().strip()
                fin = fin_var.get().strip()
                try:
                    self.service.set_espacio_hora(turno.id, espacio, inicio or None, fin or None)
                except ValidationError as exc:
                    self.show_error(f"Espacio {espacio}: {exc}")
                    return
                except Exception as exc:  # pragma: no cover
                    self.show_error(str(exc))
                    return
            self.show_info("Configuración de horas guardada.")
            dialog.destroy()

        ttk.Button(botones, text="Guardar", command=guardar).grid(row=0, column=0, padx=5)
        ttk.Button(botones, text="Cancelar", command=dialog.destroy).grid(row=0, column=1, padx=5)

        dialog.bind("<Escape>", lambda _event: dialog.destroy())
        focus_entry(tabla.winfo_children()[0].winfo_children()[1])  # type: ignore[index]


def build_turnos_view(container: tk.Misc, app: MainWindow) -> TurnosView:
    """Factory para registrar la vista en la ventana principal."""
    return TurnosView(container, app)
