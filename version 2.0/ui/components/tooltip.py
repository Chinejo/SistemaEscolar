"""Componente de ToolTip reutilizable para widgets tkinter."""
from __future__ import annotations

import tkinter as tk


class ToolTip:
    """Muestra un mensaje emergente cuando el cursor se posiciona sobre un widget."""

    def __init__(self, widget: tk.Widget, text: str) -> None:
        self.widget = widget
        self.text = text
        self.tip_window: tk.Toplevel | None = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, _event: tk.Event | None = None) -> None:
        """Crea la ventana emergente y la posiciona cerca del widget."""
        if self.tip_window or not self.text:
            return

        x, y, _cx, cy = self.widget.bbox("insert") or (0, 0, 0, 0)
        x += self.widget.winfo_rootx() + 25
        y += cy + self.widget.winfo_rooty() + 25

        self.tip_window = tk.Toplevel(self.widget)
        self.tip_window.wm_overrideredirect(True)
        self.tip_window.wm_geometry(f"+{x}+{y}")

        label = tk.Label(
            self.tip_window,
            text=self.text,
            justify="left",
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            font=("Segoe UI", 9, "normal"),
            padx=8,
            pady=6,
        )
        label.pack(ipadx=1)

    def hide_tip(self, _event: tk.Event | None = None) -> None:
        """Destruye la ventana emergente si existe."""
        if self.tip_window is not None:
            self.tip_window.destroy()
            self.tip_window = None
