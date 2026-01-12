# Plan de Refactorización - Sistema de Gestión de Horarios Escolares v2.0

## 📋 Objetivo
Refactorizar el código monolítico de 3,307 líneas en una arquitectura modular, mantenible y escalable siguiendo el patrón MVC (Modelo-Vista-Controlador) adaptado para aplicaciones de escritorio.

## 🏗️ Arquitectura Propuesta

```
version 2.0/
├── main.py                      # Punto de entrada de la aplicación
├── config.py                    # Configuración global (paths, constantes)
├── database/
│   ├── __init__.py
│   ├── connection.py            # Gestión de conexiones a BD
│   └── schema.py                # Inicialización y esquema de BD
├── models/
│   ├── __init__.py
│   ├── base.py                  # Clase base para modelos
│   ├── materia.py               # Modelo Materia
│   ├── profesor.py              # Modelo Profesor
│   ├── anio.py                  # Modelo Año
│   ├── plan.py                  # Modelo Plan de Estudio
│   ├── turno.py                 # Modelo Turno
│   ├── division.py              # Modelo División
│   └── horario.py               # Modelo Horario
├── repositories/
│   ├── __init__.py
│   ├── base_repository.py       # Repositorio base con operaciones CRUD genéricas
│   ├── materia_repository.py   # Repositorio de Materias
│   ├── profesor_repository.py  # Repositorio de Profesores
│   ├── anio_repository.py      # Repositorio de Años
│   ├── plan_repository.py      # Repositorio de Planes
│   ├── turno_repository.py     # Repositorio de Turnos
│   ├── division_repository.py  # Repositorio de Divisiones
│   └── horario_repository.py   # Repositorio de Horarios
├── services/
│   ├── __init__.py
│   ├── materia_service.py       # Lógica de negocio de Materias
│   ├── profesor_service.py      # Lógica de negocio de Profesores
│   ├── horario_service.py       # Lógica de negocio de Horarios
│   └── validation_service.py    # Validaciones comunes
├── ui/
│   ├── __init__.py
│   ├── styles.py                # Estilos y temas de la UI
│   ├── main_window.py           # Ventana principal
│   ├── components/
│   │   ├── __init__.py
│   │   ├── tooltip.py           # Componente ToolTip
│   │   └── treeview_helper.py   # Funciones helper para Treeview
│   └── views/
│       ├── __init__.py
│       ├── materias_view.py     # Vista de Materias
│       ├── profesores_view.py   # Vista de Profesores
│       ├── anios_view.py        # Vista de Años
│       ├── planes_view.py       # Vista de Planes
│       ├── turnos_view.py       # Vista de Turnos
│       ├── divisiones_view.py   # Vista de Divisiones (Cursos)
│       └── horarios_view.py     # Vista de Horarios
└── utils/
    ├── __init__.py
    ├── helpers.py               # Funciones utilitarias generales
    └── validators.py            # Validadores de datos

```

## 📦 Descripción de Módulos

### 1. **main.py** (Punto de Entrada)
- Inicializa la aplicación
- Configura la base de datos
- Lanza la ventana principal

**Líneas estimadas:** ~30 líneas

### 2. **config.py** (Configuración)
- Constantes de la aplicación
- Rutas de archivos
- Configuraciones globales
- Detección de entorno (desarrollo/producción)

**Código actual a migrar:**
- `get_base_path()` 
- `DB_DIR`, `DB_NAME`

**Líneas estimadas:** ~50 líneas

### 3. **database/** (Capa de Datos)

#### 3.1 `connection.py`
- Gestión de conexiones a SQLite
- Decorador `db_operation`
- Función `get_connection()`

**Código actual a migrar:**
- `get_connection()`
- `db_operation()`

**Líneas estimadas:** ~40 líneas

#### 3.2 `schema.py`
- Definición del esquema de BD
- Función `init_db()`
- Creación de tablas

**Código actual a migrar:**
- Toda la función `init_db()` (líneas 85-217)

**Líneas estimadas:** ~200 líneas

### 4. **models/** (Modelos de Datos)

Cada modelo representa una entidad del sistema con sus atributos y métodos básicos.

#### Estructura de cada modelo:
```python
class NombreModelo:
    def __init__(self, id=None, atributo1=None, ...):
        self.id = id
        self.atributo1 = atributo1
        ...
    
    def to_dict(self):
        """Convierte el modelo a diccionario"""
        
    @staticmethod
    def from_dict(data):
        """Crea instancia desde diccionario"""
```

**Modelos a crear:**
- `Materia` (id, nombre, horas)
- `Profesor` (id, nombre)
- `Anio` (id, nombre, plan_id)
- `Plan` (id, nombre)
- `Turno` (id, nombre)
- `Division` (id, nombre, turno_id, plan_id, anio_id)
- `Horario` (id, division_id, dia, espacio, hora_inicio, hora_fin, materia_id, profesor_id, turno_id)

**Líneas estimadas por modelo:** ~30-50 líneas
**Total estimado:** ~300 líneas

