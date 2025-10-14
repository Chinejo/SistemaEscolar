# Documentación de Cambios - Sistema de Gestión de Horarios

## Resumen de Cambios Implementados

### 1. Menú Principal
- **Antes**: Menú "Horarios" → "Gestionar Horarios"
- **Ahora**: Menú "Gestión de horarios" con dos opciones:
  - **Por curso**: Gestionar horarios por división/curso
  - **Por profesor**: Gestionar horarios por profesor

### 2. Base de Datos - Tabla Unificada: `horario`

**IMPORTANTE**: Ahora usamos UNA SOLA TABLA para ambas vistas, lo que garantiza la sincronización automática.

### 2. Base de Datos - Modificación de Tabla: `horario`

Se modificó la tabla existente `horario` para agregar el campo `turno_id`, permitiendo gestionar horarios desde ambas perspectivas (por curso y por profesor) usando **una sola tabla compartida**.

**Estructura actualizada:**
```sql
CREATE TABLE horario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    division_id INTEGER,           -- ID de la división/curso
    dia TEXT,                      -- Día de la semana
    espacio INTEGER,               -- Número de espacio horario (1-8)
    hora_inicio TEXT,              -- Hora de inicio (opcional)
    hora_fin TEXT,                 -- Hora de fin (opcional)
    materia_id INTEGER,            -- ID de la materia
    profesor_id INTEGER,           -- ID del profesor
    turno_id INTEGER,              -- ID del turno (NUEVO CAMPO)
    FOREIGN KEY(division_id) REFERENCES division(id),
    FOREIGN KEY(materia_id) REFERENCES materia(id),
    FOREIGN KEY(profesor_id) REFERENCES profesor(id),
    FOREIGN KEY(turno_id) REFERENCES turno(id),
    UNIQUE(division_id, dia, espacio)
)
```

**Beneficio clave**: Al compartir la misma tabla, cualquier cambio en una vista se refleja automáticamente en la otra.

### 3. Funciones CRUD Modificadas y Nuevas

**Función modificada:**

- `crear_horario(division_id, dia, espacio, hora_inicio, hora_fin, materia_id, profesor_id, turno_id=None)`
  - **Ahora acepta `turno_id` como parámetro opcional**
  - Si no se proporciona, lo calcula automáticamente desde la división
  - Guarda en la tabla `horario` para que sea visible en ambas vistas

**Funciones nuevas para gestión desde vista de profesor:**

- `crear_horario_profesor(profesor_id, turno_id, dia, espacio, hora_inicio, hora_fin, division_id, materia_id)`
  - Crea un nuevo horario para un profesor
  - **Guarda en la tabla `horario` compartida** (no en tabla separada)
  - Valida que el profesor esté asignado al turno
  - Valida que el profesor tenga la materia asignada
  - Previene superposiciones de horarios
  - Si se especifica división, valida que pertenezca al turno

- `obtener_horarios_profesor(profesor_id, turno_id)`
  - Obtiene todos los horarios de un profesor en un turno específico
  - **Lee de la tabla `horario`**, por lo que incluye asignaciones hechas desde cualquier vista
  - Retorna lista con información de materia y división

- `eliminar_horario_profesor(id)`
  - Elimina un horario específico del profesor
  - **Usa la misma función `eliminar_horario()`** que la vista por curso
  - El cambio se refleja automáticamente en ambas vistas

### 4. Interfaz Gráfica

#### Vista "Por Curso" (renombrada)
- Función `mostrar_horarios_curso()` (antes `mostrar_horarios()`)
- Permite seleccionar: Turno → Plan → Año → División
- Muestra grilla semanal con las materias y profesores asignados
- Permite editar cada espacio horario

#### Vista "Por Profesor" (nueva)
- Función `mostrar_horarios_profesor()`
- Permite seleccionar: Turno → Profesor
- Muestra grilla semanal del profesor seleccionado
- Muestra en cada espacio:
  - Materia que enseña
  - División donde da clase
  - Horario de inicio y fin
