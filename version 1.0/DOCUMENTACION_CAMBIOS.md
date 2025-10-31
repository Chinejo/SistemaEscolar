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

---

## Corrección de Errores (Octubre 2025)

### Bug Corregido: Configurar Horas por Turno no Actualizaba Horarios de Profesor

**Fecha:** 14 de octubre de 2025

**Problema:**
En la gestión de horarios por profesor, cuando se presionaba el botón "Configurar horas por turno", se marcaba la casilla "Aplicar a horarios existentes" y se presionaba guardar, los horarios del profesor seleccionado NO se actualizaban con las horas configuradas para el turno.

**Causa Raíz:**
El código en la función `_configurar_horas_por_turno()` estaba intentando actualizar/insertar registros en una tabla inexistente llamada `horario_profesor`. Esta tabla no existe en el esquema de la base de datos.

**Contexto Técnico:**
- El sistema utiliza una **única tabla `horario`** para gestionar tanto horarios por curso como horarios por profesor
- La función `obtener_horarios_profesor()` lee correctamente de la tabla `horario`
- Sin embargo, la función `_configurar_horas_por_turno()` intentaba escribir en `horario_profesor` (líneas 2398-2411)

**Solución Implementada:**
Se corrigió la función `_configurar_horas_por_turno()` para que actualice correctamente la tabla `horario` en lugar de la tabla inexistente `horario_profesor`.

**Cambios en el código:**

```python
# ANTES (líneas 2398-2411):
c.execute('SELECT id FROM horario_profesor WHERE profesor_id=? AND turno_id=? AND espacio=? AND dia=?', ...)
c.execute('UPDATE horario_profesor SET hora_inicio = ?, hora_fin = ? WHERE id=?', ...)
c.execute('INSERT INTO horario_profesor (...) VALUES (...)', ...)

# DESPUÉS:
c.execute('SELECT id FROM horario WHERE profesor_id=? AND turno_id=? AND espacio=? AND dia=?', ...)
c.execute('UPDATE horario SET hora_inicio = ?, hora_fin = ? WHERE id=?', ...)
c.execute('INSERT INTO horario (...) VALUES (...)', ...)
```

**Mejora Adicional:**
Se agregó código para refrescar automáticamente la grilla visual después de guardar las configuraciones de horas por turno, si el usuario está en la vista de horarios por profesor:

```python
# Refrescar la grilla si estamos en la vista de horarios por profesor
if hasattr(self, 'cb_profesor_horario') and self.cb_profesor_horario.get():
    self._dibujar_grilla_horario_profesor()
```

**Resultado:**
- ✅ Los horarios del profesor ahora se actualizan correctamente cuando se aplica la configuración de horas por turno
- ✅ La grilla visual se refresca automáticamente mostrando los cambios inmediatamente
- ✅ La funcionalidad "Aplicar a horarios existentes" ahora funciona como se esperaba

**Archivos Modificados:**
- `Horarios_v0.9.py` (líneas 2398-2414 aproximadamente)

---

### Bug Corregido: Configurar Horas por Turno Aplicaba a TODOS los Profesores

**Fecha:** 14 de octubre de 2025

**Problema:**
Al usar "Configurar horas por turno" desde la vista de horarios por profesor, cuando se marcaba "Aplicar a horarios existentes", el sistema aplicaba las horas configuradas a TODOS los profesores del turno en lugar de solo al profesor actualmente seleccionado.

**Causa Raíz:**
La función `_configurar_horas_por_turno()` no diferenciaba entre:
- Vista por curso: donde es correcto aplicar a todas las divisiones del turno
- Vista por profesor: donde debe aplicar solo al profesor seleccionado

El código siempre aplicaba las horas tanto a las divisiones como a todos los profesores del turno mediante la tabla `profesor_turno`.

**Solución Implementada:**
Se modificó la función `_configurar_horas_por_turno()` para detectar el contexto:

1. **Detecta si está en vista por profesor** verificando:
   - Existencia del combobox de profesor (`cb_profesor_horario`)
   - Existencia del diccionario de profesores (`profesores_dict_horario`)
   - Si hay un profesor actualmente seleccionado

2. **Comportamiento diferenciado:**
   - **En vista por profesor**: Aplica las horas SOLO al profesor seleccionado
   - **En vista por curso**: Aplica las horas a todas las divisiones del turno (comportamiento original)

