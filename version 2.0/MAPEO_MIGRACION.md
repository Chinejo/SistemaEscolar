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
| `crear_materia()` | `services/materia_service.py → MateriaService.crear()` | � |
| `obtener_materias()` | `services/materia_service.py → MateriaService.listar()` | � |
| `actualizar_materia()` | `services/materia_service.py → MateriaService.actualizar()` | � |
| `eliminar_materia()` | `services/materia_service.py → MateriaService.eliminar()` | � |
| - | `models/materia.py → class Materia` | 🔵 |
| - | `repositories/materia_repository.py → MateriaRepository` | 🔵 |

### Profesores
| Función Original | Nueva Ubicación | Tipo |
|-----------------|-----------------|------|
| `crear_profesor()` | `services/profesor_service.py → ProfesorService.crear()` | � |
| `obtener_profesores()` | `services/profesor_service.py → ProfesorService.listar()` | � |
| `actualizar_profesor()` | `services/profesor_service.py → ProfesorService.actualizar()` | � |
| `eliminar_profesor()` | `services/profesor_service.py → ProfesorService.eliminar()` | � |
| `asignar_turno_a_profesor()` | `services/profesor_service.py → ProfesorService.asignar_turno()` | � |
| `quitar_turno_a_profesor()` | `services/profesor_service.py → ProfesorService.quitar_turno()` | � |
| `obtener_turnos_de_profesor()` | `services/profesor_service.py → ProfesorService.obtener_turnos()` | � |
| `obtener_profesores_por_turno()` | `services/profesor_service.py → ProfesorService.obtener_por_turno()` | � |
| `asignar_banca_profesor()` | `services/profesor_service.py → ProfesorService.asignar_banca()` | � |
| `obtener_banca_profesor()` | `services/profesor_service.py → ProfesorService.obtener_banca()` | � |
| `actualizar_banca_profesor()` | `services/profesor_service.py → ProfesorService.actualizar_banca()` | � |
| `eliminar_banca_profesor()` | `services/profesor_service.py → ProfesorService.eliminar_banca()` | � |
| - | `models/profesor.py → class Profesor` | 🔵 |
| - | `repositories/profesor_repository.py → ProfesorRepository` | 🔵 |

### Años
| Función Original | Nueva Ubicación | Tipo |
|-----------------|-----------------|------|
| `crear_anio()` | `services/anio_service.py → AnioService.crear()` | 🔵 |
| `obtener_anios()` | `services/anio_service.py → AnioService.listar_por_plan()` | 🔵 |
| `eliminar_anio()` | `services/anio_service.py → AnioService.eliminar()` | 🔵 |
| `agregar_materia_a_anio()` | `services/anio_service.py → AnioService.agregar_materia()` | 🔵 |
| `quitar_materia_de_anio()` | `services/anio_service.py → AnioService.quitar_materia()` | 🔵 |
| `obtener_materias_de_anio()` | `services/anio_service.py → AnioService.obtener_materias()` | 🔵 |
| - | `models/anio.py → class Anio` | 🔵 |

### Planes de Estudio
| Función Original | Nueva Ubicación | Tipo |
|-----------------|-----------------|------|
| `crear_plan()` | `services/plan_service.py → PlanService.crear()` | 🔵 |
| `obtener_planes()` | `services/plan_service.py → PlanService.listar()` | 🔵 |
| `eliminar_plan()` | `services/plan_service.py → PlanService.eliminar()` | 🔵 |
| `agregar_materia_a_plan()` | `services/plan_service.py → PlanService.agregar_materia()` | 🔵 |
| `quitar_materia_de_plan()` | `services/plan_service.py → PlanService.quitar_materia()` | 🔵 |
| `obtener_materias_de_plan()` | `services/plan_service.py → PlanService.obtener_materias()` | 🔵 |
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
| `crear_division()` | `services/division_service.py → DivisionService.crear()` | 🔵 |
| `obtener_divisiones()` | `services/division_service.py → DivisionService.listar()` | 🔵 |
| `actualizar_division()` | `services/division_service.py → DivisionService.actualizar_nombre()` | 🔵 |
| `eliminar_division()` | `services/division_service.py → DivisionService.eliminar()` | 🔵 |
| - | `models/division.py → class Division` | 🔵 |

