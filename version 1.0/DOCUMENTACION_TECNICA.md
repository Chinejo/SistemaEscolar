# DOCUMENTACIÓN TÉCNICA
## Sistema de Gestión de Horarios Escolares v0.9

---

## ÍNDICE

1. [Información General](#1-información-general)
2. [Arquitectura del Sistema](#2-arquitectura-del-sistema)
3. [Modelo de Base de Datos](#3-modelo-de-base-de-datos)
4. [Módulos y Componentes](#4-módulos-y-componentes)
5. [API de Funciones](#5-api-de-funciones)
6. [Interfaz de Usuario](#6-interfaz-de-usuario)
7. [Flujos de Datos](#7-flujos-de-datos)
8. [Validaciones y Reglas de Negocio](#8-validaciones-y-reglas-de-negocio)
9. [Manejo de Errores](#9-manejo-de-errores)
10. [Configuración y Despliegue](#10-configuración-y-despliegue)
11. [Pruebas](#11-pruebas)
12. [Mantenimiento y Troubleshooting](#12-mantenimiento-y-troubleshooting)

---

## 1. INFORMACIÓN GENERAL

### 1.1 Datos del Sistema

| Atributo | Valor |
|----------|-------|
| **Nombre** | Sistema de Gestión de Horarios Escolares |
| **Versión** | 1.0 |
| **Lenguaje** | Python 3.9+ |
| **Framework UI** | Tkinter |
| **Base de Datos** | SQLite3 |
| **Líneas de Código** | 5,374 |
| **Archivo Principal** | SistemaEscolar_v1.py |
| **Tamaño Aprox.** | ~180 KB (código fuente) |
| **Plataforma** | Windows (compilable con PyInstaller) |

### 1.2 Requisitos del Sistema

#### Requisitos de Desarrollo
- Python 3.9 o superior
- Módulos estándar: `tkinter`, `sqlite3`, `os`, `sys`, `typing`
- PyInstaller 5.0+ (para compilación)

#### Requisitos de Ejecución (Usuario Final)
- **Sistema Operativo:** Windows 7, 8, 10, 11 (32 o 64 bits)
- **Memoria RAM:** Mínimo 2GB, Recomendado 4GB
- **Espacio en Disco:** 50 MB libres
- **Resolución de Pantalla:** Mínimo 1024x768, Recomendado 1366x768 o superior
- **Otros:** No requiere instalación de Python ni dependencias

### 1.3 Estructura de Archivos

```
Programa horarios/
├── version 1.0/
│   ├── SistemaEscolar_v1.py          # Código fuente principal
│   ├── institucion.db                 # Base de datos SQLite (creada al ejecutar)
│   ├── DOCUMENTACION_CAMBIOS.md       # Historial de cambios
│   ├── COMPILACION.md                 # Guía de compilación
│   ├── ACTA_DE_CONSTITUCION.md        # Acta del proyecto
│   ├── DOCUMENTACION_TECNICA.md       # Este documento
│   ├── MANUAL_DE_USUARIO.md           # Manual para usuarios finales
│   ├── compilar.ps1                   # Script de compilación PowerShell
│   └── diagnosticar_db.ps1            # Script de diagnóstico
├── build/                             # Archivos temporales de compilación
└── dist/                              # Ejecutable final (.exe)
```

---

## 2. ARQUITECTURA DEL SISTEMA

### 2.1 Patrón Arquitectónico

El sistema actual (v1.0) utiliza una **arquitectura monolítica** donde todo el código reside en un único archivo. Aunque funcionalmente completo, se está planificando una refactorización hacia una arquitectura modular (v2.0).

#### Arquitectura Actual (v1.0)

```
┌─────────────────────────────────────────────────────────┐
│                 SistemaEscolar_v1.py                    │
│  ┌───────────────────────────────────────────────────┐  │
│  │           Capa de Presentación (UI)               │  │
│  │  - Tkinter Widgets                                │  │
│  │  - Event Handlers                                 │  │
│  │  - Validaciones de Entrada                        │  │
│  └─────────────────────┬─────────────────────────────┘  │
│                        │                                 │
│  ┌─────────────────────▼─────────────────────────────┐  │
│  │         Capa de Lógica de Negocio                 │  │
│  │  - Funciones CRUD                                 │  │
│  │  - Validaciones de Reglas                         │  │
│  │  - Helpers y Utilidades                           │  │
│  └─────────────────────┬─────────────────────────────┘  │
│                        │                                 │
│  ┌─────────────────────▼─────────────────────────────┐  │
│  │          Capa de Acceso a Datos                   │  │
│  │  - Conexión a SQLite                              │  │
│  │  - Operaciones de BD                              │  │
│  │  - Decoradores de Transacciones                   │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
              ┌────────────────────┐
              │  institucion.db    │
              │     (SQLite3)      │
              └────────────────────┘
```

### 2.2 Componentes Principales

#### 2.2.1 Capa de Base de Datos

**Responsabilidades:**
- Gestión de conexiones a SQLite
- Inicialización del esquema de base de datos
- Transacciones con commit/rollback automático
- Migraciones de esquema

**Funciones Clave:**
- `get_connection()`: Obtiene conexión a la BD
- `init_db()`: Inicializa esquema y tablas
- `get_base_path()`: Maneja rutas para desarrollo y producción
- `@db_operation`: Decorador para operaciones transaccionales

#### 2.2.2 Capa de Lógica de Negocio

**Responsabilidades:**
- Operaciones CRUD para todas las entidades
- Validaciones de reglas de negocio
- Gestión de relaciones entre entidades
- Cálculos y transformaciones de datos

**Módulos Funcionales:**
- Gestión de Materias
- Gestión de Profesores
- Gestión de Planes de Estudio
- Gestión de Turnos
- Gestión de Divisiones
- Gestión de Horarios (dos vistas)

#### 2.2.3 Capa de Presentación (UI)

**Responsabilidades:**
- Renderizado de interfaz gráfica
- Captura de eventos de usuario
- Validación de entrada de datos
- Navegación entre vistas
- Feedback visual al usuario

**Componentes UI:**
- Ventana principal (`App` class)
- Vistas especializadas (materias, profesores, horarios, etc.)
- Componentes reutilizables (TreeView, Tooltips)
- Diálogos modales para edición

### 2.3 Flujo de Ejecución

```
1. Inicio de Aplicación
   ├─ Importación de módulos
   ├─ Aplicación de estilos TTK
   ├─ Inicialización de BD (init_db)
   └─ Creación de ventana principal (App)

2. Interfaz Principal
   ├─ Renderizado de menú
   ├─ Frame principal vacío
   └─ Escucha de eventos de usuario

3. Interacción Usuario
   ├─ Selección de menú
   ├─ Limpieza de frame principal
   ├─ Carga de vista correspondiente
   └─ Renderizado de datos

4. Operaciones CRUD
   ├─ Validación de entrada
   ├─ Llamada a función de lógica
   ├─ Operación en BD (transaccional)
   ├─ Actualización de UI
   └─ Mensaje de confirmación/error

5. Cierre de Aplicación
   └─ Liberación de recursos

### 2.4 Organización del archivo monolítico (actualización 29/11/2025)

Tras el reordenamiento de noviembre 2025, `SistemaEscolar_v1.py` mantiene su estructura monolítica pero ahora está ordenado por capas consecutivas:

1. **Imports y constantes globales**: incluye todos los módulos estándar, `tkinter` y `xlwt`, además de `DB_DIR`, `DB_NAME` y helpers de rutas para PyInstaller.
2. **Infraestructura de datos**: funciones como `get_base_path()`, `get_connection()`, el decorador `db_operation`, los helpers de exportación y migración (`_ensure_ciclo_schema`, `_migrar_ciclos_multi_plan`), así como `init_db()` y la invocación de `crear_backup_db()` para ejecutar verificaciones antes de levantar la UI.
3. **Servicios y reglas de negocio**: integra todos los CRUD, validaciones de horarios, utilitarios de backup y autenticación, manteniendo encabezados claros para cada dominio.
4. **Interfaz gráfica**: cierra el archivo con `ToolTip`, `aplicar_estilos_ttk`, los helpers de Treeview, la clase `App` y el bloque `if __name__ == "__main__":`, lo que facilita una futura extracción a módulos separados.

Este orden evita imports duplicados, deja evidente en qué sección agregar nueva lógica y garantiza que la base de datos esté lista antes de inicializar cualquier widget.
```

---

## 3. MODELO DE BASE DE DATOS

### 3.1 Diagrama Entidad-Relación

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   MATERIA   │      │  PLAN_ESTUDIO│      │    TURNO    │
├─────────────┤      ├──────────────┤      ├─────────────┤
│ id (PK)     │◄─┐   │ id (PK)      │◄─┐   │ id (PK)     │
│ nombre      │  │   │ nombre       │  │   │ nombre      │
│horas_seman. │  │   └──────────────┘  │   └─────────────┘
└─────────────┘  │                     │          ▲
                 │                     │          │
                 │   ┌──────────────┐  │          │
                 └───┤ PLAN_MATERIA │  │          │
                     ├──────────────┤  │          │
                     │ id (PK)      │  │   ┌──────┴──────┐
                     │ plan_id (FK) │──┘   │ TURNO_PLAN  │
                     │materia_id(FK)│      ├─────────────┤
                     └──────────────┘      │ id (PK)     │
                                           │ turno_id(FK)│
┌─────────────┐      ┌──────────────┐     │ plan_id (FK)│
│  PROFESOR   │      │     ANIO     │     └─────────────┘
├─────────────┤      ├──────────────┤
│ id (PK)     │      │ id (PK)      │     ┌─────────────┐
│ nombre      │      │ nombre       │     │  DIVISION   │
└─────────────┘      │ plan_id (FK) │     ├─────────────┤
       ▲             └──────────────┘     │ id (PK)     │
       │                     ▲            │ nombre      │
       │                     │            │ turno_id(FK)│
┌──────┴──────────┐  ┌───────┴────────┐  │ plan_id (FK)│
│PROFESOR_MATERIA │  │  ANIO_MATERIA  │  │ anio_id (FK)│
├─────────────────┤  ├────────────────┤  └─────────────┘
│ id (PK)         │  │ id (PK)        │         ▲
│profesor_id (FK) │  │ anio_id (FK)   │         │
│materia_id (FK)  │  │materia_id (FK) │         │
│ banca_horas     │  └────────────────┘         │
└─────────────────┘                             │
       ▲                                        │
       │                                        │
┌──────┴──────────┐                            │
│ PROFESOR_TURNO  │                            │
├─────────────────┤                            │
│ id (PK)         │                            │
│profesor_id (FK) │                            │
│ turno_id (FK)   │                            │
└─────────────────┘                            │
                                               │
                    ┌──────────────────────────┘
                    │
              ┌─────▼──────┐
              │   HORARIO  │
              ├────────────┤
              │ id (PK)    │
              │division_id │
              │ dia        │
              │ espacio    │
              │hora_inicio │
              │ hora_fin   │
              │materia_id  │
              │profesor_id │
              │ turno_id   │
              └────────────┘
                    ▲
                    │
         ┌──────────┴───────────┐
         │ TURNO_ESPACIO_HORA   │
         ├──────────────────────┤
         │ id (PK)              │
         │ turno_id (FK)        │
         │ espacio              │
         │ hora_inicio          │
         │ hora_fin             │
         └──────────────────────┘
```

### 3.2 Descripción de Tablas

#### 3.2.1 MATERIA

**Descripción:** Almacena las materias/obligaciones del plan de estudios.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Identificador único |
| `nombre` | TEXT | NOT NULL, UNIQUE | Nombre de la materia |
| `horas_semanales` | INTEGER | NOT NULL | Horas asignadas por semana |

**Índices:**
- PRIMARY KEY en `id`
- UNIQUE en `nombre`

**Ejemplo de Registro:**
```sql
INSERT INTO materia (nombre, horas_semanales) 
VALUES ('Matemática', 5);
```

#### 3.2.2 PROFESOR

**Descripción:** Almacena información del personal docente.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Identificador único |
| `nombre` | TEXT | NOT NULL, UNIQUE | Nombre completo del profesor |

**Índices:**
- PRIMARY KEY en `id`
- UNIQUE en `nombre`

**Ejemplo de Registro:**
```sql
INSERT INTO profesor (nombre) 
VALUES ('García López, Juan Carlos');
```

#### 3.2.3 PLAN_ESTUDIO

**Descripción:** Almacena los planes de estudio de la institución.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Identificador único |
| `nombre` | TEXT | NOT NULL, UNIQUE | Nombre del plan de estudios |

**Índices:**
- PRIMARY KEY en `id`
- UNIQUE en `nombre`

**Ejemplo de Registro:**
```sql
INSERT INTO plan_estudio (nombre) 
VALUES ('Bachiller en Ciencias Naturales');
```

#### 3.2.4 PLAN_MATERIA

**Descripción:** Relación muchos-a-muchos entre planes de estudio y materias.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Identificador único |
| `plan_id` | INTEGER | FOREIGN KEY → plan_estudio(id) | ID del plan de estudios |
| `materia_id` | INTEGER | FOREIGN KEY → materia(id) | ID de la materia |

**Índices:**
- PRIMARY KEY en `id`
- UNIQUE en (`plan_id`, `materia_id`)

**Ejemplo de Registro:**
```sql
-- Agregar "Matemática" al plan "Bachiller en Ciencias Naturales"
INSERT INTO plan_materia (plan_id, materia_id) 
VALUES (1, 1);
```

#### 3.2.5 ANIO

**Descripción:** Almacena los años/cursos de cada plan de estudios.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Identificador único |
| `nombre` | TEXT | NOT NULL | Nombre del año (ej: "1° Año") |
| `plan_id` | INTEGER | FOREIGN KEY → plan_estudio(id) | ID del plan de estudios |

**Índices:**
- PRIMARY KEY en `id`
- UNIQUE en (`nombre`, `plan_id`)

**Ejemplo de Registro:**
```sql
INSERT INTO anio (nombre, plan_id) 
VALUES ('1° Año', 1);
```

#### 3.2.6 ANIO_MATERIA

**Descripción:** Relación muchos-a-muchos entre años y materias.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Identificador único |
| `anio_id` | INTEGER | FOREIGN KEY → anio(id) | ID del año |
| `materia_id` | INTEGER | FOREIGN KEY → materia(id) | ID de la materia |

**Índices:**
- PRIMARY KEY en `id`
- UNIQUE en (`anio_id`, `materia_id`)

**Ejemplo de Registro:**
```sql
-- Asignar "Matemática" a "1° Año"
INSERT INTO anio_materia (anio_id, materia_id) 
VALUES (1, 1);
```

#### 3.2.7 TURNO

**Descripción:** Almacena los turnos escolares (mañana, tarde, noche).

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Identificador único |
| `nombre` | TEXT | NOT NULL, UNIQUE | Nombre del turno |

**Índices:**
- PRIMARY KEY en `id`
- UNIQUE en `nombre`

**Ejemplo de Registro:**
```sql
INSERT INTO turno (nombre) VALUES ('Mañana');
INSERT INTO turno (nombre) VALUES ('Tarde');
```

#### 3.2.8 TURNO_PLAN

**Descripción:** Relación muchos-a-muchos entre turnos y planes de estudio.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Identificador único |
| `turno_id` | INTEGER | FOREIGN KEY → turno(id) | ID del turno |
| `plan_id` | INTEGER | FOREIGN KEY → plan_estudio(id) | ID del plan de estudios |

**Índices:**
- PRIMARY KEY en `id`
- UNIQUE en (`turno_id`, `plan_id`)

**Ejemplo de Registro:**
```sql
-- El plan "Bachiller" se ofrece en turno "Mañana"
INSERT INTO turno_plan (turno_id, plan_id) 
VALUES (1, 1);
```

#### 3.2.9 PROFESOR_MATERIA

**Descripción:** Almacena la banca de horas de cada profesor por materia.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Identificador único |
| `profesor_id` | INTEGER | FOREIGN KEY → profesor(id) | ID del profesor |
| `materia_id` | INTEGER | FOREIGN KEY → materia(id) | ID de la materia |
| `banca_horas` | INTEGER | NOT NULL | Horas asignadas al profesor |

**Índices:**
- PRIMARY KEY en `id`
- UNIQUE en (`profesor_id`, `materia_id`)

**Ejemplo de Registro:**
```sql
-- Asignar 20 horas de "Matemática" al profesor
INSERT INTO profesor_materia (profesor_id, materia_id, banca_horas) 
VALUES (1, 1, 20);
```

#### 3.2.10 PROFESOR_TURNO

**Descripción:** Relación muchos-a-muchos entre profesores y turnos.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Identificador único |
| `profesor_id` | INTEGER | FOREIGN KEY → profesor(id) | ID del profesor |
| `turno_id` | INTEGER | FOREIGN KEY → turno(id) | ID del turno |

**Índices:**
- PRIMARY KEY en `id`
- UNIQUE en (`profesor_id`, `turno_id`)

**Ejemplo de Registro:**
```sql
-- Asignar profesor al turno "Mañana"
INSERT INTO profesor_turno (profesor_id, turno_id) 
VALUES (1, 1);
```

#### 3.2.11 DIVISION

**Descripción:** Almacena las divisiones/cursos de la institución.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Identificador único |
| `nombre` | TEXT | NOT NULL | Nombre de la división (ej: "A", "B") |
| `turno_id` | INTEGER | FOREIGN KEY → turno(id) | ID del turno |
| `plan_id` | INTEGER | FOREIGN KEY → plan_estudio(id) | ID del plan de estudios |
| `anio_id` | INTEGER | FOREIGN KEY → anio(id) | ID del año/curso |

**Índices:**
- PRIMARY KEY en `id`
- UNIQUE en (`nombre`, `turno_id`, `plan_id`, `anio_id`)

**Ejemplo de Registro:**
```sql
-- División "A" de 1° Año Bachiller turno Mañana
INSERT INTO division (nombre, turno_id, plan_id, anio_id) 
VALUES ('A', 1, 1, 1);
```

#### 3.2.12 HORARIO

**Descripción:** **Tabla principal** que almacena todos los horarios (tanto por curso como por profesor).

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Identificador único |
| `division_id` | INTEGER | FOREIGN KEY → division(id), NULLABLE | ID de la división (puede ser NULL en horarios de profesor) |
| `dia` | TEXT | NOT NULL | Día de la semana |
| `espacio` | INTEGER | NOT NULL | Número de espacio horario (1-8) |
| `hora_inicio` | TEXT | NULLABLE | Hora de inicio (formato HH:MM) |
| `hora_fin` | TEXT | NULLABLE | Hora de fin (formato HH:MM) |
| `materia_id` | INTEGER | FOREIGN KEY → materia(id), NULLABLE | ID de la materia |
| `profesor_id` | INTEGER | FOREIGN KEY → profesor(id), NULLABLE | ID del profesor |
| `turno_id` | INTEGER | FOREIGN KEY → turno(id), NULLABLE | ID del turno |

**Índices:**
- PRIMARY KEY en `id`
- UNIQUE en (`division_id`, `dia`, `espacio`) cuando `division_id` IS NOT NULL

**Notas Importantes:**
- Esta tabla sirve para **ambas vistas**: horarios por curso y horarios por profesor
- Cuando se asigna desde vista "Por Curso": `division_id` es obligatorio
- Cuando se asigna desde vista "Por Profesor": `division_id` puede ser NULL
- `turno_id` se agregó en versión 0.9 para sincronización entre vistas
- Las horas pueden ser NULL para permitir espacios sin horario definido

**Ejemplo de Registro (Vista por Curso):**
```sql
-- Matemática con el profesor García en 1°A, Lunes, 1ª hora
INSERT INTO horario (division_id, dia, espacio, hora_inicio, hora_fin, materia_id, profesor_id, turno_id) 
VALUES (1, 'Lunes', 1, '08:00', '08:45', 1, 1, 1);
```

**Ejemplo de Registro (Vista por Profesor):**
```sql
-- Profesor García disponible Martes 2ª hora sin división asignada
INSERT INTO horario (division_id, dia, espacio, hora_inicio, hora_fin, materia_id, profesor_id, turno_id) 
VALUES (NULL, 'Martes', 2, '08:45', '09:30', NULL, 1, 1);
```

#### 3.2.13 TURNO_ESPACIO_HORA

**Descripción:** Almacena la configuración de horas por defecto para cada espacio horario de un turno.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Identificador único |
| `turno_id` | INTEGER | FOREIGN KEY → turno(id) | ID del turno |
| `espacio` | INTEGER | NOT NULL | Número de espacio horario (1-8) |
| `hora_inicio` | TEXT | NULLABLE | Hora de inicio por defecto |
| `hora_fin` | TEXT | NULLABLE | Hora de fin por defecto |

**Índices:**
- PRIMARY KEY en `id`
- UNIQUE en (`turno_id`, `espacio`)

**Ejemplo de Registro:**
```sql
-- Configurar 1ª hora del turno Mañana: 08:00-08:45
INSERT INTO turno_espacio_hora (turno_id, espacio, hora_inicio, hora_fin) 
VALUES (1, 1, '08:00', '08:45');
```

### 3.3 Relaciones y Cardinalidades

```
PLAN_ESTUDIO ──┬── (1:N) ──> PLAN_MATERIA ──> (N:1) ──┬── MATERIA
               │                                       │
               └── (1:N) ──> ANIO ──> (1:N) ──> ANIO_MATERIA ──> (N:1) ──┘

TURNO ──┬── (1:N) ──> TURNO_PLAN ──> (N:1) ──> PLAN_ESTUDIO
        │
        └── (1:N) ──> DIVISION ──> (N:1) ──┬── PLAN_ESTUDIO
                                            └── ANIO

PROFESOR ──┬── (1:N) ──> PROFESOR_MATERIA ──> (N:1) ──> MATERIA
           │
           └── (1:N) ──> PROFESOR_TURNO ──> (N:1) ──> TURNO

HORARIO ──┬── (N:1) ──> DIVISION
          ├── (N:1) ──> MATERIA
          ├── (N:1) ──> PROFESOR
          └── (N:1) ──> TURNO

TURNO_ESPACIO_HORA ──> (N:1) ──> TURNO
```

### 3.4 Integridad Referencial

El sistema utiliza **integridad referencial de SQLite** con las siguientes políticas:

- **ON DELETE:** Por defecto CASCADE (no explícito en CREATE TABLE)
- **ON UPDATE:** Por defecto CASCADE

**Nota:** SQLite no valida claves foráneas por defecto. Para habilitarlas:
```sql
PRAGMA foreign_keys = ON;
```

---

## 4. MÓDULOS Y COMPONENTES

### 4.1 Organización del Código

El archivo `SistemaEscolar_v1.py` está organizado en las siguientes secciones:

```python
# 1. ESTILOS Y CONFIGURACIÓN UI (Líneas 1-20)
def aplicar_estilos_ttk()

# 2. IMPORTS Y CONFIGURACIÓN (Líneas 21-30)
import sqlite3, os, sys, typing, tkinter, ttk, messagebox

# 3. BASE DE DATOS - INICIALIZACIÓN (Líneas 31-180)
- get_base_path()
- get_connection()
- db_operation decorator
- init_db()

# 4. OPERACIONES CRUD GENÉRICAS (Líneas 181-220)
- crear_entidad()
- obtener_entidades()
- actualizar_entidad()
- eliminar_entidad()

# 5. CRUD MATERIAS (Líneas 221-280)
# 6. CRUD PROFESORES (Líneas 281-390)
# 7. CRUD BANCA DE HORAS (Líneas 391-450)
# 8. CRUD AÑOS (Líneas 451-510)
# 9. CRUD PLANES DE ESTUDIO (Líneas 511-600)
# 10. CRUD TURNOS (Líneas 601-700)
# 11. CRUD DIVISIONES (Líneas 701-800)
# 12. CRUD HORARIOS (Líneas 801-1100)
# 13. HELPERS CONFIGURACIÓN (Líneas 1101-1200)

# 14. INTERFAZ GRÁFICA - COMPONENTES (Líneas 1201-1800)
- ToolTip class
- crear_treeview()
- recargar_treeview()
- autocompletar_combobox()

# 15. INTERFAZ GRÁFICA - VENTANA PRINCIPAL (Líneas 1801-2000)
- App class
- _crear_menu()
- _crear_frame_principal()
- limpiar_frame()

# 16. VISTAS ESPECÍFICAS (Líneas 2001-3300)
- mostrar_materias()
- mostrar_profesores()
- mostrar_divisiones()
- mostrar_planes()
- mostrar_turnos()
- mostrar_horarios_curso()
- mostrar_horarios_profesor()

# 17. PUNTO DE ENTRADA (Líneas 3301-3307)
if __name__ == "__main__"
```

### 4.2 Decorador @db_operation

**Ubicación:** Líneas 38-48

**Propósito:** Centraliza el manejo de conexiones y transacciones de base de datos.

```python
def db_operation(func):
    def wrapper(*args, **kwargs):
        conn = get_connection()
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except sqlite3.IntegrityError as e:
            raise Exception(str(e))
        finally:
            conn.close()
    return wrapper
```

**Características:**
- ✅ Abre conexión automáticamente
- ✅ Ejecuta la función decorada
- ✅ Hace commit si la operación es exitosa
- ✅ Cierra conexión siempre (en finally)
- ✅ Convierte IntegrityError a Exception genérica

**Uso:**
```python
@db_operation
def crear_entidad(conn, tabla, campos, valores):
    placeholders = ','.join(['?']*len(valores))
    campos_str = ','.join(campos)
    conn.execute(f'INSERT INTO {tabla} ({campos_str}) VALUES ({placeholders})', valores)
```

### 4.3 Funciones CRUD Genéricas

**Ubicación:** Líneas 50-75

Estas funciones proporcionan operaciones CRUD reutilizables para tablas simples:

#### 4.3.1 crear_entidad()

```python
@db_operation
def crear_entidad(conn, tabla, campos, valores):
    """Inserta un registro en la tabla especificada."""
    placeholders = ','.join(['?']*len(valores))
    campos_str = ','.join(campos)
    conn.execute(f'INSERT INTO {tabla} ({campos_str}) VALUES ({placeholders})', valores)
```

**Parámetros:**
- `tabla` (str): Nombre de la tabla
- `campos` (list): Lista de nombres de campos
- `valores` (list): Lista de valores correspondientes

**Ejemplo:**
```python
crear_entidad('materia', ['nombre', 'horas_semanales'], ['Matemática', 5])
```

#### 4.3.2 obtener_entidades()

```python
@db_operation
def obtener_entidades(conn, tabla, campos):
    """Obtiene todos los registros de una tabla."""
    c = conn.cursor()
    c.execute(f'SELECT {','.join(campos)} FROM {tabla}')
    return [dict(zip(campos, row)) for row in c.fetchall()]
```

**Retorna:** Lista de diccionarios con los datos

**Ejemplo:**
```python
materias = obtener_entidades('materia', ['id', 'nombre', 'horas_semanales'])
# [{'id': 1, 'nombre': 'Matemática', 'horas_semanales': 5}, ...]
```

#### 4.3.3 actualizar_entidad()

```python
@db_operation
def actualizar_entidad(conn, tabla, campos, valores, id_campo, id_valor):
    """Actualiza un registro por su ID."""
    set_str = ','.join([f'{campo}=?' for campo in campos])
    conn.execute(f'UPDATE {tabla} SET {set_str} WHERE {id_campo}=?', (*valores, id_valor))
```

**Ejemplo:**
```python
actualizar_entidad('materia', ['nombre', 'horas_semanales'], ['Física', 6], 'id', 1)
```

#### 4.3.4 eliminar_entidad()

```python
@db_operation
def eliminar_entidad(conn, tabla, id_campo, id_valor):
    """Elimina un registro por su ID."""
    conn.execute(f'DELETE FROM {tabla} WHERE {id_campo}=?', (id_valor,))
```

**Ejemplo:**
```python
eliminar_entidad('materia', 'id', 1)
```

---

## 5. API DE FUNCIONES

### 5.1 Gestión de Materias

#### 5.1.1 crear_materia()

**Ubicación:** Líneas 221-227

```python
def crear_materia(nombre: str, horas: int) -> None
```

**Descripción:** Crea una nueva materia en el sistema.

**Parámetros:**
- `nombre` (str): Nombre de la materia (debe ser único)
- `horas` (int): Horas semanales asignadas (inicialmente se pasa 0)

**Excepciones:**
- `Exception`: Si ya existe una materia con ese nombre

**Ejemplo:**
```python
try:
    crear_materia('Matemática', 0)
except Exception as e:
    print(f"Error: {e}")
```

#### 5.1.2 obtener_materias()

```python
def obtener_materias() -> List[Dict[str, Any]]
```

**Descripción:** Obtiene todas las materias del sistema.

**Retorna:** Lista de diccionarios con estructura:
```python
[
    {'id': 1, 'nombre': 'Matemática', 'horas_semanales': 5},
    {'id': 2, 'nombre': 'Física', 'horas_semanales': 4}
]
```

#### 5.1.3 actualizar_materia()

```python
def actualizar_materia(id_: int, nombre: str, horas: int) -> None
```

**Descripción:** Actualiza los datos de una materia existente.

**Parámetros:**
- `id_` (int): ID de la materia a actualizar
- `nombre` (str): Nuevo nombre
- `horas` (int): Nuevas horas semanales

#### 5.1.4 eliminar_materia()

```python
def eliminar_materia(id_: int) -> None
```

**Descripción:** Elimina una materia del sistema.

**Nota:** Elimina en cascada las relaciones con planes y profesores.

### 5.2 Gestión de Profesores

#### 5.2.1 crear_profesor()

```python
def crear_profesor(nombre: str) -> None
```

**Descripción:** Crea un nuevo profesor en el sistema.

**Parámetros:**
- `nombre` (str): Nombre completo del profesor (debe ser único)

**Excepciones:**
- `Exception`: Si ya existe un profesor con ese nombre

#### 5.2.2 obtener_profesores()

```python
def obtener_profesores() -> List[Dict[str, Any]]
```

**Descripción:** Obtiene todos los profesores del sistema.

**Retorna:**
```python
[
    {'id': 1, 'nombre': 'García López, Juan Carlos'},
    {'id': 2, 'nombre': 'Rodríguez, María Elena'}
]
```

#### 5.2.3 actualizar_profesor()

```python
def actualizar_profesor(id_: int, nombre: str) -> None
```

#### 5.2.4 eliminar_profesor()

```python
def eliminar_profesor(id_: int) -> None
```

**Descripción:** Elimina un profesor del sistema.

**Nota:** También elimina:
- Turnos asignados (`profesor_turno`)
- Banca de horas (`profesor_materia`)

**Implementación:**
```python
@db_operation
def _eliminar_profesor(conn, id_):
    conn.execute('DELETE FROM profesor_turno WHERE profesor_id=?', (id_,))
    conn.execute('DELETE FROM profesor WHERE id=?', (id_,))
```

### 5.3 Gestión de Banca de Horas

#### 5.3.1 asignar_banca_profesor()

```python
def asignar_banca_profesor(profesor_id: int, materia_id: int, banca_horas: int) -> None
```

**Descripción:** Asigna una materia a un profesor con una cantidad de horas inicial.

**Parámetros:**
- `profesor_id` (int): ID del profesor
- `materia_id` (int): ID de la materia
- `banca_horas` (int): Cantidad de horas (generalmente se inicia en 0)

**Excepciones:**
- `Exception`: Si el profesor ya tiene asignada esa materia

**Ejemplo:**
```python
# Asignar Matemática al profesor con 0 horas iniciales
asignar_banca_profesor(1, 1, 0)
```

#### 5.3.2 obtener_banca_profesor()

```python
def obtener_banca_profesor(profesor_id: int) -> List[Dict[str, Any]]
```

**Descripción:** Obtiene todas las materias asignadas a un profesor con sus horas.

**Retorna:**
```python
[
    {'id': 1, 'materia': 'Matemática', 'banca_horas': 15},
    {'id': 2, 'materia': 'Física', 'banca_horas': 8}
]
```

#### 5.3.3 actualizar_banca_profesor()

```python
def actualizar_banca_profesor(pm_id: int, banca_horas: int) -> None
```

**Nota:** Las horas se actualizan automáticamente al asignar/eliminar horarios.

#### 5.3.4 eliminar_banca_profesor()

```python
def eliminar_banca_profesor(pm_id: int) -> None
```

**Descripción:** Elimina la asignación de una materia a un profesor.

### 5.4 Gestión de Turnos de Profesor

#### 5.4.1 asignar_turno_a_profesor()

```python
def asignar_turno_a_profesor(profesor_id: int, turno_id: int) -> None
```

**Descripción:** Asigna un turno a un profesor.

**Excepciones:**
- `Exception`: Si el profesor ya tiene asignado ese turno

#### 5.4.2 quitar_turno_a_profesor()

```python
def quitar_turno_a_profesor(profesor_id: int, turno_id: int) -> None
```

#### 5.4.3 obtener_turnos_de_profesor()

```python
def obtener_turnos_de_profesor(profesor_id: int) -> List[Dict[str, Any]]
```

**Retorna:**
```python
[
    {'id': 1, 'nombre': 'Mañana'},
    {'id': 2, 'nombre': 'Tarde'}
]
```

#### 5.4.4 obtener_profesores_por_turno()

```python
def obtener_profesores_por_turno(turno_id: int) -> List[Dict[str, Any]]
```

**Descripción:** Obtiene todos los profesores asignados a un turno específico.

### 5.5 Gestión de Planes de Estudio

#### 5.5.1 crear_plan()

```python
def crear_plan(nombre: str) -> None
```

**Excepciones:**
- `Exception`: Si ya existe un plan con ese nombre

#### 5.5.2 obtener_planes()

```python
def obtener_planes() -> List[Dict[str, Any]]
```

#### 5.5.3 eliminar_plan()

```python
def eliminar_plan(id_: int) -> None
```

**Nota:** Elimina en cascada: años, relaciones plan-materia, turno-plan

#### 5.5.4 agregar_materia_a_plan()

```python
def agregar_materia_a_plan(plan_id: int, materia_id: int) -> None
```

**Descripción:** Asocia una materia a un plan de estudios.

**Excepciones:**
- `Exception`: Si la materia ya está en el plan

#### 5.5.5 quitar_materia_de_plan()

```python
def quitar_materia_de_plan(plan_id: int, materia_id: int) -> None
```

#### 5.5.6 obtener_materias_de_plan()

```python
def obtener_materias_de_plan(plan_id: int) -> List[Dict[str, Any]]
```

**Retorna:**
```python
[
    {'id': 1, 'nombre': 'Matemática'},
    {'id': 2, 'nombre': 'Física'}
]
```

### 5.6 Gestión de Años/Cursos

#### 5.6.1 crear_anio()

```python
def crear_anio(nombre: str, plan_id: int) -> None
```

**Parámetros:**
- `nombre` (str): Nombre del año (ej: "1° Año", "2° Año")
- `plan_id` (int): ID del plan de estudios al que pertenece

**Excepciones:**
- `Exception`: Si ya existe un año con ese nombre en el plan

#### 5.6.2 obtener_anios()

```python
def obtener_anios(plan_id: int) -> List[Dict[str, Any]]
```

**Descripción:** Obtiene todos los años de un plan de estudios específico.

#### 5.6.3 eliminar_anio()

```python
def eliminar_anio(id_: int) -> None
```

#### 5.6.4 agregar_materia_a_anio()

```python
def agregar_materia_a_anio(anio_id: int, materia_id: int) -> None
```

**Descripción:** Asigna una materia a un año específico del plan.

#### 5.6.5 quitar_materia_de_anio()

```python
def quitar_materia_de_anio(anio_id: int, materia_id: int) -> None
```

#### 5.6.6 obtener_materias_de_anio()

```python
def obtener_materias_de_anio(anio_id: int) -> List[Dict[str, Any]]
```

### 5.7 Gestión de Turnos

#### 5.7.1 crear_turno()

```python
def crear_turno(nombre: str) -> None
```

**Excepciones:**
- `Exception`: Si ya existe un turno con ese nombre

#### 5.7.2 obtener_turnos()

```python
def obtener_turnos() -> List[Dict[str, Any]]
```

#### 5.7.3 eliminar_turno()

```python
def eliminar_turno(id_: int) -> None
```

#### 5.7.4 agregar_plan_a_turno()

```python
def agregar_plan_a_turno(turno_id: int, plan_id: int) -> None
```

**Descripción:** Asocia un plan de estudios a un turno.

**Excepciones:**
- `Exception`: Si el plan ya está en el turno

#### 5.7.5 quitar_plan_de_turno()

```python
def quitar_plan_de_turno(turno_id: int, plan_id: int) -> None
```

#### 5.7.6 obtener_planes_de_turno()

```python
def obtener_planes_de_turno(turno_id: int) -> List[Dict[str, Any]]
```

**Descripción:** Obtiene los planes de estudio asociados a un turno (sin duplicados).

### 5.8 Gestión de Divisiones/Cursos

#### 5.8.1 crear_division() - Nota Especial

```python
def crear_division(nombre: str) -> None
```

**⚠️ IMPORTANTE:** Esta función está deprecated. Para crear divisiones se debe usar el formulario de la UI que requiere turno_id, plan_id y anio_id.

#### 5.8.2 obtener_divisiones()

```python
def obtener_divisiones() -> List[Dict[str, Any]]
```

**Retorna:**
```python
[
    {
        'id': 1, 
        'nombre': 'A', 
        'turno_id': 1, 
        'plan_id': 1, 
        'anio_id': 1
    }
]
```

#### 5.8.3 actualizar_division()

```python
def actualizar_division(id_: int, nombre: str) -> None
```

**Nota:** Solo actualiza el nombre. Para cambiar turno/plan/año usar UI.

#### 5.8.4 eliminar_division()

```python
def eliminar_division(id_: int) -> None
```

### 5.9 Gestión de Horarios (Vista por Curso)

#### 5.9.1 Motor unificado de horarios (`_upsert_horario`)

Desde la refactorización de noviembre 2025 ambas vistas (por curso y por profesor) delegan sus escrituras a una única función interna `_upsert_horario(conn, division_id, dia, espacio, hora_inicio, hora_fin, materia_id, profesor_id, turno_id)`. Este motor central aplica exactamente las mismas validaciones y ajustes de contadores sin importar desde qué vista se originó el cambio, evitando divergencias y los antiguos errores de constraint UNIQUE.

##### Helpers involucrados
- `_obtener_turno_de_division(conn, division_id)`: asegura que toda operación utilice el turno real vinculado a la división y rechaza combinaciones inválidas.
- `_obtener_slot_horario(conn, division_id, dia, espacio)`: localiza el registro existente (si lo hay) para decidir entre UPDATE o INSERT.
- `_validar_profesor_para_slot(conn, profesor_id, turno_id, materia_id, dia, espacio, division_id, horario_existente_id)`: valida banca de horas, pertenencia al turno y evita superposiciones del docente.
- `_ajustar_contadores(conn, old_profesor_id, old_materia_id, new_profesor_id, new_materia_id)`: sincroniza `materia.horas_semanales` y `profesor_materia.banca_horas` únicamente cuando hay cambios reales.
- `_upsert_horario(...)`: combina todo lo anterior, ejecuta el INSERT/UPDATE y devuelve el `id` del registro afectado.

> Importante: cualquier excepción lanzada en estos helpers se propaga hacia la vista correspondiente, por lo que los mensajes que ve el usuario son consistentes en ambas pantallas.

#### 5.9.2 crear_horario()

**Ubicación:** Líneas 801-850

```python
def crear_horario(
    division_id: int, 
    dia: str, 
    espacio: int, 
    hora_inicio: str, 
    hora_fin: str, 
    materia_id: int, 
    profesor_id: int, 
    turno_id: int = None
) -> None
```

**Descripción:** Envuelve a `_upsert_horario` para crear o actualizar un horario de la división seleccionada. Al reutilizar el mismo motor que la vista por profesor garantiza que los contadores y validaciones sean idénticos.

**Parámetros:**
- `division_id` (int): ID de la división
- `dia` (str): Día de la semana ("Lunes", "Martes", etc.)
- `espacio` (int): Número de espacio horario (1-8)
- `hora_inicio` (str): Hora de inicio (formato "HH:MM")
- `hora_fin` (str): Hora de fin (formato "HH:MM")
- `materia_id` (int): ID de la materia (puede ser None)
- `profesor_id` (int): ID del profesor (puede ser None)
- `turno_id` (int, opcional): ID del turno (se calcula automáticamente si es None)

**Validaciones (delegadas en `_upsert_horario`):**
1. Comprueba que la división pertenezca al turno indicado (o lo infiere automáticamente).
2. Evita superposición del profesor en el mismo día/espacio dentro del turno.
3. Verifica que el profesor tenga la materia en su banca antes de ajustar contadores.
4. Rechaza duplicados sobre la clave única `(division_id, dia, espacio)` y devuelve un mensaje claro para la UI.
5. Permite horas vacías (`None`) y respeta los valores por defecto de turno si corresponden.

**Efectos Secundarios:**
- Incrementa `horas_semanales` de la materia en 1
- Incrementa `banca_horas` del profesor para esa materia en 1

**Excepciones:**
- `Exception`: Si el profesor ya está asignado en ese horario
- `Exception`: Si el profesor no tiene la materia asignada
- `Exception`: Si la división no existe

**Ejemplo:**
```python
# Asignar Matemática con profesor García en 1°A, Lunes, 1ª hora
crear_horario(
    division_id=1,
    dia='Lunes',
    espacio=1,
    hora_inicio='08:00',
    hora_fin='08:45',
    materia_id=1,
    profesor_id=1,
    turno_id=1
)
```

#### 5.9.3 obtener_horarios()

```python
def obtener_horarios(division_id: int) -> List[Dict[str, Any]]
```

**Descripción:** Obtiene todos los horarios de una división específica.

**Retorna:**
```python
[
    {
        'id': 1,
        'dia': 'Lunes',
        'espacio': 1,
        'hora_inicio': '08:00',
        'hora_fin': '08:45',
        'materia': 'Matemática',
        'profesor': 'García López, Juan'
    }
]
```

#### 5.9.4 eliminar_horario()

```python
def eliminar_horario(id_: int) -> None
```

**Descripción:** Elimina un horario específico.

**Efectos Secundarios:**
- Decrementa `horas_semanales` de la materia en 1
- Decrementa `banca_horas` del profesor para esa materia en 1

**Implementación:**
```python
def eliminar_horario(id_: int):
    conn = get_connection()
    c = conn.cursor()
    # Obtener datos antes de eliminar
    c.execute('SELECT materia_id, profesor_id FROM horario WHERE id=?', (id_,))
    row = c.fetchone()
    if row:
        materia_id, profesor_id = row
        # Restar horas
        if materia_id is not None:
            c.execute('UPDATE materia SET horas_semanales = horas_semanales - 1 WHERE id=?', (materia_id,))
        if profesor_id is not None and materia_id is not None:
            c.execute('UPDATE profesor_materia SET banca_horas = banca_horas - 1 WHERE profesor_id=? AND materia_id=?', (profesor_id, materia_id))
    # Eliminar el horario
    c.execute('DELETE FROM horario WHERE id=?', (id_,))
    conn.commit()
    conn.close()
```

### 5.10 Gestión de Horarios (Vista por Profesor)

#### 5.10.1 crear_horario_profesor()

```python
def crear_horario_profesor(
    profesor_id: int, 
    turno_id: int, 
    dia: str, 
    espacio: int, 
    hora_inicio: str, 
    hora_fin: str, 
    division_id: int = None, 
    materia_id: int = None
) -> None
```

**Descripción:** Llama a `_upsert_horario` con los parámetros seleccionados en la vista docente, por lo que crea o actualiza el mismo registro usado por la vista por curso.

**Parámetros:**
- `profesor_id` (int): ID del profesor
- `turno_id` (int): ID del turno
- `dia` (str): Día de la semana
- `espacio` (int): Número de espacio horario (1-8)
- `hora_inicio` (str): Hora de inicio (formato "HH:MM")
- `hora_fin` (str): Hora de fin (formato "HH:MM")
- `division_id` (int, opcional): ID de la división (puede ser None)
- `materia_id` (int, opcional): ID de la materia (puede ser None)

**Validaciones (compartidas con `crear_horario()`):**
1. Requiere que la división pertenezca al turno (se obtiene del propio registro si el parámetro es `None`).
2. Comprueba que el profesor esté habilitado para el turno.
3. Verifica banca de horas antes de incrementar contadores.
4. Garantiza que la división no tenga otro profesor en el mismo `dia/espacio`.
5. Bloquea superposiciones del profesor en todo el turno.

**Excepciones:**
- `Exception`: Si el profesor no está asignado al turno
- `Exception`: Si el profesor no tiene la materia asignada
- `Exception`: Si la división no pertenece al turno
- `Exception`: Si ya existe horario para esa división en ese día/espacio
- `Exception`: Si el profesor ya tiene horario asignado en ese día/espacio

**Nota:** Como ambas vistas llaman al mismo motor, los mensajes de error y el ajuste de contadores son exactamente los mismos para usuarios de la vista por curso y por profesor.

#### 5.10.2 obtener_horarios_profesor()

```python
def obtener_horarios_profesor(profesor_id: int, turno_id: int) -> List[Dict[str, Any]]
```

**Descripción:** Obtiene todos los horarios de un profesor en un turno específico.

**Retorna:**
```python
[
    {
        'id': 1,
        'dia': 'Lunes',
        'espacio': 1,
        'hora_inicio': '08:00',
        'hora_fin': '08:45',
        'materia': 'Matemática',
        'division': '1°A'
    }
]
```

#### 5.10.3 eliminar_horario_profesor()

```python
def eliminar_horario_profesor(id_: int) -> None
```

**Descripción:** Elimina un horario por su ID.

**Nota:** Esta función internamente llama a `eliminar_horario(id_)`, por lo que el cambio se refleja en ambas vistas.

### 5.11 Configuración de Horas por Turno

#### 5.11.1 obtener_turno_espacio_hora()

```python
def obtener_turno_espacio_hora(turno_id: int, espacio: int) -> Optional[Dict[str, str]]
```

**Descripción:** Obtiene la configuración de horas por defecto para un espacio de un turno.

**Retorna:**
```python
{
    'hora_inicio': '08:00',
    'hora_fin': '08:45'
}
# o None si no existe configuración
```

#### 5.11.2 set_turno_espacio_hora()

```python
def set_turno_espacio_hora(
    turno_id: int, 
    espacio: int, 
    hora_inicio: str, 
    hora_fin: str
) -> None
```

**Descripción:** Configura las horas por defecto para un espacio de un turno.

**Comportamiento Especial:**
- Si `hora_inicio` y `hora_fin` están vacíos, elimina el registro
- Si ya existe configuración, la reemplaza (INSERT OR REPLACE)

**Ejemplo:**
```python
# Configurar 1ª hora del turno Mañana
set_turno_espacio_hora(1, 1, '08:00', '08:45')

# Eliminar configuración
set_turno_espacio_hora(1, 1, '', '')
```

#### 5.11.3 eliminar_turno_espacio_hora()

```python
def eliminar_turno_espacio_hora(turno_id: int, espacio: int) -> None
```

**Descripción:** Elimina la configuración de horas para un espacio específico.

### 5.12 Funciones Helper de UI

#### 5.12.1 autocompletar_combobox()

**Ubicación:** Líneas 650-670

```python
def autocompletar_combobox(
    combobox: ttk.Combobox, 
    valores: List[str], 
    incluir_vacio: bool = True
) -> bool
```

**Descripción:** Configura un combobox con valores y lo autocompleta si solo hay una opción.

**Parámetros:**
- `combobox` (ttk.Combobox): Widget combobox a configurar
- `valores` (List[str]): Lista de valores para el combobox
- `incluir_vacio` (bool): Si True, incluye opción vacía al inicio

**Comportamiento:**
- Si hay 0 valores: deshabilita el combobox
- Si hay 1 valor y `incluir_vacio=False`: selecciona automáticamente ese valor
- Si hay múltiples valores: habilita para selección manual

**Retorna:** `False` (para compatibilidad histórica)

**Ejemplo:**
```python
materias = ['Matemática', 'Física', 'Química']
autocompletar_combobox(cb_materia, materias, incluir_vacio=False)
# Si solo hay una materia, la selecciona automáticamente
```

#### 5.12.2 crear_treeview()

```python
def crear_treeview(
    parent: tk.Widget, 
    columnas: Tuple[str], 
    headings: Tuple[str], 
    height: int = 10
) -> ttk.Treeview
```

**Descripción:** Crea un TreeView con scrollbars configuradas.

**Parámetros:**
- `parent` (tk.Widget): Widget contenedor
- `columnas` (Tuple[str]): Nombres de las columnas
- `headings` (Tuple[str]): Encabezados visibles
- `height` (int): Altura en filas (default: 10)

**Retorna:** Widget `ttk.Treeview` configurado

**Ejemplo:**
```python
frame = ttk.Frame(ventana)
tree = crear_treeview(
    frame, 
    ('Nombre', 'Horas'), 
    ('Nombre', 'Horas Semanales'),
    height=15
)
```

#### 5.12.3 recargar_treeview()

```python
def recargar_treeview(
    tree: ttk.Treeview, 
    datos: List[Dict[str, Any]], 
    campos: List[str]
) -> None
```

**Descripción:** Recarga los datos de un TreeView limpiando el contenido anterior.

**Parámetros:**
- `tree` (ttk.Treeview): TreeView a recargar
- `datos` (List[Dict]): Lista de diccionarios con los datos
- `campos` (List[str]): Nombres de campos a mostrar

**Ejemplo:**
```python
materias = obtener_materias()
recargar_treeview(tree_materias, materias, ['nombre', 'horas_semanales'])
```

---

## 6. INTERFAZ DE USUARIO

### 6.1 Estructura de la Interfaz

```
┌────────────────────────────────────────────────────────┐
│  Gestión de Horarios Escolares                    [_][□][X]
├────────────────────────────────────────────────────────┤
│  [Plan de estudios ▼] [Turnos ▼] [Personal ▼]         │
│  [Cursos ▼] [Gestión de horarios ▼]                   │
├────────────────────────────────────────────────────────┤
│                                                        │
│              [Frame Principal Dinámico]                │
│                                                        │
│  (Contenido cambia según la vista seleccionada)       │
│                                                        │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### 6.2 Menú Principal

El sistema cuenta con 5 menús principales:

#### 6.2.1 Menú "Plan de estudios"

```
Plan de estudios
├─ Gestionar Materias/Obligaciones
├─ ───────────────────────────────
└─ Gestionar Planes de Estudio
```

**Opciones:**
1. **Gestionar Materias/Obligaciones:** CRUD de materias
2. **Gestionar Planes de Estudio:** CRUD de planes y sus materias

#### 6.2.2 Menú "Turnos"

```
Turnos
└─ Gestionar Turnos
```

**Opciones:**
1. **Gestionar Turnos:** CRUD de turnos y asignación de planes

#### 6.2.3 Menú "Personal"

```
Personal
└─ Gestionar personal
```

**Opciones:**
1. **Gestionar personal:** CRUD de profesores, banca de horas y turnos

#### 6.2.4 Menú "Cursos"

```
Cursos
└─ Gestionar Cursos
```

**Opciones:**
1. **Gestionar Cursos:** CRUD de divisiones/cursos

#### 6.2.5 Menú "Gestión de horarios"

```
Gestión de horarios
├─ Por curso
└─ Por profesor
```

**Opciones:**
1. **Por curso:** Vista de horarios por división/curso
2. **Por profesor:** Vista de horarios por profesor

### 6.3 Componentes Reutilizables

#### 6.3.1 Clase ToolTip

**Ubicación:** Líneas 728-752

**Descripción:** Crea tooltips (mensajes emergentes) al pasar el mouse sobre un widget.

```python
class ToolTip:
    """Crear un tooltip para un widget dado"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)
```

**Características:**
- Aparece al hacer hover sobre el widget
- Desaparece al quitar el mouse
- Fondo amarillo claro (#ffffe0)
- Borde sólido
- Fuente Segoe UI 9pt

**Uso:**
```python
label = ttk.Label(frame, text='Buscar agente:')
ToolTip(label, 
        "Buscar agente:\n"
        "• Escribe para filtrar\n"
        "• Enter: selecciona primera coincidencia\n"
        "• Esc / Backspace: limpiar campo")
```

#### 6.3.2 Estilos TTK

**Ubicación:** Líneas 1-20

**Descripción:** Aplica estilos personalizados a los widgets TTK.

```python
def aplicar_estilos_ttk():
    style = ttk.Style()
    style.theme_use('clam')
    
    # Estilos generales
    style.configure('.', background='#f4f6fa', font=('Segoe UI', 10))
    
    # Labels
    style.configure('TLabel', background='#f4f6fa', font=('Segoe UI', 10))
    
    # Botones
    style.configure('TButton', 
                    font=('Segoe UI', 10, 'bold'), 
                    padding=6, 
                    relief='flat', 
                    background='#e0e7ef')
    style.map('TButton', background=[('active', '#d0d7e7')])
    
    # Treeview
    style.configure('Treeview', 
                    font=('Segoe UI', 10), 
                    rowheight=26, 
                    background='#ffffff')
    style.configure('Treeview.Heading', 
                    font=('Segoe UI', 10, 'bold'), 
                    background='#e0e7ef')
    style.map('Treeview', background=[('selected', '#b3d1ff')])
```

**Paleta de Colores:**
- Fondo principal: `#f4f6fa` (Gris azulado muy claro)
- Botones: `#e0e7ef` (Gris azulado claro)
- Botones activos: `#d0d7e7` (Gris azulado medio)
- Selección: `#b3d1ff` (Azul claro)
- Texto sobre fondo oscuro: `#222` (Negro suave)
- Encabezados: `#2a3a4a` (Gris azulado oscuro)

### 6.4 Ventana Principal (Clase App)

**Ubicación:** Líneas 1801-1950

```python
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        aplicar_estilos_ttk()
        self.title('Gestión de Horarios Escolares')
        self.geometry('900x650')
        self.configure(bg='#f4f6fa')
        self._crear_menu()
        self._crear_frame_principal()
```

**Características:**
- Ventana de 900x650 píxeles
- Fondo gris azulado claro
- Menú en la parte superior
- Frame principal dinámico que cambia según la vista

**Métodos Principales:**

```python
def _crear_menu(self):
    """Crea la barra de menú con todas las opciones"""
    
def _crear_frame_principal(self):
    """Crea el frame principal con mensaje de bienvenida"""
    
def limpiar_frame(self):
    """Limpia el contenido del frame principal"""
```

---

### 6.5 Vistas Específicas

#### 6.5.1 Vista de Materias/Obligaciones

**Función:** `mostrar_materias()`  
**Ubicación:** Líneas 950-1050

**Componentes:**
```
┌─────────────────────────────────────────────────────────┐
│  Gestión de Materias/Obligaciones                       │
├─────────────────────────────────────────────────────────┤
│  Total de materias/obligaciones: 15                     │
│  Total de horas institucionales: 120                    │
├─────────────────────────────────────────────────────────┤
│  Filtro: [___________________]                          │
├─────────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────────────┐  │
│  │ Nombre          │ Horas asignadas                 │  │
│  ├───────────────────────────────────────────────────┤  │
│  │ Biología        │ 4                               │  │
│  │ Física          │ 5                               │  │
│  │ Matemática      │ 6                               │  │
│  │ Química         │ 4                               │  │
│  └───────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────┤
│  Nombre: [_______________________]                      │
├─────────────────────────────────────────────────────────┤
│  [Agregar]  [Editar]  [Eliminar]                        │
└─────────────────────────────────────────────────────────┘
```

**Funcionalidades:**
- ✅ Visualización de totales (materias y horas)
- ✅ Filtro en tiempo real por nombre
- ✅ TreeView ordenado alfabéticamente
- ✅ Agregar nueva materia (con horas iniciales en 0)
- ✅ Editar nombre de materia (preserva horas)
- ✅ Eliminar materia
- ✅ Selección de materia en TreeView rellena campo de edición

**Flujo de Trabajo:**
1. Usuario selecciona "Plan de estudios" → "Gestionar Materias/Obligaciones"
2. Se carga la vista con todas las materias
3. Usuario puede filtrar, agregar, editar o eliminar
4. TreeView se actualiza automáticamente después de cada operación

**Código Clave:**
```python
# Filtrado en tiempo real
def filtrar_materias(*args):
    filtro = self.filtro_materia.get().lower()
    materias_filtradas = [m for m in obtener_materias() if filtro in m['nombre'].lower()]
    recargar_treeview(self.tree_materias, materias_filtradas, ['nombre', 'horas_semanales'])

self.filtro_materia.trace_add('write', filtrar_materias)
```

#### 6.5.2 Vista de Personal Docente

**Función:** `mostrar_profesores()`  
**Ubicación:** Líneas 1051-1200

**Componentes:**
```
┌─────────────────────────────────────────────────────────┐
│  Gestión de personal                                    │
├─────────────────────────────────────────────────────────┤
│  Total de agentes: 25                                   │
├─────────────────────────────────────────────────────────┤
│  Filtro: [___________]  Turno: [Todos ▼]               │
├─────────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────────────┐  │
│  │ Nombre                                            │  │
│  ├───────────────────────────────────────────────────┤  │
│  │ García López, Juan Carlos                         │  │
│  │ Martínez Pérez, María Elena                       │  │
│  │ Rodríguez Fernández, Carlos                       │  │
│  └───────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────┤
│  Nombre: [_______________________]                      │
├─────────────────────────────────────────────────────────┤
│  [Agregar]  [Editar]  [Eliminar]                        │
│  [Banca de horas]  [Turnos del agente]                  │
└─────────────────────────────────────────────────────────┘
```

**Funcionalidades:**
- ✅ Contador dinámico de profesores
- ✅ Filtro por nombre en tiempo real
- ✅ Filtro por turno
- ✅ TreeView ordenado alfabéticamente
- ✅ CRUD completo de profesores
- ✅ Gestión de banca de horas (ventana modal)
- ✅ Gestión de turnos asignados (ventana modal)

**Ventana Modal: Banca de Horas**
```
┌──────────────────────────────────────────┐
│  Obligaciones del agente                 │
├──────────────────────────────────────────┤
│  Obligaciones asignadas y horas ocupadas │
├──────────────────────────────────────────┤
│  ┌────────────────────────────────────┐  │
│  │ Obligación    │ Horas asignadas   │  │
│  ├────────────────────────────────────┤  │
│  │ Matemática    │ 15                │  │
│  │ Física        │ 8                 │  │
│  └────────────────────────────────────┘  │
├──────────────────────────────────────────┤
│  Obligación: [Matemática ▼]             │
├──────────────────────────────────────────┤
│  [Agregar obligación] [Eliminar...]     │
└──────────────────────────────────────────┘
```

**Características Especiales:**
- Las horas se incrementan automáticamente al asignar horarios
- Inicialmente se asignan con 0 horas
- Filtro inteligente de materias con autocompletado

#### 6.5.3 Vista de Divisiones/Cursos

**Función:** `mostrar_divisiones()`  
**Ubicación:** Líneas 1201-1400

**Componentes:**
```
┌─────────────────────────────────────────────────────────┐
│  Gestión de Cursos                                      │
├─────────────────────────────────────────────────────────┤
│  Total de divisiones: 24                                │
├─────────────────────────────────────────────────────────┤
│  Turno: [Mañana ▼]  Plan: [Bachiller ▼]                │
│  Curso: [1° Año ▼]                                      │
├─────────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────────────┐  │
│  │ Turno  │ Plan      │ Curso   │ División         │  │
│  ├───────────────────────────────────────────────────┤  │
│  │ Mañana │ Bachiller │ 1° Año  │ A                │  │
│  │ Mañana │ Bachiller │ 1° Año  │ B                │  │
│  │ Mañana │ Bachiller │ 2° Año  │ A                │  │
│  └───────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────┤
│  [Agregar]  [Editar]  [Eliminar]                        │
└─────────────────────────────────────────────────────────┘
```

**Funcionalidades:**
- ✅ Filtros en cascada: Turno → Plan → Curso
- ✅ Contador dinámico filtrado
- ✅ Creación con validación completa (ventana modal)
- ✅ Edición de división existente
- ✅ Eliminación con confirmación
- ✅ Autocompletado inteligente en cascada

**Ventana Modal: Agregar/Editar División**
```
┌──────────────────────────────────────────┐
│  Nueva División                          │
├──────────────────────────────────────────┤
│  Turno:      [Mañana ▼]                 │
│  Plan:       [Bachiller ▼]              │
│  Curso:      [1° Año ▼]                 │
│  División:   [___________]              │
├──────────────────────────────────────────┤
│  [Guardar]  [Cancelar]                  │
└──────────────────────────────────────────┘
```

**Validaciones:**
- Nombre único por combinación turno-plan-curso
- Plan debe estar asignado al turno seleccionado
- Curso debe pertenecer al plan seleccionado
- Navegación automática con Enter

#### 6.5.4 Vista de Horarios por Curso

**Función:** `mostrar_horarios_curso()`  
**Ubicación:** Líneas 1500-2000

**Componentes:**
```
┌─────────────────────────────────────────────────────────┐
│  Gestión de Horarios por Curso                          │
├─────────────────────────────────────────────────────────┤
│  Turno: [Mañana ▼]  Plan: [Bachiller ▼]                │
│  Curso: [1° Año ▼]  División: [A ▼]                    │
├─────────────────────────────────────────────────────────┤
│  ┌───┬────────┬────────┬─────────┬────────┬──────────┐ │
│  │   │ Lunes  │ Martes │Miércoles│ Jueves │ Viernes  │ │
│  ├───┼────────┼────────┼─────────┼────────┼──────────┤ │
│  │1ª │[Mat.  ]│[Física]│[Química]│[Mat.  ]│[Hist.   ]│ │
│  │   │García  │Pérez   │López    │García  │Martínez │ │
│  │   │08:00-  │08:00-  │08:00-   │08:00-  │08:00-   │ │
│  │   │08:45   │08:45   │08:45    │08:45   │08:45    │ │
│  ├───┼────────┼────────┼─────────┼────────┼──────────┤ │
│  │2ª │[      ]│[      ]│[       ]│[      ]│[        ]│ │
│  │...│        │        │         │        │          │ │
│  └───┴────────┴────────┴─────────┴────────┴──────────┘ │
├─────────────────────────────────────────────────────────┤
│  [Configurar horas por turno] [Limpiar horarios vacíos] │
└─────────────────────────────────────────────────────────┘
```

**Funcionalidades:**
- ✅ Selección en cascada: Turno → Plan → Curso → División
- ✅ Grilla interactiva 8x5 (8 espacios, 5 días)
- ✅ Click en celda abre ventana de edición
- ✅ Scroll vertical para toda la grilla
- ✅ Ajuste automático de ancho de columnas
- ✅ Configuración global de horas por turno
- ✅ Limpieza de horarios sin materia/profesor

**Ventana Modal: Editar Espacio Horario**
```
┌──────────────────────────────────────────┐
│  Lunes - 1ª hora                         │
├──────────────────────────────────────────┤
│  Hora inicio:  [08:00]  Hs               │
│  Hora fin:     [08:45]  Hs               │
│  Obligación:   [Matemática ▼]            │
│  Profesor:     [García López ▼]          │
├──────────────────────────────────────────┤
│  [Guardar]  [Eliminar]                   │
└──────────────────────────────────────────┘
```

**Características Especiales:**
- Auto-inserción de ":" en campos de hora (08:00)
- Navegación automática al completar hora
- Solo se habilitan profesores que tienen la materia asignada
- Validación de superposición de horarios
- Sincronización automática con vista por profesor

#### 6.5.5 Vista de Horarios por Profesor

**Función:** `mostrar_horarios_profesor()`  
**Ubicación:** Líneas 2001-2300

**Componentes:**
```
┌─────────────────────────────────────────────────────────┐
│  Gestión de Horarios por Profesor                       │
├─────────────────────────────────────────────────────────┤
│  Turno: [Mañana ▼]  Buscar agente: [garcía___]         │
│                                     (filtro activo)      │
├─────────────────────────────────────────────────────────┤
│  ┌───┬────────┬────────┬─────────┬────────┬──────────┐ │
│  │   │ Lunes  │ Martes │Miércoles│ Jueves │ Viernes  │ │
│  ├───┼────────┼────────┼─────────┼────────┼──────────┤ │
│  │1ª │[Mat.  ]│[Mat.  ]│[       ]│[Mat.  ]│[        ]│ │
│  │   │1°A     │2°B     │         │3°A     │          │ │
│  │   │08:00-  │08:00-  │         │08:00-  │          │ │
│  │   │08:45   │08:45   │         │08:45   │          │ │
│  │...│        │        │         │        │          │ │
│  └───┴────────┴────────┴─────────┴────────┴──────────┘ │
├─────────────────────────────────────────────────────────┤
│  [Configurar horas por turno] [Limpiar horarios vacíos] │
└─────────────────────────────────────────────────────────┘
```

**Funcionalidades:**
- ✅ Búsqueda de profesor con autocompletado
- ✅ Filtrado en tiempo real mientras se escribe
- ✅ Enter: selecciona primera coincidencia
- ✅ Esc/Backspace: limpia búsqueda
- ✅ Tooltip con instrucciones de uso
- ✅ Ancho dinámico del combobox según nombre
- ✅ Grilla interactiva igual que vista por curso
- ✅ Sincronización automática con vista por curso

**Ventana Modal: Editar Espacio Horario Profesor**
```
┌──────────────────────────────────────────┐
│  Lunes - 1ª hora                         │
├──────────────────────────────────────────┤
│  Hora inicio:  [08:00]  Hs               │
│  Hora fin:     [08:45]  Hs               │
│  Obligación:   [Matemática ▼]            │
│  Plan:         [Bachiller ▼]             │
│  Año:          [1° Año ▼]                │
│  División:     [A ▼]                     │
├──────────────────────────────────────────┤
│  [Guardar]  [Eliminar]                   │
└──────────────────────────────────────────┘
```

**Características Especiales:**
- Solo muestra materias de la banca del profesor
- Filtrado automático de divisiones por turno/plan/año
- Autocompletado inteligente en cascada
- Validaciones específicas para profesores
- Los cambios se reflejan inmediatamente en vista por curso

#### 6.5.6 Vista de Planes de Estudio

**Función:** `mostrar_planes()`  
**Ubicación:** Líneas 2550-2700

**Componentes:**
```
┌─────────────────────────────────────────────────────────┐
│  Gestión de Planes de Estudio                           │
├─────────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────────────┐  │
│  │ Nombre                                            │  │
│  ├───────────────────────────────────────────────────┤  │
│  │ Bachiller en Ciencias Naturales                   │  │
│  │ Bachiller en Economía                             │  │
│  │ Perito Mercantil                                  │  │
│  └───────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────┤
│  Nombre: [_______________________]                      │
├─────────────────────────────────────────────────────────┤
│  [Agregar]  [Eliminar]                                  │
│  [Materias/Obligaciones del plan]  [Cursos del plan]    │
└─────────────────────────────────────────────────────────┘
```

**Funcionalidades:**
- ✅ CRUD básico de planes
- ✅ Gestión de materias del plan (modal)
- ✅ Gestión de cursos/años del plan (modal)
- ✅ Gestión de materias por curso (modal anidado)

**Ventana Modal: Materias del Plan**
- Lista de materias asignadas al plan
- Agregar materias desde lista completa
- Quitar materias del plan

**Ventana Modal: Cursos del Plan**
- Lista de años/cursos del plan
- Crear nuevo curso
- Eliminar curso
- Botón "Materias del curso" abre modal anidado

**Ventana Modal Anidada: Materias del Curso**
- Muestra solo materias del plan
- Asignar materias al curso específico
- Quitar materias del curso

#### 6.5.7 Vista de Turnos

**Función:** `mostrar_turnos()`  
**Ubicación:** Líneas 2700-2850

**Componentes:**
```
┌─────────────────────────────────────────────────────────┐
│  Gestión de Turnos                                      │
├─────────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────────────┐  │
│  │ Nombre                                            │  │
│  ├───────────────────────────────────────────────────┤  │
│  │ Mañana                                            │  │
│  │ Tarde                                             │  │
│  │ Noche                                             │  │
│  └───────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────┤
│  Nombre: [_______________________]                      │
├─────────────────────────────────────────────────────────┤
│  [Agregar]  [Eliminar]  [Planes del turno]              │
└─────────────────────────────────────────────────────────┘
```

**Funcionalidades:**
- ✅ CRUD básico de turnos
- ✅ Gestión de planes asignados al turno (modal)

**Ventana Modal: Planes del Turno**
- Lista de planes asignados (sin duplicados)
- Agregar planes disponibles
- Quitar planes del turno

### 6.6 Ventana de Configuración de Horas por Turno

**Función:** `_configurar_horas_por_turno()`  
**Ubicación:** Líneas 2244-2524

**Componentes:**
```
┌──────────────────────────────────────────┐
│  Configurar horas por turno              │
├──────────────────────────────────────────┤
│  Turno: [Mañana ▼]                      │
├──────────────────────────────────────────┤
│  1ª:  [hh:mm] Hs  a  [hh:mm] Hs         │
│  2ª:  [hh:mm] Hs  a  [hh:mm] Hs         │
│  3ª:  [hh:mm] Hs  a  [hh:mm] Hs         │
│  4ª:  [hh:mm] Hs  a  [hh:mm] Hs         │
│  5ª:  [hh:mm] Hs  a  [hh:mm] Hs         │
│  6ª:  [hh:mm] Hs  a  [hh:mm] Hs         │
│  7ª:  [hh:mm] Hs  a  [hh:mm] Hs         │
│  8ª:  [hh:mm] Hs  a  [hh:mm] Hs         │
├──────────────────────────────────────────┤
│  ☐ Aplicar a horario actual              │
│  ☐ Aplicar a todos los horarios del     │
│     turno                                │
├──────────────────────────────────────────┤
│  [Guardar]  [Cancelar]                  │
└──────────────────────────────────────────┘
```

**Funcionalidades:**
- ✅ Configuración de 8 espacios horarios
- ✅ Placeholders "hh:mm" con focus in/out
- ✅ Auto-inserción de ":" después de 2 dígitos
- ✅ Navegación automática al completar campo
- ✅ Carga automática de valores existentes
- ✅ Dos opciones de aplicación independientes

**Opciones de Aplicación:**

1. **Aplicar a horario actual:**
   - Vista por curso: Solo la división seleccionada
   - Vista por profesor: Solo el profesor seleccionado

2. **Aplicar a todos los horarios del turno:**
   - Vista por curso: Todas las divisiones del turno
   - Vista por profesor: Todos los profesores del turno

**Comportamiento:**
- Los checkboxes pueden marcarse independientemente
- Sobrescribe horas existentes con los nuevos valores
- Inserta nuevos registros si no existen
- Actualiza grilla automáticamente después de guardar

---

## 7. FLUJOS DE DATOS

### 7.1 Flujo de Creación de Horario por Curso

```
┌──────────────┐
│   USUARIO    │
└──────┬───────┘
       │ 1. Selecciona menú "Gestión de horarios" → "Por curso"
       ▼
┌──────────────────────┐
│ mostrar_horarios_    │
│      curso()         │
└──────┬───────────────┘
       │ 2. Renderiza vista con filtros
       ▼
┌──────────────────────┐
│  Selección Cascada   │
│  Turno → Plan →      │
│  Curso → División    │
└──────┬───────────────┘
       │ 3. Cada selección filtra siguiente nivel
       ▼
┌──────────────────────┐
│ _dibujar_grilla_     │
│  horario_curso()     │
└──────┬───────────────┘
       │ 4. Dibuja grilla 8x5 con horarios existentes
       ▼
┌──────────────────────┐
│   USUARIO CLICK      │
│   en celda de        │
│   grilla             │
└──────┬───────────────┘
       │ 5. Abre modal de edición
       ▼
┌──────────────────────┐
│ _editar_espacio_     │
│  horario_curso()     │
└──────┬───────────────┘
       │ 6. Carga datos existentes (si hay)
       │ 7. Habilita profesor según materia
       ▼
┌──────────────────────┐
│  Usuario completa    │
│  formulario          │
└──────┬───────────────┘
       │ 8. Click en "Guardar"
       ▼
┌──────────────────────┐
│  Validaciones:       │
│  - Materia requerida │
│    si hay profesor   │
│  - Profesor en banca │
│  - No superposición  │
└──────┬───────────────┘
       │ 9. Validaciones OK
       ▼
┌──────────────────────┐
│  eliminar_horario()  │
│  (si existía)        │
└──────┬───────────────┘
       │ 10. Elimina registro viejo
       ▼
┌──────────────────────┐
│  crear_horario()     │
└──────┬───────────────┘
       │ 11. INSERT en tabla horario
       │ 12. UPDATE horas_semanales materia
       │ 13. UPDATE banca_horas profesor
       ▼
┌──────────────────────┐
│    conn.commit()     │
└──────┬───────────────┘
       │ 14. Confirma transacción
       ▼
┌──────────────────────┐
│ _dibujar_grilla_     │
│  horario_curso()     │
└──────┬───────────────┘
       │ 15. Refresca grilla
       ▼
┌──────────────────────┐
│   Modal se cierra    │
│   Cambio visible     │
└──────────────────────┘
```

### 7.2 Flujo de Sincronización Entre Vistas

```
VISTA POR CURSO                    TABLA HORARIO                    VISTA POR PROFESOR

┌────────────────┐                ┌──────────────┐                ┌────────────────┐
│ Usuario asigna │                │              │                │                │
│ Matemática a   │──────INSERT───▶│ division_id  │                │                │
│ García en 1°A  │                │ profesor_id  │◀───SELECT──────│ Usuario ve     │
│ Lunes 1ª hora  │                │ materia_id   │                │ su horario de  │
│                │                │ dia, espacio │                │ García         │
└────────────────┘                │ turno_id     │                └────────────────┘
                                  └──────────────┘
                                        │
                                        │ MISMA TABLA
                                        │ Sincronización
                                        │ Automática
                                        ▼
┌────────────────┐                ┌──────────────┐                ┌────────────────┐
│                │                │              │                │                │
│ Usuario ve     │◀───SELECT──────│ SELECT *     │                │ Usuario modifica│
│ horario        │                │ WHERE        │────UPDATE─────▶│ u elimina      │
│ actualizado    │                │ division_id  │                │ desde su vista │
│                │                │              │                │                │
└────────────────┘                └──────────────┘                └────────────────┘

                                  Resultado:
                            ✅ Cambios inmediatos
                         ✅ No hay duplicación de datos
                        ✅ Integridad referencial garantizada
```

### 7.3 Flujo de Validación de Superposición de Horarios

```
┌──────────────────────┐
│ Usuario asigna       │
│ profesor a horario   │
└──────┬───────────────┘
       │
       ▼
┌─────────────────────────────────────────────────┐
│ SELECT h.id FROM horario h                      │
│ JOIN division d ON h.division_id = d.id         │
│ WHERE h.dia = ? AND h.espacio = ?               │
│   AND h.profesor_id = ?                         │
│   AND d.turno_id = ?                            │
│   AND h.division_id != ?                        │
└──────┬──────────────────────────────────────────┘
       │
       ├─── Si encuentra registros ───┐
       │                               │
       ▼                               ▼
┌──────────────────┐      ┌──────────────────────────┐
│  No hay conflicto│      │ Exception:               │
│  Continúa con    │      │ "El profesor ya está     │
│  INSERT          │      │  asignado en ese horario │
└──────────────────┘      │  en otra división"       │
                          └──────────────────────────┘
```

### 7.4 Flujo de Aplicación Masiva de Horas por Turno

```
┌──────────────────────┐
│ Usuario configura    │
│ horas por turno      │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Marca checkboxes:    │
│ ☑ Aplicar a actual   │
│ ☑ Aplicar a todos    │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Click en "Guardar"   │
└──────┬───────────────┘
       │
       ├────────────────────────────────┐
       │                                │
       ▼                                ▼
┌──────────────────┐          ┌──────────────────┐
│ Detecta contexto │          │ Detecta contexto │
│ Vista por Curso  │          │ Vista por Profe. │
└──────┬───────────┘          └──────┬───────────┘
       │                             │
       │ Aplicar a actual            │ Aplicar a actual
       ▼                             ▼
┌──────────────────┐          ┌──────────────────┐
│ UPDATE horario   │          │ UPDATE horario   │
│ WHERE            │          │ WHERE            │
│ division_id = X  │          │ profesor_id = Y  │
└──────┬───────────┘          └──────┬───────────┘
       │                             │
       │ Aplicar a todos             │ Aplicar a todos
       ▼                             ▼
┌──────────────────┐          ┌──────────────────┐
│ UPDATE horario   │          │ UPDATE horario   │
│ WHERE division_id│          │ WHERE profesor_id│
│ IN (SELECT id    │          │ IN (SELECT       │
│     FROM division│          │     profesor_id  │
│     WHERE        │          │     FROM prof_   │
│     turno_id=?)  │          │     turno WHERE  │
│                  │          │     turno_id=?)  │
└──────┬───────────┘          └──────┬───────────┘
       │                             │
       └──────────┬──────────────────┘
                  │
                  ▼
         ┌─────────────────┐
         │ conn.commit()   │
         └────────┬────────┘
                  │
                  ▼
         ┌─────────────────┐
         │ Refresca grilla │
         └─────────────────┘
```

---

## 8. VALIDACIONES Y REGLAS DE NEGOCIO

### 8.1 Validaciones de Integridad de Datos

#### 8.1.1 Unicidad de Nombres

**Regla:** Los nombres de entidades principales deben ser únicos.

**Implementación:**
```sql
-- Nivel de Base de Datos
CREATE TABLE materia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    horas_semanales INTEGER NOT NULL
);
```

**Entidades Afectadas:**
- ✅ Materias
- ✅ Profesores
- ✅ Planes de Estudio
- ✅ Turnos

**Manejo de Errores:**
```python
try:
    crear_entidad('materia', ['nombre', 'horas_semanales'], ['Matemática', 0])
except Exception as e:
    if 'UNIQUE constraint failed' in str(e):
        messagebox.showerror('Error', 'Ya existe una materia con ese nombre.')
```

#### 8.1.2 Unicidad Compuesta

**Regla:** Algunas entidades requieren unicidad en combinación de campos.

**Ejemplos:**

**División:**
```sql
UNIQUE(nombre, turno_id, plan_id, anio_id)
```
- Una división "A" puede existir en 1° Año y 2° Año
- Pero no puede haber dos divisiones "A" en el mismo curso

**Año:**
```sql
UNIQUE(nombre, plan_id)
```
- "1° Año" puede existir en múltiples planes
- Pero no puede duplicarse dentro del mismo plan

**Horario:**
```sql
UNIQUE(division_id, dia, espacio)
```
- Una división no puede tener dos materias en el mismo día y espacio

### 8.2 Validaciones de Relaciones

#### 8.2.1 Profesor-Materia

**Regla:** Un profesor solo puede dar clases de materias que tenga en su banca.

**Implementación:**
```python
# En crear_horario()
if profesor_id is not None and materia_id is not None:
    c.execute('''SELECT 1 FROM profesor_materia 
                 WHERE profesor_id=? AND materia_id=?''', 
              (profesor_id, materia_id))
    if not c.fetchone():
        conn.close()
        raise Exception('El profesor no tiene asignada la materia seleccionada.')
```

**Flujo:**
1. Usuario selecciona materia en formulario
2. Combobox de profesores se filtra automáticamente
3. Solo aparecen profesores con esa materia en su banca
4. Validación adicional al guardar

#### 8.2.2 Profesor-Turno

**Regla:** Un profesor solo puede tener horarios en turnos a los que está asignado.

**Implementación:**
```python
# En crear_horario_profesor()
c.execute('''SELECT 1 FROM profesor_turno 
             WHERE profesor_id=? AND turno_id=?''', 
          (profesor_id, turno_id))
if not c.fetchone():
    conn.close()
    raise Exception('El profesor no está asignado a este turno.')
```

#### 8.2.3 División-Turno-Plan-Año

**Regla:** Una división debe pertenecer a un plan que esté asignado al turno, y a un año de ese plan.

**Validación en UI:**
```python
def on_turno_selected(event=None):
    turno_id = turnos_dict[turno_nombre]
    # Solo muestra planes asignados al turno
    planes = obtener_planes_de_turno(turno_id)
    
def on_plan_selected(event=None):
    plan_id = planes_dict[plan_nombre]
    # Solo muestra años del plan seleccionado
    anios = obtener_anios(plan_id)
```

### 8.3 Validaciones de Horarios

#### 8.3.1 No Superposición de Profesor

**Regla:** Un profesor no puede estar en dos lugares al mismo tiempo.

**Validación:**
```python
# Verificar que el profesor no esté asignado en otro curso 
# en el mismo turno, día y espacio
c.execute('''
    SELECT h.id FROM horario h
    JOIN division d ON h.division_id = d.id
    WHERE h.dia=? AND h.espacio=? 
      AND h.profesor_id=? 
      AND d.turno_id=? 
      AND h.division_id != ?
''', (dia, espacio, profesor_id, turno_id, division_id))

if c.fetchone():
    raise Exception('El profesor ya está asignado en ese horario 
                    en otra división del mismo turno.')
```

**Nota:** La validación es por turno, porque un profesor puede estar en turno Mañana y Tarde.

#### 8.3.2 No Superposición de División

**Regla:** Una división no puede tener dos materias en el mismo día y espacio.

**Implementación:**
```sql
-- A nivel de BD
UNIQUE(division_id, dia, espacio)
```

**Manejo en Código:**
```python
# Al intentar INSERT con división-día-espacio existente
# SQLite lanza IntegrityError
# Decorador @db_operation lo captura y lanza Exception
```

#### 8.3.3 Validación de División en Turno (Vista Profesor)

**Regla:** Si un profesor asigna una división, debe ser del turno que está editando.

**Implementación:**
```python
if division_id is not None:
    c.execute('SELECT turno_id FROM division WHERE id=?', (division_id,))
    row = c.fetchone()
    if not row:
        raise Exception('División no encontrada.')
    if row[0] != turno_id:
        raise Exception('La división no pertenece al turno seleccionado.')
```

### 8.4 Reglas de Cálculo Automático

#### 8.4.1 Incremento/Decremento de Horas

**Regla:** Al asignar/eliminar un horario, las horas se actualizan automáticamente.

**Implementación en crear_horario():**
```python
# Después del INSERT
if materia_id is not None:
    c.execute('UPDATE materia SET horas_semanales = horas_semanales + 1 
               WHERE id=?', (materia_id,))
if profesor_id is not None and materia_id is not None:
    c.execute('UPDATE profesor_materia SET banca_horas = banca_horas + 1 
               WHERE profesor_id=? AND materia_id=?', (profesor_id, materia_id))
```

**Implementación en eliminar_horario():**
```python
# Antes del DELETE, obtener datos
c.execute('SELECT materia_id, profesor_id FROM horario WHERE id=?', (id_,))
row = c.fetchone()
if row:
    materia_id, profesor_id = row
    # Restar horas
    if materia_id is not None:
        c.execute('UPDATE materia SET horas_semanales = horas_semanales - 1 
                   WHERE id=?', (materia_id,))
    if profesor_id is not None and materia_id is not None:
        c.execute('UPDATE profesor_materia SET banca_horas = banca_horas - 1 
                   WHERE profesor_id=? AND materia_id=?', (profesor_id, materia_id))
```

**Consistencia:**
- Las horas se calculan automáticamente
- No hay entrada manual de horas
- Siempre están sincronizadas con los horarios asignados

#### 8.4.2 Horas por Defecto de Turno

**Regla:** Si un horario no tiene horas específicas, se usan las del turno.

**Implementación:**
```python
if not hora_inicio or not hora_fin:
    # Obtener turno_id de la división
    c.execute('SELECT turno_id FROM division WHERE id=?', (division_id,))
    r = c.fetchone()
    if r:
        turno_id_tmp = r[0]
        default_h = obtener_turno_espacio_hora(turno_id_tmp, espacio)
        if default_h:
            if not hora_inicio:
                hora_inicio = default_h.get('hora_inicio') or ''
            if not hora_fin:
                hora_fin = default_h.get('hora_fin') or ''
```

### 8.5 Validaciones de Entrada de Usuario

#### 8.5.1 Campos Obligatorios

**Implementación:**
```python
def _agregar_materia(self):
    nombre = self.entry_nombre_materia.get().strip()
    if not nombre:
        messagebox.showerror('Error', 'Ingrese un nombre válido.')
        return
    # ... procesar
```

**Campos Obligatorios por Entidad:**
- Materia: nombre
- Profesor: nombre
- Plan: nombre
- Turno: nombre
- División: nombre, turno, plan, año
- Horario: división/profesor, día, espacio

#### 8.5.2 Formato de Horas

**Regla:** Las horas deben estar en formato HH:MM.

**Auto-corrección:**
```python
def autoinsert_colon(event, entry, next_widget=None):
    val = entry.get()
    # Auto-insertar ':' después de 2 dígitos
    if len(val) == 2 and ':' not in val:
        entry.insert(2, ':')
    # Limitar a 5 caracteres (HH:MM)
    if len(val) > 5:
        entry.delete(5, tk.END)
    # Navegar al siguiente campo al completar
    if len(val.replace(':', '')) == 4 and next_widget:
        next_widget.focus_set()
```

**Características:**
- Usuario escribe "0845" → se convierte en "08:45"
- Máximo 5 caracteres
- Navegación automática al completar

#### 8.5.3 Valores Nulos Permitidos

**Regla:** Algunos campos pueden ser NULL en la base de datos.

**Campos Opcionales en Horarios:**
- `hora_inicio` y `hora_fin`: Pueden ser NULL
- `materia_id`: Puede ser NULL (espacio libre)
- `profesor_id`: Puede ser NULL (sin profesor asignado)
- `division_id`: Puede ser NULL (en vista por profesor)

**Manejo:**
```python
# Permitir valores vacíos
hora_inicio_db = hora_inicio if hora_inicio else None
hora_fin_db = hora_fin if hora_fin else None

# INSERT con NULL
c.execute('''INSERT INTO horario (...) VALUES (?, ?, ...)''',
          (division_id, hora_inicio_db, hora_fin_db, ...))
```

---

## 9. MANEJO DE ERRORES

### 9.1 Jerarquía de Excepciones

El sistema utiliza principalmente excepciones estándar de Python y SQLite:

```
Exception (base)
├── sqlite3.Error
│   ├── sqlite3.IntegrityError    # Violación de constraints
│   ├── sqlite3.OperationalError  # Errores de operación
│   └── sqlite3.DatabaseError     # Errores de BD
├── ValueError                     # Valores inválidos
├── KeyError                       # Claves no encontradas
└── Exception                      # Excepciones genéricas
```

### 9.2 Manejo de Errores en Capa de Datos

#### 9.2.1 Decorador @db_operation

**Ubicación:** Líneas 38-48

**Propósito:** Centraliza el manejo de transacciones y errores de base de datos.

```python
def db_operation(func):
    """Decorador para manejar operaciones de BD con transacciones automáticas"""
    def wrapper(*args, **kwargs):
        conn = get_connection()
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except sqlite3.IntegrityError as e:
            conn.rollback()
            raise Exception(str(e))
        finally:
            conn.close()
    return wrapper
```

**Características:**
- ✅ **Commit automático:** Si la función se ejecuta sin errores
- ✅ **Rollback automático:** Si ocurre un IntegrityError
- ✅ **Cierre garantizado:** Siempre cierra la conexión (finally)
- ✅ **Conversión de excepciones:** IntegrityError → Exception genérica

**Tipos de IntegrityError Capturados:**
1. **UNIQUE constraint failed:** Violación de unicidad
2. **FOREIGN KEY constraint failed:** Referencia inválida
3. **NOT NULL constraint failed:** Campo obligatorio nulo
4. **CHECK constraint failed:** Validación CHECK fallida

#### 9.2.2 Manejo en Funciones Específicas

Algunas funciones manejan errores de forma más específica:

```python
def eliminar_horario(id_: int):
    """Elimina un horario y actualiza contadores automáticamente"""
    conn = get_connection()
    try:
        c = conn.cursor()
        # Obtener datos antes de eliminar
        c.execute('SELECT materia_id, profesor_id FROM horario WHERE id=?', (id_,))
        row = c.fetchone()
        
        if not row:
            raise Exception('Horario no encontrado.')
        
        materia_id, profesor_id = row
        
        # Restar horas si existen
        if materia_id is not None:
            c.execute('UPDATE materia SET horas_semanales = horas_semanales - 1 
                       WHERE id=?', (materia_id,))
        
        if profesor_id is not None and materia_id is not None:
            c.execute('UPDATE profesor_materia SET banca_horas = banca_horas - 1 
                       WHERE profesor_id=? AND materia_id=?', 
                      (profesor_id, materia_id))
        
        # Eliminar el horario
        c.execute('DELETE FROM horario WHERE id=?', (id_,))
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        raise Exception(f'Error al eliminar horario: {str(e)}')
    finally:
        conn.close()
```

### 9.3 Manejo de Errores en Capa de UI

#### 9.3.1 MessageBox para Errores

**Patrón Estándar:**
```python
try:
    # Operación que puede fallar
    crear_materia(nombre, 0)
    messagebox.showinfo('Éxito', 'Materia agregada correctamente.')
    self._cargar_materias()
except Exception as e:
    messagebox.showerror('Error', str(e))
```

**Tipos de MessageBox:**
1. **showinfo:** Operación exitosa
2. **showerror:** Error capturado
3. **showwarning:** Advertencia (poco usado)
4. **askyesno:** Confirmación de eliminación

#### 9.3.2 Validaciones Previas a Operaciones

**Ejemplo: Validación antes de crear entidad**
```python
def _agregar_materia(self):
    nombre = self.entry_nombre_materia.get().strip()
    
    # Validación de campo vacío
    if not nombre:
        messagebox.showerror('Error', 'Ingrese un nombre válido.')
        return
    
    # Validación de duplicados (adicional a BD)
    materias_existentes = [m['nombre'].lower() for m in obtener_materias()]
    if nombre.lower() in materias_existentes:
        messagebox.showerror('Error', 'Ya existe una materia con ese nombre.')
        return
    
    try:
        crear_materia(nombre, 0)
        messagebox.showinfo('Éxito', 'Materia agregada correctamente.')
        self.entry_nombre_materia.delete(0, tk.END)
        self._cargar_materias()
    except Exception as e:
        messagebox.showerror('Error', str(e))
```

#### 9.3.3 Confirmaciones de Eliminación

**Patrón:**
```python
def _eliminar_materia(self):
    selected = self.tree_materias.selection()
    if not selected:
        messagebox.showwarning('Advertencia', 'Seleccione una materia para eliminar.')
        return
    
    # Confirmación explícita
    if not messagebox.askyesno('Confirmar', 
                               '¿Está seguro de eliminar esta materia?\n'
                               'Se eliminarán también sus relaciones con '
                               'planes y profesores.'):
        return
    
    try:
        item = self.tree_materias.item(selected[0])
        materia_id = item['values'][0]  # ID está oculto en columna 0
        eliminar_materia(materia_id)
        messagebox.showinfo('Éxito', 'Materia eliminada correctamente.')
        self._cargar_materias()
    except Exception as e:
        messagebox.showerror('Error', f'Error al eliminar: {str(e)}')
```

### 9.4 Mensajes de Error Comunes

#### 9.4.1 Errores de Integridad Referencial

**Mensaje Original (SQLite):**
```
UNIQUE constraint failed: materia.nombre
```

**Mensaje al Usuario:**
```python
# Capturado por @db_operation y re-lanzado como Exception
# Mostrado en UI con messagebox.showerror
"UNIQUE constraint failed: materia.nombre"
```

**Mejora Posible:** Traducir mensajes técnicos a mensajes amigables:
```python
except sqlite3.IntegrityError as e:
    error_msg = str(e)
    if 'UNIQUE constraint failed' in error_msg:
        if 'materia.nombre' in error_msg:
            raise Exception('Ya existe una materia con ese nombre.')
        elif 'profesor.nombre' in error_msg:
            raise Exception('Ya existe un profesor con ese nombre.')
    else:
        raise Exception(error_msg)
```

#### 9.4.2 Errores de Validación de Negocio

**Mensajes Implementados:**

1. **Profesor sin materia asignada:**
   ```
   "El profesor no tiene asignada la materia seleccionada."
   ```

2. **Profesor sin turno:**
   ```
   "El profesor no está asignado a este turno."
   ```

3. **Superposición de horarios:**
   ```
   "El profesor ya está asignado en ese horario en otra división del mismo turno."
   ```

4. **División en turno incorrecto:**
   ```
   "La división no pertenece al turno seleccionado."
   ```

5. **Horario no encontrado:**
   ```
   "Horario no encontrado."
   ```

### 9.5 Logging y Diagnóstico

#### 9.5.1 Estado Actual

**El sistema actualmente NO implementa logging estructurado.**

Características actuales:
- ❌ No hay archivo de log
- ❌ No se registran operaciones exitosas
- ❌ No se registran timestamps
- ✅ Los errores se muestran al usuario inmediatamente

#### 9.5.2 Recomendaciones para Futuras Versiones

**Implementar logging básico:**

```python
import logging
from datetime import datetime

# Configuración al inicio del programa
logging.basicConfig(
    filename=os.path.join(get_base_path(), 'horarios.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Uso en funciones críticas
@db_operation
def crear_horario(conn, division_id, dia, espacio, ...):
    logging.info(f'Creando horario: division={division_id}, dia={dia}, espacio={espacio}')
    try:
        # ... operación
        logging.info(f'Horario creado exitosamente: id={cursor.lastrowid}')
    except Exception as e:
        logging.error(f'Error al crear horario: {str(e)}')
        raise
```

**Beneficios:**
- Rastreo de operaciones
- Diagnóstico de errores intermitentes
- Auditoría de cambios
- Análisis de uso del sistema

### 9.6 Manejo de Errores en Compilación

#### 9.6.1 Errores de Ruta de Base de Datos

**Problema:** En modo desarrollo vs. producción, las rutas difieren.

**Solución Implementada:**
```python
def get_base_path():
    """Obtiene la ruta base del programa (desarrollo o producción)"""
    if getattr(sys, 'frozen', False):
        # Si está compilado con PyInstaller
        return os.path.dirname(sys.executable)
    else:
        # Si se ejecuta desde script Python
        return os.path.dirname(os.path.abspath(__file__))
```

**Uso:**
```python
def get_connection():
    """Obtiene conexión a la base de datos"""
    db_path = os.path.join(get_base_path(), 'institucion.db')
    return sqlite3.connect(db_path)
```

#### 9.6.2 Errores de Importación de Tkinter

**Problema:** Tkinter puede faltar en algunas instalaciones de Python.

**Manejo Recomendado:**
```python
try:
    import tkinter as tk
    from tkinter import ttk, messagebox
except ImportError:
    print("Error: Tkinter no está instalado.")
    print("En Debian/Ubuntu: sudo apt-get install python3-tk")
    print("En Fedora: sudo dnf install python3-tkinter")
    sys.exit(1)
```

### 9.7 Recuperación de Errores

#### 9.7.1 Transacciones Atómicas

**Garantía:** Todas las operaciones de BD son atómicas gracias a `@db_operation`.

**Comportamiento:**
- Si una operación falla, se hace rollback automático
- La base de datos vuelve al estado anterior
- No quedan datos inconsistentes

**Ejemplo: Crear Horario**
```
INICIO TRANSACCIÓN
├─ INSERT INTO horario (...)
├─ UPDATE materia SET horas_semanales = horas_semanales + 1
├─ UPDATE profesor_materia SET banca_horas = banca_horas + 1
└─ COMMIT (si todo OK) / ROLLBACK (si falla)
```

Si el UPDATE falla, el INSERT también se revierte.

#### 9.7.2 Validación Post-Operación

**Patrón:** Después de operaciones críticas, validar el estado.

**Ejemplo:**
```python
def crear_horario(conn, division_id, dia, espacio, ...):
    c = conn.cursor()
    
    # Validaciones previas
    # ...
    
    # Inserción
    c.execute('INSERT INTO horario (...) VALUES (...)', (...))
    
    # Actualización de contadores
    # ...
    
    # Validación post-operación (opcional)
    c.execute('SELECT COUNT(*) FROM horario WHERE division_id=? AND dia=? AND espacio=?',
              (division_id, dia, espacio))
    count = c.fetchone()[0]
    
    if count != 1:
        raise Exception('Error de consistencia: múltiples horarios en mismo espacio.')
```

---

## 10. CONFIGURACIÓN Y DESPLIEGUE

### 10.1 Configuración de Desarrollo

#### 10.1.1 Requisitos del Entorno

**Python 3.9+:**
```powershell
# Verificar versión
python --version

# Debe mostrar: Python 3.9.x o superior
```

**Módulos Requeridos:**
```python
# Todos son módulos estándar, no requieren pip install
import sqlite3      # Base de datos
import tkinter      # Interfaz gráfica
import os           # Sistema operativo
import sys          # Sistema Python
from typing import List, Dict, Any, Optional  # Type hints
```

**Estructura de Proyecto:**
```
Programa horarios/
└── version 1.0/
    ├── SistemaEscolar_v1.py    # Archivo principal
    ├── institucion.db          # Base de datos (auto-creada)
    └── [documentación]
```

#### 10.1.2 Primera Ejecución

**Desde PowerShell:**
```powershell
# Navegar al directorio
cd "C:\Chino\Tecnicatura\Metodologia de sistemas\Programa horarios\version 1.0"

# Ejecutar
python SistemaEscolar_v1.py
```

**Desde CMD:**
```cmd
cd "C:\Chino\Tecnicatura\Metodologia de sistemas\Programa horarios\version 1.0"
python SistemaEscolar_v1.py
```

**Comportamiento Primera Ejecución:**
1. Se crea archivo `institucion.db` si no existe
2. Se ejecuta `init_db()` para crear esquema
3. Se muestra pantalla de login para crear usuario administrador

#### 10.1.3 Verificación de Base de Datos

**Script PowerShell:** `diagnosticar_db.ps1`

```powershell
# Contenido del script
$dbPath = Join-Path $PSScriptRoot "institucion.db"

if (Test-Path $dbPath) {
    Write-Host "Base de datos encontrada: $dbPath" -ForegroundColor Green
    
    # Listar tablas
    sqlite3 $dbPath ".tables"
    
    # Contar registros
    Write-Host "`nConteo de registros:" -ForegroundColor Cyan
    sqlite3 $dbPath "SELECT 'Materias: ' || COUNT(*) FROM materia;"
    sqlite3 $dbPath "SELECT 'Profesores: ' || COUNT(*) FROM profesor;"
    sqlite3 $dbPath "SELECT 'Planes: ' || COUNT(*) FROM plan_estudio;"
    sqlite3 $dbPath "SELECT 'Turnos: ' || COUNT(*) FROM turno;"
    sqlite3 $dbPath "SELECT 'Divisiones: ' || COUNT(*) FROM division;"
    sqlite3 $dbPath "SELECT 'Horarios: ' || COUNT(*) FROM horario;"
} else {
    Write-Host "Base de datos no encontrada." -ForegroundColor Red
}
```

**Uso:**
```powershell
.\diagnosticar_db.ps1
```

### 10.2 Compilación a Ejecutable

#### 10.2.1 Instalación de PyInstaller

```powershell
# Instalar PyInstaller
pip install pyinstaller

# Verificar instalación
pyinstaller --version
```

#### 10.2.2 Script de Compilación

**Archivo:** `compilar.ps1`

```powershell
# Configuración
$scriptPath = "SistemaEscolar_v1.py"
$exeName = "SistemaHorarios"
$iconPath = "icon.ico"  # Opcional

# Limpiar compilaciones anteriores
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "*.spec") { Remove-Item -Force "*.spec" }

Write-Host "Compilando $scriptPath..." -ForegroundColor Cyan

# Compilar
pyinstaller --onefile `
            --windowed `
            --name $exeName `
            --add-data "institucion.db;." `
            $scriptPath

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nCompilación exitosa!" -ForegroundColor Green
    Write-Host "Ejecutable: dist\$exeName.exe" -ForegroundColor Green
} else {
    Write-Host "`nError en la compilación." -ForegroundColor Red
}
```

**Opciones de PyInstaller:**
- `--onefile`: Un solo archivo .exe (portable)
- `--windowed`: Sin consola de fondo (GUI pura)
- `--name`: Nombre del ejecutable
- `--add-data`: Incluir archivos adicionales (DB, iconos)
- `--icon`: Ícono del ejecutable (opcional)

#### 10.2.3 Ejecución del Script

```powershell
# Dar permisos de ejecución (primera vez)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Ejecutar compilación
.\compilar.ps1
```

**Resultado:**
```
dist/
└── SistemaHorarios.exe  (tamaño ~15-25 MB)
```

#### 10.2.4 Problemas Comunes de Compilación

**Problema 1: Tkinter no se incluye**

**Solución:**
```powershell
# Especificar explícitamente
pyinstaller --onefile --windowed --hidden-import tkinter SistemaEscolar_v1.py
```

**Problema 2: Base de datos no se encuentra**

**Solución:** Verificar que `get_base_path()` esté correctamente implementado:
```python
def get_base_path():
    if getattr(sys, 'frozen', False):
        # Ejecutable PyInstaller
        return os.path.dirname(sys.executable)
    else:
        # Script Python
        return os.path.dirname(os.path.abspath(__file__))
```

**Problema 3: Error "Failed to execute script"**

**Solución:** Ejecutar sin `--windowed` para ver errores en consola:
```powershell
pyinstaller --onefile SistemaEscolar_v1.py
dist\SistemaHorarios.exe  # Ver errores en consola
```

### 10.3 Distribución

#### 10.3.1 Ejecutable Standalone

**Archivo generado:**
```
SistemaHorarios.exe  (~20 MB)
```

**Características:**
- ✅ No requiere Python instalado
- ✅ No requiere bibliotecas adicionales
- ✅ Portable (puede ejecutarse desde USB)
- ✅ Compatible con Windows 7, 8, 10, 11

**Distribución:**
1. Copiar `SistemaHorarios.exe` a carpeta de destino
2. Primera ejecución crea `institucion.db` en mismo directorio
3. Usuario debe configurar usuario administrador inicial

#### 10.3.2 Paquete con Base de Datos Pre-cargada

**Estructura:**
```
SistemaHorarios/
├── SistemaHorarios.exe
├── institucion.db        (con datos pre-cargados)
├── Leeme.txt
└── Manual_Usuario.pdf
```

**Ventaja:** La institución puede distribuir con datos iniciales (turnos, planes, profesores).

#### 10.3.3 Instalador (Opcional)

Para distribución más profesional, usar **Inno Setup**:

**Script Inno Setup:** `installer.iss`
```iss
[Setup]
AppName=Sistema de Gestión de Horarios Escolares
AppVersion=0.9
DefaultDirName={pf}\SistemaHorarios
DefaultGroupName=Sistema Horarios
OutputDir=.
OutputBaseFilename=SistemaHorarios_Setup

[Files]
Source: "dist\SistemaHorarios.exe"; DestDir: "{app}"
Source: "MANUAL_DE_USUARIO.pdf"; DestDir: "{app}"; Flags: isreadme

[Icons]
Name: "{group}\Sistema de Horarios"; Filename: "{app}\SistemaHorarios.exe"
Name: "{commondesktop}\Sistema de Horarios"; Filename: "{app}\SistemaHorarios.exe"
```

**Compilar:**
```
Inno Setup Compiler > Abrir installer.iss > Build
```

**Resultado:** `SistemaHorarios_Setup.exe` (instalador completo)

### 10.4 Configuración de Base de Datos

#### 10.4.1 Inicialización Automática

**Función:** `init_db()`  
**Ubicación:** Líneas 50-150

**Proceso:**
```python
def init_db():
    """Inicializa la base de datos con el esquema completo"""
    conn = get_connection()
    c = conn.cursor()
    
    # 1. Habilitar foreign keys
    c.execute('PRAGMA foreign_keys = ON')
    
    # 2. Crear tablas si no existen
    c.execute('''CREATE TABLE IF NOT EXISTS materia (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE NOT NULL,
        horas_semanales INTEGER NOT NULL DEFAULT 0
    )''')
    
    # ... (resto de tablas)
    
    conn.commit()
    conn.close()
```

**Llamada:**
```python
if __name__ == "__main__":
    init_db()  # Se ejecuta al inicio del programa
    root = App()
    root.mainloop()
```

#### 10.4.2 Migraciones de Esquema

**Versión 0.9 agregó campo `turno_id` a tabla `horario`.**

**Proceso de Migración Manual:**
```sql
-- 1. Verificar si el campo existe
PRAGMA table_info(horario);

-- 2. Si no existe, agregar columna
ALTER TABLE horario ADD COLUMN turno_id INTEGER REFERENCES turno(id);

-- 3. Poblar valores para registros existentes
UPDATE horario 
SET turno_id = (SELECT turno_id FROM division WHERE division.id = horario.division_id)
WHERE division_id IS NOT NULL;
```

**Para Futuras Versiones:** Implementar sistema de migraciones automáticas:
```python
def get_db_version():
    """Obtiene versión actual del esquema"""
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute('SELECT version FROM schema_version')
        return c.fetchone()[0]
    except:
        return 0
    finally:
        conn.close()

def migrate_db():
    """Ejecuta migraciones pendientes"""
    version = get_db_version()
    
    if version < 1:
        # Migración a versión 1
        conn = get_connection()
        c = conn.cursor()
        c.execute('ALTER TABLE horario ADD COLUMN turno_id INTEGER')
        c.execute('UPDATE horario SET turno_id = ...')
        c.execute('UPDATE schema_version SET version = 1')
        conn.commit()
        conn.close()
```

#### 10.4.3 Backup y Restauración

**Backup Manual:**
```powershell
# Copiar base de datos
Copy-Item "institucion.db" "institucion_backup_$(Get-Date -Format 'yyyyMMdd').db"
```

**Backup Programático:**
```python
import shutil
from datetime import datetime

def crear_backup():
    """Crea backup de la base de datos"""
    db_path = os.path.join(get_base_path(), 'institucion.db')
    fecha = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = os.path.join(get_base_path(), f'institucion_backup_{fecha}.db')
    
    try:
        shutil.copy2(db_path, backup_path)
        return True, f'Backup creado: {backup_path}'
    except Exception as e:
        return False, f'Error al crear backup: {str(e)}'
```

**Restauración:**
```powershell
# Detener aplicación
# Renombrar DB actual
Rename-Item "institucion.db" "institucion_old.db"

# Restaurar backup
Copy-Item "institucion_backup_20251108.db" "institucion.db"

# Reiniciar aplicación
```

### 10.5 Configuración de Sistema Operativo

#### 10.5.1 Requisitos de Windows

**Versiones Compatibles:**
- ✅ Windows 7 SP1 (32/64 bits)
- ✅ Windows 8 / 8.1
- ✅ Windows 10 (todas las versiones)
- ✅ Windows 11

**Dependencias del Sistema:**
- Visual C++ Redistributable 2015-2022 (incluido con Windows Update)
- .NET Framework 4.5+ (incluido desde Windows 8)

#### 10.5.2 Permisos de Usuario

**Permisos Necesarios:**
- ✅ Lectura/Escritura en directorio de instalación
- ✅ Creación de archivos (institucion.db)
- ❌ NO requiere permisos de administrador

**Ubicación Recomendada:**
```
C:\Users\[Usuario]\Documents\SistemaHorarios\
```
En lugar de:
```
C:\Program Files\SistemaHorarios\  (requiere admin para escribir DB)
```

#### 10.5.3 Firewall y Antivirus

**Problema Potencial:** Algunos antivirus bloquean ejecutables de PyInstaller.

**Solución:**
1. Firmar digitalmente el ejecutable (costoso)
2. Agregar excepción en antivirus corporativo
3. Distribuir código fuente + Python para instituciones sensibles

---

## 11. PRUEBAS

### 11.1 Estrategia de Testing

**Estado Actual:** El sistema v0.9 **no implementa pruebas automatizadas**.

**Tipo de Testing Aplicado:**
- ✅ **Pruebas manuales** durante desarrollo
- ✅ **Pruebas de integración** ad-hoc
- ❌ **Pruebas unitarias** (no implementadas)
- ❌ **Pruebas de regresión** (no implementadas)

### 11.2 Pruebas Manuales Recomendadas

#### 11.2.1 Checklist de Pruebas por Módulo

**MÓDULO: Materias**

| # | Caso de Prueba | Resultado Esperado | ✓ |
|---|---------------|-------------------|---|
| 1 | Crear materia nueva | Se agrega a la lista | ☐ |
| 2 | Crear materia duplicada | Error: "Ya existe" | ☐ |
| 3 | Crear materia con nombre vacío | Error: "Ingrese nombre válido" | ☐ |
| 4 | Editar materia existente | Nombre se actualiza en lista | ☐ |
| 5 | Eliminar materia sin uso | Se elimina correctamente | ☐ |
| 6 | Eliminar materia con horarios | Se eliminan en cascada | ☐ |
| 7 | Filtrar materias por texto | Solo muestra coincidencias | ☐ |

**MÓDULO: Profesores**

| # | Caso de Prueba | Resultado Esperado | ✓ |
|---|---------------|-------------------|---|
| 1 | Crear profesor nuevo | Se agrega a la lista | ☐ |
| 2 | Crear profesor duplicado | Error: "Ya existe" | ☐ |
| 3 | Asignar banca de horas | Materia aparece en listado | ☐ |
| 4 | Asignar turno a profesor | Turno aparece asignado | ☐ |
| 5 | Eliminar profesor sin horarios | Se elimina correctamente | ☐ |
| 6 | Eliminar profesor con horarios | Confirmar eliminación en cascada | ☐ |
| 7 | Filtrar por turno | Solo muestra profesores del turno | ☐ |

**MÓDULO: Horarios por Curso**

| # | Caso de Prueba | Resultado Esperado | ✓ |
|---|---------------|-------------------|---|
| 1 | Asignar horario nuevo | Aparece en grilla | ☐ |
| 2 | Asignar horario con profesor ocupado | Error: "Ya está asignado" | ☐ |
| 3 | Asignar profesor sin materia | Error: "No tiene la materia" | ☐ |
| 4 | Verificar incremento de horas | horas_semanales +1 en materia | ☐ |
| 5 | Verificar incremento banca | banca_horas +1 en profesor | ☐ |
| 6 | Eliminar horario | Decrementan contadores | ☐ |
| 7 | Configurar horas por turno | Se aplican a toda la división | ☐ |
| 8 | Limpiar horarios vacíos | Solo quedan con materia/profesor | ☐ |

**MÓDULO: Horarios por Profesor**

| # | Caso de Prueba | Resultado Esperado | ✓ |
|---|---------------|-------------------|---|
| 1 | Ver horario de profesor | Muestra horarios existentes | ☐ |
| 2 | Asignar horario en turno no asignado | Error: "No está en el turno" | ☐ |
| 3 | Asignar división de otro turno | Error: "División no pertenece" | ☐ |
| 4 | Sincronización con vista por curso | Cambios visibles en ambas vistas | ☐ |
| 5 | Eliminar horario | Se elimina en ambas vistas | ☐ |

**MÓDULO: Divisiones**

| # | Caso de Prueba | Resultado Esperado | ✓ |
|---|---------------|-------------------|---|
| 1 | Crear división nueva | Se agrega a la lista | ☐ |
| 2 | Crear división duplicada | Error: "Ya existe" | ☐ |
| 3 | Filtro en cascada turno→plan | Solo planes del turno | ☐ |
| 4 | Filtro en cascada plan→curso | Solo cursos del plan | ☐ |
| 5 | Autocompletado con 1 opción | Se selecciona automáticamente | ☐ |

#### 11.2.2 Pruebas de Reglas de Negocio

**RN-01: No superposición de profesores**

```
ENTRADA:
- Profesor: García
- Día: Lunes, Espacio: 1
- División A: Matemática

PASO 1: Asignar García en División A
RESULTADO ESPERADO: ✅ OK

PASO 2: Intentar asignar García en División B (mismo día/espacio/turno)
RESULTADO ESPERADO: ❌ Error "Ya está asignado"
```

**RN-02: Validación profesor-materia**

```
ENTRADA:
- Profesor: García
- Banca: [Matemática, Física]

PASO 1: Asignar García en Matemática
RESULTADO ESPERADO: ✅ OK

PASO 2: Intentar asignar García en Química (no está en banca)
RESULTADO ESPERADO: ❌ Error "No tiene la materia"
```

**RN-03: Contadores automáticos**

```
ENTRADA:
- Materia: Matemática (horas_semanales = 0)
- Profesor: García (banca_horas = 0)

PASO 1: Asignar 3 horarios de Matemática con García
RESULTADO ESPERADO: 
- Matemática.horas_semanales = 3
- García.banca_horas (Matemática) = 3

PASO 2: Eliminar 1 horario
RESULTADO ESPERADO:
- Matemática.horas_semanales = 2
- García.banca_horas (Matemática) = 2
```

### 11.3 Pruebas de Integración

#### 11.3.1 Flujo Completo: Alta de División con Horarios

```
ESCENARIO: Crear división nueva y asignar horarios completos

PREREQUISITOS:
- 1 Turno: Mañana
- 1 Plan: Bachiller
- 1 Año: 1° Año
- 3 Materias: Matemática, Física, Lengua
- 2 Profesores: García (Mat), Pérez (Fís, Len)

PASOS:
1. Crear división "A" - Mañana - Bachiller - 1° Año
   ✓ División creada

2. Configurar horas por turno (8 espacios)
   ✓ Horas guardadas en turno_espacio_hora

3. Asignar 20 horarios a la división
   ✓ Todos los horarios creados

4. Verificar contadores:
   - Matemática: 6 horas ✓
   - Física: 6 horas ✓
   - Lengua: 8 horas ✓
   - García banca: 6 horas ✓
   - Pérez banca: 14 horas ✓

5. Ver horario de García en vista por profesor
   ✓ Muestra 6 horarios correctos

6. Modificar 1 horario desde vista por profesor
   ✓ Cambio visible en vista por curso

7. Eliminar división completa
   ✓ Horarios eliminados en cascada
   ✓ Contadores vuelven a 0
```

#### 11.3.2 Pruebas de Sincronización Entre Vistas

```
ESCENARIO: Sincronización bidireccional

VISTA POR CURSO:
1. Asignar Matemática-García en 1°A Lunes 1ª
   ✓ Horario creado

VISTA POR PROFESOR:
2. Ver horario de García
   ✓ Aparece el horario creado en paso 1

VISTA POR PROFESOR:
3. Modificar horario: cambiar de 1°A a 1°B
   ✓ Horario actualizado

VISTA POR CURSO:
4. Ver horario de 1°A
   ✓ Ya no aparece el horario
   
5. Ver horario de 1°B
   ✓ Aparece el horario modificado
```

### 11.4 Pruebas de Rendimiento

#### 11.4.1 Volumen de Datos Esperado

**Datos Típicos de Institución Mediana:**
- Materias: ~40
- Profesores: ~60
- Turnos: 3 (Mañana, Tarde, Noche)
- Planes: ~5
- Años por plan: ~5
- Divisiones: ~30 (10 por turno)
- Horarios: ~1,200 (40 horas/semana × 30 divisiones)

**Consultas Críticas:**
1. **Cargar grilla de horarios:** ~40 horarios por división
2. **Filtrar profesores por turno:** ~20 profesores
3. **Obtener horarios de profesor:** ~40 horarios

**Tiempos Esperados (SQLite en disco local):**
- Cargar grilla: <100ms ✓
- Filtrar profesores: <50ms ✓
- Guardar horario: <50ms ✓

#### 11.4.2 Pruebas de Estrés

**Escenario:** Base de datos con 10,000 horarios

```python
# Script de prueba (no incluido en sistema)
import sqlite3
import time

conn = sqlite3.connect('horarios_test.db')
c = conn.cursor()

# Insertar 10,000 horarios
start = time.time()
for i in range(10000):
    c.execute('INSERT INTO horario (...) VALUES (...)', (...))
conn.commit()
end = time.time()

print(f'Tiempo de inserción: {end - start:.2f}s')
# Esperado: <5 segundos

# Consultar 100 veces
start = time.time()
for i in range(100):
    c.execute('SELECT * FROM horario WHERE division_id = ?', (1,))
    c.fetchall()
end = time.time()

print(f'Tiempo de consulta: {(end - start) / 100 * 1000:.2f}ms por consulta')
# Esperado: <10ms por consulta
```

### 11.5 Pruebas de Usabilidad

#### 11.5.1 Checklist de UX

| # | Aspecto | Cumplimiento | Notas |
|---|---------|-------------|-------|
| 1 | Filtros actualizan en tiempo real | ✅ | |
| 2 | Enter navega entre campos | ✅ | |
| 3 | Autocompletado de combobox | ✅ | |
| 4 | Tooltips en campos complejos | ✅ | |
| 5 | Confirmación antes de eliminar | ✅ | |
| 6 | Mensajes de error claros | ⚠️ | Algunos muy técnicos |
| 7 | Grilla scrollable | ✅ | |
| 8 | Selección con click en TreeView | ✅ | |
| 9 | Atajos de teclado | ❌ | No implementados |
| 10 | Indicador de carga | ❌ | No necesario (es rápido) |

#### 11.5.2 Pruebas con Usuario Final

**Protocolo de Testing:**
1. Dar al usuario tareas específicas sin instrucciones
2. Observar dificultades y confusiones
3. Registrar tiempo de completado
4. Solicitar feedback sobre intuitividad

**Tareas Típicas:**
- Crear una nueva materia
- Asignar un profesor a una materia
- Crear una división
- Asignar horarios a una división
- Buscar el horario de un profesor específico
- Modificar un horario existente
- Configurar las horas de un turno

**Métricas:**
- Tasa de éxito (sin ayuda)
- Tiempo de completado
- Número de errores
- Satisfacción subjetiva (escala 1-5)

### 11.6 Pruebas de Seguridad

#### 11.6.1 Inyección SQL

**Estado Actual:** ✅ **Protegido**

El sistema utiliza **consultas parametrizadas** en todas las operaciones:

```python
# ✅ CORRECTO (implementado)
c.execute('SELECT * FROM materia WHERE nombre=?', (nombre,))

# ❌ VULNERABLE (NO usado)
c.execute(f'SELECT * FROM materia WHERE nombre="{nombre}"')
```

**Prueba:**
```
ENTRADA: nombre = "'; DROP TABLE materia; --"
RESULTADO: Se trata como texto literal, no se ejecuta SQL
```

#### 11.6.2 Validación de Entrada

**Validaciones Implementadas:**
- ✅ Campos obligatorios no vacíos
- ✅ Formato de hora (HH:MM)
- ✅ Valores numéricos donde corresponde
- ⚠️ Longitud máxima (solo por límite de UI)

**Pruebas:**
- Ingresar texto muy largo (>1000 caracteres)
- Ingresar caracteres especiales en todos los campos
- Ingresar valores negativos en campos numéricos

---

## 12. MANTENIMIENTO Y TROUBLESHOOTING

### 12.1 Problemas Comunes y Soluciones

#### 12.1.1 Base de Datos

**PROBLEMA:** "Database is locked"

**Causa:** Múltiples instancias intentando acceder simultáneamente.

**Solución:**
```python
# Asegurar cierre de conexiones
finally:
    conn.close()

# O configurar timeout
conn = sqlite3.connect('institucion.db', timeout=10.0)
```

**Solución Usuario:**
- Cerrar todas las instancias del programa
- Verificar que no haya procesos colgados (Task Manager)
- Reiniciar el programa

---

**PROBLEMA:** "No such table: horario"

**Causa:** Base de datos corrupta o no inicializada.

**Solución:**
1. Cerrar aplicación
2. Eliminar `institucion.db`
3. Reiniciar aplicación (se crea nuevo esquema)
4. Restaurar desde backup si existe

---

**PROBLEMA:** "Foreign key constraint failed"

**Causa:** Intento de insertar datos con referencias inválidas.

**Solución:**
- Verificar que las entidades referenciadas existan
- Ejemplo: No se puede crear horario con `profesor_id=999` si no existe ese profesor

**Debug:**
```sql
-- Verificar referencias
SELECT * FROM profesor WHERE id = 999;
SELECT * FROM materia WHERE id = 5;
```

#### 12.1.2 Interfaz Gráfica

**PROBLEMA:** Ventana se abre minimizada o fuera de pantalla

**Causa:** Configuración de ventana guardada en posición inválida.

**Solución:**
```python
# Forzar posición centrada
def centrar_ventana(ventana, ancho, alto):
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    x = (screen_width - ancho) // 2
    y = (screen_height - alto) // 2
    ventana.geometry(f'{ancho}x{alto}+{x}+{y}')
```

---

**PROBLEMA:** Combobox no muestra opciones

**Causa:** No se cargaron datos previos (división sin plan, plan sin materias, etc.)

**Solución Usuario:**
1. Verificar datos previos en orden jerárquico:
   - Turnos → Planes → Materias → Años → Divisiones
2. Crear entidades faltantes

---

**PROBLEMA:** Grilla de horarios no actualiza

**Causa:** No se llamó a `_dibujar_grilla_horario_curso()` después de guardar.

**Solución Desarrollador:**
```python
def _guardar_espacio_horario():
    # ... guardar datos
    self._dibujar_grilla_horario_curso()  # ← Agregar esta línea
    ventana.destroy()
```

#### 12.1.3 Compilación

**PROBLEMA:** "Failed to execute script 'SistemaEscolar_v1'"

**Causa:** Error en tiempo de ejecución que solo aparece en ejecutable.

**Diagnóstico:**
```powershell
# Compilar sin --windowed para ver errores
pyinstaller --onefile SistemaEscolar_v1.py

# Ejecutar desde consola
dist\SistemaHorarios.exe
```

**Posibles Causas:**
- Ruta de base de datos incorrecta
- Módulo no incluido en compilación
- Permisos de escritura en directorio

---

**PROBLEMA:** Ejecutable muy pesado (>50 MB)

**Causa:** PyInstaller incluye todas las dependencias.

**Optimización:**
```powershell
# Usar UPX para comprimir
pyinstaller --onefile --windowed --upx-dir=C:\upx SistemaEscolar_v1.py
```

**Nota:** UPX puede ser detectado como malware por algunos antivirus.

### 12.2 Mantenimiento Preventivo

#### 12.2.1 Backup Automático

**Recomendación:** Implementar backup automático semanal.

```python
import os
import shutil
from datetime import datetime

def backup_automatico():
    """Crea backup si han pasado 7 días desde el último"""
    db_path = os.path.join(get_base_path(), 'institucion.db')
    backup_dir = os.path.join(get_base_path(), 'backups')
    
    # Crear directorio de backups
    os.makedirs(backup_dir, exist_ok=True)
    
    # Verificar último backup
    backups = os.listdir(backup_dir)
    if backups:
        ultimo_backup = max(backups)
        # ... verificar fecha
    
    # Crear nuevo backup
    fecha = datetime.now().strftime('%Y%m%d')
    backup_path = os.path.join(backup_dir, f'horarios_{fecha}.db')
    shutil.copy2(db_path, backup_path)
    
    # Eliminar backups antiguos (>30 días)
    # ...
```

**Llamada:** Al inicio de la aplicación (`__main__`).

#### 12.2.2 Limpieza de Datos

**Horarios Huérfanos:**

Detectar horarios sin materia ni profesor:
```sql
SELECT COUNT(*) FROM horario 
WHERE materia_id IS NULL AND profesor_id IS NULL;
```

**Función de limpieza implementada:**
```python
def _limpiar_horarios_vacios(self):
    """Elimina horarios sin materia ni profesor"""
    if not messagebox.askyesno('Confirmar', 
                               '¿Eliminar horarios vacíos?\n'
                               'Esta acción no se puede deshacer.'):
        return
    
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM horario WHERE materia_id IS NULL AND profesor_id IS NULL')
    filas_eliminadas = c.rowcount
    conn.commit()
    conn.close()
    
    messagebox.showinfo('Éxito', f'{filas_eliminadas} horarios vacíos eliminados.')
    self._dibujar_grilla_horario_curso()
```

#### 12.2.3 Optimización de Base de Datos

**Vacuum (compactar):**
```sql
-- Ejecutar periódicamente para recuperar espacio
VACUUM;
```

**Reindexar:**
```sql
-- Reconstruir índices
REINDEX;
```

**Análisis de estadísticas:**
```sql
-- Actualizar estadísticas del optimizador
ANALYZE;
```

**Script de mantenimiento:**
```python
def mantenimiento_db():
    """Ejecuta mantenimiento de la base de datos"""
    conn = get_connection()
    c = conn.cursor()
    
    print("Ejecutando VACUUM...")
    c.execute('VACUUM')
    
    print("Ejecutando REINDEX...")
    c.execute('REINDEX')
    
    print("Ejecutando ANALYZE...")
    c.execute('ANALYZE')
    
    conn.close()
    print("Mantenimiento completado.")
```

### 12.3 Logs y Diagnóstico

#### 12.3.1 Información de Versión

**Agregar constantes al inicio del archivo:**
```python
VERSION = "0.9"
BUILD_DATE = "2024-11-08"
```

**Mostrar en ventana "Acerca de":**
```python
def mostrar_acerca_de(self):
    info = (
        f"Sistema de Gestión de Horarios Escolares\n"
        f"Versión: {VERSION}\n"
        f"Build: {BUILD_DATE}\n\n"
        f"Desarrollado para [Institución]\n"
        f"© 2024"
    )
    messagebox.showinfo('Acerca de', info)
```

#### 12.3.2 Diagnóstico de Instalación

**Script:** `diagnosticar_instalacion.py`

```python
import sys
import sqlite3
import os
import tkinter as tk

print("=== DIAGNÓSTICO DEL SISTEMA ===\n")

# Python
print(f"Python: {sys.version}")
print(f"Ejecutable: {sys.executable}")

# SQLite
print(f"\nSQLite: {sqlite3.sqlite_version}")

# Tkinter
try:
    root = tk.Tk()
    print(f"\nTkinter: OK")
    print(f"Tcl/Tk: {root.tk.call('info', 'patchlevel')}")
    root.destroy()
except Exception as e:
    print(f"\nTkinter: ERROR - {e}")

# Base de datos
db_path = "institucion.db"
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    print(f"\nBase de datos: ENCONTRADA")
    print(f"Tamaño: {os.path.getsize(db_path) / 1024:.2f} KB")
    
    # Contar registros
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tablas = [row[0] for row in c.fetchall()]
    print(f"Tablas: {len(tablas)}")
    
    for tabla in tablas:
        c.execute(f'SELECT COUNT(*) FROM {tabla}')
        count = c.fetchone()[0]
        print(f"  - {tabla}: {count} registros")
    
    conn.close()
else:
    print(f"\nBase de datos: NO ENCONTRADA")

print("\n=== FIN DEL DIAGNÓSTICO ===")
```

### 12.4 Actualización de Versiones

#### 12.4.1 Proceso de Actualización

**Pasos:**
1. Crear backup de `institucion.db`
2. Cerrar aplicación
3. Reemplazar `SistemaHorarios.exe`
4. Ejecutar migraciones de BD (si aplica)
5. Abrir aplicación y verificar

**Script de actualización:**
```powershell
# actualizar.ps1
$backupDir = "backups"
$dbFile = "institucion.db"
$exeFile = "SistemaHorarios.exe"

# 1. Backup
New-Item -ItemType Directory -Force -Path $backupDir
$fecha = Get-Date -Format "yyyyMMdd_HHmmss"
Copy-Item $dbFile "$backupDir\institucion_$fecha.db"

Write-Host "Backup creado: $backupDir\institucion_$fecha.db" -ForegroundColor Green

# 2. Detener procesos
Get-Process -Name SistemaHorarios -ErrorAction SilentlyContinue | Stop-Process

# 3. Reemplazar ejecutable
Copy-Item "nueva_version\$exeFile" $exeFile -Force

Write-Host "Ejecutable actualizado." -ForegroundColor Green
Write-Host "Puede iniciar la aplicación." -ForegroundColor Cyan
```

#### 12.4.2 Compatibilidad de Versiones

**Versión 0.9:**
- ✅ Compatible con BD de v0.8 (con migración)
- ❓ Compatibilidad futura con v1.0 (requiere migración de esquema)

**Migración v0.8 → v0.9:**
```sql
-- Agregar campo turno_id a horario
ALTER TABLE horario ADD COLUMN turno_id INTEGER REFERENCES turno(id);

-- Poblar valores
UPDATE horario 
SET turno_id = (
    SELECT turno_id 
    FROM division 
    WHERE division.id = horario.division_id
)
WHERE division_id IS NOT NULL;
```

### 12.5 Soporte y Contacto

#### 12.5.1 Recursos de Ayuda

**Documentación:**
- `ACTA_DE_CONSTITUCION.md` - Visión general del proyecto
- `DOCUMENTACION_TECNICA.md` - Este documento (referencia técnica)
- `MANUAL_DE_USUARIO.md` - Guía para usuarios finales

**Repositorio:**
- GitHub: `Chinejo/SistemaEscolar`
- Branch: `dev` (desarrollo activo)

#### 12.5.2 Reporte de Bugs

**Información a incluir:**
1. **Versión del sistema:** (ver "Acerca de")
2. **Sistema operativo:** Windows X, versión
3. **Descripción del problema:** Qué estaba haciendo
4. **Pasos para reproducir:** Secuencia exacta
5. **Resultado esperado:** Qué debería pasar
6. **Resultado actual:** Qué pasó realmente
7. **Capturas de pantalla:** Si aplica
8. **Archivo de log:** Si existe

**Plantilla:**
```markdown
## Reporte de Bug

**Versión:** 0.9
**SO:** Windows 10 Pro 64-bit

**Descripción:**
Al intentar asignar un horario en la vista por profesor, aparece un error.

**Pasos:**
1. Abrir "Gestión de horarios" → "Por profesor"
2. Seleccionar profesor "García"
3. Hacer click en Lunes 1ª hora
4. Completar formulario
5. Click en "Guardar"

**Resultado esperado:**
El horario se guarda correctamente.

**Resultado actual:**
Error: "Foreign key constraint failed"

**Capturas:**
[adjuntar imagen]
```

#### 12.5.3 Solicitudes de Funcionalidades

**Proceso:**
1. Verificar que no esté en versión de desarrollo (v2.0)
2. Crear issue en GitHub con etiqueta "enhancement"
3. Describir funcionalidad con casos de uso
4. Indicar prioridad (baja/media/alta)

---

## 13. CONCLUSIONES

### 13.1 Estado Actual del Sistema

**Versión 0.9** es un sistema **funcional y completo** que cumple con los requisitos básicos de gestión de horarios escolares. 

**Características Principales:**
- ✅ CRUD completo de todas las entidades
- ✅ Dos vistas de horarios (por curso y por profesor)
- ✅ Sincronización automática entre vistas
- ✅ Validaciones de reglas de negocio
- ✅ Interfaz intuitiva con filtros y autocompletado
- ✅ Base de datos relacional con integridad referencial
- ✅ Compilable a ejecutable standalone

**Limitaciones Conocidas:**
- ⚠️ Arquitectura monolítica (dificulta mantenimiento)
- ⚠️ Sin pruebas automatizadas
- ⚠️ Sin sistema de logging
- ⚠️ Sin gestión de usuarios ni permisos
- ⚠️ Sin exportación a formatos externos (PDF, Excel)
- ⚠️ Sin respaldo automático

### 13.2 Próximos Pasos (v2.0)

El plan de refactorización para la **versión 2.0** incluye:

1. **Arquitectura modular:** Separación en paquetes (ver `version 2.0/` en workspace)
2. **Testing automatizado:** Implementar pytest con cobertura >70%
3. **Logging estructurado:** Registro de todas las operaciones
4. **Exportación:** PDF de horarios por curso y profesor
5. **Backup automático:** Copias diarias/semanales
6. **Gestión de períodos:** Soporte para cuatrimestres/semestres
7. **Impresión optimizada:** Formatos listos para imprimir

**Referencia:** Ver `version 2.0/PLAN_REFACTORIZACION.md` para detalles completos.

### 13.3 Consideraciones Finales

**Para Desarrolladores:**
- El código es legible y está bien estructurado a pesar de ser monolítico
- Las funciones están bien nombradas y documentadas
- El decorador `@db_operation` centraliza la lógica transaccional
- La separación en secciones facilita la navegación del código

**Para Administradores del Sistema:**
- El sistema es estable y puede usarse en producción
- Realizar backups periódicos de `institucion.db`
- Mantener documentación actualizada para usuarios finales
- Capacitar usuarios en flujo de trabajo jerárquico

**Para Usuarios Finales:**
- Seguir el orden lógico: Turnos → Planes → Materias → Profesores → Divisiones → Horarios
- Utilizar filtros para agilizar búsquedas
- Verificar siempre las validaciones antes de guardar
- Reportar inconsistencias inmediatamente

---

**FIN DE LA DOCUMENTACIÓN TÉCNICA**

**Versión del Documento:** 1.0  
**Fecha:** 8 de noviembre de 2025  
**Autor:** Sistema de Documentación Automatizada  
**Revisión:** [Pendiente]

---

**Anexos:**
- Ver `ACTA_DE_CONSTITUCION.md` para contexto del proyecto
- Ver `MANUAL_DE_USUARIO.md` para guías de uso (próximo documento)
- Ver `version 2.0/` para planificación de refactorización