**Cambios en el código:**
```python
# Verificar si estamos en la vista de horarios por profesor
en_vista_profesor = (hasattr(self, 'cb_profesor_horario') and 
                    hasattr(self, 'profesores_dict_horario') and 
                    self.cb_profesor_horario.get() and 
                    self.cb_profesor_horario.get() in self.profesores_dict_horario)

if en_vista_profesor:
    # Aplicar solo al profesor seleccionado
    profesor_id = self.profesores_dict_horario[self.cb_profesor_horario.get()]
    # ... actualizar solo horarios de este profesor
else:
    # Aplicar a todas las divisiones del turno
    # ... comportamiento original
```

**Resultado:**
- ✅ Desde vista por profesor: aplica horas solo al profesor seleccionado
- ✅ Desde vista por curso: aplica horas a todas las divisiones del turno
- ✅ No se afectan profesores no relacionados

---

### Bug Corregido: Botón "Limpiar Horarios Vacíos" no Funcionaba

**Fecha:** 14 de octubre de 2025

**Problema:**
El botón "Limpiar horarios vacíos" en la vista de horarios por profesor no funcionaba y generaba un error en la base de datos.

**Causa Raíz:**
La función `_limpiar_horarios_vacios_profesor()` intentaba ejecutar una consulta DELETE sobre la tabla `horario_profesor`, que no existe en la base de datos. El sistema utiliza una única tabla `horario` para ambas vistas.

**Solución Implementada:**
Se corrigió la consulta SQL para utilizar la tabla correcta:

```python
# ANTES:
c.execute('''DELETE FROM horario_profesor 
            WHERE profesor_id = ? ...''', (profesor_id, turno_id))

# DESPUÉS:
c.execute('''DELETE FROM horario 
            WHERE profesor_id = ? ...''', (profesor_id, turno_id))
```

**Resultado:**
- ✅ El botón "Limpiar horarios vacíos" ahora funciona correctamente
- ✅ Elimina correctamente los horarios que solo tienen hora de inicio/fin
- ✅ Conserva los horarios que tienen división o materia asignadas

**Archivos Modificados:**
- `Horarios_v0.9.py` (líneas 1993 y 2367-2419 aproximadamente)

---

### Bug Corregido: Configurar Horas por Turno Dejó de Funcionar en Vista por Curso

**Fecha:** 14 de octubre de 2025

**Problema:**
Después de implementar la detección de contexto para aplicar horas solo al profesor seleccionado, la funcionalidad "Configurar horas por turno" dejó de funcionar en la vista de gestión de horarios por curso.

**Causa Raíz:**
La condición para detectar si estábamos en la vista por profesor no era lo suficientemente robusta. Los atributos `cb_profesor_horario` y `profesores_dict_horario` pueden existir en memoria de sesiones anteriores (cuando el usuario navegó previamente por la vista de profesor), lo que causaba falsos positivos en la detección del contexto.

**Solución Implementada:**
Se mejoró la detección de contexto agregando validaciones adicionales:

1. **Verificar `cb_turno_horario_prof`**: Este combobox solo existe en la vista por profesor
2. **Verificar que el widget existe visualmente**: Se usa `winfo_exists()` para confirmar que el widget está realmente visible en pantalla

**Cambios en el código:**
```python
# ANTES:
en_vista_profesor = (hasattr(self, 'cb_profesor_horario') and 
                    hasattr(self, 'profesores_dict_horario') and 
                    self.cb_profesor_horario.get() and 
                    self.cb_profesor_horario.get() in self.profesores_dict_horario)

# DESPUÉS:
en_vista_profesor = (hasattr(self, 'cb_turno_horario_prof') and    # ← Nuevo: específico de vista profesor
                    hasattr(self, 'cb_profesor_horario') and 
                    hasattr(self, 'profesores_dict_horario') and 
                    self.cb_profesor_horario.get() and 
                    self.cb_profesor_horario.get() in self.profesores_dict_horario and
                    self.cb_turno_horario_prof.winfo_exists())      # ← Nuevo: verifica que esté visible
```

**Resultado:**
- ✅ "Configurar horas por turno" funciona correctamente en vista por curso
- ✅ "Configurar horas por turno" funciona correctamente en vista por profesor
- ✅ La detección de contexto es ahora robusta y precisa
- ✅ No hay interferencia entre las dos vistas

**Archivos Modificados:**
- `Horarios_v0.9.py` (líneas 2372-2377 aproximadamente)

---

## Mejoras en "Configurar Horas por Turno" (Octubre 2025)

