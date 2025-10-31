# Mapeo de Migración - Código Original → Código Refactorizado

Este documento mapea cada función y clase del archivo original `Horarios_v0.9.py` a su nueva ubicación en la arquitectura refactorizada.

## 📋 Leyenda

- 🟢 **Migración directa:** Función se mueve sin cambios significativos
- 🟡 **Refactorización:** Función se divide o modifica
- 🔵 **Integración:** Función se integra en una clase
- 🟣 **Deprecada:** Función ya no es necesaria

---

## 1. Configuración y Base de Datos (Líneas 1-217)

### Estilos
| Función Original | Nueva Ubicación | Tipo |
|-----------------|-----------------|------|
| `aplicar_estilos_ttk()` | `ui/styles.py → aplicar_estilos()` | 🟢 |

### Configuración de Base de Datos
| Función Original | Nueva Ubicación | Tipo |
|-----------------|-----------------|------|
| `get_base_path()` | `config.py → get_base_path()` | 🟢 |
| `DB_DIR` (variable) | `config.py → DB_DIR` | 🟢 |
| `DB_NAME` (variable) | `config.py → DB_NAME` | 🟢 |
| `get_connection()` | `database/connection.py → get_connection()` | 🟢 |
| `db_operation()` (decorador) | `database/connection.py → db_operation()` | 🟢 |

### CRUD Genérico
| Función Original | Nueva Ubicación | Tipo |
|-----------------|-----------------|------|
| `crear_entidad()` | `repositories/base_repository.py → BaseRepository.create()` | 🔵 |
| `obtener_entidades()` | `repositories/base_repository.py → BaseRepository.find_all()` | 🔵 |
| `actualizar_entidad()` | `repositories/base_repository.py → BaseRepository.update()` | 🔵 |
| `eliminar_entidad()` | `repositories/base_repository.py → BaseRepository.delete()` | 🔵 |

### Inicialización de Base de Datos
| Función Original | Nueva Ubicación | Tipo |
|-----------------|-----------------|------|
| `init_db()` | `database/schema.py → init_db()` | 🟢 |

---

## 2. Modelos y Funciones CRUD (Líneas 218-730)

### Materias
| Función Original | Nueva Ubicación | Tipo |
|-----------------|-----------------|------|
| `crear_materia()` | `repositories/materia_repository.py → MateriaRepository.crear()` | 🔵 |
| `obtener_materias()` | `repositories/materia_repository.py → MateriaRepository.obtener_todas()` | 🔵 |
| `actualizar_materia()` | `repositories/materia_repository.py → MateriaRepository.actualizar()` | 🔵 |
| `eliminar_materia()` | `repositories/materia_repository.py → MateriaRepository.eliminar()` | 🔵 |
| - | `models/materia.py → class Materia` | 🔵 |

### Profesores
| Función Original | Nueva Ubicación | Tipo |
|-----------------|-----------------|------|
| `crear_profesor()` | `repositories/profesor_repository.py → ProfesorRepository.crear()` | 🔵 |
| `obtener_profesores()` | `repositories/profesor_repository.py → ProfesorRepository.obtener_todos()` | 🔵 |
| `actualizar_profesor()` | `repositories/profesor_repository.py → ProfesorRepository.actualizar()` | 🔵 |
| `eliminar_profesor()` | `repositories/profesor_repository.py → ProfesorRepository.eliminar()` | 🔵 |
| `asignar_turno_a_profesor()` | `repositories/profesor_repository.py → ProfesorRepository.asignar_turno()` | 🔵 |
| `quitar_turno_a_profesor()` | `repositories/profesor_repository.py → ProfesorRepository.quitar_turno()` | 🔵 |
| `obtener_turnos_de_profesor()` | `repositories/profesor_repository.py → ProfesorRepository.obtener_turnos()` | 🔵 |
| `obtener_profesores_por_turno()` | `repositories/profesor_repository.py → ProfesorRepository.obtener_por_turno()` | 🔵 |
| `asignar_banca_profesor()` | `repositories/profesor_repository.py → ProfesorRepository.asignar_banca()` | 🔵 |
| `obtener_banca_profesor()` | `repositories/profesor_repository.py → ProfesorRepository.obtener_banca()` | 🔵 |
| `actualizar_banca_profesor()` | `repositories/profesor_repository.py → ProfesorRepository.actualizar_banca()` | 🔵 |
| `eliminar_banca_profesor()` | `repositories/profesor_repository.py → ProfesorRepository.eliminar_banca()` | 🔵 |
| - | `models/profesor.py → class Profesor` | 🔵 |

