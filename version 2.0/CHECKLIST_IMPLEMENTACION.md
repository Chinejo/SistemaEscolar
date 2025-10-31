# Checklist de Implementación - Versión 2.0

Este documento rastrea el progreso de la migración del código monolítico a la arquitectura modular.

## 📊 Progreso General

- [ ] **Fase 1:** Fundamentos (0/5)
- [ ] **Fase 2:** Modelos y Repositorios (0/15)
- [ ] **Fase 3:** Servicios (0/4)
- [ ] **Fase 4:** UI Base (0/5)
- [ ] **Fase 5:** Vistas (0/7)
- [ ] **Fase 6:** Integración y Pruebas (0/3)

**Total:** 0/39 tareas completadas (0%)

---

## Fase 1: Fundamentos (Base) 🏗️

### 1.1 Estructura de Carpetas
- [ ] Crear todas las carpetas necesarias
- [ ] Crear archivos `__init__.py` en cada paquete

### 1.2 Configuración
- [ ] `config.py`
  - [ ] `get_base_path()`
  - [ ] `DB_DIR`, `DB_NAME`
  - [ ] Constantes globales (días, espacios)

### 1.3 Database
- [ ] `database/__init__.py`
- [ ] `database/connection.py`
  - [ ] `get_connection()`
  - [ ] `db_operation()` decorador
- [ ] `database/schema.py`
  - [ ] `init_db()` completa
  - [ ] Todas las tablas creadas

### 1.4 Modelos Base
- [ ] `models/__init__.py`
- [ ] `models/base.py`
  - [ ] Clase `BaseModel`
  - [ ] Método `to_dict()`
  - [ ] Método estático `from_dict()`

---

## Fase 2: Modelos y Repositorios 🔷

### 2.1 Modelos de Datos
- [ ] `models/materia.py` - Clase `Materia`
- [ ] `models/profesor.py` - Clase `Profesor`
- [ ] `models/anio.py` - Clase `Anio`
- [ ] `models/plan.py` - Clase `Plan`
- [ ] `models/turno.py` - Clase `Turno`
- [ ] `models/division.py` - Clase `Division`
- [ ] `models/horario.py` - Clase `Horario`

### 2.2 Repositorio Base
- [ ] `repositories/__init__.py`
- [ ] `repositories/base_repository.py`
  - [ ] Clase `BaseRepository`
  - [ ] `create()`
  - [ ] `find_all()`
  - [ ] `find_by_id()`
  - [ ] `update()`
  - [ ] `delete()`

### 2.3 Repositorios Específicos
- [ ] `repositories/materia_repository.py`
  - [ ] Métodos CRUD básicos
  
- [ ] `repositories/profesor_repository.py`
  - [ ] Métodos CRUD básicos
  - [ ] `asignar_turno()`
  - [ ] `quitar_turno()`
  - [ ] `obtener_turnos()`
  - [ ] `obtener_por_turno()`
  - [ ] `asignar_banca()`
  - [ ] `obtener_banca()`
  - [ ] `actualizar_banca()`
  - [ ] `eliminar_banca()`
  
- [ ] `repositories/anio_repository.py`
  - [ ] Métodos CRUD básicos
  - [ ] `obtener_por_plan()`
  - [ ] `agregar_materia()`
  - [ ] `quitar_materia()`
  - [ ] `obtener_materias()`
  
- [ ] `repositories/plan_repository.py`
  - [ ] Métodos CRUD básicos
  - [ ] `agregar_materia()`
  - [ ] `quitar_materia()`
  - [ ] `obtener_materias()`
  
- [ ] `repositories/turno_repository.py`
  - [ ] Métodos CRUD básicos
  - [ ] `agregar_plan()`
  - [ ] `quitar_plan()`
  - [ ] `obtener_planes()`
  - [ ] `obtener_espacio_hora()`
  - [ ] `set_espacio_hora()`
  - [ ] `eliminar_espacio_hora()`
  
- [ ] `repositories/division_repository.py`
  - [ ] Métodos CRUD básicos
  
- [ ] `repositories/horario_repository.py`
  - [ ] `crear()` con validaciones
  - [ ] `obtener_por_division()`
  - [ ] `obtener_por_profesor()`
  - [ ] `eliminar()`
  - [ ] Métodos auxiliares de validación

---

## Fase 3: Servicios (Lógica de Negocio) ⚙️

### 3.1 Servicios de Validación
- [ ] `services/__init__.py`
- [ ] `services/validation_service.py`
  - [ ] Validación de conflictos de horarios
  - [ ] Validación de disponibilidad de profesores
  - [ ] Validación de espacios ocupados
  - [ ] Validación de límites de horas

### 3.2 Servicios Específicos
- [ ] `services/materia_service.py`
  - [ ] Lógica de negocio de materias
  
- [ ] `services/profesor_service.py`
  - [ ] Lógica de negocio de profesores
  - [ ] Cálculo de horas asignadas
  