### Nueva Funcionalidad: Dos Opciones de Aplicación de Horas

**Fecha:** 14 de octubre de 2025

**Mejoras Implementadas:**

#### 1. Dos Checkboxes para Mayor Control

Se reemplazó el checkbox único "Aplicar a horarios existentes" por dos opciones independientes:

1. **"Aplicar a horario actual"**: Aplica las horas configuradas solo al horario que estás viendo actualmente
   - En vista por profesor: Solo al profesor seleccionado
   - En vista por curso: Solo a la división seleccionada

2. **"Aplicar a todos los horarios del turno"**: Aplica las horas a todos los horarios del turno
   - En vista por profesor: A todos los profesores del turno
   - En vista por curso: A todas las divisiones del turno

**Beneficio**: Mayor flexibilidad y control sobre qué horarios se actualizan.

#### 2. Comportamiento Contextual Inteligente

**En Vista por Curso:**
- ✅ "Aplicar a horario actual" → Actualiza solo la división seleccionada
- ✅ "Aplicar a todos los horarios del turno" → Actualiza todas las divisiones del turno
- ✅ Ambos checkboxes pueden marcarse simultáneamente

**En Vista por Profesor:**
- ✅ "Aplicar a horario actual" → Actualiza solo el profesor seleccionado
- ✅ "Aplicar a todos los horarios del turno" → Actualiza todos los profesores asignados al turno
- ✅ Ambos checkboxes pueden marcarse simultáneamente

#### 3. Actualización Automática de Grilla

La grilla visual ahora se actualiza automáticamente después de aplicar las configuraciones:

- ✅ **Vista por profesor**: La grilla se refresca mostrando las horas actualizadas
- ✅ **Vista por curso**: La grilla se refresca mostrando las horas actualizadas (NUEVO)

**Antes**: Solo la vista por profesor se actualizaba automáticamente
**Ahora**: Ambas vistas se actualizan automáticamente

#### 4. Detección Mejorada de Contexto

Se mejoró la lógica para detectar si el usuario está en vista por curso o por profesor:

```python
# Detectar vista por profesor
en_vista_profesor = (hasattr(self, 'cb_turno_horario_prof') and 
                    hasattr(self, 'cb_profesor_horario') and 
                    hasattr(self, 'profesores_dict_horario') and 
                    self.cb_profesor_horario.get() and 
                    self.cb_profesor_horario.get() in self.profesores_dict_horario and
                    self.cb_turno_horario_prof.winfo_exists())

# Detectar vista por curso
en_vista_curso = (hasattr(self, 'cb_turno_horario') and 
                hasattr(self, 'cb_division_horario') and 
                hasattr(self, 'divisiones_dict_horario') and
                self.cb_division_horario.get() and 
                self.cb_division_horario.get() in self.divisiones_dict_horario and
                self.cb_turno_horario.winfo_exists())
```

#### 5. Cambios en la Interfaz

- **Tamaño de ventana**: Aumentado de `280x430` a `280x480` para acomodar los dos checkboxes
- **Disposición**: Los checkboxes están claramente separados visualmente
- **Etiquetas descriptivas**: Texto claro que indica exactamente qué hace cada opción

### Casos de Uso

**Ejemplo 1: Actualizar solo un curso específico**
1. Ir a "Gestión de horarios" → "Por curso"
2. Seleccionar el curso deseado
3. Click en "Configurar horas por turno"
4. Configurar las horas
5. ✅ Marcar "Aplicar a horario actual"
6. Guardar
→ Solo ese curso se actualiza

**Ejemplo 2: Actualizar todos los cursos del turno mañana**
1. Ir a "Gestión de horarios" → "Por curso"
2. Seleccionar cualquier curso del turno mañana
3. Click en "Configurar horas por turno"
4. Configurar las horas
5. ✅ Marcar "Aplicar a todos los horarios del turno"
6. Guardar
→ Todos los cursos del turno mañana se actualizan

**Ejemplo 3: Actualizar un profesor específico**
1. Ir a "Gestión de horarios" → "Por profesor"
2. Seleccionar el profesor
3. Click en "Configurar horas por turno"
4. Configurar las horas
5. ✅ Marcar "Aplicar a horario actual"
6. Guardar
→ Solo ese profesor se actualiza

**Ejemplo 4: Actualizar todos los profesores del turno**
1. Ir a "Gestión de horarios" → "Por profesor"
2. Seleccionar cualquier profesor del turno
3. Click en "Configurar horas por turno"
4. Configurar las horas
5. ✅ Marcar "Aplicar a todos los horarios del turno"
6. Guardar
→ Todos los profesores del turno se actualizan

