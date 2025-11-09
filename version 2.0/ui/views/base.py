"""Clases base y utilidades compartidas para las vistas."""
from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from ui.main_window import MainWindow


class BaseView(ttk.Frame):
    """Base común para todas las vistas, ofrece utilidades de UI."""

    def __init__(self, master: tk.Misc, app: MainWindow, *, title: str | None = None) -> None:
        super().__init__(master)
        self.app = app
        self.configure(padding=16)

        if title:
            self._title_label = ttk.Label(self, text=title, font=("Segoe UI", 16, "bold"))
            self._title_label.pack(anchor="w", pady=(0, 12))
        else:
            self._title_label = None

    # ------------------------------------------------------------------
    # Helpers de mensajería
    # ------------------------------------------------------------------
    def show_info(self, message: str, *, title: str = "Información") -> None:
        messagebox.showinfo(title, message, parent=self.winfo_toplevel())

    def show_error(self, message: str, *, title: str = "Error") -> None:
        messagebox.showerror(title, message, parent=self.winfo_toplevel())

    def ask_yes_no(self, message: str, *, title: str = "Confirmar") -> bool:
        return messagebox.askyesno(title, message, parent=self.winfo_toplevel())

    def set_status(self, text: str) -> None:
        """Actualiza la barra de estado de la ventana principal."""
        self.app.set_status(text)
