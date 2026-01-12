# Sistema de Gestión de Horarios Escolares - Versión 2.0

## 🎯 Descripción

Refactorización completa del sistema monolítico (3,307 líneas) en una arquitectura modular, mantenible y escalable basada en el patrón MVC adaptado para aplicaciones de escritorio.

## 📁 Estructura del Proyecto

```
version 2.0/
├── main.py                          # Punto de entrada
├── config.py                        # Configuración global
├── database/                        # Capa de datos
│   ├── __init__.py
│   ├── connection.py               # Gestión de conexiones
│   └── schema.py                   # Esquema de BD
├── models/                          # Modelos de datos
│   ├── __init__.py
│   ├── base.py
│   ├── materia.py
│   ├── profesor.py
│   ├── anio.py
│   ├── plan.py
│   ├── turno.py
│   ├── division.py
│   └── horario.py
├── repositories/                    # Acceso a datos
│   ├── __init__.py
│   ├── base_repository.py
│   ├── materia_repository.py
│   ├── profesor_repository.py
│   ├── anio_repository.py
│   ├── plan_repository.py
│   ├── turno_repository.py
│   ├── division_repository.py
│   └── horario_repository.py
├── services/                        # Lógica de negocio
│   ├── __init__.py
│   ├── validation_service.py
│   ├── materia_service.py
│   ├── profesor_service.py
│   ├── horario_service.py
│   ├── turno_service.py
│   ├── plan_service.py
│   ├── anio_service.py
│   └── division_service.py
├── ui/                              # Interfaz de usuario
│   ├── __init__.py
│   ├── styles.py
│   ├── main_window.py
│   ├── components/
│   │   ├── __init__.py
│   │   ├── tooltip.py
│   │   └── treeview_helper.py
│   └── views/
│       ├── __init__.py
│       ├── materias_view.py
│       ├── profesores_view.py
│       ├── anios_view.py
│       ├── planes_view.py
│       ├── turnos_view.py
│       ├── divisiones_view.py
│       └── horarios_view.py
└── utils/                           # Utilidades
    ├── __init__.py
    ├── helpers.py
    └── validators.py
```

## 🚀 Características

### ✅ Beneficios de la Arquitectura

- **Modularidad:** Código organizado en módulos independientes
- **Mantenibilidad:** Fácil de mantener y actualizar
- **Escalabilidad:** Preparado para crecer
- **Testabilidad:** Cada módulo puede probarse independientemente
- **Reusabilidad:** Componentes reutilizables
- **Colaboración:** Múltiples desarrolladores pueden trabajar en paralelo

### 🎨 Patrón de Arquitectura

**Modelo-Vista-Controlador (MVC) Adaptado:**
- **Modelos:** Representan las entidades del dominio
- **Repositorios:** Acceso a datos (equivalente a DAO)
- **Servicios:** Lógica de negocio y validaciones
- **Vistas:** Interfaz de usuario
- **Main Window:** Orquestador de vistas

## 📚 Documentación

- **[PLAN_REFACTORIZACION.md](./PLAN_REFACTORIZACION.md):** Plan detallado de refactorización
- **[MAPEO_MIGRACION.md](./MAPEO_MIGRACION.md):** Mapeo de código original → nuevo
- **[CHECKLIST_IMPLEMENTACION.md](./CHECKLIST_IMPLEMENTACION.md):** Progreso de implementación

## 🔧 Instalación y Ejecución

### Requisitos
- Python 3.9+
- tkinter (incluido en Python estándar)
- SQLite3 (incluido en Python estándar)

### Ejecutar en Desarrollo
```bash
cd "version 2.0"
python main.py
```

### Compilar Ejecutable
```bash
# Ver instrucciones en la raíz del proyecto
cd ..
.\compilar.ps1
```

## 📊 Estado del Proyecto

Ver [CHECKLIST_IMPLEMENTACION.md](./CHECKLIST_IMPLEMENTACION.md) para el estado actual de la migración.

## 🎯 Próximos Pasos

1. Ejecutar pruebas funcionales y de integración
2. Preparar la compilación y distribución

## 👥 Contribución

Este proyecto está en proceso de refactorización. Para contribuir:

1. Revisar el plan de refactorización
2. Seleccionar un módulo del checklist
3. Implementar siguiendo las convenciones
4. Probar exhaustivamente
5. Actualizar el checklist

## 📝 Convenciones de Código

### Nombres
- Archivos: `snake_case.py`
- Clases: `PascalCase`
- Funciones: `snake_case()`
- Constantes: `UPPER_SNAKE_CASE`

### Imports
```python
# Estándar
import os
import sys

# Terceros
import tkinter as tk

# Locales
from models.materia import Materia
from repositories.materia_repository import MateriaRepository
```

### Docstrings
```python
def metodo(param1: str) -> bool:
    """
    Breve descripción.
    
    Args:
        param1: Descripción
        
    Returns:
        Descripción del retorno
    """
    pass
```

## 📄 Licencia

[Especificar licencia]

## 📞 Contacto

[Tu información de contacto]

---

**Versión:** 2.0  
**Estado:** En Desarrollo  
**Última actualización:** 31 de Octubre 2025