### Resumen de Cambios Técnicos

**Archivos Modificados:**
- `Horarios_v0.9.py`:
  - Línea 2244: Tamaño de ventana aumentado a `280x480`
  - Líneas 2313-2321: Nuevos checkboxes `apply_actual_var` y `apply_todos_var`
  - Líneas 2373-2518: Lógica mejorada de aplicación con detección de contexto
  - Líneas 2520-2524: Actualización automática de grilla en ambas vistas

**Beneficios:**
- ✅ Mayor control sobre qué horarios se actualizan
- ✅ Claridad en las opciones disponibles
- ✅ Feedback visual inmediato (grilla se actualiza automáticamente)
- ✅ Funciona perfectamente en ambas vistas (curso y profesor)
- ✅ Los checkboxes pueden usarse de forma independiente o combinada

---

### Bug Corregido: Checkboxes no Funcionaban en Vista por Profesor

**Fecha:** 14 de octubre de 2025

**Problema:**
Después de implementar los dos nuevos checkboxes, la funcionalidad dejó de funcionar correctamente en la vista por profesor.

**Causa Raíz:**
En el código del segundo checkbox ("Aplicar a todos los horarios del turno"), se usaba una estructura `if/else`:

```python
if en_vista_profesor:
    # Código para profesores
else:
    # Código para divisiones
```

El problema era que si `en_vista_profesor` era `False` (por cualquier motivo, incluso si no estábamos en vista por curso), el código caía en el `else` y ejecutaba la lógica incorrecta.

**Solución Implementada:**
Se cambió el `else` por `elif en_vista_curso:` para asegurar que solo se ejecute el código correspondiente cuando efectivamente estamos en cada vista:

```python
if en_vista_profesor:
    # Código para profesores
elif en_vista_curso:  # ← Cambiado de 'else' a 'elif en_vista_curso'
    # Código para divisiones
```

**Resultado:**
- ✅ Los checkboxes funcionan correctamente en vista por profesor
- ✅ Los checkboxes funcionan correctamente en vista por curso
- ✅ No hay interferencia entre vistas
- ✅ La detección de contexto es precisa

**Archivos Modificados:**
- `Horarios_v0.9.py` (línea 2495: cambio de `else` a `elif en_vista_curso`)

---

### Bug Corregido: Error TclError al Usar Configurar Horas por Turno

**Fecha:** 14 de octubre de 2025

**Problema:**
Al abrir "Configurar horas por turno" desde la vista por profesor, se producía el siguiente error:

```
_tkinter.TclError: invalid command name ".!frame.!frame.!combobox4"
```

El error ocurría al intentar guardar la configuración.

**Causa Raíz:**
El código intentaba llamar al método `.get()` en widgets que podrían no existir o estar destruidos **antes** de verificar su existencia con `winfo_exists()`. 

En las validaciones de contexto:
```python
# ANTES (orden incorrecto):
self.cb_division_horario.get() and           # ❌ Llama .get() primero
self.cb_turno_horario.winfo_exists()         # ✓ Verifica existencia después
```

Si el widget no existía, la llamada a `.get()` causaba el error `TclError`.

**Solución Implementada:**
Se invirtió el orden de las validaciones para verificar **primero** la existencia del widget con `winfo_exists()` antes de intentar acceder a su valor con `.get()`:

```python
# DESPUÉS (orden correcto):
self.cb_turno_horario.winfo_exists() and     # ✓ Verifica existencia primero
self.cb_division_horario.get() and           # ✓ Llama .get() después
```

**Cambios aplicados:**

1. **Detección de vista por profesor** (líneas 2382-2387):
   ```python
   en_vista_profesor = (hasattr(self, 'cb_turno_horario_prof') and 
                       hasattr(self, 'cb_profesor_horario') and 
                       hasattr(self, 'profesores_dict_horario') and 
                       self.cb_turno_horario_prof.winfo_exists() and  # ✓ Primero
                       self.cb_profesor_horario.get() and             # ✓ Después
                       self.cb_profesor_horario.get() in self.profesores_dict_horario)
   ```