### Años
| Función Original | Nueva Ubicación | Tipo |
|-----------------|-----------------|------|
| `crear_anio()` | `repositories/anio_repository.py → AnioRepository.crear()` | 🔵 |
| `obtener_anios()` | `repositories/anio_repository.py → AnioRepository.obtener_por_plan()` | 🔵 |
| `eliminar_anio()` | `repositories/anio_repository.py → AnioRepository.eliminar()` | 🔵 |
| `agregar_materia_a_anio()` | `repositories/anio_repository.py → AnioRepository.agregar_materia()` | 🔵 |
| `quitar_materia_de_anio()` | `repositories/anio_repository.py → AnioRepository.quitar_materia()` | 🔵 |
| `obtener_materias_de_anio()` | `repositories/anio_repository.py → AnioRepository.obtener_materias()` | 🔵 |
| - | `models/anio.py → class Anio` | 🔵 |

### Planes de Estudio
| Función Original | Nueva Ubicación | Tipo |
|-----------------|-----------------|------|
| `crear_plan()` | `repositories/plan_repository.py → PlanRepository.crear()` | 🔵 |
| `obtener_planes()` | `repositories/plan_repository.py → PlanRepository.obtener_todos()` | 🔵 |
| `eliminar_plan()` | `repositories/plan_repository.py → PlanRepository.eliminar()` | 🔵 |
| `agregar_materia_a_plan()` | `repositories/plan_repository.py → PlanRepository.agregar_materia()` | 🔵 |
| `quitar_materia_de_plan()` | `repositories/plan_repository.py → PlanRepository.quitar_materia()` | 🔵 |
| `obtener_materias_de_plan()` | `repositories/plan_repository.py → PlanRepository.obtener_materias()` | 🔵 |
| - | `models/plan.py → class Plan` | 🔵 |

### Turnos
| Función Original | Nueva Ubicación | Tipo |
|-----------------|-----------------|------|
| `crear_turno()` | `repositories/turno_repository.py → TurnoRepository.crear()` | 🔵 |
| `obtener_turnos()` | `repositories/turno_repository.py → TurnoRepository.obtener_todos()` | 🔵 |
| `eliminar_turno()` | `repositories/turno_repository.py → TurnoRepository.eliminar()` | 🔵 |
| `agregar_plan_a_turno()` | `repositories/turno_repository.py → TurnoRepository.agregar_plan()` | 🔵 |
| `quitar_plan_de_turno()` | `repositories/turno_repository.py → TurnoRepository.quitar_plan()` | 🔵 |
| `obtener_planes_de_turno()` | `repositories/turno_repository.py → TurnoRepository.obtener_planes()` | 🔵 |
| `obtener_turno_espacio_hora()` | `repositories/turno_repository.py → TurnoRepository.obtener_espacio_hora()` | 🔵 |
| `set_turno_espacio_hora()` | `repositories/turno_repository.py → TurnoRepository.set_espacio_hora()` | 🔵 |
| `eliminar_turno_espacio_hora()` | `repositories/turno_repository.py → TurnoRepository.eliminar_espacio_hora()` | 🔵 |
| - | `models/turno.py → class Turno` | 🔵 |

### Divisiones
| Función Original | Nueva Ubicación | Tipo |
|-----------------|-----------------|------|
| `crear_division()` | `repositories/division_repository.py → DivisionRepository.crear()` | 🔵 |
| `obtener_divisiones()` | `repositories/division_repository.py → DivisionRepository.obtener_todas()` | 🔵 |
| `actualizar_division()` | `repositories/division_repository.py → DivisionRepository.actualizar()` | 🔵 |
| `eliminar_division()` | `repositories/division_repository.py → DivisionRepository.eliminar()` | 🔵 |
| - | `models/division.py → class Division` | 🔵 |

