"""Funciones helper reutilizables para la interfaz de usuario."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable, Iterable


def clear_container(container: tk.Misc) -> None:
    """Elimina todos los widgets hijos de un contenedor."""
    for widget in container.winfo_children():
        widget.destroy()


def center_window(window: tk.Tk | tk.Toplevel, width: int, height: int) -> None:
    """Centra una ventana en pantalla con el ancho y alto indicados."""
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_position = max((screen_width - width) // 2, 0)
    y_position = max((screen_height - height) // 2, 0)
    window.geometry(f"{width}x{height}+{x_position}+{y_position}")


def focus_entry(entry: ttk.Entry) -> None:
    """Da foco al entry y selecciona su contenido para facilitar la edición."""
    entry.focus_set()
    entry.selection_range(0, tk.END)


def bind_enter(widget: tk.Widget, callback: Callable[[], None]) -> None:
    """Asocia la tecla Enter a una acción determinada."""

    def _on_return(_event: tk.Event) -> None:
        callback()

    widget.bind("<Return>", _on_return)


def iterate_selected(tree: ttk.Treeview) -> Iterable[str]:
    """Itera sobre los identificadores seleccionados de un treeview."""
    return tree.selection()


def get_first_selection(tree: ttk.Treeview) -> str | None:
    """Devuelve el primer elemento seleccionado de un treeview o ``None`` si no hay selección."""
    selected = tree.selection()
    if not selected:
        return None
    return selected[0]