2. **Detección de vista por curso** (líneas 2390-2395):
   ```python
   en_vista_curso = (hasattr(self, 'cb_turno_horario') and 
                    hasattr(self, 'cb_division_horario') and 
                    hasattr(self, 'divisiones_dict_horario') and
                    self.cb_turno_horario.winfo_exists() and        # ✓ Primero
                    self.cb_division_horario.get() and              # ✓ Después
                    self.cb_division_horario.get() in self.divisiones_dict_horario)
   ```

**Resultado:**
- ✅ No más errores TclError al usar "Configurar horas por turno"
- ✅ La función detecta correctamente el contexto sin intentar acceder a widgets inexistentes
- ✅ Funciona perfectamente tanto en vista por curso como en vista por profesor

**Archivos Modificados:**
- `Horarios_v0.9.py` (líneas 2382-2395: orden de validaciones corregido)

---

## Mejora de Usabilidad: Selección Rápida con Enter en Combobox de Profesores (Octubre 2025)

### Nueva Funcionalidad: Selección con Enter

**Fecha:** 14 de octubre de 2025

**Mejora Implementada:**

En la vista "Gestión de Horarios por Profesor", el combobox de selección de profesor ahora permite seleccionar rápidamente la primera coincidencia presionando **Enter**.

#### Comportamiento Anterior:
1. Escribir parte del nombre del profesor
2. El filtro muestra coincidencias
3. Usar el mouse para hacer clic en la opción deseada
4. O usar las flechas y luego Enter

#### Comportamiento Nuevo:
1. Escribir parte del nombre del profesor
2. El filtro muestra coincidencias automáticamente
3. **Presionar Enter** → Selecciona automáticamente la primera coincidencia
4. La grilla se dibuja inmediatamente

#### Ejemplo de Uso:

**Escenario:** Tienes 10 profesores y buscas "García Martínez, Juan"

**Flujo anterior:**
1. Escribir "gar"
2. Ver lista filtrada: "García López, Ana", "García Martínez, Juan", etc.
3. Usar mouse o flechas para seleccionar "García Martínez, Juan"

**Flujo nuevo:**
1. Escribir "garcia m"
2. Ver que "García Martínez, Juan" es la primera coincidencia
3. **Presionar Enter** ✓
4. ¡Listo! Horario del profesor mostrado

#### Ventajas:
- ✅ **Más rápido**: No necesitas usar el mouse
- ✅ **Navegación por teclado**: Todo se hace sin soltar las manos del teclado
- ✅ **Eficiente**: Especialmente útil con listas largas de profesores
- ✅ **Intuitivo**: Comportamiento esperado al escribir y presionar Enter

#### Detalles Técnicos:

**Función implementada:**
```python
def seleccionar_primera_coincidencia(event=None):
    # Al presionar Enter, selecciona la primera coincidencia del filtro
    typed = self.cb_profesor_horario.get().lower()
    if typed:
        # Buscar coincidencias
        filtered = [p for p in self.profesores_lista_completa if typed in p.lower()]
        if filtered:
            # Seleccionar la primera coincidencia
            self.cb_profesor_horario.set(filtered[0])
            # Disparar el evento de selección
            on_profesor_selected()
            return 'break'  # Prevenir el comportamiento por defecto de Enter
```

**Binding agregado:**
```python
self.cb_profesor_horario.bind('<Return>', seleccionar_primera_coincidencia)
```

**Características:**
- Usa la misma lógica de filtrado que el autocompletado existente
- Dispara automáticamente el evento de selección para dibujar la grilla
- Retorna `'break'` para prevenir el comportamiento por defecto de Enter en el combobox

#### Compatibilidad:
- ✅ Funciona junto con el filtrado en tiempo real existente
- ✅ Compatible con la selección manual por mouse
- ✅ Compatible con navegación por flechas del teclado
- ✅ No interfiere con el autocompletado automático

**Archivos Modificados:**
- `Horarios_v0.9.py` (líneas 1850-1860 aproximadamente)

---

## Mejoras de Usabilidad: Atajos de Teclado y Ancho Dinámico del Combobox (Octubre 2025)

### Nuevas Funcionalidades en Combobox de Profesor

**Fecha:** 14 de octubre de 2025

Se implementaron tres mejoras significativas en el combobox de selección de profesor para una navegación más eficiente:

#### 1. Ancho Dinámico del Combobox

**Problema anterior:** El combobox tenía un ancho fijo, lo que podía hacer que nombres largos se cortaran o que hubiera mucho espacio vacío con nombres cortos.

**Solución:** El ancho del combobox ahora se ajusta automáticamente según la longitud del nombre del profesor seleccionado.