### Horarios
| Función Original | Nueva Ubicación | Tipo |
|-----------------|-----------------|------|
| `crear_horario()` | `repositories/horario_repository.py → HorarioRepository.crear()` | 🟡 |
| `obtener_horarios()` | `repositories/horario_repository.py → HorarioRepository.obtener_por_division()` | 🔵 |
| `eliminar_horario()` | `repositories/horario_repository.py → HorarioRepository.eliminar()` | 🔵 |
| `crear_horario_profesor()` | `repositories/horario_repository.py → HorarioRepository.crear_profesor()` | 🟡 |
| `obtener_horarios_profesor()` | `repositories/horario_repository.py → HorarioRepository.obtener_por_profesor()` | 🔵 |
| `eliminar_horario_profesor()` | `repositories/horario_repository.py → HorarioRepository.eliminar_profesor()` | 🔵 |
| - | `models/horario.py → class Horario` | 🔵 |
| - | `services/horario_service.py → HorarioService` (validaciones) | 🔵 |

### Utilidades
| Función Original | Nueva Ubicación | Tipo |
|-----------------|-----------------|------|
| `autocompletar_combobox()` | `ui/components/treeview_helper.py → autocompletar_combobox()` | 🟢 |

---

## 3. Interfaz de Usuario (Líneas 731-3307)

### Componentes UI
| Clase/Función Original | Nueva Ubicación | Tipo |
|------------------------|-----------------|------|
| `class ToolTip` | `ui/components/tooltip.py → class ToolTip` | 🟢 |
| `crear_treeview()` | `ui/components/treeview_helper.py → crear_treeview()` | 🟢 |
| `recargar_treeview()` | `ui/components/treeview_helper.py → recargar_treeview()` | 🟢 |

### Ventana Principal
| Método Original (class App) | Nueva Ubicación | Tipo |
|----------------------------|-----------------|------|
| `__init__()` | `ui/main_window.py → MainWindow.__init__()` | 🟡 |
| `crear_menu()` | `ui/main_window.py → MainWindow.crear_menu()` | 🟢 |
| `limpiar_frame()` | `ui/main_window.py → MainWindow.limpiar_frame()` | 🟢 |

### Vistas - Materias
| Método Original | Nueva Ubicación | Tipo |
|-----------------|-----------------|------|
| `mostrar_materias()` | `ui/views/materias_view.py → MateriasView.mostrar()` | 🔵 |
| `_agregar_materia()` | `ui/views/materias_view.py → MateriasView._agregar()` | 🔵 |
| `_editar_materia()` | `ui/views/materias_view.py → MateriasView._editar()` | 🔵 |
| `_eliminar_materia()` | `ui/views/materias_view.py → MateriasView._eliminar()` | 🔵 |
| `_cargar_materias_en_tree()` | `ui/views/materias_view.py → MateriasView._recargar_tree()` | 🔵 |
| `_on_select_materia()` | `ui/views/materias_view.py → MateriasView._on_select()` | 🔵 |

### Vistas - Profesores
| Método Original | Nueva Ubicación | Tipo |
|-----------------|-----------------|------|
| `mostrar_profesores()` | `ui/views/profesores_view.py → ProfesoresView.mostrar()` | 🔵 |
| `_abrir_asignacion_turnos()` | `ui/views/profesores_view.py → ProfesoresView._abrir_asignacion_turnos()` | 🔵 |
| `_abrir_banca_materias()` | `ui/views/profesores_view.py → ProfesoresView._abrir_banca_materias()` | 🔵 |
| `_agregar_profesor()` | `ui/views/profesores_view.py → ProfesoresView._agregar()` | 🔵 |
| `_editar_profesor()` | `ui/views/profesores_view.py → ProfesoresView._editar()` | 🔵 |
| `_eliminar_profesor()` | `ui/views/profesores_view.py → ProfesoresView._eliminar()` | 🔵 |
| `_cargar_profesores_en_tree()` | `ui/views/profesores_view.py → ProfesoresView._recargar_tree()` | 🔵 |