### 5. **repositories/** (Repositorios - Acceso a Datos)

Patrón Repository: Abstrae el acceso a datos, separando la lógica de negocio de la persistencia.

#### 5.1 `base_repository.py`
```python
class BaseRepository:
    def __init__(self, tabla):
        self.tabla = tabla
    
    def create(self, campos, valores)
    def find_all(self, campos)
    def find_by_id(self, id_)
    def update(self, id_, campos, valores)
    def delete(self, id_)
```

**Código actual a migrar:**
- `crear_entidad()`
- `obtener_entidades()`
- `actualizar_entidad()`
- `eliminar_entidad()`

**Líneas estimadas:** ~80 líneas

#### 5.2 Repositorios específicos

Cada repositorio extiende `BaseRepository` y añade métodos específicos:

**MateriaRepository:**
- Código a migrar: `crear_materia()`, `obtener_materias()`, `actualizar_materia()`, `eliminar_materia()`
- Líneas: ~60

**ProfesorRepository:**
- Código a migrar: funciones de profesor + relaciones con turnos y banca
- Métodos: `asignar_turno()`, `obtener_turnos()`, `asignar_banca()`, etc.
- Líneas: ~150

**AnioRepository:**
- Código a migrar: funciones de año + relaciones con materias
- Métodos: `crear()`, `obtener()`, `agregar_materia()`, etc.
- Líneas: ~100

**PlanRepository:**
- Código a migrar: funciones de plan + relaciones con materias
- Líneas: ~100

**TurnoRepository:**
- Código a migrar: funciones de turno + relaciones con planes
- Métodos adicionales: `get_espacio_hora()`, `set_espacio_hora()`
- Líneas: ~120

**DivisionRepository:**
- Código a migrar: `crear_division()`, `obtener_divisiones()`, etc.
- Líneas: ~60

**HorarioRepository:**
- Código a migrar: funciones de horario por curso y por profesor
- Métodos más complejos para validaciones
- Líneas: ~200

**Total repositories:** ~870 líneas

### 6. **services/** (Lógica de Negocio)

Los servicios contienen la lógica de negocio y orquestan los repositorios.

#### 6.1 `validation_service.py`
- Validaciones de conflictos de horarios
- Validaciones de capacidad de profesores
- Validaciones de unicidad

**Líneas estimadas:** ~150 líneas

#### 6.2 Servicios por entidad
- `materia_service.py`: ~80 líneas ✅
- `profesor_service.py`: ~120 líneas ✅
- `horario_service.py`: ~200 líneas ✅
- `turno_service.py`: ~120 líneas ✅
- `plan_service.py`: ~120 líneas ✅
- `anio_service.py`: ~140 líneas ✅
- `division_service.py`: ~120 líneas ✅

**Total services:** ~920 líneas

### 7. **ui/** (Interfaz de Usuario)

#### 7.1 `styles.py`
**Código a migrar:**
- Función `aplicar_estilos_ttk()` completa

**Líneas estimadas:** ~30 líneas

#### 7.2 `components/tooltip.py`
**Código a migrar:**
- Clase `ToolTip` completa

**Líneas estimadas:** ~40 líneas

#### 7.3 `components/treeview_helper.py`
**Código a migrar:**
- `crear_treeview()`
- `recargar_treeview()`
- `autocompletar_combobox()`

**Líneas estimadas:** ~60 líneas

#### 7.4 `main_window.py`
**Código a migrar:**
- Clase `App` base (sin los métodos específicos de vistas)
- Menú principal
- Inicialización de la ventana

**Líneas estimadas:** ~150 líneas

#### 7.5 `views/` (Vistas específicas)

Cada vista es responsable de una pantalla completa:

**materias_view.py:**
- `mostrar_materias()`
- Formularios CRUD de materias
- Líneas: ~200

**profesores_view.py:**
- `mostrar_profesores()`
- `_abrir_asignacion_turnos()`
- `_abrir_banca_materias()`
- Líneas: ~300

**turnos_view.py:**
- `mostrar_turnos()`
- `_abrir_asignacion_planes_turno()`
- `_abrir_configurar_horas()`
- Líneas: ~400

**planes_view.py:**
- `mostrar_planes()`
- `_abrir_asignacion_materias_plan()`
- Líneas: ~250

**anios_view.py:**
- `mostrar_anios()`
- Gestión de materias por año
- Líneas: ~300

**divisiones_view.py:**
- `mostrar_divisiones()` (refactorizado)
- Popups de CRUD
- Líneas: ~300

**horarios_view.py:**
- `mostrar_horarios_curso()`
- `mostrar_horarios_profesor()`
- Grillas de horarios
- Líneas: ~600

**Total UI:** ~2,630 líneas

### 8. **utils/** (Utilidades)

#### 8.1 `helpers.py`
- Funciones utilitarias generales
- Conversiones de datos
- Formateo

**Líneas estimadas:** ~100 líneas