**Características:**
- 📏 **Ancho mínimo**: 20 caracteres
- 📏 **Ancho máximo**: 60 caracteres
- 🔄 **Ajuste automático**: Se actualiza al seleccionar un profesor
- 📐 **Fórmula**: `ancho = longitud_nombre + 5 caracteres`

**Beneficio:** Mejor aprovechamiento del espacio y visualización completa de los nombres.

#### 2. Tecla Esc: Limpiar y Enfocar

**Atajo:** `Esc`

**Funcionalidad:**
1. Borra completamente el contenido del combobox
2. Restablece el ancho al valor por defecto
3. Limpia la grilla de horarios
4. Mantiene el foco en el combobox
5. Resetea el estado de "profesor seleccionado"

**Uso:**
- Cuando quieres empezar a buscar otro profesor rápidamente
- Para limpiar una selección sin usar el mouse
- Útil para corregir rápidamente una búsqueda

**Ejemplo:**
```
Estado: "García Martínez, Juan" seleccionado
Acción: Presionar Esc (o Backspace)
Resultado: Campo vacío, listo para nueva búsqueda
```

#### 3. Teclas Esc y Backspace: Limpiar Campo

**Atajos:** `Esc` y `Backspace`

**Funcionalidad unificada:**
Ambas teclas realizan la misma acción: limpiar completamente el campo de búsqueda y preparar para una nueva búsqueda.

**Comportamiento:**
- Limpia completamente el campo de búsqueda
- Marca que no hay profesor seleccionado
- Ajusta el ancho del combobox al tamaño mínimo (20 caracteres)
- Reenfoca automáticamente el combobox
- Limpia la grilla de horarios
- Previene el comportamiento por defecto de las teclas

**Lógica:**
```python
def limpiar_y_enfocar(event=None):
    self.cb_profesor_horario.set('')
    self.profesor_seleccionado = False
    ajustar_ancho_combobox()
    self.cb_profesor_horario.focus_set()
    # Limpiar grilla
    for widget in self.frame_grilla_horario_prof.winfo_children():
        widget.destroy()
    return 'break'
```

**Uso típico:**
1. Seleccionas un profesor (Enter o clic)
2. Decides buscar otro
3. Presionas Esc o Backspace
4. El campo se limpia completamente
5. Puedes empezar a escribir otro nombre inmediatamente

**Ejemplo:**
```
Estado: "García Martínez, Juan" [SELECCIONADO]
Acción: Presionar Esc o Backspace
Resultado: Campo vacío, listo para nueva búsqueda
```

#### Flujo de Trabajo Optimizado

**Escenario: Cambiar rápidamente entre profesores**

**Método unificado:**
1. Profesor actual: "García López, Ana"
2. Presionar `Esc` o `Backspace`
3. Escribir nuevo nombre: "perez"
4. Presionar `Enter`
5. ✓ Nuevo profesor seleccionado

**Comparación con método anterior:**
- ❌ Antes: Clic en combobox → Ctrl+A → Delete → Escribir → Enter
- ✅ Ahora: Esc/Backspace → Escribir → Enter

#### Detalles Técnicos

**Función de ajuste de ancho:**
```python
def ajustar_ancho_combobox(nombre=''):
    if nombre:
        # Min 20, Max 60 caracteres
        ancho = max(20, min(len(nombre) + 5, 60))
    else:
        ancho = 20  # Ancho por defecto
    self.cb_profesor_horario.config(width=ancho)
```

**Función Esc/Backspace:**
```python
def limpiar_y_enfocar(event=None):
    # Al presionar Esc o Backspace, limpiar el combobox y enfocarlo
    self.cb_profesor_horario.set('')
    self.profesor_seleccionado = False
    ajustar_ancho_combobox()
    self.cb_profesor_horario.focus_set()
    # Limpiar grilla
    for widget in self.frame_grilla_horario_prof.winfo_children():
        widget.destroy()
    return 'break'
```

**Bindings agregados:**
```python
self.cb_profesor_horario.bind('<Escape>', limpiar_y_enfocar)
self.cb_profesor_horario.bind('<BackSpace>', limpiar_y_enfocar)
```

#### Resumen de Atajos de Teclado

| Tecla | Acción |
|-------|--------|
| **Enter** | Selecciona la primera coincidencia del filtro |
| **Esc** | Limpia el campo y mantiene el foco |
| **Backspace** | Limpia el campo y mantiene el foco |
| Escribir | Filtra en tiempo real |