### Vistas - Turnos
| Método Original | Nueva Ubicación | Tipo |
|-----------------|-----------------|------|
| `mostrar_turnos()` | `ui/views/turnos_view.py → TurnosView.mostrar()` | 🔵 |
| `_abrir_asignacion_planes_turno()` | `ui/views/turnos_view.py → TurnosView._abrir_asignacion_planes()` | 🔵 |
| `_abrir_configurar_horas()` | `ui/views/turnos_view.py → TurnosView._abrir_configurar_horas()` | 🔵 |
| Métodos CRUD de turnos | `ui/views/turnos_view.py → TurnosView._*()` | 🔵 |

### Vistas - Planes
| Método Original | Nueva Ubicación | Tipo |
|-----------------|-----------------|------|
| `mostrar_planes()` | `ui/views/planes_view.py → PlanesView.mostrar()` | 🔵 |
| `_abrir_asignacion_materias_plan()` | `ui/views/planes_view.py → PlanesView._abrir_asignacion_materias()` | 🔵 |
| Métodos CRUD de planes | `ui/views/planes_view.py → PlanesView._*()` | 🔵 |

### Vistas - Años
| Método Original | Nueva Ubicación | Tipo |
|-----------------|-----------------|------|
| `mostrar_anios()` | `ui/views/anios_view.py → AniosView.mostrar()` | 🔵 |
| `_abrir_asignacion_materias_anio()` | `ui/views/anios_view.py → AniosView._abrir_asignacion_materias()` | 🔵 |
| Métodos CRUD de años | `ui/views/anios_view.py → AniosView._*()` | 🔵 |

### Vistas - Divisiones
| Método Original | Nueva Ubicación | Tipo |
|-----------------|-----------------|------|
| `mostrar_divisiones()` | `ui/views/divisiones_view.py → DivisionesView.mostrar()` | 🔵 |
| `_agregar_division()` | `ui/views/divisiones_view.py → DivisionesView._agregar()` | 🔵 |
| `_editar_division()` | `ui/views/divisiones_view.py → DivisionesView._editar()` | 🔵 |
| `_eliminar_division()` | `ui/views/divisiones_view.py → DivisionesView._eliminar()` | 🔵 |
| `_recargar_divisiones_tree()` | `ui/views/divisiones_view.py → DivisionesView._recargar_tree()` | 🔵 |

### Vistas - Horarios
| Método Original | Nueva Ubicación | Tipo |
|-----------------|-----------------|------|
| `mostrar_horarios_curso()` | `ui/views/horarios_view.py → HorariosView.mostrar_por_curso()` | 🟡 |
| `mostrar_horarios_profesor()` | `ui/views/horarios_view.py → HorariosView.mostrar_por_profesor()` | 🟡 |
| Métodos de grilla de horarios | `ui/views/horarios_view.py → HorariosView._*()` | 🔵 |

---

## 4. Punto de Entrada

| Código Original | Nueva Ubicación | Tipo |
|----------------|-----------------|------|
| `if __name__ == '__main__':` | `main.py` | 🟡 |
| Inicialización de App | `main.py → main()` | 🟡 |

---

## 📊 Resumen de Migración

### Por Tipo
- 🟢 **Migración Directa:** ~15 funciones
- 🟡 **Refactorización:** ~10 funciones
- 🔵 **Integración en Clases:** ~80 funciones/métodos
- 🟣 **Deprecadas:** 0

### Por Módulo Destino
- **config.py:** 3 elementos
- **database/:** 6 funciones
- **models/:** 7 clases nuevas
- **repositories/:** 8 clases con ~60 métodos
- **services/:** 4 clases con validaciones
- **ui/styles.py:** 1 función
- **ui/components/:** 4 funciones + 1 clase
- **ui/main_window.py:** 1 clase base
- **ui/views/:** 7 vistas con ~50 métodos
- **utils/:** ~10 funciones

---

## 🎯 Notas Importantes

1. **IDs únicos:** Todos los métodos `_on_select_*()` se simplifican a `_on_select()` en cada vista

2. **Métodos _recargar_tree():** Unificados bajo un mismo nombre en cada vista

3. **Validaciones:** Extraídas a `services/validation_service.py` y `services/horario_service.py`

4. **Popups:** Cada popup de CRUD se convierte en un método privado de su vista correspondiente

5. **Constantes:** Días de semana, espacios horarios → `config.py`

6. **Decoradores:** El decorador `@db_operation` se mantiene igual pero en su propio módulo

---

**Última actualización:** 31 de Octubre 2025
