"""Vista para gestionar profesores y sus asignaciones."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from models.profesor import Profesor
from models.turno import Turno
from services import ValidationError
from ui.components import crear_treeview, recargar_treeview
from ui.main_window import MainWindow
from ui.views.base import BaseView
from utils import bind_enter, center_window, focus_entry, get_first_selection


class ProfesoresView(BaseView):
	"""Permite listar, crear y administrar profesores."""

	def __init__(self, master: tk.Misc, app: MainWindow) -> None:  # type: ignore[override]
		super().__init__(master, app, title="Gestión de personal")
		self.service = app.profesor_service
		self.materia_service = app.materia_service
		self.turno_service = app.turno_service

		self._profesores: list[Profesor] = []
		self._turnos: list[Turno] = []
		self._selected_id: int | None = None

		self._filter_var = tk.StringVar()
		self._turno_filter_var = tk.StringVar(value="Todos")
		self._nombre_var = tk.StringVar()

		self._build_layout()
		self.refresh()

	# ------------------------------------------------------------------
	# Construcción de UI
	# ------------------------------------------------------------------
	def _build_layout(self) -> None:
		resumen = ttk.Frame(self)
		resumen.pack(fill="x", pady=(0, 10))
		self._total_label = ttk.Label(resumen, text="Total de agentes: 0")
		self._total_label.pack(side="left")

		filtro = ttk.Frame(self)
		filtro.pack(fill="x", pady=(0, 12))
		ttk.Label(filtro, text="Filtro por nombre:").grid(row=0, column=0, padx=5, pady=2)
		entrada_filtro = ttk.Entry(filtro, textvariable=self._filter_var, width=30)
		entrada_filtro.grid(row=0, column=1, padx=5, pady=2)
		ttk.Label(filtro, text="Turno:").grid(row=0, column=2, padx=5, pady=2)
		self._turno_combobox = ttk.Combobox(
			filtro,
			textvariable=self._turno_filter_var,
			state="readonly",
			width=20,
		)
		self._turno_combobox.grid(row=0, column=3, padx=5, pady=2)

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
		ttk.Button(botones, text="Banca de horas", command=self._abrir_banca).grid(row=0, column=3, padx=5)
		ttk.Button(botones, text="Turnos del agente", command=self._abrir_turnos).grid(row=0, column=4, padx=5)

		bind_enter(self._nombre_entry, self._agregar)
		focus_entry(self._nombre_entry)

		self._filter_var.trace_add("write", lambda *_: self._apply_filters())
		self._turno_filter_var.trace_add("write", lambda *_: self._apply_filters())

	# ------------------------------------------------------------------
	# Datos y refresco
	# ------------------------------------------------------------------
	def refresh(self) -> None:
		self._profesores = sorted(
			self.service.listar(),
			key=lambda profesor: (profesor.nombre or "").lower(),
		)
		self._turnos = sorted(
			self.turno_service.listar(),
			key=lambda turno: (turno.nombre or "").lower(),
		)
		self._selected_id = None
		self._nombre_var.set("")
		self._populate_turno_filter()
		self._apply_filters()
		self.set_status("Profesores actualizados")

	def _populate_turno_filter(self) -> None:
		opciones = ["Todos"] + [turno.nombre or "" for turno in self._turnos]
		current = self._turno_filter_var.get() or "Todos"
		self._turno_combobox["values"] = opciones
		if current not in opciones:
			self._turno_filter_var.set("Todos")

	def _apply_filters(self) -> None:
		filtro = self._filter_var.get().strip().lower()
		turno_nombre = self._turno_filter_var.get().strip()

		visibles = list(self._profesores)
		if turno_nombre and turno_nombre != "Todos":
			turno = next((t for t in self._turnos if (t.nombre or "").lower() == turno_nombre.lower()), None)
			if turno and turno.id is not None:
				ids_turno = {
					registro.get("id")
					for registro in self.service.obtener_turnos(turno.id)
				}
				visibles = [profesor for profesor in visibles if profesor.id in ids_turno]
			else:
				visibles = []

		if filtro:
			visibles = [profesor for profesor in visibles if filtro in (profesor.nombre or "").lower()]

		filas = [
			{
				"id": profesor.id,
				"nombre": profesor.nombre or "",
			}
			for profesor in visibles
		]

		recargar_treeview(self._tree, filas, ["nombre"])
		self._total_label.config(text=f"Total de agentes: {len(visibles)}")

	# ------------------------------------------------------------------
	# Helpers
	# ------------------------------------------------------------------
	def _get_profesor(self) -> Profesor | None:
		if self._selected_id is None:
			return None
		return next((prof for prof in self._profesores if prof.id == self._selected_id), None)

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
		profesor = self._get_profesor()
		if profesor:
			self._nombre_var.set(profesor.nombre or "")

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
		except Exception as exc:  # pragma: no cover - mensaje genérico
			self.show_error(str(exc))
			return

		self.show_info("Profesor creado correctamente.")
		self.refresh()

	def _editar(self) -> None:
		if self._selected_id is None:
			self.show_error("Seleccione un profesor para editar.")
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

		self.show_info("Profesor actualizado correctamente.")
		self.refresh()

	def _eliminar(self) -> None:
		if self._selected_id is None:
			self.show_error("Seleccione un profesor para eliminar.")
			return
		if not self.ask_yes_no("¿Desea eliminar el profesor seleccionado?"):
			return
		try:
			self.service.eliminar(self._selected_id)
		except ValidationError as exc:
			self.show_error(str(exc))
			return
		except Exception as exc:  # pragma: no cover
			self.show_error(str(exc))
			return

		self.show_info("Profesor eliminado.")
		self.refresh()

	# ------------------------------------------------------------------
	# Gestión de banca de horas
	# ------------------------------------------------------------------
	def _abrir_banca(self) -> None:
		profesor = self._get_profesor()
		if profesor is None or profesor.id is None:
			self.show_error("Seleccione un profesor para gestionar la banca de horas.")
			return

		dialog = tk.Toplevel(self)
		dialog.title("Obligaciones del agente")
		dialog.configure(padx=12, pady=12)
		dialog.transient(self.winfo_toplevel())
		dialog.grab_set()
		dialog.focus_set()
		center_window(dialog, 560, 420)

		ttk.Label(
			dialog,
			text=f"Obligaciones asignadas a {profesor.nombre or ''}",
			font=("Segoe UI", 12, "bold"),
		).pack(anchor="w", pady=(0, 8))

		tabla_frame = ttk.Frame(dialog)
		tabla_frame.pack(fill="both", expand=True)

		tree = ttk.Treeview(tabla_frame, columns=("materia", "horas"), show="headings", height=10)
		tree.heading("materia", text="Obligación")
		tree.heading("horas", text="Horas")
		tree.column("materia", anchor="w", width=320)
		tree.column("horas", anchor="center", width=100)
		tree.grid(row=0, column=0, sticky="nsew")

		scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=tree.yview)
		tree.configure(yscroll=scrollbar.set)
		scrollbar.grid(row=0, column=1, sticky="ns")

		tabla_frame.grid_rowconfigure(0, weight=1)
		tabla_frame.grid_columnconfigure(0, weight=1)

		def cargar_banca() -> None:
			registros = self.service.obtener_banca(profesor.id or 0)
			filas = [
				{
					"id": registro["id"],
					"materia": registro.get("materia", ""),
					"horas": registro.get("banca_horas", 0),
				}
				for registro in registros
			]
			recargar_treeview(tree, filas, ["materia", "horas"])

		cargar_banca()

		materias = self.materia_service.listar()
		materia_por_nombre = {
			(materia.nombre or ""): materia.id
			for materia in materias
			if materia.id is not None
		}
		nombres_materia = sorted(materia_por_nombre.keys(), key=str.lower)

		formulario = ttk.Frame(dialog)
		formulario.pack(fill="x", pady=10)
		ttk.Label(formulario, text="Obligación:").grid(row=0, column=0, padx=5, pady=2)
		materia_var = tk.StringVar()
		cb_materia = ttk.Combobox(
			formulario,
			textvariable=materia_var,
			values=nombres_materia,
			state="readonly",
			width=35,
		)
		cb_materia.grid(row=0, column=1, padx=5, pady=2, sticky="w")

		botones = ttk.Frame(dialog)
		botones.pack(pady=5)

		def agregar_materia() -> None:
			nombre = materia_var.get()
			materia_id = materia_por_nombre.get(nombre)
			if materia_id is None:
				self.show_error("Seleccione una materia válida.")
				return
			try:
				self.service.asignar_banca(profesor.id, materia_id, 0)
			except ValidationError as exc:
				self.show_error(str(exc))
				return
			except Exception as exc:  # pragma: no cover
				self.show_error(str(exc))
				return
			materia_var.set("")
			cargar_banca()

		def eliminar_materia() -> None:
			seleccion = get_first_selection(tree)
			if seleccion is None:
				self.show_error("Seleccione una obligación para eliminar.")
				return
			if not self.ask_yes_no("¿Eliminar la obligación seleccionada?"):
				return
			try:
				self.service.eliminar_banca(int(seleccion))
			except Exception as exc:  # pragma: no cover
				self.show_error(str(exc))
				return
			cargar_banca()

		ttk.Button(botones, text="Agregar obligación", command=agregar_materia).grid(row=0, column=0, padx=5)
		ttk.Button(botones, text="Eliminar obligación", command=eliminar_materia).grid(row=0, column=1, padx=5)

		bind_enter(cb_materia, agregar_materia)
		dialog.bind("<Escape>", lambda _event: dialog.destroy())

	# ------------------------------------------------------------------
	# Gestión de turnos asignados
	# ------------------------------------------------------------------
	def _abrir_turnos(self) -> None:
		profesor = self._get_profesor()
		if profesor is None or profesor.id is None:
			self.show_error("Seleccione un profesor para gestionar turnos.")
			return

		dialog = tk.Toplevel(self)
		dialog.title("Turnos del agente")
		dialog.configure(padx=12, pady=12)
		dialog.transient(self.winfo_toplevel())
		dialog.grab_set()
		dialog.focus_set()
		center_window(dialog, 460, 480)

		ttk.Label(
			dialog,
			text=f"Turnos asignados a {profesor.nombre or ''}",
			font=("Segoe UI", 12, "bold"),
		).pack(anchor="w", pady=(0, 8))

		tabla_frame = ttk.Frame(dialog)
		tabla_frame.pack(fill="both", expand=True)

		tree = ttk.Treeview(tabla_frame, columns=("nombre",), show="headings", height=8)
		tree.heading("nombre", text="Turno")
		tree.column("nombre", anchor="w", width=260)
		tree.grid(row=0, column=0, sticky="nsew")

		scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=tree.yview)
		tree.configure(yscroll=scrollbar.set)
		scrollbar.grid(row=0, column=1, sticky="ns")
		tabla_frame.grid_rowconfigure(0, weight=1)
		tabla_frame.grid_columnconfigure(0, weight=1)

		turnos_totales = {turno.id: turno for turno in self._turnos if turno.id is not None}
		turno_var = tk.StringVar()

		def cargar_turnos_asignados() -> None:
			registros = self.service.obtener_turnos(profesor.id or 0)
			filas = [
				{
					"id": registro["id"],
					"nombre": registro.get("nombre", ""),
				}
				for registro in registros
			]
			recargar_treeview(tree, filas, ["nombre"])

		def turnos_disponibles() -> list[str]:
			asignados = {registro["id"] for registro in self.service.obtener_turnos(profesor.id or 0)}
			disponibles = [turno.nombre or "" for turno_id, turno in turnos_totales.items() if turno_id not in asignados]
			return sorted(disponibles, key=str.lower)

		cargar_turnos_asignados()

		formulario = ttk.Frame(dialog)
		formulario.pack(fill="x", pady=10)
		ttk.Label(formulario, text="Agregar turno:").grid(row=0, column=0, padx=5, pady=2)
		cb_turno = ttk.Combobox(
			formulario,
			textvariable=turno_var,
			values=turnos_disponibles(),
			state="readonly",
			width=30,
		)
		cb_turno.grid(row=0, column=1, padx=5, pady=2, sticky="w")

		botones = ttk.Frame(dialog)
		botones.pack(pady=5)

		def refrescar_combobox() -> None:
			cb_turno["values"] = turnos_disponibles()
			turno_var.set("")

		def agregar_turno() -> None:
			nombre = turno_var.get()
			turno = next((t for t in turnos_totales.values() if (t.nombre or "") == nombre), None)
			if turno is None or turno.id is None:
				self.show_error("Seleccione un turno válido.")
				return
			try:
				self.service.asignar_turno(profesor.id, turno.id)
			except ValidationError as exc:
				self.show_error(str(exc))
				return
			except Exception as exc:  # pragma: no cover
				self.show_error(str(exc))
				return
			cargar_turnos_asignados()
			refrescar_combobox()
			self._apply_filters()

		def quitar_turno() -> None:
			seleccion = get_first_selection(tree)
			if seleccion is None:
				self.show_error("Seleccione un turno para quitar.")
				return
			if not self.ask_yes_no("¿Quitar el turno seleccionado del profesor?"):
				return
			try:
				self.service.quitar_turno(profesor.id, int(seleccion))
			except Exception as exc:  # pragma: no cover
				self.show_error(str(exc))
				return
			cargar_turnos_asignados()
			refrescar_combobox()
			self._apply_filters()

		ttk.Button(botones, text="Agregar", command=agregar_turno).grid(row=0, column=0, padx=5)
		ttk.Button(botones, text="Quitar", command=quitar_turno).grid(row=0, column=1, padx=5)

		bind_enter(cb_turno, agregar_turno)
		dialog.bind("<Escape>", lambda _event: dialog.destroy())


def build_profesores_view(container: tk.Misc, app: MainWindow) -> ProfesoresView:
	"""Factory utilizado por la ventana principal para registrar la vista."""
	return ProfesoresView(container, app)