#### Ventajas

- ✅ **Navegación 100% por teclado**: No necesitas el mouse
- ✅ **Más eficiente**: Menos teclas para cambiar de profesor
- ✅ **Ancho adaptativo**: Mejor uso del espacio en pantalla
- ✅ **Consistente**: Esc y Backspace hacen lo mismo
- ✅ **Productivo**: Ideal para uso frecuente

**Archivos Modificados:**
- `Horarios_v0.9.py`:
  - Líneas 1810-1817: Función `ajustar_ancho_combobox`
  - Líneas 1829-1843: Actualización de `on_turno_selected_prof`
  - Líneas 1845-1852: Actualización de `on_profesor_selected`
  - Líneas 1920-1930: Función `limpiar_y_enfocar` (Esc y Backspace)
  - Líneas 1950-1951: Bindings de teclas

---

## Mejora de UX: Label "Buscar Agente" con Tooltip Interactivo (Octubre 2025)

### Cambios Implementados

**Fecha:** 14 de octubre de 2025

Se realizaron dos mejoras en la interfaz de usuario para hacer más intuitiva la búsqueda de profesores:

#### 1. Cambio de Etiqueta: "Profesor:" → "Buscar agente:"

**Razón del cambio:**
- Más descriptivo de la funcionalidad (es un campo de búsqueda, no solo selección)
- Sugiere que se puede escribir para buscar
- Más acorde con la funcionalidad de filtrado en tiempo real

**Antes:**
```
Turno: [Combobox]  Profesor: [Combobox]
```

**Ahora:**
```
Turno: [Combobox]  Buscar agente: [Combobox]
```

#### 2. Tooltip Hover con Instrucciones de Uso

**Funcionalidad:**
Al pasar el mouse sobre el label "Buscar agente:", aparece un tooltip con instrucciones completas de uso.

**Contenido del tooltip:**
```
Buscar agente:
• Escribe para filtrar
• Enter: selecciona primera coincidencia
• Esc / Backspace: limpiar campo
```

