"""Funciones helper para widgets Treeview y Combobox."""
from __future__ import annotations

from typing import Iterable, Mapping, Sequence

import tkinter as tk
from tkinter import ttk


def crear_treeview(
    parent: tk.Misc,
    columnas: Sequence[str],
    headings: Sequence[str],
    *,
    height: int = 10,
) -> ttk.Treeview:
    """Crea un treeview con scrollbars vertical y horizontal configurados."""
    tree = ttk.Treeview(parent, columns=columnas, show="headings", height=height)
    for column, heading in zip(columnas, headings):
        tree.heading(column, text=heading)

    vsb = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(parent, orient="horizontal", command=tree.xview)
    tree.configure(yscroll=vsb.set, xscroll=hsb.set)

    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")

    parent.grid_rowconfigure(0, weight=1)
    parent.grid_columnconfigure(0, weight=1)
    return tree


def recargar_treeview(tree: ttk.Treeview, datos: Iterable[Mapping[str, object]], campos: Sequence[str]) -> None:
    """Reemplaza el contenido del treeview con los datos proporcionados."""
    for item in tree.get_children():
        tree.delete(item)
    for registro in datos:
        values = tuple(registro.get(campo) for campo in campos)
        identificador = registro.get("id")
        tree.insert("", "end", iid=identificador, values=values)


def autocompletar_combobox(
    combobox: ttk.Combobox,
    valores: Sequence[str],
    *,
    incluir_vacio: bool = True,
) -> bool:
    """Configura los valores disponibles del combobox y ajusta su estado.

    Devuelve siempre ``False`` para mantener compatibilidad con antiguos callbacks
    que esperan ese valor al usarlo como validador.
    """
    opciones = list(valores)
    if incluir_vacio:
        opciones.insert(0, "")
    combobox["values"] = opciones

    if len(valores) >= 1:
        if not incluir_vacio:
            combobox.set("")
        combobox.config(state="readonly")
    else:
        combobox.set("")
        combobox.config(state="disabled")
    return False
