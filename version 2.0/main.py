"""Punto de entrada de la aplicación refactorizada."""
from __future__ import annotations

import logging
import sys

from database.schema import init_db
from ui.main_window import MainWindow
from ui.views import register_views


def main() -> int:
    """Inicializa la base de datos, registra las vistas y ejecuta la UI."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    try:
        init_db()
        logging.info("Base de datos inicializada correctamente.")
    except Exception:  # pragma: no cover - condiciones excepcionales
        logging.exception("Error al inicializar la base de datos")
        return 1

    try:
        app = MainWindow()
        register_views(app)
        app.run()
    except Exception:  # pragma: no cover - captura de errores en runtime
        logging.exception("Error inesperado durante la ejecución de la aplicación")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