- Permite editar cada espacio horario
- Solo permite asignar materias que el profesor tiene en su banca de horas
- Solo muestra divisiones del turno seleccionado

### 5. Validaciones Implementadas

**En horarios por profesor:**
1. El profesor debe estar asignado al turno
2. El profesor debe tener la materia en su banca de horas
3. No se permite superposición de horarios (mismo turno, día y espacio)
4. Las horas de inicio y fin son opcionales
5. La división y materia son opcionales (permite espacios libres)

### 6. Funcionalidades Compartidas

Ambas vistas (Por Curso y Por Profesor) comparten:
- Sistema de configuración de horas por turno y espacio
- Grilla visual de lunes a viernes con 8 espacios horarios
- Sistema de scroll para visualizar toda la grilla
- Edición modal de cada espacio horario
- Validaciones de integridad de datos
- **LA MISMA TABLA DE DATOS** - cambios en una vista se ven en la otra

## Uso del Sistema

### Para gestionar horarios por curso:
1. Ir a menú: **Gestión de horarios** → **Por curso**
2. Seleccionar: Turno → Plan → Año → División
3. Hacer clic en cualquier espacio de la grilla para editarlo
4. Asignar materia, profesor y horarios
5. **Los datos se sincronizan automáticamente** con la vista por profesor

### Para gestionar horarios por profesor:
1. Ir a menú: **Gestión de horarios** → **Por profesor**
2. Seleccionar: Turno → Profesor
3. Hacer clic en cualquier espacio de la grilla para editarlo
4. Asignar materia (de su banca), división y horarios
5. **Los datos se sincronizan automáticamente** con la vista por curso

## Sincronización Bidireccional

**Ejemplo de flujo:**

1. **Desde vista "Por curso"**: Asignas al profesor "Juan Pérez" la materia "Matemática" en 1ºA los lunes a las 8:00
   - Se guarda en tabla `horario` con: `division_id=1ºA`, `profesor_id=Juan`, `materia_id=Matemática`, `turno_id=Mañana`

2. **Desde vista "Por profesor"**: Seleccionas al profesor "Juan Pérez" en turno "Mañana"
   - **Automáticamente aparece** la clase de Matemática en 1ºA los lunes a las 8:00

3. **Si modificas o eliminas** desde cualquiera de las dos vistas, el cambio se refleja en ambas instantáneamente

## Notas Técnicas

- La base de datos se actualiza automáticamente al iniciar el programa
- **Se usa UNA SOLA TABLA `horario`** para ambas vistas (no hay tabla `horario_profesor` separada)
- Los horarios por profesor y por curso son **dos vistas diferentes de los mismos datos**
- Se utiliza ruta absoluta para la base de datos, evitando problemas de directorio de trabajo
- La columna `turno_id` se agrega automáticamente a registros existentes mediante migración
- Script `migrar_datos.py` disponible para actualizar datos antiguos

---

## Mejoras de Interfaz de Usuario (UI/UX)

### 3. Cambios de Nomenclatura
- **Divisiones → Cursos**: Se renombró "Divisiones" a "Cursos" en toda la interfaz para mayor claridad

### 4. Vista de Horarios por Profesor

#### 4.1 Dropdown de Profesor con Autocompletar
- **Filtrado en tiempo real**: Al tipear, filtra la lista de profesores
- **Auto-expand**: El menú desplegable se abre automáticamente al comenzar a tipear
- Facilita la búsqueda de profesores en listas largas

#### 4.2 Formato de Columnas Unificado
- Ambas vistas (Por curso y Por profesor) usan el mismo formato para horas: **1ª, 2ª, 3ª...**
- Consistencia visual entre las dos perspectivas de gestión