### Horarios
| Función Original | Nueva Ubicación | Tipo |
|-----------------|-----------------|------|
| `crear_horario()` | `services/horario_service.py → HorarioService.crear_para_division()` | 🟡 |
| `obtener_horarios()` | `services/horario_service.py → HorarioService.obtener_por_division()` | � |
| `eliminar_horario()` | `services/horario_service.py → HorarioService.eliminar()` | � |
| `crear_horario_profesor()` | `services/horario_service.py → HorarioService.crear_para_profesor()` | 🟡 |
| `obtener_horarios_profesor()` | `services/horario_service.py → HorarioService.obtener_por_profesor()` | � |
| `eliminar_horario_profesor()` | `services/horario_service.py → HorarioService.eliminar()` | � |
| - | `models/horario.py → class Horario` | 🔵 |
| - | `services/horario_service.py → HorarioService` (validaciones) | 🔵 |
| - | `repositories/horario_repository.py → HorarioRepository` | 🔵 |

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
| `crear_menu()` | `ui/main_window.py → MainWindow._build_menu()` | � |
| `limpiar_frame()` | `utils/helpers.py → clear_container()` | � |

### Vistas - Materias
| Método Original | Nueva Ubicación | Tipo |
|-----------------|-----------------|------|
| `mostrar_materias()` | `ui/views/materias_view.py → MateriasView.refresh()` | � |
| `_agregar_materia()` | `ui/views/materias_view.py → MateriasView._agregar()` | 🔵 |
| `_editar_materia()` | `ui/views/materias_view.py → MateriasView._editar()` | 🔵 |
| `_eliminar_materia()` | `ui/views/materias_view.py → MateriasView._eliminar()` | 🔵 |
| `_cargar_materias_en_tree()` | `ui/views/materias_view.py → MateriasView._apply_filter()` | � |
| `_on_select_materia()` | `ui/views/materias_view.py → MateriasView._on_tree_select()` | 🔵 |

### Vistas - Profesores
| Método Original | Nueva Ubicación | Tipo |
|-----------------|-----------------|------|
| `mostrar_profesores()` | `ui/views/profesores_view.py → ProfesoresView.mostrar()` | 🔵 |
| `_gestionar_turnos_profesor()` | `ui/views/profesores_view.py → ProfesoresView._gestionar_turnos_profesor()` | 🔵 |
| `_gestionar_banca_profesor()` | `ui/views/profesores_view.py → ProfesoresView._gestionar_banca_profesor()` | 🔵 |
| `_abrir_ventana_banca_profesor()` | `ui/views/profesores_view.py → ProfesoresView._abrir_ventana_banca_profesor()` | 🔵 |
| `_agregar_profesor()` | `ui/views/profesores_view.py → ProfesoresView._agregar()` | 🔵 |
| `_editar_profesor()` | `ui/views/profesores_view.py → ProfesoresView._editar()` | 🔵 |
| `_eliminar_profesor()` | `ui/views/profesores_view.py → ProfesoresView._eliminar()` | 🔵 |
| `_cargar_profesores_en_tree()` | `ui/views/profesores_view.py → ProfesoresView._recargar_tree()` | 🔵 |

### Vistas - Turnos
| Método Original | Nueva Ubicación | Tipo |
|-----------------|-----------------|------|
| `mostrar_turnos()` | `ui/views/turnos_view.py → TurnosView.mostrar()` | 🔵 |
| `_gestionar_planes_turno()` | `ui/views/turnos_view.py → TurnosView._gestionar_planes_turno()` | 🔵 |
| `_configurar_horas_por_turno()` | `ui/views/turnos_view.py → TurnosView._configurar_horas_por_turno()` | 🔵 |
| Métodos CRUD de turnos | `ui/views/turnos_view.py → TurnosView._*()` | 🔵 |

### Vistas - Planes
| Método Original | Nueva Ubicación | Tipo |
|-----------------|-----------------|------|
| `mostrar_planes()` | `ui/views/planes_view.py → PlanesView.mostrar()` | 🔵 |
| `_gestionar_materias_plan()` | `ui/views/planes_view.py → PlanesView._gestionar_materias_plan()` | 🔵 |
| `_gestionar_anios_plan()` | `ui/views/planes_view.py → PlanesView._gestionar_anios_plan()` | 🔵 |
| Métodos CRUD de planes | `ui/views/planes_view.py → PlanesView._*()` | 🔵 |
| `_cargar_planes_en_tree()` | `ui/views/planes_view.py → PlanesView._recargar_tree()` | 🔵 |

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

6. **Decoradores:** El decorador `@db_operation` se mantiene en `database/connection.py`, ahora compatible con métodos de instancia gracias a la inyección automática de la conexión después de `self`

---

**Última actualización:** 31 de Octubre 2025