#### 8.2 `validators.py`
- Validadores de entrada
- Sanitización de datos

**Líneas estimadas:** ~80 líneas

## 📊 Resumen de Distribución

| Módulo | Líneas Estimadas | % del Total |
|--------|-----------------|-------------|
| main.py | 30 | 0.6% |
| config.py | 50 | 1.0% |
| database/ | 240 | 4.9% |
| models/ | 300 | 6.2% |
| repositories/ | 870 | 17.9% |
| services/ | 670 | 13.8% |
| ui/ | 2,630 | 54.2% |
| utils/ | 180 | 3.7% |
| **TOTAL** | **~4,970** | **150%** |
*Nota: El total estimado supera al original debido a imports, docstrings y estructura de clases adicionales.*

## 🔄 Orden de Implementación Recomendado

### Fase 1: Fundamentos (Base)
1. [x] Crear estructura de carpetas
2. [x] `config.py`
3. [x] `database/connection.py`
4. [x] `database/schema.py`
5. [x] `models/base.py`

### Fase 2: Modelos y Repositorios
6. [x] Todos los modelos (`models/*.py`)
7. [x] `repositories/base_repository.py`
8. [x] Todos los repositorios específicos

### Fase 3: Servicios
9. [x] `services/validation_service.py`
10. [x] Servicios específicos (materia, profesor, horario, turno)

### Fase 4: UI Base
11. [x] `ui/styles.py`
12. [x] `ui/components/`
13. [x] `utils/`
14. [x] `ui/main_window.py` (estructura base)

### Fase 5: Vistas (Pantallas)
15. [x] `ui/views/materias_view.py`
16. [x] `ui/views/profesores_view.py`
17. [ ] `ui/views/turnos_view.py`
18. [ ] `ui/views/planes_view.py`
19. [ ] `ui/views/anios_view.py`
20. [ ] `ui/views/divisiones_view.py`
21. [ ] `ui/views/horarios_view.py`

### Fase 6: Integración y Pruebas
22. [ ] `main.py` (punto de entrada)
23. [ ] Pruebas de integración
24. [ ] Ajustes y correcciones

## 🎯 Beneficios de la Refactorización

### Mantenibilidad
- ✅ Código organizado y fácil de navegar
- ✅ Responsabilidades claramente definidas
- ✅ Fácil localización de bugs

### Escalabilidad
- ✅ Agregar nuevas funcionalidades sin modificar código existente
- ✅ Fácil extensión de modelos y vistas
- ✅ Preparado para crecer

### Reusabilidad
- ✅ Componentes reutilizables
- ✅ Lógica de negocio independiente de la UI
- ✅ Repositorios genéricos

### Testabilidad
- ✅ Cada módulo puede testearse independientemente
- ✅ Fácil crear mocks de repositorios
- ✅ Tests unitarios por capa

### Colaboración
- ✅ Múltiples desarrolladores pueden trabajar en paralelo
- ✅ Menos conflictos en control de versiones
- ✅ Code reviews más efectivos

## 📝 Convenciones de Código

### Nombres
- **Archivos:** snake_case (`materia_repository.py`)
- **Clases:** PascalCase (`MateriaRepository`)
- **Funciones/Métodos:** snake_case (`crear_materia()`)
- **Constantes:** UPPER_SNAKE_CASE (`DB_NAME`)

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
def metodo_ejemplo(param1: str, param2: int) -> bool:
    """
    Descripción breve del método.
    
    Args:
        param1: Descripción del parámetro 1
        param2: Descripción del parámetro 2
        
    Returns:
        Descripción del valor de retorno
        
    Raises:
        Exception: Cuando ocurre X condición
    """
    pass
```

## 🚀 Siguientes Pasos

1. **Revisar y aprobar** este plan
2. **Crear estructura de carpetas** en `version 2.0/`
3. **Implementar fase por fase** siguiendo el orden recomendado
4. **Probar cada módulo** antes de pasar al siguiente
5. **Documentar cambios** en cada commit

## ⚠️ Consideraciones Importantes

- **Mantener version 1.0 intacta** como referencia y backup
- **Migrar funcionalidad gradualmente** para evitar errores
- **Probar exhaustivamente** cada módulo
- **Actualizar documentación** conforme avanzamos
- **Compatibilidad con PyInstaller** debe mantenerse

---

**Versión del Plan:** 1.1  
**Fecha:** 31 de Octubre 2025  
**Estado:** En progreso

## 📝 Historial de Cambios

### v1.1 - 31 de Octubre 2025
- ✅ Completadas Fases 1-4 (Fundamentos, Modelos, Repositorios, Servicios base, UI base)
- ✅ Implementadas vistas: `materias_view.py`, `profesores_view.py`
- ✅ Agregado `turno_service.py` con validaciones completas
- ✅ Integración de servicios en `MainWindow`
- 🔄 Pendientes: vistas de turnos, planes, años, divisiones y horarios

### v1.0 - 31 de Octubre 2025
- 📋 Plan inicial aprobado