### 5. Ventana "Configurar Horas por Turno"
**Mejoras implementadas:**
- ✅ Tamaño optimizado: **420x400** (no redimensionable)
- ✅ Layout compacto y organizado
- ✅ Etiquetas descriptivas: "Hs" entre campos de inicio y fin, "a" antes de hora fin
- ✅ Placeholders en formato **hh:mm** para guiar entrada de datos
- ✅ Validación automática de formato de hora:
  - Auto-inserción de `:` después de dos dígitos
  - Navegación automática al siguiente campo al completar
  - Limita a 5 caracteres (hh:mm)

### 6. Ventanas de Edición de Espacios Horarios

#### 6.1 Por Curso
- Tamaño optimizado: **380x320** (no redimensionable)
- Estilo visual uniforme con fondo `#f4f6fa`
- Validación de entrada de horarios con auto-colon

#### 6.2 Por Profesor
**Mejoras para equiparar con vista Por Curso:**
- ✅ Tamaño optimizado: **380x370** (no redimensionable)
- ✅ Estilo visual uniforme (mismo fondo y colores)
- ✅ **Selección de Año antes de División**: Flujo más lógico
  - Primero se selecciona el año
  - Luego se filtran y muestran solo las divisiones de ese año
- ✅ Validación de horarios con auto-colon (igual que Por Curso)
- ✅ Layout consistente entre ambas vistas

### 7. Autocompletado Inteligente de Dropdowns

**Nueva funcionalidad global implementada:**

Se agregó una función helper `autocompletar_combobox()` que detecta automáticamente cuando un dropdown tiene solo una opción disponible y la selecciona automáticamente.

**Aplicado en:**

1. **Vista de Horarios por Curso:**
   - ✅ Turno (si solo hay uno)
   - ✅ Plan de estudios (si solo hay uno para el turno)
   - ✅ Año (si solo hay uno para el plan)
   - ✅ División (si solo hay una para el año)
   - ✅ Materia (si solo hay una en el sistema)
   - ✅ Profesor (si solo hay uno asignado a la materia)

2. **Vista de Horarios por Profesor:**
   - ✅ Turno (si solo hay uno)
   - ✅ Profesor (si solo hay uno en el turno)
   - ✅ Plan de estudios (si solo hay uno para el turno)
   - ✅ Año (si solo hay uno para el plan)
   - ✅ División (si solo hay una para el año)
   - ✅ Materia (si solo hay una en la banca del profesor)

**Comportamiento:**
- La función detecta automáticamente cuántas opciones hay disponibles
- Si hay solo una opción, la selecciona automáticamente
- Si hay múltiples opciones, el usuario debe elegir manualmente
- Si no hay opciones, el dropdown se deshabilita
- Las cascadas se activan automáticamente (ej: si se autocompleta Plan, se cargan los Años automáticamente)

**Beneficio:** Ahorra clics y acelera la navegación cuando las opciones son obvias o únicas.

### 8. Jerarquía de Selección en Horarios por Profesor

**Antes:** Turno → Profesor → (popup) Año → División

**Ahora:** Turno → Profesor → (popup) **Plan** → Año → División

**Justificación:**
- Cada Plan de estudios tiene sus propios Años
- Cada Año tiene sus propias Divisiones
- La jerarquía correcta es: Plan → Año → División
- Esto garantiza que solo se muestren las opciones válidas en cada nivel

**Tamaño de ventana actualizado:**
- Ventana de edición por profesor: `330x420` (ajustado para incluir campo Plan)

### 9. Resumen de Beneficios de UI/UX

**Consistencia:**
- Mismo formato de horas en ambas vistas
- Estilo visual unificado en todas las ventanas popup
- Tamaños de ventana optimizados y no redimensionables
- Jerarquía Plan → Año → División en ambas vistas

**Eficiencia:**
- Filtrado rápido de profesores con autocompletar
- Auto-expansión de dropdowns
- Navegación automática entre campos de hora
- **Autocompletado inteligente** reduce clics innecesarios

**Usabilidad:**
- Placeholders que guían el formato correcto
- Validación automática de entrada de tiempo
- Flujo lógico: Plan → Año → División → Materia
- Etiquetas descriptivas ("Hs", "a") para mayor claridad
- **Selección automática** cuando solo hay una opción
