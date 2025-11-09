# MANUAL DE USUARIO
## Sistema de Gestión de Horarios Escolares v0.9

---

## ÍNDICE

### PARTE 1: INTRODUCCIÓN Y CONCEPTOS BÁSICOS
1. [Bienvenida](#1-bienvenida)
2. [Requisitos del Sistema](#2-requisitos-del-sistema)
3. [Instalación y Primer Inicio](#3-instalación-y-primer-inicio)
4. [Conceptos Básicos](#4-conceptos-básicos)
5. [Navegación de la Interfaz](#5-navegación-de-la-interfaz)

### PARTE 2: CONFIGURACIÓN INICIAL
6. [Configuración Inicial del Sistema](#6-configuración-inicial-del-sistema)
7. [Gestión de Turnos](#7-gestión-de-turnos)
8. [Gestión de Planes de Estudio](#8-gestión-de-planes-de-estudio)
9. [Gestión de Materias/Obligaciones](#9-gestión-de-materiasobligaciones)

### PARTE 3: GESTIÓN DE PERSONAL Y CURSOS
10. [Gestión de Personal Docente](#10-gestión-de-personal-docente)
11. [Gestión de Cursos/Divisiones](#11-gestión-de-cursosdivisiones)

### PARTE 4: GESTIÓN DE HORARIOS
12. [Configuración de Horas por Turno](#12-configuración-de-horas-por-turno)
13. [Horarios por Curso](#13-horarios-por-curso)
14. [Horarios por Profesor](#14-horarios-por-profesor)

### PARTE 5: OPERACIONES AVANZADAS Y TROUBLESHOOTING
15. [Operaciones Avanzadas](#15-operaciones-avanzadas)
16. [Preguntas Frecuentes](#16-preguntas-frecuentes)
17. [Solución de Problemas](#17-solución-de-problemas)
18. [Glosario](#18-glosario)

---

# PARTE 1: INTRODUCCIÓN Y CONCEPTOS BÁSICOS

## 1. BIENVENIDA

### 1.1 ¿Qué es el Sistema de Gestión de Horarios Escolares?

El **Sistema de Gestión de Horarios Escolares** es una aplicación diseñada para facilitar la organización y administración de horarios de clases en instituciones educativas. Permite gestionar de manera centralizada toda la información relacionada con:

- 📚 **Materias y planes de estudio**
- 👨‍🏫 **Personal docente y sus asignaciones**
- 🏫 **Divisiones/cursos y turnos**
- 📅 **Horarios semanales completos**

### 1.2 ¿Para quién está diseñado este sistema?

Este sistema está pensado para ser utilizado por:

- **Secretarios/as de la institución:** Carga inicial de datos y mantenimiento
- **Coordinadores/as pedagógicos:** Asignación de horarios y profesores
- **Personal administrativo:** Consulta de horarios y reportes
- **Directivos:** Supervisión general de la distribución horaria

### 1.3 Características principales

✅ **Gestión integral de datos educativos**
- Materias, profesores, planes de estudio, turnos, cursos

✅ **Dos vistas de horarios**
- Por curso: Ver todas las materias de una división
- Por profesor: Ver todos los horarios de un docente

✅ **Sincronización automática**
- Los cambios en una vista se reflejan instantáneamente en la otra

✅ **Validaciones inteligentes**
- Previene errores como superposición de horarios
- Valida que los profesores tengan las materias asignadas

✅ **Interfaz amigable**
- Filtros en tiempo real
- Autocompletado de campos
- Navegación intuitiva

✅ **Sin necesidad de conexión a internet**
- Funciona completamente offline
- Datos almacenados localmente de forma segura

### 1.4 ¿Qué NO hace este sistema?

Para tener expectativas claras, el sistema **NO** incluye:

- ❌ Gestión de alumnos o inscripciones
- ❌ Calificaciones o notas
- ❌ Asistencia de profesores o estudiantes
- ❌ Gestión de aulas físicas o recursos
- ❌ Comunicación con padres o estudiantes
- ❌ Generación de certificados o constancias

**Nota:** Este sistema se enfoca exclusivamente en la organización de horarios semanales.

---

## 2. REQUISITOS DEL SISTEMA

### 2.1 Requisitos de Hardware

#### Mínimos (requeridos)
- **Procesador:** Intel Pentium 4 o equivalente
- **Memoria RAM:** 2 GB
- **Espacio en disco:** 50 MB libres
- **Resolución de pantalla:** 1024x768 píxeles

#### Recomendados (para mejor experiencia)
- **Procesador:** Intel Core i3 o superior
- **Memoria RAM:** 4 GB o más
- **Espacio en disco:** 100 MB libres
- **Resolución de pantalla:** 1366x768 píxeles o superior

### 2.2 Requisitos de Software

#### Sistema Operativo (uno de los siguientes)
- ✅ Windows 7 SP1 o superior
- ✅ Windows 8 / 8.1
- ✅ Windows 10 (todas las versiones)
- ✅ Windows 11

#### Otros requisitos
- **NO** requiere instalación de Python
- **NO** requiere conexión a internet
- **NO** requiere permisos de administrador (si se ejecuta desde carpeta de usuario)

### 2.3 Permisos necesarios

El programa necesita:
- ✅ **Lectura y escritura** en la carpeta donde se encuentra instalado
- ✅ **Creación de archivos** (para la base de datos `horarios.db`)

**Recomendación:** Instalar en `Mis Documentos` o en `C:\SistemaHorarios` (evitar `Archivos de programa` que requiere permisos de administrador para escribir).

---

## 3. INSTALACIÓN Y PRIMER INICIO

### 3.1 Instalación del Sistema

El sistema viene en formato de **ejecutable standalone** (archivo `.exe`), lo que significa que no requiere instalación tradicional.

#### Opción A: Ejecutable portable (recomendado)

**Pasos:**

1. **Descargar** el archivo `SistemaHorarios.exe`

2. **Crear una carpeta** para el sistema:
   ```
   Ejemplo: C:\SistemaHorarios\
   o: C:\Users\[TuUsuario]\Documents\SistemaHorarios\
   ```

3. **Copiar** el archivo `SistemaHorarios.exe` a esa carpeta

4. **Listo!** Ya puede ejecutar el programa

**Ventajas:**
- No modifica el sistema operativo
- Fácil de respaldar (solo copiar la carpeta completa)
- Puede ejecutarse desde una memoria USB

#### Opción B: Con instalador

Si recibió un instalador (`SistemaHorarios_Setup.exe`):

1. **Ejecutar** el instalador
2. **Seguir** los pasos del asistente
3. El programa se instalará en `C:\Program Files\SistemaHorarios\`
4. Se creará un acceso directo en el Escritorio y en el Menú Inicio

### 3.2 Primer inicio del programa

**Al ejecutar por primera vez:**

1. **Doble clic** en `SistemaHorarios.exe`

2. Se abrirá la ventana principal:
   ```
   ┌────────────────────────────────────────┐
   │ Gestión de Horarios Escolares    [_][□][X]│
   ├────────────────────────────────────────┤
   │ [Plan de estudios ▼] [Turnos ▼] ...   │
   ├────────────────────────────────────────┤
   │                                        │
   │   Bienvenido al Sistema de Gestión    │
   │        de Horarios Escolares          │
   │                                        │
   │   Seleccione una opción del menú      │
   │         para comenzar                 │
   │                                        │
   └────────────────────────────────────────┘
   ```

3. Se creará automáticamente el archivo `horarios.db` en la misma carpeta del programa

4. El sistema está listo para usar (pero sin datos aún)

### 3.3 Estructura de archivos

Después del primer inicio, verá:

```
SistemaHorarios/
├── SistemaHorarios.exe    (programa ejecutable)
└── horarios.db            (base de datos - creado automáticamente)
```

**Importante:**
- ⚠️ **NUNCA elimine ni modifique manualmente** el archivo `horarios.db`
- ✅ Este archivo contiene TODOS los datos del sistema
- ✅ Para hacer respaldo, simplemente copie este archivo

### 3.4 Creación de respaldos

**Es MUY IMPORTANTE hacer copias de seguridad periódicas.**

#### Respaldo manual simple:

1. **Cerrar** el programa
2. **Copiar** el archivo `horarios.db`
3. **Pegar** en una carpeta de respaldo con la fecha:
   ```
   Ejemplo: 
   C:\Respaldos\horarios_2025-11-08.db
   ```

#### Frecuencia recomendada:
- 📅 **Diario:** Si se realizan muchos cambios
- 📅 **Semanal:** Para uso moderado
- 📅 **Mensual:** Mínimo recomendado

#### Restauración desde respaldo:

1. **Cerrar** el programa
2. **Eliminar** (o renombrar) el archivo `horarios.db` actual
3. **Copiar** el respaldo y renombrarlo a `horarios.db`
4. **Abrir** el programa nuevamente

---

## 4. CONCEPTOS BÁSICOS

### 4.1 Jerarquía de datos

El sistema maneja los datos en un orden jerárquico. Es importante entender este orden para usarlo correctamente:

```
1. TURNOS
   ├─ Mañana
   ├─ Tarde
   └─ Noche
   
2. PLANES DE ESTUDIO
   ├─ Bachiller en Ciencias Naturales
   ├─ Bachiller en Economía
   └─ Perito Mercantil
   
3. MATERIAS/OBLIGACIONES
   ├─ Matemática
   ├─ Física
   ├─ Lengua
   └─ ...
   
4. AÑOS/CURSOS (dentro de cada plan)
   ├─ 1° Año
   ├─ 2° Año
   └─ ...
   
5. PERSONAL DOCENTE
   ├─ García López, Juan
   ├─ Martínez, María
   └─ ...
   
6. DIVISIONES (combinación de Turno + Plan + Año)
   ├─ Mañana - Bachiller - 1° Año - División A
   ├─ Mañana - Bachiller - 1° Año - División B
   └─ ...
   
7. HORARIOS (asignación de Profesor + Materia a División)
   └─ Lunes 8:00 - Matemática - Prof. García - 1°A
```

**Regla de oro:** Siempre se deben crear los datos en este orden, de arriba hacia abajo.

### 4.2 Relaciones entre entidades

#### Turno ↔ Plan de Estudio
- Un **turno** puede tener varios **planes**
- Un **plan** puede ofrecerse en varios **turnos**
- Ejemplo: "Bachiller" se ofrece en turno Mañana y Tarde

#### Plan de Estudio ↔ Materias
- Un **plan** tiene varias **materias**
- Una **materia** puede estar en varios **planes**
- Ejemplo: "Matemática" está en todos los planes

#### Año ↔ Materias
- Un **año** tiene varias **materias**
- Una **materia** puede estar en varios **años**
- Ejemplo: "Matemática" está en 1°, 2° y 3° año

#### Profesor ↔ Materias (Banca de horas)
- Un **profesor** puede dar varias **materias**
- Una **materia** puede ser dada por varios **profesores**
- Cada relación tiene una **banca de horas** (cantidad asignada)

#### División
- Combina: **Turno + Plan + Año + Nombre**
- Ejemplo: "Turno Mañana - Bachiller - 1° Año - División A"

#### Horario
- Combina: **División + Día + Hora + Materia + Profesor**
- Es la pieza final que une todo

### 4.3 Contadores automáticos

El sistema mantiene dos contadores que se actualizan automáticamente:

#### 1. Horas semanales de materia
- **Qué es:** Total de horas asignadas a una materia en toda la institución
- **Cómo se calcula:** Se incrementa al asignar un horario, se decrementa al eliminarlo
- **Ejemplo:** Si "Matemática" tiene 5 horas en 1°A, 5 horas en 1°B y 4 horas en 2°A, el total es 14 horas semanales

#### 2. Banca de horas de profesor
- **Qué es:** Horas efectivamente asignadas a un profesor en una materia
- **Cómo se calcula:** Se incrementa al asignar un horario con ese profesor, se decrementa al eliminarlo
- **Ejemplo:** Si el profesor García tiene 5 horarios de Matemática asignados, su banca de horas en Matemática es 5

**Importante:** Estos números son automáticos. NO se ingresan manualmente.

### 4.4 Las dos vistas de horarios

El sistema ofrece dos formas diferentes de ver y gestionar los horarios:

#### Vista "Por Curso"
```
Objetivo: Ver todas las materias de una división/curso
Uso típico: Planificar el horario semanal de un curso
```

**Ejemplo:**
```
1° Año A - Turno Mañana
        Lunes    Martes   Miércoles
1ª hora Matemát. Física   Matemát.
        García   Pérez    García
2ª hora Lengua   Lengua   Química
        López    López    Martínez
```

#### Vista "Por Profesor"
```
Objetivo: Ver todos los horarios de un docente
Uso típico: Verificar la carga horaria de un profesor
```

**Ejemplo:**
```
Profesor García - Turno Mañana
        Lunes    Martes   Miércoles
1ª hora 1°A      1°B      1°A
        Matemát. Matemát. Matemát.
2ª hora 2°A      -        2°B
        Matemát.          Matemát.
```

**Sincronización:** Ambas vistas muestran la misma información. Si modifica un horario en una vista, el cambio se refleja automáticamente en la otra.

### 4.5 Validaciones del sistema

El sistema incluye validaciones para prevenir errores:

#### ✅ Validaciones implementadas:

1. **No duplicar nombres**
   - No puede haber dos materias con el mismo nombre
   - No puede haber dos profesores con el mismo nombre

2. **No superposición de profesores**
   - Un profesor no puede estar en dos lugares al mismo tiempo
   - Se valida por turno, día y hora

3. **Profesor debe tener la materia asignada**
   - Solo puede asignar materias que el profesor tiene en su "banca de horas"

4. **Profesor debe estar en el turno**
   - Solo puede asignar profesores que trabajen en ese turno

5. **División debe pertenecer al turno**
   - Al asignar desde vista por profesor, solo se pueden seleccionar divisiones del turno correcto

#### 🔔 Mensajes de validación:

Cuando intente hacer algo no permitido, verá mensajes como:
- ❌ "El profesor ya está asignado en ese horario en otra división del mismo turno"
- ❌ "El profesor no tiene asignada la materia seleccionada"
- ❌ "Ya existe una materia con ese nombre"

**Estos mensajes NO son errores del sistema, son protecciones para mantener la consistencia de los datos.**

---

## 5. NAVEGACIÓN DE LA INTERFAZ

### 5.1 Ventana principal

```
┌──────────────────────────────────────────────────────────┐
│  Gestión de Horarios Escolares                     [_][□][X]│
├──────────────────────────────────────────────────────────┤
│  [Plan de estudios ▼] [Turnos ▼] [Personal ▼]           │  ← Barra de menú
│  [Cursos ▼] [Gestión de horarios ▼]                     │
├──────────────────────────────────────────────────────────┤
│                                                          │
│                                                          │
│                                                          │
│              ÁREA DE TRABAJO PRINCIPAL                   │  ← Contenido cambia
│              (cambia según la vista)                     │     según la opción
│                                                          │     seleccionada
│                                                          │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### 5.2 Elementos comunes de la interfaz

#### Campos de texto
```
Nombre: [_______________________]
```
- Haga clic y escriba
- Use Tab para pasar al siguiente campo

#### Listas desplegables (Combobox)
```
Turno: [Mañana ▼]
```
- Haga clic en la flecha para ver opciones
- O empiece a escribir para filtrar

#### Botones
```
[Agregar]  [Editar]  [Eliminar]
```
- Haga clic para ejecutar la acción

#### Tablas (TreeView)
```
┌────────────────────────────────────┐
│ Nombre          │ Horas asignadas  │
├────────────────────────────────────┤
│ Matemática      │ 5                │
│ Física          │ 4                │
└────────────────────────────────────┘
```
- Haga clic en una fila para seleccionarla
- Doble clic NO hace nada (use botones)

#### Filtros
```
Filtro: [___________]
```
- Escriba para filtrar en tiempo real
- Borre el texto para ver todo

### 5.3 Menús del sistema

#### Menú "Plan de estudios"
```
Plan de estudios
├─ Gestionar Materias/Obligaciones
└─ Gestionar Planes de Estudio
```

#### Menú "Turnos"
```
Turnos
└─ Gestionar Turnos
```

#### Menú "Personal"
```
Personal
└─ Gestionar personal
```

#### Menú "Cursos"
```
Cursos
└─ Gestionar Cursos
```

#### Menú "Gestión de horarios"
```
Gestión de horarios
├─ Por curso
└─ Por profesor
```

### 5.4 Atajos de teclado

#### Globales
- **Tab:** Pasar al siguiente campo
- **Shift + Tab:** Volver al campo anterior
- **Enter:** En algunos casos, guarda o confirma (varía según la pantalla)
- **Esc:** Cerrar ventanas emergentes

#### En campos de búsqueda de profesor
- **Enter:** Selecciona la primera coincidencia
- **Esc:** Limpia el campo de búsqueda
- **Backspace:** Limpia el campo si está vacío

#### En campos de hora
- **Automático:** Al escribir "0845" se convierte en "08:45"
- **Navegación automática:** Al completar hora, pasa al siguiente campo

### 5.5 Consejos de navegación

#### ✅ Buenas prácticas:

1. **Use Tab para navegar entre campos**
   - Es más rápido que usar el mouse

2. **Use filtros para encontrar datos rápidamente**
   - Especialmente útil con muchos profesores o materias

3. **Los filtros funcionan mientras escribe**
   - No es necesario presionar Enter

4. **Seleccione en la tabla antes de editar o eliminar**
   - Los botones Editar/Eliminar actúan sobre la fila seleccionada

5. **Lea los mensajes del sistema**
   - Los mensajes de error suelen indicar exactamente qué falta o qué está mal

#### ⚠️ Errores comunes:

1. ❌ **Intentar editar sin seleccionar una fila**
   - Siempre seleccione la fila primero

2. ❌ **Ignorar los mensajes de validación**
   - Si algo no se guarda, lea el mensaje de error

3. ❌ **No usar los filtros con muchos datos**
   - Con 50+ profesores, use el filtro en lugar de buscar visualmente

---

# PARTE 2: CONFIGURACIÓN INICIAL

## 6. CONFIGURACIÓN INICIAL DEL SISTEMA

### 6.1 Orden recomendado de configuración

Para configurar el sistema desde cero, siga este orden estrictamente:

```
PASO 1: Crear Turnos
   ↓
PASO 2: Crear Planes de Estudio
   ↓
PASO 3: Crear Materias/Obligaciones
   ↓
PASO 4: Asignar Materias a Planes
   ↓
PASO 5: Crear Años/Cursos dentro de cada Plan
   ↓
PASO 6: Asignar Materias a cada Año
   ↓
PASO 7: Asignar Planes a Turnos
   ↓
PASO 8: Crear Personal Docente
   ↓
PASO 9: Asignar Materias a Profesores (Banca de horas)
   ↓
PASO 10: Asignar Turnos a Profesores
   ↓
PASO 11: Crear Divisiones/Cursos
   ↓
PASO 12: Configurar Horas por Turno (opcional pero recomendado)
   ↓
PASO 13: Asignar Horarios
```

**Tiempo estimado para configuración inicial completa:** 2-4 horas (dependiendo de la cantidad de datos)

### 6.2 Lista de verificación inicial

Antes de empezar, tenga preparada la siguiente información:

#### ✅ Información institucional:
- [ ] Lista de turnos que ofrece la institución (Mañana, Tarde, Noche)
- [ ] Lista de planes de estudio (Bachiller, Perito, etc.)
- [ ] Lista completa de materias/obligaciones
- [ ] Estructura de años por cada plan (1°, 2°, 3°, etc.)
- [ ] Materias por año en cada plan

#### ✅ Información del personal:
- [ ] Lista de profesores (nombre completo)
- [ ] Materias que puede dar cada profesor
- [ ] Turnos en los que trabaja cada profesor

#### ✅ Información de divisiones:
- [ ] Cantidad de divisiones por año y turno
- [ ] Nomenclatura de divisiones (A, B, C, etc.)

#### ✅ Información horaria:
- [ ] Horarios de entrada y salida por turno
- [ ] Duración de cada módulo/hora
- [ ] Cantidad de módulos por día

### 6.3 Ejemplo práctico: Institución "Escuela Ejemplo"

A lo largo de este manual, usaremos como ejemplo una institución ficticia con:

**Turnos:**
- Mañana (8:00 - 12:45)
- Tarde (13:00 - 17:45)

**Planes de Estudio:**
- Bachiller en Ciencias Naturales

**Materias:**
- Matemática, Física, Química, Biología, Lengua, Historia

**Años:**
- 1° Año, 2° Año, 3° Año

**Profesores:**
- García López, Juan Carlos (Matemática)
- Pérez Martínez, María Elena (Física, Química)
- Rodríguez, Carlos Alberto (Lengua, Historia)

**Divisiones:**
- 1° Año A (Mañana)
- 1° Año B (Mañana)
- 2° Año A (Tarde)

---

## 7. GESTIÓN DE TURNOS

### 7.1 ¿Qué son los turnos?

Los **turnos** representan los horarios en los que funciona la institución (Mañana, Tarde, Noche, etc.). Son la base de la organización horaria.

### 7.2 Acceder a la gestión de turnos

1. En el menú principal, haga clic en **"Turnos"**
2. Seleccione **"Gestionar Turnos"**

```
┌──────────────────────────────────────────┐
│  Gestión de Turnos                       │
├──────────────────────────────────────────┤
│  ┌────────────────────────────────────┐  │
│  │ Nombre                             │  │
│  ├────────────────────────────────────┤  │
│  │ (vacío)                            │  │
│  │                                    │  │
│  └────────────────────────────────────┘  │
├──────────────────────────────────────────┤
│  Nombre: [_______________________]       │
├──────────────────────────────────────────┤
│  [Agregar]  [Eliminar]                   │
│  [Planes del turno]                      │
└──────────────────────────────────────────┘
```

### 7.3 Crear un turno nuevo

**Ejemplo: Crear el turno "Mañana"**

**Paso 1:** Escriba el nombre en el campo "Nombre"
```
Nombre: [Mañana_____________]
```

**Paso 2:** Haga clic en el botón **[Agregar]**

**Resultado:**
```
┌────────────────────────────────────┐
│ Nombre                             │
├────────────────────────────────────┤
│ Mañana                             │ ← Aparece en la lista
└────────────────────────────────────┘
```

**Paso 3:** Repita para crear otros turnos (Tarde, Noche, etc.)

### 7.4 Asignar planes a un turno

Una vez creados los turnos y los planes de estudio (ver siguiente sección), debe vincularlos.

**Paso 1:** Seleccione un turno de la lista (haga clic sobre él)

**Paso 2:** Haga clic en el botón **[Planes del turno]**

Se abrirá una ventana emergente:

```
┌──────────────────────────────────────────┐
│  Planes del turno Mañana                 │
├──────────────────────────────────────────┤
│  Planes asignados al turno:              │
│  ┌────────────────────────────────────┐  │
│  │ Nombre                             │  │
│  ├────────────────────────────────────┤  │
│  │ (vacío inicialmente)               │  │
│  └────────────────────────────────────┘  │
├──────────────────────────────────────────┤
│  Plan: [Seleccione un plan ▼]            │
├──────────────────────────────────────────┤
│  [Agregar plan]  [Quitar seleccionado]   │
└──────────────────────────────────────────┘
```

**Paso 3:** Seleccione un plan de la lista desplegable

**Paso 4:** Haga clic en **[Agregar plan]**

**Resultado:** El plan aparece en la lista de "Planes asignados al turno"

**Paso 5:** Cierre la ventana cuando termine

### 7.5 Eliminar un turno

⚠️ **ADVERTENCIA:** Eliminar un turno eliminará también:
- Todas las divisiones de ese turno
- Todos los horarios asociados

**Paso 1:** Seleccione el turno de la lista

**Paso 2:** Haga clic en **[Eliminar]**

**Paso 3:** Confirme la acción en el mensaje que aparece

**Recomendación:** Solo elimine turnos si está seguro y ha hecho un respaldo antes.

### 7.6 Consejos para turnos

✅ **Buenas prácticas:**
- Use nombres claros y consistentes: "Mañana", "Tarde", "Noche"
- No use abreviaturas confusas
- Cree todos los turnos al inicio, antes de continuar

⚠️ **Errores comunes:**
- ❌ Crear turno "Mañ" en lugar de "Mañana"
- ❌ Crear turnos con espacios extras: "Mañana " vs "Mañana"
- ❌ Intentar crear divisiones antes de asignar planes al turno

---

## 8. GESTIÓN DE PLANES DE ESTUDIO

### 8.1 ¿Qué son los planes de estudio?

Los **planes de estudio** son los diferentes programas educativos que ofrece la institución:
- Bachiller en Ciencias Naturales
- Bachiller en Economía y Gestión
- Perito Mercantil
- Técnico en Computación
- etc.

### 8.2 Acceder a la gestión de planes

1. En el menú principal, haga clic en **"Plan de estudios"**
2. Seleccione **"Gestionar Planes de Estudio"**

```
┌──────────────────────────────────────────┐
│  Gestión de Planes de Estudio            │
├──────────────────────────────────────────┤
│  ┌────────────────────────────────────┐  │
│  │ Nombre                             │  │
│  ├────────────────────────────────────┤  │
│  │ (vacío)                            │  │
│  │                                    │  │
│  └────────────────────────────────────┘  │
├──────────────────────────────────────────┤
│  Nombre: [_______________________]       │
├──────────────────────────────────────────┤
│  [Agregar]  [Eliminar]                   │
│  [Materias/Obligaciones del plan]        │
│  [Cursos del plan]                       │
└──────────────────────────────────────────┘
```

### 8.3 Crear un plan de estudio

**Ejemplo: Crear "Bachiller en Ciencias Naturales"**

**Paso 1:** Escriba el nombre completo del plan
```
Nombre: [Bachiller en Ciencias Naturales_]
```

**Paso 2:** Haga clic en **[Agregar]**

**Resultado:**
```
┌────────────────────────────────────────┐
│ Nombre                                 │
├────────────────────────────────────────┤
│ Bachiller en Ciencias Naturales       │
└────────────────────────────────────────┘
```

### 8.4 Asignar materias al plan

Después de crear materias (ver siguiente sección), debe asignarlas a cada plan.

**Paso 1:** Seleccione el plan de la lista

**Paso 2:** Haga clic en **[Materias/Obligaciones del plan]**

Se abre una ventana:

```
┌──────────────────────────────────────────┐
│  Materias del plan: Bachiller...         │
├──────────────────────────────────────────┤
│  Materias asignadas:                     │
│  ┌────────────────────────────────────┐  │
│  │ Nombre                             │  │
│  ├────────────────────────────────────┤  │
│  │ (vacío inicialmente)               │  │
│  └────────────────────────────────────┘  │
├──────────────────────────────────────────┤
│  Materia: [Seleccione una materia ▼]    │
├──────────────────────────────────────────┤
│  [Agregar materia]  [Quitar seleccionada]│
└──────────────────────────────────────────┘
```

**Paso 3:** Seleccione una materia de la lista desplegable

**Paso 4:** Haga clic en **[Agregar materia]**

**Paso 5:** Repita para todas las materias del plan

**Paso 6:** Cierre la ventana

### 8.5 Crear y gestionar años/cursos del plan

Cada plan tiene varios años (1°, 2°, 3°, etc.). Debe crearlos y asignar materias a cada uno.

**Paso 1:** Seleccione el plan de la lista

**Paso 2:** Haga clic en **[Cursos del plan]**

Se abre una ventana:

```
┌──────────────────────────────────────────┐
│  Cursos del plan: Bachiller...           │
├──────────────────────────────────────────┤
│  Cursos/Años:                            │
│  ┌────────────────────────────────────┐  │
│  │ Nombre                             │  │
│  ├────────────────────────────────────┤  │
│  │ (vacío inicialmente)               │  │
│  └────────────────────────────────────┘  │
├──────────────────────────────────────────┤
│  Nombre del año: [_________________]     │
├──────────────────────────────────────────┤
│  [Agregar año]  [Eliminar año]           │
│  [Materias del año]                      │
└──────────────────────────────────────────┘
```

**Paso 3:** Escriba el nombre del año
```
Ejemplo: "1° Año" o "Primer Año"
```

**Paso 4:** Haga clic en **[Agregar año]**

**Paso 5:** Repita para todos los años del plan (2°, 3°, etc.)

### 8.6 Asignar materias a cada año

Dentro de la ventana de "Cursos del plan":

**Paso 1:** Seleccione un año de la lista

**Paso 2:** Haga clic en **[Materias del año]**

Se abre una nueva ventana:

```
┌──────────────────────────────────────────┐
│  Materias del año: 1° Año                │
├──────────────────────────────────────────┤
│  Materias asignadas a este año:          │
│  ┌────────────────────────────────────┐  │
│  │ Nombre                             │  │
│  ├────────────────────────────────────┤  │
│  │ (vacío)                            │  │
│  └────────────────────────────────────┘  │
├──────────────────────────────────────────┤
│  Materia: [Seleccione ▼]                 │
│  (Solo materias del plan)                │
├──────────────────────────────────────────┤
│  [Agregar materia]  [Quitar seleccionada]│
└──────────────────────────────────────────┘
```

**Paso 3:** Seleccione las materias que corresponden a ese año

**Paso 4:** Agregue una por una

**Paso 5:** Cierre las ventanas cuando termine

### 8.7 Ejemplo completo: Plan Bachiller

**Estructura del plan:**

```
Bachiller en Ciencias Naturales
├── 1° Año
│   ├── Matemática
│   ├── Física
│   ├── Lengua
│   └── Historia
├── 2° Año
│   ├── Matemática
│   ├── Química
│   ├── Biología
│   └── Lengua
└── 3° Año
    ├── Física
    ├── Química
    └── Proyecto Final
```

### 8.8 Eliminar un plan

⚠️ **ADVERTENCIA CRÍTICA:** Eliminar un plan eliminará:
- Todos los años del plan
- Todas las divisiones asociadas
- Todos los horarios de esas divisiones

**Solo elimine planes si está completamente seguro.**

### 8.9 Consejos para planes de estudio

✅ **Buenas prácticas:**
- Use nombres oficiales completos
- Cree la estructura completa de años antes de crear divisiones
- Asigne todas las materias correspondientes a cada año
- Documente la estructura en un archivo externo (Excel, Word)

⚠️ **Errores comunes:**
- ❌ Olvidar asignar materias a los años (solo asignar al plan)
- ❌ Crear divisiones antes de completar la estructura del plan
- ❌ No verificar que todas las materias estén correctamente asignadas

---

## 9. GESTIÓN DE MATERIAS/OBLIGACIONES

### 9.1 ¿Qué son las materias?

Las **materias** (también llamadas obligaciones) son las asignaturas que se dictan:
- Matemática, Física, Lengua, Historia, etc.
- También pueden incluir espacios curriculares, talleres, etc.

### 9.2 Acceder a la gestión de materias

1. En el menú principal, haga clic en **"Plan de estudios"**
2. Seleccione **"Gestionar Materias/Obligaciones"**

```
┌──────────────────────────────────────────┐
│  Gestión de Materias/Obligaciones        │
├──────────────────────────────────────────┤
│  Total de materias/obligaciones: 0       │
│  Total de horas institucionales: 0       │
├──────────────────────────────────────────┤
│  Filtro: [___________________]           │
├──────────────────────────────────────────┤
│  ┌────────────────────────────────────┐  │
│  │ Nombre       │ Horas asignadas     │  │
│  ├────────────────────────────────────┤  │
│  │ (vacío)                            │  │
│  └────────────────────────────────────┘  │
├──────────────────────────────────────────┤
│  Nombre: [_______________________]       │
├──────────────────────────────────────────┤
│  [Agregar]  [Editar]  [Eliminar]         │
└──────────────────────────────────────────┘
```

### 9.3 Crear una materia

**Ejemplo: Crear "Matemática"**

**Paso 1:** Escriba el nombre de la materia
```
Nombre: [Matemática_____________]
```

**Paso 2:** Haga clic en **[Agregar]**

**Resultado:**
```
┌────────────────────────────────────┐
│ Nombre       │ Horas asignadas     │
├────────────────────────────────────┤
│ Matemática   │ 0                   │ ← Horas en 0 inicialmente
└────────────────────────────────────┘
```

**Nota importante:** Las "Horas asignadas" empiezan en 0 y se incrementan automáticamente al asignar horarios. **NO se editan manualmente.**

**Paso 3:** Repita para crear todas las materias

**Ejemplo de lista completa:**
```
┌────────────────────────────────────┐
│ Nombre       │ Horas asignadas     │
├────────────────────────────────────┤
│ Biología     │ 0                   │
│ Física       │ 0                   │
│ Historia     │ 0                   │
│ Lengua       │ 0                   │
│ Matemática   │ 0                   │
│ Química      │ 0                   │
└────────────────────────────────────┘
```

### 9.4 Editar una materia

Solo puede editar el **nombre** de una materia. Las horas son automáticas.

**Paso 1:** Seleccione la materia en la lista (haga clic sobre ella)

**Paso 2:** El nombre aparece en el campo "Nombre"
```
Nombre: [Matemática_____________]
```

**Paso 3:** Modifique el nombre si es necesario

**Paso 4:** Haga clic en **[Editar]**

**Resultado:** El nombre se actualiza en la lista

### 9.5 Eliminar una materia

⚠️ **ADVERTENCIA:** Eliminar una materia eliminará:
- Su asignación en todos los planes
- Su asignación en la banca de todos los profesores
- Todos los horarios donde se usa

**Solo elimine materias si está seguro.**

**Paso 1:** Seleccione la materia

**Paso 2:** Haga clic en **[Eliminar]**

**Paso 3:** Confirme la eliminación

### 9.6 Usar el filtro

Con muchas materias, use el filtro para buscar rápidamente:

**Ejemplo: Buscar "matemática"**

```
Filtro: [matem____________]
```

La lista se filtra mientras escribe:
```
┌────────────────────────────────────┐
│ Nombre       │ Horas asignadas     │
├────────────────────────────────────┤
│ Matemática   │ 5                   │ ← Solo muestra coincidencias
└────────────────────────────────────┘
```

**Para ver todo nuevamente:** Borre el texto del filtro

### 9.7 Interpretar las "Horas asignadas"

La columna "Horas asignadas" muestra el **total de horas semanales** de esa materia en toda la institución.

**Ejemplo:**
```
Matemática   │ 15
```

Significa que en total hay **15 horas semanales** de Matemática asignadas, sumando:
- Todas las divisiones
- Todos los turnos
- Todos los años

**Cómo se calcula:**
- Se suma 1 por cada horario asignado
- Ejemplo: Si 1°A tiene 5 horas de Matemática, 1°B tiene 5, y 2°A tiene 5, el total es 15

**Actualización:**
- ➕ Aumenta automáticamente al asignar un horario con esa materia
- ➖ Disminuye automáticamente al eliminar un horario

### 9.8 Totales institucionales

En la parte superior verá dos contadores:

```
Total de materias/obligaciones: 6
Total de horas institucionales: 85
```

**Total de materias:** Cantidad de materias creadas

**Total de horas institucionales:** Suma de todas las horas asignadas de todas las materias

**Ejemplo de interpretación:**
```
Total de horas institucionales: 240
```
Significa que la institución tiene un total de 240 módulos/horas de clase por semana entre todas las divisiones.

### 9.9 Consejos para materias

✅ **Buenas prácticas:**
- Use nombres completos y oficiales
- Sea consistente con mayúsculas/minúsculas
- Evite abreviaturas confusas
- Cree todas las materias de una vez al inicio
- Use nombres que identifiquen claramente la materia

**Ejemplos de buenos nombres:**
- ✅ "Matemática"
- ✅ "Lengua y Literatura"
- ✅ "Educación Física"
- ✅ "Taller de Programación I"

**Ejemplos de malos nombres:**
- ❌ "Mat" (muy abreviado)
- ❌ "Matemática " (espacio al final)
- ❌ "matematica" (sin tilde)
- ❌ "MATEMATICA" (todo mayúsculas)

⚠️ **Errores comunes:**
- ❌ Crear materias con nombres similares: "Matemática" y "Matematica" (sin tilde)
- ❌ Intentar editar las horas manualmente (son automáticas)
- ❌ Eliminar materias que ya tienen horarios asignados sin verificar
- ❌ No usar el filtro cuando hay muchas materias

### 9.10 Caso de uso: Preparar materias para un plan nuevo

**Escenario:** Va a agregar un nuevo plan "Técnico en Computación" que tiene materias específicas.

**Paso 1:** Identifique qué materias ya existen
```
Existentes: Matemática, Física, Lengua
```

**Paso 2:** Cree solo las materias nuevas
```
Nuevas: Programación I, Programación II, Base de Datos, Redes
```

**Paso 3:** Al configurar el plan, asigne tanto las existentes como las nuevas

**Ventaja:** Las materias comunes (Matemática, Física) se reutilizan entre planes.

---

# PARTE 3: GESTIÓN DE PERSONAL Y CURSOS

## 10. GESTIÓN DE PERSONAL DOCENTE

### 10.1 ¿Qué es el personal docente?

El **personal docente** representa a todos los profesores que trabajan en la institución. Para cada profesor se gestiona:
- Nombre completo
- Materias que puede dictar (Banca de horas)
- Turnos en los que trabaja
- Horas efectivamente asignadas en horarios

### 10.2 Acceder a la gestión de personal

1. En el menú principal, haga clic en **"Personal"**
2. Seleccione **"Gestionar personal"**

```
┌──────────────────────────────────────────────────────┐
│  Gestión de personal                                 │
├──────────────────────────────────────────────────────┤
│  Total de agentes: 0                                 │
├──────────────────────────────────────────────────────┤
│  Filtro: [___________]  Turno: [Todos ▼]            │
├──────────────────────────────────────────────────────┤
│  ┌────────────────────────────────────────────────┐  │
│  │ Nombre                                         │  │
│  ├────────────────────────────────────────────────┤  │
│  │ (vacío)                                        │  │
│  └────────────────────────────────────────────────┘  │
├──────────────────────────────────────────────────────┤
│  Nombre: [_________________________________]         │
├──────────────────────────────────────────────────────┤
│  [Agregar]  [Editar]  [Eliminar]                     │
│  [Banca de horas]  [Turnos del agente]               │
└──────────────────────────────────────────────────────┘
```

### 10.3 Crear un profesor

**Ejemplo: Crear el profesor "García López, Juan Carlos"**

**Paso 1:** Escriba el nombre completo del profesor
```
Nombre: [García López, Juan Carlos_______]
```

**Formato recomendado:**
- Apellido(s), Nombre(s)
- Ejemplo: "García López, Juan Carlos"
- Ejemplo: "Martínez, María Elena"
- Ejemplo: "Rodríguez Pérez, Carlos Alberto"

**Paso 2:** Haga clic en **[Agregar]**

**Resultado:**
```
┌────────────────────────────────────────────────┐
│ Nombre                                         │
├────────────────────────────────────────────────┤
│ García López, Juan Carlos                      │
└────────────────────────────────────────────────┘
```

**Paso 3:** Repita para crear todos los profesores

### 10.4 Gestionar la banca de horas

La **banca de horas** es la lista de materias que puede dictar cada profesor, junto con la cantidad de horas asignadas.

**Importante:** 
- Las horas iniciales son **0**
- Se incrementan automáticamente al asignar horarios
- NO se editan manualmente

#### 10.4.1 Asignar materias a un profesor

**Paso 1:** Seleccione el profesor de la lista

**Paso 2:** Haga clic en **[Banca de horas]**

Se abre una ventana:

```
┌──────────────────────────────────────────────────────┐
│  Obligaciones del agente García López, Juan Carlos   │
├──────────────────────────────────────────────────────┤
│  Obligaciones asignadas y horas ocupadas             │
│  ┌────────────────────────────────────────────────┐  │
│  │ Obligación    │ Horas asignadas              │  │
│  ├────────────────────────────────────────────────┤  │
│  │ (vacío inicialmente)                          │  │
│  └────────────────────────────────────────────────┘  │
├──────────────────────────────────────────────────────┤
│  Obligación: [Seleccione una materia ▼]             │
├──────────────────────────────────────────────────────┤
│  [Agregar obligación]  [Eliminar seleccionada]       │
└──────────────────────────────────────────────────────┘
```

**Paso 3:** Seleccione una materia de la lista desplegable
```
Ejemplo: Matemática
```

**Paso 4:** Haga clic en **[Agregar obligación]**

**Resultado:**
```
┌────────────────────────────────────────────────┐
│ Obligación    │ Horas asignadas              │
├────────────────────────────────────────────────┤
│ Matemática    │ 0                            │ ← Comienza en 0
└────────────────────────────────────────────────┘
```

**Paso 5:** Repita para todas las materias que puede dictar el profesor

**Ejemplo completo:**
```
┌────────────────────────────────────────────────┐
│ Obligación    │ Horas asignadas              │
├────────────────────────────────────────────────┤
│ Física        │ 0                            │
│ Matemática    │ 0                            │
│ Química       │ 0                            │
└────────────────────────────────────────────────┘
```

**Paso 6:** Cierre la ventana cuando termine

#### 10.4.2 Interpretar las "Horas asignadas"

Las horas se actualizan automáticamente:

**Estado inicial (sin horarios):**
```
Matemática    │ 0
```

**Después de asignar 5 horarios de Matemática:**
```
Matemática    │ 5
```

**Después de asignar más horarios en otra división:**
```
Matemática    │ 12
```

**Significado:** El profesor tiene 12 módulos/horas de Matemática asignados por semana en total.

#### 10.4.3 Quitar materias de la banca

**Paso 1:** En la ventana "Obligaciones del agente", seleccione una materia

**Paso 2:** Haga clic en **[Eliminar seleccionada]**

**Advertencia:** Si hay horarios asignados con esa materia, se eliminarán también.

### 10.5 Asignar turnos a un profesor

Cada profesor trabaja en uno o más turnos. Debe asignarlos explícitamente.

**Paso 1:** Seleccione el profesor de la lista

**Paso 2:** Haga clic en **[Turnos del agente]**

Se abre una ventana:

```
┌──────────────────────────────────────────────────────┐
│  Turnos del agente García López, Juan Carlos         │
├──────────────────────────────────────────────────────┤
│  Turnos asignados:                                   │
│  ┌────────────────────────────────────────────────┐  │
│  │ Nombre                                         │  │
│  ├────────────────────────────────────────────────┤  │
│  │ (vacío inicialmente)                          │  │
│  └────────────────────────────────────────────────┘  │
├──────────────────────────────────────────────────────┤
│  Turno: [Seleccione un turno ▼]                     │
├──────────────────────────────────────────────────────┤
│  [Agregar turno]  [Quitar seleccionado]              │
└──────────────────────────────────────────────────────┘
```

**Paso 3:** Seleccione un turno (Mañana, Tarde, Noche)

**Paso 4:** Haga clic en **[Agregar turno]**

**Resultado:**
```
┌────────────────────────────────────────────────┐
│ Nombre                                         │
├────────────────────────────────────────────────┤
│ Mañana                                         │
└────────────────────────────────────────────────┘
```

**Paso 5:** Repita si el profesor trabaja en múltiples turnos

**Ejemplo: Profesor en dos turnos:**
```
┌────────────────────────────────────────────────┐
│ Nombre                                         │
├────────────────────────────────────────────────┤
│ Mañana                                         │
│ Tarde                                          │
└────────────────────────────────────────────────┘
```

### 10.6 Editar un profesor

Solo puede editar el **nombre** del profesor.

**Paso 1:** Seleccione el profesor de la lista

**Paso 2:** El nombre aparece en el campo
```
Nombre: [García López, Juan Carlos_______]
```

**Paso 3:** Modifique el nombre

**Paso 4:** Haga clic en **[Editar]**

### 10.7 Eliminar un profesor

⚠️ **ADVERTENCIA CRÍTICA:** Eliminar un profesor eliminará:
- Toda su banca de horas
- Todos sus turnos asignados
- Todos los horarios donde está asignado

**Solo elimine profesores si está completamente seguro.**

**Paso 1:** Seleccione el profesor

**Paso 2:** Haga clic en **[Eliminar]**

**Paso 3:** Confirme la eliminación

### 10.8 Filtros disponibles

#### 10.8.1 Filtro por nombre

Use el campo "Filtro" para buscar profesores:

```
Filtro: [garcía___________]
```

La lista se filtra mientras escribe:
```
┌────────────────────────────────────────────────┐
│ Nombre                                         │
├────────────────────────────────────────────────┤
│ García López, Juan Carlos                      │ ← Solo coincidencias
│ García Martínez, Ana María                     │
└────────────────────────────────────────────────┘
```

#### 10.8.2 Filtro por turno

Use la lista desplegable "Turno" para ver solo profesores de un turno:

```
Turno: [Mañana ▼]
```

La lista muestra solo profesores asignados a ese turno.

**"Todos":** Muestra todos los profesores (sin filtrar)

### 10.9 Contador de agentes

En la parte superior verá:
```
Total de agentes: 25
```

Este número cambia según los filtros aplicados.

**Ejemplos:**
- Sin filtros: Muestra el total de profesores
- Con filtro por turno "Mañana": Muestra solo los del turno mañana
- Con filtro por nombre "garcía": Muestra solo coincidencias

### 10.10 Flujo completo: Configurar un profesor

**Ejemplo: Configurar al profesor "Pérez Martínez, María Elena"**

**Paso 1:** Crear el profesor
```
Nombre: [Pérez Martínez, María Elena___]
[Agregar]
```

**Paso 2:** Asignar materias a su banca
```
Seleccionar profesor → [Banca de horas]
Agregar: Física
Agregar: Química
```

**Paso 3:** Asignar turnos
```
Seleccionar profesor → [Turnos del agente]
Agregar: Mañana
```

**Resultado final:**
- Profesor creado: "Pérez Martínez, María Elena"
- Puede dictar: Física, Química
- Trabaja en: Turno Mañana
- Horas asignadas: 0 (se incrementarán al asignar horarios)

### 10.11 Consejos para gestión de personal

✅ **Buenas prácticas:**
- Use formato consistente de nombres: "Apellido(s), Nombre(s)"
- Configure la banca completa antes de asignar horarios
- Asigne todos los turnos correspondientes
- Verifique que las materias coincidan con los planes
- Use el filtro con listas grandes

⚠️ **Errores comunes:**
- ❌ Olvidar asignar materias a la banca antes de crear horarios
- ❌ No asignar el turno correspondiente
- ❌ Crear nombres inconsistentes: "García, Juan" vs "Juan García"
- ❌ Intentar editar las horas manualmente (son automáticas)
- ❌ Eliminar profesores con horarios asignados sin verificar

### 10.12 Caso de uso: Profesor suplente temporal

**Escenario:** Necesita agregar un profesor suplente que cubrirá temporalmente a otro.

**Paso 1:** Cree el profesor suplente

**Paso 2:** Asigne las mismas materias que el profesor titular

**Paso 3:** Asigne el turno correspondiente

**Paso 4:** Al asignar horarios, podrá elegir entre el titular y el suplente

**Paso 5:** Cuando termine el reemplazo, puede:
- Opción A: Eliminar el suplente (se eliminan sus horarios)
- Opción B: Dejar el suplente pero reasignar horarios al titular

---

## 11. GESTIÓN DE CURSOS/DIVISIONES

### 11.1 ¿Qué son las divisiones?

Las **divisiones** (también llamadas cursos) son los grupos de alumnos que tienen un horario común. Cada división es única y se identifica por:
- **Turno:** Mañana, Tarde, Noche
- **Plan de estudios:** Bachiller, Perito, etc.
- **Año/Curso:** 1° Año, 2° Año, etc.
- **Nombre de división:** A, B, C, etc.

**Ejemplo completo:** "Turno Mañana - Bachiller - 1° Año - División A"

### 11.2 Acceder a la gestión de divisiones

1. En el menú principal, haga clic en **"Cursos"**
2. Seleccione **"Gestionar Cursos"**

```
┌──────────────────────────────────────────────────────┐
│  Gestión de Cursos                                   │
├──────────────────────────────────────────────────────┤
│  Total de divisiones: 0                              │
├──────────────────────────────────────────────────────┤
│  Turno: [Todos ▼]  Plan: [Todos ▼]                  │
│  Curso: [Todos ▼]                                    │
├──────────────────────────────────────────────────────┤
│  ┌────────────────────────────────────────────────┐  │
│  │ Turno │Plan  │Curso │División                 │  │
│  ├────────────────────────────────────────────────┤  │
│  │ (vacío)                                        │  │
│  └────────────────────────────────────────────────┘  │
├──────────────────────────────────────────────────────┤
│  [Agregar]  [Editar]  [Eliminar]                     │
└──────────────────────────────────────────────────────┘
```

### 11.3 Crear una división

**Ejemplo: Crear "1° Año A - Turno Mañana - Bachiller"**

**Paso 1:** Haga clic en el botón **[Agregar]**

Se abre una ventana emergente:

```
┌──────────────────────────────────────────┐
│  Nueva División                          │
├──────────────────────────────────────────┤
│  Turno:      [Seleccione ▼]             │
│                                          │
│  Plan:       [Seleccione ▼]             │
│                                          │
│  Curso:      [Seleccione ▼]             │
│                                          │
│  División:   [___________]              │
├──────────────────────────────────────────┤
│  [Guardar]  [Cancelar]                  │
└──────────────────────────────────────────┘
```

**Paso 2:** Seleccione el **Turno**
```
Turno: [Mañana ▼]
```

**Resultado:** La lista de planes se actualiza mostrando solo los planes asignados a ese turno.

**Paso 3:** Seleccione el **Plan de estudios**
```
Plan: [Bachiller en Ciencias Naturales ▼]
```

**Resultado:** La lista de cursos se actualiza mostrando solo los años de ese plan.

**Paso 4:** Seleccione el **Curso/Año**
```
Curso: [1° Año ▼]
```

**Paso 5:** Escriba el **nombre de la división**
```
División: [A___________]
```

**Formato típico:** A, B, C, D, etc.

**Paso 6:** Haga clic en **[Guardar]**

**Resultado:** La división aparece en la lista principal:
```
┌────────────────────────────────────────────────┐
│ Turno │Plan      │Curso  │División          │
├────────────────────────────────────────────────┤
│Mañana │Bachiller │1° Año │A                 │
└────────────────────────────────────────────────┘
```

### 11.4 Navegación en cascada de los filtros

Los filtros están relacionados: cada selección filtra las opciones del siguiente.

**Secuencia:**
```
1. TURNO
   ↓ (filtra)
2. PLAN (solo planes de ese turno)
   ↓ (filtra)
3. CURSO (solo años de ese plan)
```

**Ejemplo práctico:**

**Estado inicial:**
```
Turno: [Todos ▼]
Plan:  [Todos ▼]
Curso: [Todos ▼]
```
Muestra todas las divisiones.

**Selecciono Turno Mañana:**
```
Turno: [Mañana ▼]
Plan:  [Todos ▼]  ← Solo planes del turno Mañana
Curso: [Todos ▼]
```
Muestra solo divisiones del turno Mañana.

**Selecciono Plan Bachiller:**
```
Turno: [Mañana ▼]
Plan:  [Bachiller ▼]
Curso: [Todos ▼]  ← Solo años del plan Bachiller
```
Muestra solo divisiones de Mañana-Bachiller.

**Selecciono Curso 1° Año:**
```
Turno: [Mañana ▼]
Plan:  [Bachiller ▼]
Curso: [1° Año ▼]
```
Muestra solo 1° Año de Mañana-Bachiller (todas las divisiones A, B, C...).

### 11.5 Autocompletado inteligente

Si en algún nivel solo hay **una opción**, el sistema la selecciona automáticamente.

**Ejemplo:**

**Situación:** El turno Mañana solo tiene un plan: Bachiller

**Comportamiento:**
```
1. Selecciona Turno: Mañana
2. Plan se completa automáticamente: Bachiller
3. Solo debe seleccionar el Curso
```

**Ventaja:** Acelera la creación cuando hay pocas opciones.

### 11.6 Editar una división

Solo puede editar el **nombre** de la división (A, B, C, etc.). No puede cambiar turno, plan o curso.

**Para cambiar turno/plan/curso:** Debe eliminar y crear nuevamente.

**Paso 1:** Seleccione la división de la lista

**Paso 2:** Haga clic en **[Editar]**

Se abre una ventana:

```
┌──────────────────────────────────────────┐
│  Editar División                         │
├──────────────────────────────────────────┤
│  Turno:      Mañana (no editable)        │
│  Plan:       Bachiller (no editable)     │
│  Curso:      1° Año (no editable)        │
│                                          │
│  División:   [A___________]              │
├──────────────────────────────────────────┤
│  [Guardar]  [Cancelar]                  │
└──────────────────────────────────────────┘
```

**Paso 3:** Modifique el nombre de la división

**Paso 4:** Haga clic en **[Guardar]**

### 11.7 Eliminar una división

⚠️ **ADVERTENCIA CRÍTICA:** Eliminar una división eliminará:
- Todos los horarios de esa división
- Todos los contadores de horas se actualizarán (decrementan)

**Solo elimine divisiones si está completamente seguro.**

**Paso 1:** Seleccione la división

**Paso 2:** Haga clic en **[Eliminar]**

**Paso 3:** Confirme la eliminación

### 11.8 Contador de divisiones

En la parte superior verá:
```
Total de divisiones: 12
```

Este número cambia según los filtros aplicados.

**Ejemplos:**
- Sin filtros: Total de divisiones de la institución
- Con filtro "Turno Mañana": Solo divisiones del turno mañana
- Con filtro "Turno Mañana + Plan Bachiller + 1° Año": Solo divisiones de ese conjunto específico

### 11.9 Verificar configuración antes de crear divisiones

Antes de crear una división, verifique que existen:

✅ **Pre-requisitos obligatorios:**
- [ ] El turno está creado
- [ ] El plan de estudios está creado
- [ ] El plan está asignado al turno
- [ ] Los años del plan están creados
- [ ] Las materias están asignadas a cada año

**Si falta algo:** Los filtros no mostrarán opciones o estarán vacíos.

### 11.10 Ejemplo completo: Crear estructura de divisiones

**Escenario:** Crear divisiones para 1° Año de Bachiller en turno Mañana (2 divisiones: A y B)

**Paso 1:** Crear división A
```
[Agregar]
Turno: Mañana
Plan: Bachiller
Curso: 1° Año
División: A
[Guardar]
```

**Paso 2:** Crear división B
```
[Agregar]
Turno: Mañana
Plan: Bachiller
Curso: 1° Año
División: B
[Guardar]
```

**Resultado:**
```
┌────────────────────────────────────────────────┐
│ Turno │Plan      │Curso  │División          │
├────────────────────────────────────────────────┤
│Mañana │Bachiller │1° Año │A                 │
│Mañana │Bachiller │1° Año │B                 │
└────────────────────────────────────────────────┘
```

**Paso 3:** Repetir para otros años o turnos

### 11.11 Consejos para gestión de divisiones

✅ **Buenas prácticas:**
- Cree todas las divisiones de un año antes de pasar al siguiente
- Use nomenclatura consistente: A, B, C (o 1, 2, 3)
- Verifique los pre-requisitos antes de crear
- Use los filtros para navegar con muchas divisiones
- Documente externamente la estructura (Excel, Word)

⚠️ **Errores comunes:**
- ❌ Intentar crear divisiones antes de configurar planes/turnos
- ❌ Olvidar asignar el plan al turno
- ❌ No crear los años del plan
- ❌ Nomenclatura inconsistente: "A", "a", "División A"
- ❌ Eliminar divisiones con horarios sin hacer backup

### 11.12 Validaciones del sistema

El sistema valida que:

✅ **No puede haber dos divisiones con el mismo nombre** en el mismo Turno+Plan+Año

**Ejemplo permitido:**
```
Turno Mañana - Bachiller - 1° Año - A
Turno Tarde  - Bachiller - 1° Año - A  ← Permitido (diferente turno)
```

**Ejemplo NO permitido:**
```
Turno Mañana - Bachiller - 1° Año - A
Turno Mañana - Bachiller - 1° Año - A  ← ERROR: duplicado
```

❌ **Error mostrado:** "UNIQUE constraint failed"

### 11.13 Caso de uso: Reorganizar divisiones

**Escenario:** Necesita cambiar la división "A" de turno Mañana a turno Tarde.

**Problema:** No se puede editar el turno de una división existente.

**Solución:**

**Opción 1: Recrear la división**
1. **Exportar/anotar** los horarios actuales (tomar captura de pantalla)
2. **Eliminar** la división del turno Mañana
3. **Crear** nueva división en turno Tarde
4. **Reasignar** los horarios manualmente

**Opción 2: Si NO tiene horarios asignados aún**
1. Simplemente **eliminar** y **crear** nuevamente en el turno correcto

**Recomendación:** Planifique bien la estructura antes de crear divisiones para evitar reorganizaciones posteriores.

---

# PARTE 4: GESTIÓN DE HORARIOS

## 12. CONFIGURACIÓN DE HORAS POR TURNO

### 12.1 ¿Qué es la configuración de horas?

La **configuración de horas por turno** permite definir las horas de inicio y fin de cada espacio horario (módulo) para un turno específico. Esto establece los horarios "por defecto" que se aplicarán automáticamente.

**Ejemplo:**
```
Turno Mañana:
1ª hora: 08:00 - 08:45
2ª hora: 08:45 - 09:30
3ª hora: 09:30 - 10:15
... etc.
```

### 12.2 ¿Por qué configurar las horas?

**Ventajas:**
- ✅ Evita escribir las mismas horas repetidamente
- ✅ Garantiza consistencia en todos los horarios
- ✅ Facilita cambios masivos (si cambia el horario institucional)
- ✅ Acelera la carga de horarios

**Sin configuración:**
```
Debe escribir manualmente:
- Lunes 1ª: 08:00 - 08:45
- Lunes 2ª: 08:45 - 09:30
- Martes 1ª: 08:00 - 08:45
... (repetir 40 veces por división)
```

**Con configuración:**
```
Las horas se completan automáticamente.
Solo debe seleccionar materia y profesor.
```

### 12.3 Acceder a la configuración

**Desde vista "Por curso":**
1. Menú **"Gestión de horarios"** → **"Por curso"**
2. Botón **[Configurar horas por turno]**

**Desde vista "Por profesor":**
1. Menú **"Gestión de horarios"** → **"Por profesor"**
2. Botón **[Configurar horas por turno]**

**Resultado:** Se abre una ventana emergente:

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

### 12.4 Configurar horas paso a paso

**Ejemplo: Configurar turno Mañana**

**Paso 1:** Seleccione el turno
```
Turno: [Mañana ▼]
```

**Paso 2:** Complete las horas de cada espacio

**Formato de entrada:**
- Puede escribir: `0800` y se convierte en `08:00`
- O escribir directamente: `08:00`
- Los dos puntos (`:`) se insertan automáticamente

**Ejemplo de configuración completa:**
```
1ª:  [08:00] Hs  a  [08:45] Hs
2ª:  [08:45] Hs  a  [09:30] Hs
3ª:  [09:30] Hs  a  [10:15] Hs
4ª:  [10:15] Hs  a  [11:00] Hs  ← Recreo
5ª:  [11:15] Hs  a  [12:00] Hs
6ª:  [12:00] Hs  a  [12:45] Hs
7ª:  [      ] Hs  a  [      ] Hs  ← Vacío (no se usa)
8ª:  [      ] Hs  a  [      ] Hs  ← Vacío (no se usa)
```

**Notas:**
- ✅ Puede dejar espacios vacíos si no se usan
- ✅ El recreo NO es un espacio (4ª termina a 11:00, 5ª empieza a 11:15)
- ✅ Navegación automática: al completar un campo, pasa al siguiente

**Paso 3:** Elija las opciones de aplicación (ver siguiente sección)

**Paso 4:** Haga clic en **[Guardar]**

### 12.5 Opciones de aplicación

Hay dos checkboxes independientes:

#### 12.5.1 "Aplicar a horario actual"

**Qué hace:**
- Actualiza las horas de la división o profesor que está viendo actualmente

**Cuándo usarlo:**
- Cuando quiere actualizar solo UNA división específica
- Cuando está configurando inicialmente un profesor específico

**Ejemplo desde vista "Por curso":**
```
Está viendo: 1° Año A - Turno Mañana
☑ Aplicar a horario actual
→ Solo actualiza los horarios de 1° Año A
```

**Ejemplo desde vista "Por profesor":**
```
Está viendo: Profesor García - Turno Mañana
☑ Aplicar a horario actual
→ Solo actualiza los horarios del profesor García en turno Mañana
```

#### 12.5.2 "Aplicar a todos los horarios del turno"

**Qué hace:**
- Actualiza las horas de TODAS las divisiones del turno (vista por curso)
- Actualiza las horas de TODOS los profesores del turno (vista por profesor)

**Cuándo usarlo:**
- Configuración inicial del turno
- Cuando cambia el horario institucional de todo el turno

**Ejemplo desde vista "Por curso":**
```
Turno Mañana tiene: 1°A, 1°B, 2°A, 2°B, 3°A
☑ Aplicar a todos los horarios del turno
→ Actualiza horarios de TODAS las divisiones del turno Mañana
```

**Ejemplo desde vista "Por profesor":**
```
Turno Mañana tiene profesores: García, Pérez, López, Martínez
☑ Aplicar a todos los horarios del turno
→ Actualiza horarios de TODOS los profesores en turno Mañana
```

#### 12.5.3 Usar ambas opciones

**Puede marcar ambos checkboxes simultáneamente:**

```
☑ Aplicar a horario actual
☑ Aplicar a todos los horarios del turno
```

**Efecto:**
- Aplica ambas actualizaciones
- Útil cuando quiere asegurarse de que todo el turno tenga las mismas horas

#### 12.5.4 No marcar ninguna opción

**Si guarda sin marcar nada:**
- Las horas se guardan como configuración del turno
- NO se aplican a horarios existentes
- Solo afectarán a horarios NUEVOS que se creen después

**Cuándo hacerlo:**
- Configuración preventiva antes de crear horarios
- Solo quiere actualizar la configuración sin tocar datos existentes

### 12.6 Casos de uso comunes

#### Caso 1: Primera configuración (sin horarios aún)

**Situación:** Acaba de crear el turno, no hay horarios asignados.

**Pasos:**
1. Abrir configuración
2. Seleccionar turno
3. Completar todas las horas
4. NO marcar ningún checkbox (o marcar "todos" igualmente)
5. Guardar

**Resultado:** Los horarios que cree después usarán estas horas automáticamente.

---

#### Caso 2: Cambio del horario institucional

**Situación:** La institución cambió el horario de entrada de 8:00 a 8:15.

**Pasos:**
1. Abrir configuración
2. Seleccionar turno (Mañana)
3. Modificar todas las horas (+15 minutos)
```
Antes:
1ª: [08:00] a [08:45]
2ª: [08:45] a [09:30]

Después:
1ª: [08:15] a [09:00]
2ª: [09:00] a [09:45]
```
4. Marcar: ☑ **Aplicar a todos los horarios del turno**
5. Guardar

**Resultado:** TODOS los horarios del turno se actualizan automáticamente.

---

#### Caso 3: Ajustar horario de una división específica

**Situación:** Una división tiene un horario diferente (entra más tarde por ejemplo).

**Pasos:**
1. Ir a vista "Por curso"
2. Seleccionar esa división específica
3. Abrir configuración
4. Completar las horas específicas de esa división
5. Marcar: ☑ **Aplicar a horario actual** (solo esta división)
6. Guardar

**Resultado:** Solo esa división tiene horarios diferentes.

---

#### Caso 4: Corregir un error en la configuración

**Situación:** Se equivocó al configurar las horas, ya hay horarios asignados.

**Pasos:**
1. Abrir configuración
2. Corregir las horas
3. Marcar: ☑ **Aplicar a todos los horarios del turno**
4. Guardar

**Resultado:** Todos los horarios existentes se corrigen.

### 12.7 Comportamiento de carga automática

**Al abrir la ventana de configuración:**
- Si el turno YA tiene horas configuradas, los campos se completan automáticamente
- Si NO tiene configuración, los campos están vacíos

**Ejemplo:**
```
Primera vez (turno nuevo):
1ª:  [      ] Hs  a  [      ] Hs  ← Vacío

Segunda vez (ya configurado):
1ª:  [08:00] Hs  a  [08:45] Hs  ← Cargado automáticamente
```

### 12.8 Consejos para configuración de horas

✅ **Buenas prácticas:**
- Configure las horas ANTES de asignar horarios (ahorra tiempo)
- Use formato de 24 horas: 08:00, 13:00, 20:00
- Sea consistente con la duración de módulos
- Considere los recreos en la planificación
- Documente la configuración en un documento externo

⚠️ **Errores comunes:**
- ❌ Olvidar los recreos (espacios sin clase entre módulos)
- ❌ Superponer horarios: 08:00-09:00 y luego 08:45-09:30
- ❌ No aplicar cambios masivos cuando corresponde
- ❌ Configurar horas después de asignar todos los horarios manualmente

### 12.9 Preguntas frecuentes

**P: ¿Puedo tener diferentes horas para cada división del mismo turno?**
R: Sí, use "Aplicar a horario actual" para cada división específica.

**P: ¿Qué pasa si dejo espacios vacíos?**
R: Esos espacios no tendrán horas por defecto. Deberá ingresarlas manualmente al crear horarios.

**P: ¿Puedo cambiar las horas después de asignar horarios?**
R: Sí, use "Aplicar a todos los horarios del turno" para actualizar en masa.

**P: ¿Las horas afectan a otros turnos?**
R: No, cada turno tiene su propia configuración independiente.

**P: ¿Debo configurar los 8 espacios?**
R: No, solo configure los que realmente usa. Deje el resto vacío.

---

## 13. HORARIOS POR CURSO

### 13.1 ¿Qué es la vista "Por curso"?

La vista **"Horarios por Curso"** muestra el horario semanal completo de una división/curso específica. Es la vista más utilizada para:
- Planificar el horario de cada división
- Ver qué materias tiene cada curso cada día
- Verificar la distribución de materias en la semana

**Ejemplo visual:**
```
División 1° Año A - Turno Mañana
        Lunes    Martes   Miércoles Jueves   Viernes
1ª hora Matemát. Física   Matemát.  Lengua   Historia
        García   Pérez    García    López    Martínez
        08:00-   08:00-   08:00-    08:00-   08:00-
        08:45    08:45    08:45     08:45    08:45
```

### 13.2 Acceder a los horarios por curso

1. En el menú principal, haga clic en **"Gestión de horarios"**
2. Seleccione **"Por curso"**

```
┌──────────────────────────────────────────────────────┐
│  Gestión de Horarios por Curso                       │
├──────────────────────────────────────────────────────┤
│  Turno: [Todos ▼]  Plan: [Todos ▼]                  │
│  Curso: [Todos ▼]  División: [Todos ▼]              │
├──────────────────────────────────────────────────────┤
│                                                      │
│  (Seleccione una división para ver su horario)      │
│                                                      │
├──────────────────────────────────────────────────────┤
│  [Configurar horas por turno]                        │
│  [Limpiar horarios vacíos]                           │
└──────────────────────────────────────────────────────┘
```

### 13.3 Seleccionar una división

Los filtros funcionan en cascada (cada selección filtra el siguiente):

**Paso 1:** Seleccione el **Turno**
```
Turno: [Mañana ▼]
```
→ La lista de planes se actualiza (solo planes de ese turno)

**Paso 2:** Seleccione el **Plan**
```
Plan: [Bachiller en Ciencias Naturales ▼]
```
→ La lista de cursos se actualiza (solo años de ese plan)

**Paso 3:** Seleccione el **Curso/Año**
```
Curso: [1° Año ▼]
```
→ La lista de divisiones se actualiza (solo divisiones de ese turno+plan+año)

**Paso 4:** Seleccione la **División**
```
División: [A ▼]
```

**Resultado:** Se muestra la grilla de horarios de esa división.

### 13.4 La grilla de horarios

Una vez seleccionada la división, aparece la grilla:

```
┌───┬─────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│   │   Lunes     │   Martes    │  Miércoles  │   Jueves    │   Viernes   │
├───┼─────────────┼─────────────┼─────────────┼─────────────┼─────────────┤
│1ª │             │             │             │             │             │
│   │             │             │             │             │             │
│   │             │             │             │             │             │
├───┼─────────────┼─────────────┼─────────────┼─────────────┼─────────────┤
│2ª │             │             │             │             │             │
│   │             │             │             │             │             │
│   │             │             │             │             │             │
├───┼─────────────┼─────────────┼─────────────┼─────────────┼─────────────┤
│...│             │             │             │             │             │
└───┴─────────────┴─────────────┴─────────────┴─────────────┴─────────────┘
```

**Estructura:**
- **Filas:** Espacios horarios (1ª a 8ª)
- **Columnas:** Días de la semana (Lunes a Viernes)
- **Celdas:** Cada celda puede contener:
  - Materia
  - Profesor
  - Hora inicio - Hora fin

### 13.5 Asignar un horario

**Ejemplo: Asignar Matemática con el profesor García el Lunes a 1ª hora**

**Paso 1:** Haga clic en la celda correspondiente
```
Click en: Lunes - 1ª hora
```

**Resultado:** Se abre una ventana emergente:

```
┌──────────────────────────────────────────┐
│  Lunes - 1ª hora                         │
├──────────────────────────────────────────┤
│  Hora inicio:  [08:00]  Hs               │
│  Hora fin:     [08:45]  Hs               │
│                                          │
│  Obligación:   [Seleccione ▼]            │
│                                          │
│  Profesor:     [Seleccione ▼]            │
├──────────────────────────────────────────┤
│  [Guardar]  [Eliminar]                   │
└──────────────────────────────────────────┘
```

**Nota:** Si configuró las horas por turno, los campos "Hora inicio" y "Hora fin" ya están completados.

**Paso 2:** Verifique/ajuste las horas si es necesario
```
Hora inicio:  [08:00]  Hs
Hora fin:     [08:45]  Hs
```

**Paso 3:** Seleccione la materia
```
Obligación:   [Matemática ▼]
```

**Paso 4:** Seleccione el profesor
```
Profesor:     [García López, Juan Carlos ▼]
```

**Filtrado inteligente:** La lista de profesores solo muestra aquellos que:
- ✅ Tienen la materia en su banca de horas
- ✅ Están asignados al turno de esta división

**Paso 5:** Haga clic en **[Guardar]**

**Resultado:** La celda se actualiza mostrando la información:

```
┌───┬─────────────┬─────────────┬─────────────┐
│   │   Lunes     │   Martes    │  Miércoles  │
├───┼─────────────┼─────────────┼─────────────┤
│1ª │ Matemática  │             │             │
│   │ García      │             │             │
│   │ 08:00-08:45 │             │             │
└───┴─────────────┴─────────────┴─────────────┘
```

### 13.6 Modificar un horario existente

**Paso 1:** Haga clic en la celda que quiere modificar

**Paso 2:** La ventana se abre mostrando los datos actuales:
```
┌──────────────────────────────────────────┐
│  Lunes - 1ª hora                         │
├──────────────────────────────────────────┤
│  Hora inicio:  [08:00]  Hs               │
│  Hora fin:     [08:45]  Hs               │
│                                          │
│  Obligación:   [Matemática ▼]            │ ← Ya seleccionado
│                                          │
│  Profesor:     [García López... ▼]       │ ← Ya seleccionado
├──────────────────────────────────────────┤
│  [Guardar]  [Eliminar]                   │
└──────────────────────────────────────────┘
```

**Paso 3:** Modifique lo que necesite (horas, materia o profesor)

**Paso 4:** Haga clic en **[Guardar]**

**Efecto:** 
- Se elimina el horario anterior (contadores se decrementan)
- Se crea el nuevo horario (contadores se incrementan)

### 13.7 Eliminar un horario

**Opción A: Desde la ventana de edición**

**Paso 1:** Haga clic en la celda con el horario

**Paso 2:** En la ventana que se abre, haga clic en **[Eliminar]**

**Paso 3:** Confirme la eliminación

**Resultado:** La celda queda vacía

---

**Opción B: Limpieza masiva de horarios vacíos**

Use el botón **[Limpiar horarios vacíos]** para eliminar todos los horarios que NO tienen materia NI profesor asignados.

**Cuándo usar:** Cuando tiene muchas celdas "basura" sin información útil.

### 13.8 Validaciones al asignar horarios

El sistema valida varios aspectos al guardar:

#### 13.8.1 Profesor ya ocupado

**Validación:** Un profesor no puede estar en dos lugares al mismo tiempo.

**Ejemplo de error:**
```
Intenta asignar:
- División 1°A, Lunes 1ª: García
- División 1°B, Lunes 1ª: García (MISMO turno)

❌ Error: "El profesor ya está asignado en ese 
horario en otra división del mismo turno."
```

**Solución:**
- Cambiar el horario a otro espacio
- O seleccionar otro profesor

#### 13.8.2 Profesor sin la materia

**Validación:** El profesor debe tener la materia en su banca.

**Ejemplo de error:**
```
García tiene en su banca: Matemática, Física
Intenta asignar: Química

❌ Error: "El profesor no tiene asignada la 
materia seleccionada."
```

**Solución:**
- Ir a "Gestionar personal"
- Agregar la materia a la banca del profesor
- Volver a asignar el horario

#### 13.8.3 Profesor sin turno asignado

**Validación:** El profesor debe estar asignado al turno.

**Ejemplo de error:**
```
García trabaja en: Turno Mañana
División es de: Turno Tarde

❌ Error: "El profesor no está asignado a este turno."
```

**Solución:**
- Ir a "Gestionar personal"
- Asignar el turno correspondiente al profesor
- Volver a asignar el horario

#### 13.8.4 Materia sin profesor (permitido)

**Validación:** Puede asignar solo la materia, sin profesor.

**Uso típico:** Cuando sabe qué materia va en ese horario pero aún no definió el profesor.

```
Obligación:   [Matemática ▼]
Profesor:     [              ]  ← Vacío (permitido)
```

### 13.9 Contadores automáticos en acción

**Cada vez que asigna un horario:**

✅ **Se incrementa la "Horas semanales" de la materia** (+1)
✅ **Se incrementa la "Banca de horas" del profesor** en esa materia (+1)

**Cada vez que elimina un horario:**

➖ **Se decrementa la "Horas semanales" de la materia** (-1)
➖ **Se decrementa la "Banca de horas" del profesor** en esa materia (-1)

**Ejemplo práctico:**

**Estado inicial:**
```
Materia Matemática: 0 horas semanales
Profesor García (Matemática): 0 horas asignadas
```

**Asignar 5 horarios de Matemática con García en 1°A:**
```
Materia Matemática: 5 horas semanales
Profesor García (Matemática): 5 horas asignadas
```

**Asignar 5 horarios más de Matemática con García en 1°B:**
```
Materia Matemática: 10 horas semanales (5+5)
Profesor García (Matemática): 10 horas asignadas
```

**Eliminar 2 horarios:**
```
Materia Matemática: 8 horas semanales
Profesor García (Matemática): 8 horas asignadas
```

### 13.10 Estrategias para asignar horarios

#### Estrategia 1: Por materia

**Objetivo:** Asignar todos los horarios de una materia en todas las divisiones.

**Pasos:**
1. Decida qué materia asignar (ej: Matemática)
2. Para cada división (1°A, 1°B, 2°A, etc.):
   - Asigne los espacios correspondientes de Matemática
3. Pase a la siguiente materia

**Ventaja:** Fácil control de la distribución de una materia.

---

#### Estrategia 2: Por división

**Objetivo:** Completar el horario completo de una división antes de pasar a la siguiente.

**Pasos:**
1. Seleccione una división (1°A)
2. Complete todo su horario semanal
3. Pase a la siguiente división (1°B)

**Ventaja:** Fácil visualización del horario completo del curso.

---

#### Estrategia 3: Por profesor

**Objetivo:** Asignar todos los horarios de un profesor en todas sus divisiones.

**Pasos:**
1. Decida qué profesor configurar (García)
2. Para cada división donde debe dar clase:
   - Asigne sus horarios
3. Pase al siguiente profesor

**Ventaja:** Control de la carga horaria del docente.

**Nota:** Para esta estrategia, es más práctico usar la vista "Por profesor" (ver siguiente sección).

### 13.11 Ejemplos de horarios completos

**Ejemplo 1: División con horario regular**

```
1° Año A - Bachiller - Turno Mañana
┌───┬──────────┬──────────┬──────────┬──────────┬──────────┐
│   │  Lunes   │  Martes  │Miércoles │  Jueves  │ Viernes  │
├───┼──────────┼──────────┼──────────┼──────────┼──────────┤
│1ª │Matemática│ Física   │Matemática│ Lengua   │ Historia │
│   │ García   │ Pérez    │ García   │ López    │Martínez  │
│   │08:00-    │08:00-    │08:00-    │08:00-    │08:00-    │
│   │08:45     │08:45     │08:45     │08:45     │08:45     │
├───┼──────────┼──────────┼──────────┼──────────┼──────────┤
│2ª │Matemática│ Física   │ Química  │ Lengua   │ Historia │
│   │ García   │ Pérez    │ López    │ López    │Martínez  │
│   │08:45-    │08:45-    │08:45-    │08:45-    │08:45-    │
│   │09:30     │09:30     │09:30     │09:30     │09:30     │
├───┼──────────┼──────────┼──────────┼──────────┼──────────┤
│3ª │ Lengua   │Matemática│ Física   │Matemática│ Química  │
│   │ López    │ García   │ Pérez    │ García   │ López    │
│   │09:30-    │09:30-    │09:30-    │09:30-    │09:30-    │
│   │10:15     │10:15     │10:15     │10:15     │10:15     │
├───┼──────────┼──────────┼──────────┼──────────┼──────────┤
│4ª │ Biología │ Biología │ Historia │ Física   │Matemática│
│   │Fernández │Fernández │Martínez  │ Pérez    │ García   │
│   │10:15-    │10:15-    │10:15-    │10:15-    │10:15-    │
│   │11:00     │11:00     │11:00     │11:00     │11:00     │
├───┼──────────┼──────────┼──────────┼──────────┼──────────┤
│5ª │ Ed.Física│ Química  │ Biología │ Ed.Física│ Lengua   │
│   │ Torres   │ López    │Fernández │ Torres   │ López    │
│   │11:15-    │11:15-    │11:15-    │11:15-    │11:15-    │
│   │12:00     │12:00     │12:00     │12:00     │12:00     │
├───┼──────────┼──────────┼──────────┼──────────┼──────────┤
│6ª │          │          │          │          │          │
│   │          │          │          │          │          │
└───┴──────────┴──────────┴──────────┴──────────┴──────────┘
```

**Análisis:**
- Total: 25 horas semanales
- 6 espacios usados (1ª a 5ª)
- Materias: Matemática (5), Física (3), Lengua (3), Química (2), Historia (2), Biología (3), Ed.Física (2)
- Todos los espacios tienen profesor asignado

### 13.12 Consejos para horarios por curso

✅ **Buenas prácticas:**
- Configure las horas por turno ANTES de asignar horarios
- Complete una división antes de pasar a la siguiente
- Verifique que todos los profesores estén configurados correctamente
- Revise las validaciones para evitar errores
- Considere la distribución equilibrada de materias en la semana
- Evite asignar materias "pesadas" todas el mismo día

⚠️ **Errores comunes:**
- ❌ No configurar la banca de horas de los profesores antes
- ❌ Olvidar asignar turnos a los profesores
- ❌ Intentar asignar profesores en horarios donde ya están ocupados
- ❌ No verificar los contadores automáticos
- ❌ Eliminar horarios sin considerar el impacto en contadores

### 13.13 Preguntas frecuentes

**P: ¿Puedo dejar espacios sin horario?**
R: Sí, simplemente no asigne nada en esa celda.

**P: ¿Puedo asignar solo la materia sin profesor?**
R: Sí, útil cuando aún no definió el docente.

**P: ¿Puedo cambiar un profesor por otro en un horario ya asignado?**
R: Sí, edite el horario y cambie el profesor. Los contadores se ajustan automáticamente.

**P: ¿Qué pasa si elimino un horario por error?**
R: Los contadores se decrementan. Debe volver a asignarlo manualmente.

**P: ¿Los cambios aquí afectan la vista "Por profesor"?**
R: Sí, ambas vistas están sincronizadas automáticamente.

**P: ¿Puedo copiar horarios de una división a otra?**
R: No directamente. Debe asignar manualmente o usar configuración de horas para acelerar.

---

## 14. HORARIOS POR PROFESOR

### 14.1 ¿Qué es la vista "Por profesor"?

La vista **"Horarios por Profesor"** muestra todos los horarios asignados a un docente específico en un turno. Es útil para:
- Ver la carga horaria completa de un profesor
- Verificar qué divisiones tiene asignadas
- Planificar la distribución de materias del docente
- Detectar huecos o superposiciones en su horario

**Ejemplo visual:**
```
Profesor García - Turno Mañana
        Lunes    Martes   Miércoles Jueves   Viernes
1ª hora 1°A      1°B      1°A       2°A      1°C
        Matemát. Matemát. Matemát.  Matemát. Matemát.
        08:00-   08:00-   08:00-    08:00-   08:00-
        08:45    08:45    08:45     08:45    08:45
```

### 14.2 Acceder a los horarios por profesor

1. En el menú principal, haga clic en **"Gestión de horarios"**
2. Seleccione **"Por profesor"**

```
┌──────────────────────────────────────────────────────┐
│  Gestión de Horarios por Profesor                    │
├──────────────────────────────────────────────────────┤
│  Turno: [Todos ▼]                                    │
│                                                      │
│  Buscar agente: [___________________________]        │
│                 (Escriba para filtrar)               │
├──────────────────────────────────────────────────────┤
│                                                      │
│  (Seleccione un profesor para ver su horario)       │
│                                                      │
├──────────────────────────────────────────────────────┤
│  [Configurar horas por turno]                        │
│  [Limpiar horarios vacíos]                           │
└──────────────────────────────────────────────────────┘
```

### 14.3 Seleccionar un profesor

#### 14.3.1 Paso 1: Seleccionar el turno

```
Turno: [Mañana ▼]
```

**Efecto:** La lista de profesores se filtra para mostrar solo aquellos asignados a ese turno.

#### 14.3.2 Paso 2: Buscar el profesor

Hay dos formas de seleccionar un profesor:

**Forma A: Búsqueda por texto**

Escriba el nombre (o parte) en el campo "Buscar agente":

```
Buscar agente: [garcía___________________]
```

**Comportamiento:**
- La lista se filtra mientras escribe
- Muestra solo coincidencias
- No distingue mayúsculas/minúsculas

**Ejemplo:**
```
Buscar: "gar"
Muestra:
- García López, Juan Carlos
- García Martínez, Ana María
```

**Atajos de teclado:**
- **Enter:** Selecciona la primera coincidencia
- **Esc:** Limpia el campo de búsqueda
- **Backspace (campo vacío):** Limpia el campo

---

**Forma B: Selección directa**

Si la lista no es muy larga, puede hacer clic directamente en el nombre del profesor en el combobox.

#### 14.3.3 Tooltip de ayuda

Al pasar el mouse sobre el campo "Buscar agente", verá un tooltip:

```
Buscar agente:
• Escribe para filtrar
• Enter: selecciona primera coincidencia
• Esc / Backspace: limpiar campo
```

### 14.4 La grilla de horarios del profesor

Una vez seleccionado el profesor, aparece la grilla:

```
Profesor: García López, Juan Carlos - Turno Mañana
┌───┬─────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│   │   Lunes     │   Martes    │  Miércoles  │   Jueves    │   Viernes   │
├───┼─────────────┼─────────────┼─────────────┼─────────────┼─────────────┤
│1ª │             │             │             │             │             │
│   │             │             │             │             │             │
│   │             │             │             │             │             │
├───┼─────────────┼─────────────┼─────────────┼─────────────┼─────────────┤
│2ª │             │             │             │             │             │
│   │             │             │             │             │             │
│   │             │             │             │             │             │
├───┼─────────────┼─────────────┼─────────────┼─────────────┼─────────────┤
│...│             │             │             │             │             │
└───┴─────────────┴─────────────┴─────────────┴─────────────┴─────────────┘
```

**Estructura:**
- **Filas:** Espacios horarios (1ª a 8ª)
- **Columnas:** Días de la semana (Lunes a Viernes)
- **Celdas:** Cada celda puede contener:
  - División
  - Materia
  - Hora inicio - Hora fin

### 14.5 Asignar un horario

**Ejemplo: Asignar al profesor García en 1°A, Lunes 1ª hora, Matemática**

**Paso 1:** Haga clic en la celda correspondiente
```
Click en: Lunes - 1ª hora
```

**Resultado:** Se abre una ventana emergente:

```
┌──────────────────────────────────────────┐
│  Lunes - 1ª hora                         │
├──────────────────────────────────────────┤
│  Hora inicio:  [08:00]  Hs               │
│  Hora fin:     [08:45]  Hs               │
│                                          │
│  Obligación:   [Seleccione ▼]            │
│                                          │
│  Plan:         [Seleccione ▼]            │
│  Año:          [Seleccione ▼]            │
│  División:     [Seleccione ▼]            │
├──────────────────────────────────────────┤
│  [Guardar]  [Eliminar]                   │
└──────────────────────────────────────────┘
```

**Diferencia con vista "Por curso":** Aquí debe seleccionar la división (antes era automática).

**Paso 2:** Verifique/ajuste las horas
```
Hora inicio:  [08:00]  Hs
Hora fin:     [08:45]  Hs
```

**Paso 3:** Seleccione la materia
```
Obligación:   [Matemática ▼]
```

**Filtrado:** Solo muestra materias que el profesor tiene en su banca.

**Paso 4:** Seleccione el plan
```
Plan:         [Bachiller en Ciencias Naturales ▼]
```

**Filtrado:** Solo planes del turno seleccionado.

**Paso 5:** Seleccione el año
```
Año:          [1° Año ▼]
```

**Filtrado:** Solo años del plan seleccionado.

**Paso 6:** Seleccione la división
```
División:     [A ▼]
```

**Filtrado:** Solo divisiones del turno+plan+año.

**Paso 7:** Haga clic en **[Guardar]**

**Resultado:** La celda se actualiza:

```
┌───┬─────────────┬─────────────┬─────────────┐
│   │   Lunes     │   Martes    │  Miércoles  │
├───┼─────────────┼─────────────┼─────────────┤
│1ª │ 1°A         │             │             │
│   │ Matemática  │             │             │
│   │ 08:00-08:45 │             │             │
└───┴─────────────┴─────────────┴─────────────┘
```

### 14.6 Autocompletado en cascada

Similar a la creación de divisiones, los campos se filtran automáticamente:

```
Secuencia:
1. Selecciona MATERIA
   ↓
2. Solo muestra PLANES que tienen esa materia
   ↓
3. Solo muestra AÑOS de ese plan que tienen esa materia
   ↓
4. Solo muestra DIVISIONES del turno+plan+año
```

**Si en algún nivel solo hay una opción, se selecciona automáticamente.**

**Ejemplo:**
```
Selecciona: Matemática
Plan: Solo hay "Bachiller" → se completa automáticamente
Año: Hay "1°", "2°", "3°" → debe elegir manualmente
```

### 14.7 Modificar un horario existente

**Paso 1:** Haga clic en la celda que quiere modificar

**Paso 2:** La ventana se abre mostrando los datos actuales:
```
┌──────────────────────────────────────────┐
│  Lunes - 1ª hora                         │
├──────────────────────────────────────────┤
│  Hora inicio:  [08:00]  Hs               │
│  Hora fin:     [08:45]  Hs               │
│                                          │
│  Obligación:   [Matemática ▼]            │
│  Plan:         [Bachiller... ▼]          │
│  Año:          [1° Año ▼]                │
│  División:     [A ▼]                     │
├──────────────────────────────────────────┤
│  [Guardar]  [Eliminar]                   │
└──────────────────────────────────────────┘
```

**Paso 3:** Modifique lo necesario

**Paso 4:** Haga clic en **[Guardar]**

### 14.8 Eliminar un horario

**Opción A: Desde la ventana de edición**

Haga clic en **[Eliminar]** en la ventana de edición del horario.

**Opción B: Limpieza masiva**

Use **[Limpiar horarios vacíos]** para eliminar horarios sin materia ni división.

### 14.9 Validaciones al asignar horarios

#### 14.9.1 Materia no en la banca

**Validación:** Solo puede asignar materias que el profesor tiene en su banca.

**Ejemplo de error:**
```
Profesor García tiene: Matemática, Física
Intenta asignar: Química

❌ Error: "El profesor no tiene asignada la 
materia seleccionada."
```

**Solución:**
- Ir a "Gestionar personal" → Banca de horas
- Agregar Química a la banca de García
- Volver a asignar

#### 14.9.2 División de otro turno

**Validación:** La división debe pertenecer al turno que está viendo.

**Ejemplo de error:**
```
Viendo: Profesor García - Turno Mañana
Intenta asignar: División de Turno Tarde

❌ Error: "La división no pertenece al turno 
seleccionado."
```

**Solución:**
- Verifique que seleccionó la división correcta
- O cambie de turno en el filtro superior

#### 14.9.3 Horario ya ocupado por división

**Validación:** La división no puede tener dos profesores al mismo tiempo.

**Ejemplo de error:**
```
División 1°A, Lunes 1ª ya tiene: Profesor Pérez
Intenta asignar: Profesor García (mismo horario)

❌ Error: "Ya existe un horario para esa división 
en ese día y espacio."
```

**Solución:**
- Seleccione otro horario (día u hora diferente)
- O elimine el horario existente primero

#### 14.9.4 Profesor ya ocupado

**Validación:** El profesor no puede estar en dos lugares al mismo tiempo.

**Ejemplo de error:**
```
García ya tiene: 1°A, Lunes 1ª (Turno Mañana)
Intenta asignar: 1°B, Lunes 1ª (Turno Mañana)

❌ Error: "El profesor ya tiene un horario 
asignado en ese día y espacio."
```

**Solución:**
- Seleccione otro horario
- O elimine el horario conflictivo primero

### 14.10 Sincronización entre vistas

**Característica clave:** Los cambios en esta vista se reflejan INMEDIATAMENTE en la vista "Por curso" y viceversa.

**Ejemplo de sincronización:**

**Vista "Por profesor":**
```
Profesor García
Lunes 1ª: 1°A - Matemática
```

**Vista "Por curso" (1°A):**
```
1° Año A
Lunes 1ª: Matemática - García
```

**Si cambia en cualquier vista:**
- El cambio se guarda en la misma tabla de BD
- Al actualizar la otra vista, verá el cambio reflejado

**No hay duplicación de datos:** Ambas vistas consultan la misma tabla `horario`.

### 14.11 Casos de uso prácticos

#### Caso 1: Verificar carga horaria del profesor

**Objetivo:** Ver cuántas horas tiene asignadas un profesor.

**Pasos:**
1. Vista "Por profesor"
2. Seleccionar turno
3. Buscar profesor
4. Contar celdas ocupadas en la grilla

**Ejemplo visual:**
```
García - Turno Mañana
Tiene ocupadas: 15 celdas
= 15 horas semanales
```

**Verificación adicional:**
- Ir a "Gestionar personal" → Banca de horas
- Ver el contador automático de cada materia

---

#### Caso 2: Detectar huecos en el horario

**Objetivo:** Ver si un profesor tiene espacios libres que podrían optimizarse.

**Ejemplo:**
```
García - Turno Mañana
        Lunes    Martes   Miércoles
1ª hora 1°A      [vacío]  1°A
2ª hora [vacío]  1°B      [vacío]
3ª hora 2°A      [vacío]  2°A
```

**Análisis:** Tiene muchos huecos, podría consolidar horarios.

---

#### Caso 3: Asignar toda la carga de un profesor

**Objetivo:** Configurar todos los horarios de un profesor desde esta vista.

**Ventaja:** No necesita cambiar entre divisiones, todo en una pantalla.

**Pasos:**
1. Seleccionar profesor
2. Ir asignando cada horario en la grilla
3. Automáticamente se distribuye en todas sus divisiones

---

#### Caso 4: Reasignar profesor en un horario

**Situación:** Necesita cambiar el profesor García por Pérez en un horario específico.

**Opción A: Desde vista "Por curso"**
1. Ir a la división
2. Editar el horario
3. Cambiar profesor

**Opción B: Desde vista "Por profesor"**
1. Vista de García → Eliminar el horario
2. Vista de Pérez → Agregar el horario

**Ambas opciones tienen el mismo efecto.**

### 14.12 Estrategias de uso combinado

**Recomendación:** Use ambas vistas según la tarea.

**Vista "Por curso" es mejor para:**
- ✅ Planificar el horario completo de una división
- ✅ Ver qué materias tiene un curso cada día
- ✅ Distribuir materias equilibradamente

**Vista "Por profesor" es mejor para:**
- ✅ Ver la carga horaria de un docente
- ✅ Detectar conflictos de horarios del profesor
- ✅ Optimizar la distribución de un profesor
- ✅ Verificar que el profesor no tenga huecos excesivos

**Flujo de trabajo típico:**
1. Crear estructura base en vista "Por curso" (dividir materias por división)
2. Revisar y ajustar en vista "Por profesor" (optimizar horarios de docentes)
3. Refinamiento final en vista "Por curso" (verificar horarios de cada división)

### 14.13 Ejemplo completo: Horario de un profesor

```
Profesor: García López, Juan Carlos - Turno Mañana
Materias: Matemática

┌───┬──────────┬──────────┬──────────┬──────────┬──────────┐
│   │  Lunes   │  Martes  │Miércoles │  Jueves  │ Viernes  │
├───┼──────────┼──────────┼──────────┼──────────┼──────────┤
│1ª │   1°A    │   1°B    │   1°A    │   2°A    │   1°C    │
│   │Matemática│Matemática│Matemática│Matemática│Matemática│
│   │08:00-    │08:00-    │08:00-    │08:00-    │08:00-    │
│   │08:45     │08:45     │08:45     │08:45     │08:45     │
├───┼──────────┼──────────┼──────────┼──────────┼──────────┤
│2ª │   1°A    │   1°B    │          │   2°A    │   1°C    │
│   │Matemática│Matemática│          │Matemática│Matemática│
│   │08:45-    │08:45-    │          │08:45-    │08:45-    │
│   │09:30     │09:30     │          │09:30     │09:30     │
├───┼──────────┼──────────┼──────────┼──────────┼──────────┤
│3ª │   2°B    │   1°A    │   1°B    │   1°A    │   2°A    │
│   │Matemática│Matemática│Matemática│Matemática│Matemática│
│   │09:30-    │09:30-    │09:30-    │09:30-    │09:30-    │
│   │10:15     │10:15     │10:15     │10:15     │10:15     │
├───┼──────────┼──────────┼──────────┼──────────┼──────────┤
│4ª │          │   2°A    │   1°C    │   1°B    │   2°B    │
│   │          │Matemática│Matemática│Matemática│Matemática│
│   │          │10:15-    │10:15-    │10:15-    │10:15-    │
│   │          │11:00     │11:00     │11:00     │11:00     │
├───┼──────────┼──────────┼──────────┼──────────┼──────────┤
│5ª │   2°A    │          │   2°B    │          │   1°A    │
│   │Matemática│          │Matemática│          │Matemática│
│   │11:15-    │          │11:15-    │          │11:15-    │
│   │12:00     │          │12:00     │          │12:00     │
├───┼──────────┼──────────┼──────────┼──────────┼──────────┤
│6ª │          │          │          │          │          │
└───┴──────────┴──────────┴──────────┴──────────┴──────────┘

Total: 19 horas semanales
Divisiones atendidas: 1°A, 1°B, 1°C, 2°A, 2°B
```

**Análisis:**
- Carga horaria: 19 horas/semana
- 5 divisiones diferentes
- Huecos: Miércoles 2ª, Martes 5ª, Jueves 5ª
- Distribución: Equilibrada entre semana

### 14.14 Diferencias clave con vista "Por curso"

| Aspecto | Vista "Por curso" | Vista "Por profesor" |
|---------|-------------------|---------------------|
| **Enfoque** | Una división | Un profesor |
| **Muestra** | Todas las materias del curso | Todas las divisiones del profesor |
| **Profesor** | Seleccionable (múltiples opciones) | Fijo (el seleccionado) |
| **División** | Fija (la seleccionada) | Seleccionable (múltiples opciones) |
| **Uso típico** | Planificar horario del curso | Verificar carga del docente |
| **Filtrado** | Turno→Plan→Curso→División | Turno→Profesor |

### 14.15 Consejos para horarios por profesor

✅ **Buenas prácticas:**
- Use esta vista para verificar cargas horarias
- Detecte y elimine huecos innecesarios
- Verifique que no haya superposiciones
- Use el filtro de búsqueda con muchos profesores
- Combine con vista "Por curso" para planificación completa

⚠️ **Errores comunes:**
- ❌ Olvidar que el profesor debe estar en el turno
- ❌ Intentar asignar materias fuera de la banca
- ❌ No verificar si la división ya tiene horario en ese espacio
- ❌ Confundir qué vista está usando (por curso vs por profesor)
- ❌ Asignar todo desde esta vista sin verificar balance en las divisiones

### 14.16 Preguntas frecuentes

**P: ¿Los cambios aquí afectan la vista "Por curso"?**
R: Sí, ambas vistas están sincronizadas. Son dos formas de ver los mismos datos.

**P: ¿Puedo ver varios profesores a la vez?**
R: No, debe seleccionar un profesor a la vez. Para comparar, cambie de profesor.

**P: ¿Puedo asignar un profesor a una división sin materia?**
R: No, la materia es obligatoria en esta vista.

**P: ¿Qué pasa si asigno el mismo horario a dos divisiones del mismo profesor?**
R: No es posible, el sistema valida que no haya superposiciones.

**P: ¿Cómo sé cuántas horas tiene asignadas un profesor?**
R: Cuente las celdas ocupadas en la grilla, o vaya a "Gestionar personal" → Banca de horas.

**P: ¿Puedo dejar espacios vacíos?**
R: Sí, los espacios vacíos indican que el profesor no tiene clases en ese horario.

---

# PARTE 5: OPERACIONES AVANZADAS Y TROUBLESHOOTING

## 15. OPERACIONES AVANZADAS

### 15.1 Limpiar horarios vacíos

**Qué hace:** Elimina todos los horarios que NO tienen materia NI profesor asignados.

**Cuándo usar:**
- Después de experimentar con diferentes configuraciones
- Cuando hay muchas celdas "basura" sin información
- Para limpiar la base de datos antes de un backup

**Cómo hacerlo:**

**Desde vista "Por curso":**
1. Haga clic en **[Limpiar horarios vacíos]**
2. Confirme la acción

**Desde vista "Por profesor":**
1. Haga clic en **[Limpiar horarios vacíos]**
2. Confirme la acción

**Resultado:** 
```
Mensaje: "X horarios vacíos eliminados."
```

**Importante:** Esta acción NO se puede deshacer. Haga backup antes si no está seguro.

### 15.2 Exportar/Respaldar horarios

**Método actual:** Respaldo completo de la base de datos.

**Pasos:**
1. Cerrar el programa
2. Copiar el archivo `horarios.db`
3. Pegarlo en carpeta de respaldos con fecha:
   ```
   horarios_2025-11-08.db
   ```

**Para restaurar:**
1. Cerrar el programa
2. Reemplazar `horarios.db` con el respaldo
3. Abrir el programa

**Nota para versión futura:** Exportación a PDF o Excel no implementada en v0.9.

### 15.3 Verificar integridad de datos

**Indicadores de problemas:**
- Contadores de horas no coinciden con horarios asignados
- Profesores aparecen sin turnos asignados
- Materias sin asignar a planes
- Divisiones huérfanas (sin plan o turno)

**Verificaciones manuales:**

#### Verificación 1: Contadores de materias
1. Ir a "Gestionar Materias"
2. Anotar las horas de una materia (ej: Matemática = 15)
3. Ir a "Horarios por Curso"
4. Contar manualmente en todas las divisiones
5. Debe coincidir el total

#### Verificación 2: Banca de profesores
1. Ir a "Gestionar Personal" → Banca de horas
2. Anotar las horas de un profesor en una materia
3. Ir a "Horarios por Profesor"
4. Contar horarios del profesor
5. Debe coincidir

#### Verificación 3: Superposiciones
1. Ir a "Horarios por Profesor"
2. Verificar que cada celda tenga solo una división
3. Si hay texto superpuesto, hay un error de datos

### 15.4 Optimizar horarios

**Objetivo:** Minimizar huecos y optimizar distribución.

**Estrategias:**

#### Estrategia 1: Consolidar horarios de profesores
```
Antes:
Lunes 1ª: 1°A
Lunes 3ª: 1°B (hueco en 2ª)

Después:
Lunes 1ª: 1°A
Lunes 2ª: 1°B (sin hueco)
```

#### Estrategia 2: Equilibrar materias por día
```
Antes:
Lunes: Matemática (3), Física (2), Lengua (0)
Martes: Matemática (0), Física (0), Lengua (5)

Después:
Lunes: Matemática (2), Física (1), Lengua (2)
Martes: Matemática (1), Física (1), Lengua (3)
```

#### Estrategia 3: Agrupar divisiones
```
Si un profesor da clase a 1°A y 1°B:
Intente agrupar sus horarios en los mismos días
(facilita traslados y preparación)
```

### 15.5 Copiar horarios entre divisiones

**Nota:** El sistema NO tiene función de copia automática.

**Método manual:**
1. Abrir el horario de la división origen (ej: 1°A)
2. Anotar o capturar pantalla del horario
3. Abrir el horario de la división destino (ej: 1°B)
4. Replicar manualmente cada horario

**Alternativa:** Usar configuración de horas para acelerar la entrada.

### 15.6 Reportes y consultas

**Reportes disponibles en v0.9:**
- ❌ Exportación a PDF: No disponible
- ❌ Exportación a Excel: No disponible
- ❌ Impresión optimizada: No disponible
- ✅ Visualización en pantalla: Disponible

**Alternativa para generar reportes:**
1. Captura de pantalla de cada división
2. Pegar en documento Word/Excel
3. Imprimir o distribuir digitalmente

**Nota:** Funcionalidad de reportes está planificada para v2.0.

---

## 16. PREGUNTAS FRECUENTES (FAQ)

### 16.1 Problemas de instalación

**P: El programa no inicia después de descargarlo.**
R: Verifique que Windows no lo haya bloqueado. Click derecho → Propiedades → Desbloquear.

**P: Antivirus marca el archivo como amenaza.**
R: Es un falso positivo común con ejecutables de PyInstaller. Agregue excepción en el antivirus.

**P: Aparece error "archivo horarios.db en uso".**
R: Cierre todas las instancias del programa. Si persiste, reinicie la PC.

### 16.2 Problemas con datos

**P: No aparecen opciones en los filtros de división.**
R: Verifique que creó: Turnos → Planes → Asignó planes a turnos → Creó años → Asignó materias.

**P: Los contadores de horas no coinciden.**
R: Es un problema grave. Haga backup y contacte soporte. Puede intentar recrear horarios afectados.

**P: Eliminé algo por error, ¿puedo recuperarlo?**
R: Solo si tiene un backup reciente. No hay función de "deshacer" en v0.9.

**P: Tengo datos duplicados (dos materias "Matemática").**
R: No debería ser posible por validación UNIQUE. Si ocurre, elimine el duplicado.

### 16.3 Problemas con horarios

**P: No puedo asignar un profesor a un horario.**
R: Verifique: 1) El profesor tiene la materia en su banca, 2) El profesor está asignado al turno, 3) El profesor no está ocupado en ese horario en otra división.

**P: Al asignar horario dice "UNIQUE constraint failed".**
R: Ya existe un horario en esa división en ese día y espacio. Edite el existente o elija otro horario.

**P: Los cambios en "Por curso" no aparecen en "Por profesor".**
R: No debería pasar (están sincronizados). Intente cerrar y volver a abrir la vista.

**P: Configuré las horas pero no se aplican.**
R: Debe marcar los checkboxes de aplicación. O solo afecta a horarios NUEVOS.

### 16.4 Rendimiento

**P: El programa va lento.**
R: Con bases de datos grandes (+1000 horarios) puede haber lentitud. Cierre otros programas para liberar RAM.

**P: La grilla de horarios tarda en cargar.**
R: Normal con muchos horarios. Use filtros para limitar la cantidad de datos mostrados.

### 16.5 Varios

**P: ¿Puedo usar el sistema en múltiples PC?**
R: Sí, pero debe copiar el archivo `horarios.db` entre PCs. No hay sincronización automática.

**P: ¿Cuántos horarios puede manejar el sistema?**
R: Testeado hasta 5,000 horarios sin problemas. Límite teórico de SQLite es millones.

**P: ¿Puedo cambiar el idioma?**
R: No, el sistema solo está en español.

**P: ¿Hay versión para celular/tablet?**
R: No, solo Windows desktop.

---

## 17. SOLUCIÓN DE PROBLEMAS

### 17.1 El programa no inicia

**Síntomas:**
- Doble clic no hace nada
- Aparece brevemente y se cierra
- Error inmediato al abrir

**Soluciones:**

**Solución 1:** Verificar permisos
- Click derecho en el .exe → Propiedades
- Pestaña "General" → Si dice "Desbloquear", marcar y aplicar
- Intentar ejecutar nuevamente

**Solución 2:** Ejecutar desde terminal
```powershell
cd "C:\ruta\al\programa"
.\SistemaHorarios.exe
```
Esto mostrará mensajes de error si los hay.

**Solución 3:** Verificar antivirus
- Agregar excepción en el antivirus
- O temporalmente desactivar antivirus y probar

**Solución 4:** Reinstalar
- Eliminar completamente el programa
- Descargar nueva copia
- Extraer en ubicación diferente

### 17.2 Base de datos corrupta

**Síntomas:**
- Errores al guardar datos
- Programa se cierra inesperadamente
- Mensajes "database disk image is malformed"

**Soluciones:**

**Solución 1:** Restaurar desde backup
- Cerrar programa
- Reemplazar `horarios.db` con backup reciente
- Abrir programa

**Solución 2:** Intentar reparación (avanzado)
```powershell
# Instalar SQLite
# Ejecutar:
sqlite3 horarios.db "PRAGMA integrity_check;"
sqlite3 horarios.db ".recover" | sqlite3 horarios_recuperado.db
```

**Solución 3:** Recrear base de datos
- Renombrar `horarios.db` a `horarios_viejo.db`
- Abrir programa (crea nuevo `horarios.db` vacío)
- Recargar datos manualmente

### 17.3 Errores al asignar horarios

**Síntoma:** Mensaje de error al guardar horario.

**Diagnóstico:** Lea el mensaje de error con atención.

**Errores comunes:**

| Mensaje de Error | Causa | Solución |
|------------------|-------|----------|
| "El profesor ya está asignado..." | Superposición de horarios | Cambiar horario o profesor |
| "El profesor no tiene la materia..." | Falta en banca de horas | Agregar materia a banca |
| "El profesor no está asignado al turno..." | Falta turno | Asignar turno al profesor |
| "UNIQUE constraint failed" | Horario duplicado | Editar existente en lugar de crear |
| "La división no pertenece..." | División de otro turno | Verificar filtros |

### 17.4 Interfaz se ve mal

**Síntomas:**
- Botones cortados
- Texto superpuesto
- Ventana muy pequeña o muy grande

**Soluciones:**

**Solución 1:** Ajustar resolución de pantalla
- Mínimo recomendado: 1024x768
- Óptimo: 1366x768 o superior

**Solución 2:** Ajustar escalado de Windows
- Configuración → Sistema → Pantalla
- Cambiar escala a 100% (no 125% ni 150%)

**Solución 3:** Maximizar ventana
- Click en botón maximizar
- O presionar Win + Flecha arriba

### 17.5 Datos desincronizados

**Síntomas:**
- Vista "Por curso" muestra diferentes datos que "Por profesor"
- Contadores no coinciden con horarios

**Solución:**
1. Cerrar completamente el programa
2. Verificar que no haya procesos colgados (Task Manager)
3. Reabrir el programa
4. Verificar nuevamente

**Si persiste:**
- Hacer backup de `horarios.db`
- Contactar soporte con descripción detallada

### 17.6 Problemas de rendimiento

**Síntomas:**
- Programa lento
- Grillas tardan en cargar
- Ventanas tardan en abrir

**Soluciones:**

**Solución 1:** Cerrar otros programas
- Liberar memoria RAM
- Cerrar navegadores y aplicaciones pesadas

**Solución 2:** Optimizar base de datos
- Cerrar programa
- Ejecutar en terminal:
```powershell
sqlite3 horarios.db "VACUUM;"
```

**Solución 3:** Limpiar datos innecesarios
- Usar "Limpiar horarios vacíos"
- Eliminar profesores no utilizados
- Eliminar materias no utilizadas

### 17.7 Contacto con soporte

**Si ninguna solución funciona:**

**Información a proporcionar:**
1. Versión del sistema (si está disponible en "Acerca de")
2. Sistema operativo (Windows 7/8/10/11)
3. Descripción detallada del problema
4. Pasos exactos para reproducir
5. Capturas de pantalla
6. Mensaje de error completo (si aplica)

**Canales de soporte:**
- [Repositorio GitHub si está disponible]
- [Email de soporte si existe]
- [Sistema de tickets si está configurado]

---

## 18. GLOSARIO

**Año/Curso:** Nivel educativo dentro de un plan de estudios (1°, 2°, 3°, etc.).

**Banca de horas:** Conjunto de materias que un profesor puede dictar, junto con las horas efectivamente asignadas.

**Base de datos:** Archivo `horarios.db` que contiene todos los datos del sistema.

**Combobox:** Lista desplegable donde se selecciona una opción.

**División:** Grupo específico de estudiantes identificado por turno+plan+año+nombre (ej: "Turno Mañana - Bachiller - 1° Año - A").

**Espacio horario:** Cada uno de los módulos o bloques de tiempo (1ª hora, 2ª hora, etc.).

**Filtro en cascada:** Mecanismo donde cada selección limita las opciones del siguiente filtro.

**Grilla:** Tabla visual que muestra los horarios en formato día-por-espacio.

**Horario:** Asignación específica de materia+profesor a una división en un día y espacio determinado.

**Horas asignadas:** Cantidad de módulos/horas que tiene asignado un profesor en una materia específica (se calcula automáticamente).

**Horas semanales:** Total de módulos/horas de una materia en toda la institución (se calcula automáticamente).

**Materia/Obligación:** Asignatura que se dicta en la institución (Matemática, Física, etc.).

**Plan de estudios:** Programa educativo completo (Bachiller, Perito, etc.).

**Profesor/Agente/Docente:** Personal que dicta clases.

**Sincronización:** Actualización automática de datos entre las vistas "Por curso" y "Por profesor".

**TreeView:** Tabla que muestra datos en filas y columnas, permitiendo selección.

**Turno:** Horario en que funciona la institución (Mañana, Tarde, Noche).

**Validación:** Verificación automática que previene ingresar datos incorrectos o inconsistentes.

**Vista:** Forma de visualización de los datos (Por curso o Por profesor).

---

**FIN DEL MANUAL DE USUARIO**

**Versión del Documento:** 1.0  
**Fecha:** 8 de noviembre de 2025  
**Sistema:** Gestión de Horarios Escolares v0.9  
**Revisión:** [Pendiente]

---

**Documentos relacionados:**
- `ACTA_DE_CONSTITUCION.md` - Información general del proyecto
- `DOCUMENTACION_TECNICA.md` - Referencia técnica para desarrolladores
- `DOCUMENTACION_CAMBIOS.md` - Historial de versiones y cambios

**Para más ayuda o soporte:**
Contacte al administrador del sistema o consulte la documentación técnica.
