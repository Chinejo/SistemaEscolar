"""Estilos comunes para widgets ttk."""
from __future__ import annotations

from tkinter import ttk


def aplicar_estilos() -> None:
    """Aplica la configuración visual personalizada utilizada por la aplicación."""
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except Exception:
        # Ignorar si el tema no está disponible en la plataforma actual.
        pass

    style.configure(".", background="#f4f6fa", font=("Segoe UI", 10))
    style.configure("TLabel", background="#f4f6fa", font=("Segoe UI", 10))
    style.configure(
        "TButton",
        font=("Segoe UI", 10, "bold"),
        padding=6,
        relief="flat",
        background="#e0e7ef",
    )
    style.map("TButton", background=[("active", "#d0d7e7")])

    style.configure("TEntry", relief="flat", padding=4)
    style.configure(
        "TCombobox",
        padding=4,
        fieldbackground="#ffffff",
        background="#ffffff",
        selectbackground="#ffffff",
        selectforeground="#222222",
    )
    style.map(
        "TCombobox",
        fieldbackground=[("disabled", "#e9ecef"), ("readonly", "#ffffff"), ("!readonly", "#ffffff")],
        background=[("disabled", "#e9ecef"), ("readonly", "#ffffff"), ("!readonly", "#ffffff")],
        selectbackground=[("!focus", "#ffffff"), ("focus", "#ffffff")],
        selectforeground=[("!focus", "#222222"), ("focus", "#222222")],
    )

    style.configure(
        "Treeview",
        font=("Segoe UI", 10),
        rowheight=26,
        fieldbackground="#ffffff",
        background="#ffffff",
    )
    style.configure(
        "Treeview.Heading",
        font=("Segoe UI", 10, "bold"),
        background="#e0e7ef",
        foreground="#222222",
    )
    style.map("Treeview", background=[("selected", "#b3d1ff")])
    style.map("Treeview", foreground=[("selected", "#222222")])