- [ ] `services/horario_service.py`
  - [ ] Orquestación de validaciones
  - [ ] Asignación inteligente de horarios
  - [ ] Detección de conflictos

---

## Fase 4: UI Base 🎨

### 4.1 Estilos
- [ ] `ui/__init__.py`
- [ ] `ui/styles.py`
  - [ ] `aplicar_estilos()` migrado

### 4.2 Componentes Reutilizables
- [ ] `ui/components/__init__.py`
- [ ] `ui/components/tooltip.py`
  - [ ] Clase `ToolTip` migrada
  
- [ ] `ui/components/treeview_helper.py`
  - [ ] `crear_treeview()`
  - [ ] `recargar_treeview()`
  - [ ] `autocompletar_combobox()`

### 4.3 Utilidades
- [ ] `utils/__init__.py`
- [ ] `utils/helpers.py`
  - [ ] Funciones utilitarias
  
- [ ] `utils/validators.py`
  - [ ] Validadores de entrada
  - [ ] Sanitización

### 4.4 Ventana Principal
- [ ] `ui/main_window.py`
  - [ ] Clase `MainWindow`
  - [ ] `__init__()`
  - [ ] `crear_menu()`
  - [ ] `limpiar_frame()`
  - [ ] Métodos de navegación entre vistas

---

## Fase 5: Vistas (Pantallas) 🖼️

### 5.1 Vistas Base
- [ ] `ui/views/__init__.py`

### 5.2 Vista de Materias
- [ ] `ui/views/materias_view.py`
  - [ ] Clase `MateriasView`
  - [ ] `mostrar()`
  - [ ] `_agregar()`
  - [ ] `_editar()`
  - [ ] `_eliminar()`
  - [ ] `_recargar_tree()`
  - [ ] `_on_select()`

### 5.3 Vista de Profesores
- [ ] `ui/views/profesores_view.py`
  - [ ] Clase `ProfesoresView`
  - [ ] `mostrar()`
  - [ ] `_abrir_asignacion_turnos()`
  - [ ] `_abrir_banca_materias()`
  - [ ] Métodos CRUD

### 5.4 Vista de Turnos
- [ ] `ui/views/turnos_view.py`
  - [ ] Clase `TurnosView`
  - [ ] `mostrar()`
  - [ ] `_abrir_asignacion_planes()`
  - [ ] `_abrir_configurar_horas()`
  - [ ] Métodos CRUD

### 5.5 Vista de Planes
- [ ] `ui/views/planes_view.py`
  - [ ] Clase `PlanesView`
  - [ ] `mostrar()`
  - [ ] `_abrir_asignacion_materias()`
  - [ ] Métodos CRUD

### 5.6 Vista de Años
- [ ] `ui/views/anios_view.py`
  - [ ] Clase `AniosView`
  - [ ] `mostrar()`
  - [ ] `_abrir_asignacion_materias()`
  - [ ] Métodos CRUD

### 5.7 Vista de Divisiones
- [ ] `ui/views/divisiones_view.py`
  - [ ] Clase `DivisionesView`
  - [ ] `mostrar()`
  - [ ] `_agregar()` con popup
  - [ ] `_editar()` con popup
  - [ ] `_eliminar()`
  - [ ] `_recargar_tree()` con filtros

### 5.8 Vista de Horarios
- [ ] `ui/views/horarios_view.py`
  - [ ] Clase `HorariosView`
  - [ ] `mostrar_por_curso()`
  - [ ] `mostrar_por_profesor()`
  - [ ] Grilla de horarios
  - [ ] Asignación de materias/profesores
  - [ ] Validaciones en tiempo real

---

## Fase 6: Integración y Pruebas ✅

### 6.1 Punto de Entrada
- [ ] `main.py`
  - [ ] Función `main()`
  - [ ] Inicialización de BD
  - [ ] Lanzamiento de aplicación
  - [ ] Manejo de excepciones

### 6.2 Pruebas
- [ ] Pruebas de modelos
- [ ] Pruebas de repositorios
- [ ] Pruebas de servicios
- [ ] Pruebas de integración UI
- [ ] Pruebas de flujos completos

### 6.3 Ajustes Finales
- [ ] Verificar imports circulares
- [ ] Optimizar rendimiento
- [ ] Documentación completa
- [ ] Compatibilidad con PyInstaller
- [ ] Compilación y distribución

---

## 📝 Notas de Implementación

### Convenciones
- Completar módulos en orden de dependencias
- Probar cada módulo antes de continuar
- Documentar con docstrings
- Seguir PEP 8

### Prioridades
1. **Alta:** Fundamentos, Modelos, Repositorios
2. **Media:** Servicios, UI Base
3. **Baja:** Vistas individuales (pueden hacerse en paralelo)

### Consideraciones
- Mantener compatibilidad con BD existente
- No romper funcionalidad durante migración
- Código limpio y legible
- Preparado para testing

---

**Última actualización:** 31 de Octubre 2025  
**Estado:** Pendiente de inicio  
**Próximo paso:** Crear archivos de configuración base