**Características del tooltip:**
- ✅ Aparece al pasar el mouse (hover)
- ✅ Desaparece al quitar el mouse
- ✅ Fondo amarillo suave (#ffffe0) para visibilidad
- ✅ Borde sólido para definición
- ✅ Posicionado cerca del cursor
- ✅ Texto justificado a la izquierda con viñetas
- ✅ Padding adecuado para legibilidad

#### Implementación Técnica

**Clase ToolTip creada:**
```python
class ToolTip:
    """Crear un tooltip para un widget dado"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)
    
    def show_tip(self, event=None):
        # Muestra el tooltip en una ventana temporal
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + cy + self.widget.winfo_rooty() + 25
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify='left',
                        background="#ffffe0", relief='solid', borderwidth=1,
                        font=("Segoe UI", 9, "normal"), padx=8, pady=6)
        label.pack(ipadx=1)
    
    def hide_tip(self, event=None):
        # Oculta el tooltip
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None
```

**Uso en el código:**
```python
# Label "Buscar agente:" con tooltip
lbl_buscar = ttk.Label(frame_sel, text='Buscar agente:')
lbl_buscar.grid(row=0, column=2, padx=5)
ToolTip(lbl_buscar, 
        "Buscar agente:\n"
        "• Escribe para filtrar\n"
        "• Enter: selecciona primera coincidencia\n"
        "• Esc / Backspace: limpiar campo")
```

#### Ventajas de Usabilidad

- ✅ **Autodocumentado**: Los usuarios pueden ver cómo usar la búsqueda
- ✅ **Descubrimiento de funcionalidades**: Muestra atajos que el usuario podría no conocer
- ✅ **No invasivo**: Solo aparece cuando el usuario muestra interés (hover)
- ✅ **Rápido acceso a ayuda**: Sin necesidad de documentación externa
- ✅ **Mejora la curva de aprendizaje**: Usuarios nuevos aprenden rápidamente

#### Diseño Visual del Tooltip

**Apariencia:**
```
┌─────────────────────────────────────┐
│ Buscar agente:                      │
│ • Escribe para filtrar              │
│ • Enter: selecciona primera...     │
│ • Esc / Backspace: limpiar campo    │
└─────────────────────────────────────┘
```

**Estilo:**
- Fondo: Amarillo claro (#ffffe0)
- Borde: Sólido negro
- Fuente: Segoe UI, 9pt
- Padding: 8px horizontal, 6px vertical
- Alineación: Izquierda

#### Beneficios para el Usuario

1. **Primera vez usando el sistema**:
   - Pasa el mouse sobre "Buscar agente:"
   - Ve las instrucciones completas
   - Aprende todos los atajos de teclado

2. **Usuario olvidó un atajo**:
   - Hover rápido sobre el label
   - Recuerda la funcionalidad
   - Continúa trabajando eficientemente

3. **Capacitación de nuevos usuarios**:
   - No necesitan leer manuales
   - La interfaz les enseña cómo usarla
   - Menos tiempo de capacitación

**Archivos Modificados:**
- `Horarios_v0.9.py`:
  - Líneas 728-752: Nueva clase `ToolTip`
  - Líneas 1827-1835: Label "Buscar agente:" con tooltip

---

## Simplificación: Esc y Backspace con Funcionalidad Unificada (Octubre 2025)

### Cambio Implementado

**Fecha:** 14 de octubre de 2025

Se simplificó el comportamiento de las teclas Esc y Backspace para que realicen la misma acción.

#### Razón del Cambio

**Problema identificado:**
Durante las pruebas de usabilidad, se detectó que las funcionalidades de Esc y Backspace eran prácticamente idénticas en la práctica. La diferenciación entre "borrado condicional" (Backspace) y "limpiar siempre" (Esc) añadía complejidad innecesaria sin beneficio tangible.

**Solución:**
Unificar ambas teclas para que realicen exactamente la misma acción: limpiar completamente el campo de búsqueda.

#### Cambios Técnicos

**Antes:**
```python
# Dos funciones separadas con lógica diferente
def limpiar_y_enfocar(event=None):
    # Esc: limpiar siempre
    ...

def borrar_completo(event=None):
    # Backspace: condicional según estado
    if self.profesor_seleccionado and self.cb_profesor_horario.get():
        # Borrar todo
        ...
    else:
        # Permitir borrado normal
        self.profesor_seleccionado = False

# Bindings diferentes
self.cb_profesor_horario.bind('<Escape>', limpiar_y_enfocar)
self.cb_profesor_horario.bind('<BackSpace>', borrar_completo)
```

**Ahora:**
```python
# Una sola función para ambas teclas
def limpiar_y_enfocar(event=None):
    # Al presionar Esc o Backspace, limpiar el combobox y enfocarlo
    self.cb_profesor_horario.set('')
    self.profesor_seleccionado = False
    ajustar_ancho_combobox()
    self.cb_profesor_horario.focus_set()
    # Limpiar la grilla
    for widget in self.frame_grilla_horario_prof.winfo_children():
        widget.destroy()
    return 'break'

# Ambas teclas vinculadas a la misma función
self.cb_profesor_horario.bind('<Escape>', limpiar_y_enfocar)
self.cb_profesor_horario.bind('<BackSpace>', limpiar_y_enfocar)
```

#### Ventajas de la Simplificación

1. **Menos código**: Eliminada función `borrar_completo` completa (~14 líneas)
2. **Más predecible**: Ambas teclas hacen exactamente lo mismo
3. **Más simple de documentar**: Una sola acción para dos teclas
4. **Menos carga cognitiva**: El usuario no necesita recordar cuál tecla usar
5. **Más eficiente**: Menor complejidad de mantenimiento

#### Tooltip Actualizado

**Antes:**
```
• Esc: limpiar campo
• Backspace: borrar todo (si seleccionado)
```

**Ahora:**
```
• Esc / Backspace: limpiar campo
```

**Resultado:** Más conciso y claro.

#### Beneficios para el Usuario

- ✅ **Intuitivo**: Cualquiera de las dos teclas funciona igual
- ✅ **Flexible**: Usa la tecla que prefieras
- ✅ **Rápido**: Menos tiempo pensando qué tecla usar
- ✅ **Consistente**: Comportamiento predecible

**Archivos Modificados:**
- `Horarios_v0.9.py`:
  - Líneas 1920-1930: Función `limpiar_y_enfocar` actualizada (comentario modificado)
  - Líneas 1950-1951: Ambos bindings apuntan a la misma función
  - Eliminadas: ~14 líneas de la función `borrar_completo`
  - Líneas 1835-1840: Tooltip actualizado
- `DOCUMENTACION_CAMBIOS.md`:
  - Sección "Tecla Backspace" actualizada a "Teclas Esc y Backspace"
  - Resumen de atajos actualizado
  - Tooltip documentación actualizada

---

