"""Ventana principal de la aplicación y registro de vistas."""
from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable, Dict

from services import AnioService, DivisionService, HorarioService, MateriaService, PlanService, ProfesorService, TurnoService
from ui.styles import aplicar_estilos
from utils.helpers import clear_container

ViewBuilder = Callable[[ttk.Frame, "MainWindow"], tk.Widget | None]


class MainWindow(tk.Tk):
    """Gestiona la ventana principal, el menú y la carga dinámica de vistas."""

    def __init__(
        self,
        *,
        plan_service: PlanService | None = None,
        anio_service: AnioService | None = None,
    division_service: DivisionService | None = None,
        materia_service: MateriaService | None = None,
        profesor_service: ProfesorService | None = None,
        horario_service: HorarioService | None = None,
        turno_service: TurnoService | None = None,
    ) -> None:
        super().__init__()
        aplicar_estilos()

        self.title("Gestión de Horarios Escolares")
        self.geometry("900x650")
        self.minsize(900, 650)
        self.configure(bg="#f4f6fa")

        self._plan_service = plan_service or PlanService()
        self._anio_service = anio_service or AnioService()
        self._division_service = division_service or DivisionService()
        self._materia_service = materia_service or MateriaService()
        self._profesor_service = profesor_service or ProfesorService()
        self._horario_service = horario_service or HorarioService()
        self._turno_service = turno_service or TurnoService()
        self._services: Dict[str, object] = {
            "materias": self._materia_service,
            "profesores": self._profesor_service,
            "horarios": self._horario_service,
            "turnos": self._turno_service,
            "planes": self._plan_service,
            "anios": self._anio_service,
            "divisiones": self._division_service,
        }
        self._view_builders: Dict[str, ViewBuilder] = {}
        self._current_widget: tk.Widget | None = None

        self._content_frame = ttk.Frame(self, padding=16)
        self._content_frame.pack(fill="both", expand=True)

        self._status_var = tk.StringVar(value="Listo")
        status_bar = ttk.Label(self, textvariable=self._status_var, anchor="w", padding=(10, 5))
        status_bar.pack(fill="x", side="bottom")

        self._build_menu()
        self.show_home()

    # ------------------------------------------------------------------
    # Propiedades y helpers
    # ------------------------------------------------------------------
    @property
    def materia_service(self) -> MateriaService:
        return self._materia_service

    @property
    def plan_service(self) -> PlanService:
        return self._plan_service

    @property
    def anio_service(self) -> AnioService:
        return self._anio_service

    @property
    def division_service(self) -> DivisionService:
        return self._division_service

    @property
    def profesor_service(self) -> ProfesorService:
        return self._profesor_service

    @property
    def horario_service(self) -> HorarioService:
        return self._horario_service

    @property
    def turno_service(self) -> TurnoService:
        return self._turno_service

    def get_service(self, key: str) -> object:
        """Obtiene un servicio registrado por su clave."""
        return self._services[key]

    # ------------------------------------------------------------------
    # Registro y navegación de vistas
    # ------------------------------------------------------------------
    def register_view(self, name: str, factory: ViewBuilder, *, replace: bool = False) -> None:
        """Registra una vista para que pueda cargarse desde el menú."""
        if not replace and name in self._view_builders:
            raise ValueError(f"La vista '{name}' ya se encuentra registrada.")
        self._view_builders[name] = factory

    def open_view(self, name: str) -> None:
        """Carga la vista indicada o muestra un aviso si aún no está disponible."""
        builder = self._view_builders.get(name)
        if builder is None:
            self._show_placeholder(name)
            return

        clear_container(self._content_frame)
        self._current_widget = builder(self._content_frame, self)
        if isinstance(self._current_widget, tk.Widget):
            self._current_widget.pack(fill="both", expand=True)
        self.set_status(f"Vista: {name.capitalize()}")

    def show_home(self) -> None:
        """Muestra la pantalla de bienvenida por defecto."""
        clear_container(self._content_frame)
        self._current_widget = ttk.Label(
            self._content_frame,
            text="Bienvenido al sistema de gestión de horarios escolares",
            font=("Segoe UI", 18, "bold"),
            background="#f4f6fa",
            foreground="#2a3a4a",
            anchor="center",
        )
        self._current_widget.pack(fill="both", expand=True, pady=50)
        self.set_status("Inicio")

    def _show_placeholder(self, name: str) -> None:
        """Presenta un mensaje indicando que la vista aún no fue implementada."""
        clear_container(self._content_frame)
        self._current_widget = ttk.Label(
            self._content_frame,
            text=f"La vista '{name}' estará disponible en próximas fases.",
            font=("Segoe UI", 12),
            background="#f4f6fa",
            foreground="#2a3a4a",
            anchor="center",
            wraplength=480,
        )
        self._current_widget.pack(fill="both", expand=True, pady=80)
        self.set_status("En construcción")
        messagebox.showinfo("Vista en construcción", f"La vista '{name}' se implementará en la fase correspondiente.")

    # ------------------------------------------------------------------
    # Menú
    # ------------------------------------------------------------------
    def _build_menu(self) -> None:
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        plan_menu = tk.Menu(menu_bar, tearoff=0)
        plan_menu.add_command(label="Gestionar Materias/Obligaciones", command=lambda: self.open_view("materias"))
        plan_menu.add_separator()
        plan_menu.add_command(label="Gestionar Planes de Estudio", command=lambda: self.open_view("planes"))
        plan_menu.add_command(label="Gestionar Cursos/Años", command=lambda: self.open_view("anios"))
        menu_bar.add_cascade(label="Plan de estudios", menu=plan_menu)

        turnos_menu = tk.Menu(menu_bar, tearoff=0)
        turnos_menu.add_command(label="Gestionar Turnos", command=lambda: self.open_view("turnos"))
        menu_bar.add_cascade(label="Turnos", menu=turnos_menu)

        profesores_menu = tk.Menu(menu_bar, tearoff=0)
        profesores_menu.add_command(label="Gestionar Personal", command=lambda: self.open_view("profesores"))
        menu_bar.add_cascade(label="Personal", menu=profesores_menu)

        cursos_menu = tk.Menu(menu_bar, tearoff=0)
        cursos_menu.add_command(label="Gestionar Cursos", command=lambda: self.open_view("divisiones"))
        menu_bar.add_cascade(label="Cursos", menu=cursos_menu)

        horarios_menu = tk.Menu(menu_bar, tearoff=0)
        horarios_menu.add_command(label="Por curso", command=lambda: self.open_view("horarios_curso"))
        horarios_menu.add_command(label="Por profesor", command=lambda: self.open_view("horarios_profesor"))
        menu_bar.add_cascade(label="Gestión de horarios", menu=horarios_menu)

    # ------------------------------------------------------------------
    # Estado inferior
    # ------------------------------------------------------------------
    def set_status(self, text: str) -> None:
        """Actualiza el mensaje de estado inferior."""
        self._status_var.set(text)

    # ------------------------------------------------------------------
    # Cierre controlado
    # ------------------------------------------------------------------
    def confirm_exit(self) -> None:
        """Pregunta al usuario si desea salir de la aplicación."""
        if messagebox.askyesno("Confirmar", "¿Desea salir del sistema?"):
            self.destroy()

    def run(self) -> None:
        """Ejecuta el loop principal de la aplicación."""
        self.protocol("WM_DELETE_WINDOW", self.confirm_exit)
        self.mainloop()
