# GUÍA PARA DESARROLLADORES - LECTURA Y NAVEGACIÓN
## SistemaEscolar_v1.py Versión 1.0 Documentada

---

## 📋 TABLA DE CONTENIDOS RÁPIDA

### Por Tema

**Autenticación y Seguridad**
- Línea ~1750: Funciones de usuario y password
- Línea ~2025: Pantalla de login
- Línea ~6380: Gestión de usuarios (admin)

**Base de Datos - CRUD por Entidad**
- Materias: Línea 770
- Profesores: Línea 848
- Ciclos: Línea 1118
- Turnos: Línea ~1210
- Divisiones: Línea ~1306
- Horarios: Línea ~1427

**Interfaz Gráfica (GUI)**
- Clase App: Línea 1987
- Materias View: Línea 2257
- Personal y Ciclos: Línea 2540
- Horarios por Curso: Línea 3864
- Horarios por Profesor: Línea 4294
- Usuarios (Admin): Línea 6375

**Utilidades**
- Exportación a Excel: Línea ~350
- Respaldos (Backups): Línea ~1600
- Estilos GUI: Línea ~1950

---

## 🔍 CÓMO ENCONTRAR LO QUE NECESITAS

### Buscar por Nombre de Función
```
Ctrl+F para abrir búsqueda
Escribe: obtener_materias
```

### Buscar por Sección
Las secciones principales están marcadas con:
```
# ═══════════════════════════════════════════════════════════════════════════════
# N. NOMBRE DE LA SECCIÓN
```

Usa búsqueda: `# ═════` para ver todas las secciones.

### Buscar por Módulo de Refactorización
Todas las funciones incluyen notas como:
```
Candidato para: database/materias.py
```

Busca por nombre de archivo propuesto (ej: `materias.py`)

---

## 📚 ESTRUCTURA DE DOCSTRINGS

Cada función importante tiene un docstring con este formato:

```python
def crear_materia(nombre: str, horas: int):
    """
    Crear una nueva materia en el sistema.
    
    Parámetros:
        nombre (str): Nombre de la materia
        horas (int): Horas semanales
        
    Retorna:
        None (pero confirma cambios en BD)
        
    Lanza:
        Exception: Si ya existe una materia con ese nombre
        
    Dependencias:
        - Tabla: materia
        - Requerida por: crear_ciclo, mostrar_materias
        
    Candidato para: database/materias.py
    """
```

**Siempre revisa**:
1. **Parámetros** - Qué debes pasar
2. **Retorna** - Qué obtendrás
3. **Lanza** - Qué excepciones puede lanzar
4. **Dependencias** - De qué depende
5. **Candidato para** - Dónde va en version 2.0

---

## 🏗️ ARQUITECTURA DEL SISTEMA

```
┌─────────────────────────────────────────────┐
│  INTERFAZ GRÁFICA (Tkinter - GUI)           │
│  - Clase App (línea 1987)                   │
│  - 10 vistas principales (mostrar_*)        │
│  - Métodos privados para eventos            │
└──────────────┬──────────────────────────────┘
               │ Usa
               ↓
┌─────────────────────────────────────────────┐
│  FUNCIONES DE BASE DE DATOS                 │
│  - CRUD Materias (línea 770)                │
│  - CRUD Profesores (línea 848)              │
│  - CRUD Ciclos (línea 1118)                 │
│  - Etc...                                   │
└──────────────┬──────────────────────────────┘
               │ Usa
               ↓
┌─────────────────────────────────────────────┐
│  CONEXIÓN Y DECORADORES                     │
│  - obtener_conexion() (línea 135)           │
│  - @operacion_bd decorator (línea 160)      │
│  - Funciones genéricas CRUD (línea 205)     │
└──────────────┬──────────────────────────────┘
               │ Usa
               ↓
┌─────────────────────────────────────────────┐
│  SQLITE3 BASE DE DATOS                      │
│  - institucion.db (en mismo directorio)     │
│  - 15+ tablas relacionales                  │
└─────────────────────────────────────────────┘
```

---

## 📖 LECTURA RECOMENDADA POR NIVEL

### Principiante (Primeras 500 líneas)
1. Encabezado y glosario (línea 1-80)
2. Funciones de inicialización (línea 95-160)
3. Funciones genéricas CRUD (línea 205-285)
4. Constantes (línea 340-360)

**Objetivo**: Entender cómo funciona la BD

### Intermedio (500-2000 líneas)
1. Módulos CRUD por entidad (línea 770-1600)
2. Autenticación (línea 1750-1900)
3. Clase App (línea 1987-2050)

**Objetivo**: Entender operaciones de negocio

### Avanzado (2000+ líneas)
1. Vistas GUI (línea 2257-6700)
2. Métodos privados de cada vista
3. Diálogos modales y validaciones

**Objetivo**: Entender flujo de usuario completo

---

## 🔗 DEPENDENCIAS CRÍTICAS

**Siempre ejecutar primero:**
```python
init_db()  # Crea tablas si no existen
```

**Base para todo:**
```python
@operacion_bd  # Decorador - maneja conexión automáticamente
def mi_funcion(conn, ...):
    pass
```

**Más usado:**
- `obtener_conexion()` - Abre conexión
- `crear_entidad()` - INSERT genérico
- `obtener_entidades()` - SELECT genérico
- `actualizar_entidad()` - UPDATE genérico
- `eliminar_entidad()` - DELETE genérico

---

## 🚀 CÓMO AÑADIR UNA NUEVA CARACTERÍSTICA

### Ejemplo: Añadir nuevo atributo a Materia

1. **Identificar línea de CRUD Materia** (línea 770)
2. **Entender estructura actual** de `crear_materia()`
3. **Copiar patrón** de docstring y parámetros
4. **Añadir a tabla** en `init_db()` (línea ~350)
5. **Actualizar funciones CRUD** de materias
6. **Actualizar GUI** en `mostrar_materias()` (línea 2257)
7. **Probar** cambios

---

## ⚠️ COSAS A TENER CUIDADO

### 1. Cambios en Base de Datos
Si modificas tabla, **debes**:
- Actualizar `init_db()`
- Pasar BD antigua si existe (sqlite3 no migra automáticamente)
- Considerar bacups

### 2. Restricciones de Clave Foránea
Están ACTIVAS (`PRAGMA foreign_keys = ON`):
- No puedes eliminar profesor si tiene horarios asignados
- Verifica `contar_dependencias_*()` antes de eliminar

### 3. Nombres en Español
Todo debe estar en español para coherencia:
- Variables: `nombre_profesor`, no `teacher_name`
- Funciones: `crear_materia()`, no `create_subject()`
- Comentarios: En español

### 4. Compatibilidad hacia Atrás
Si cambias nombres, mantén aliases:
```python
# Nuevo nombre
def obtener_ruta_base():
    ...

# Alias para compatibilidad
get_base_path = obtener_ruta_base
```

---

## 🎯 PARA LA REFACTORIZACIÓN (version 2.0)

### Usa estos archivos como guía:
1. **MAPA_ESTRUCTURA_REFACTORIZACION.md** - Qué extraer y dónde
2. **RESUMEN_DOCUMENTACION.md** - Qué se hizo en esta versión

### Orden recomendado de extracción:
1. `database/base.py` - Conexión y decorador
2. `database/crud.py` - Genéricos
3. `database/materias.py` - CRUD materias
4. ... continuar con otros módulos

### Mantén el nombre:
`SistemaEscolar_v1.py` es la **referencia documentada**  
`SistemaEscolar_v2.0/` será la **versión modular**

---

## 💡 TIPS DE PROGRAMACIÓN

### Usar Búsqueda Efectivamente
```
Ctrl+F: "Candidato para: database/materias.py"
Te muestra TODO relacionado con materias
```

### Saltar a Definición
La mayoría de editores permiten:
```
Ctrl+Click en función
O: F12 (Go to Definition)
```

### Buscar Usos de Función
```
Ctrl+Shift+F: "crear_materia"
Muestra dónde se llama esta función
```

### Ver Estructura
Muchos editores tienen:
- Outline (Esquema) que muestra todas las funciones
- Breadcrumb que muestra ubicación actual
- Symbol search (Ctrl+T) para saltar a función

---

## 📞 PREGUNTAS FRECUENTES

**P: ¿Dónde está la función X?**  
R: Usa `Ctrl+F` para buscar. Todos los nombres están documentados.

**P: ¿Cómo agrego una nueva materia?**  
R: Llama `crear_materia("Nombre", 4)`. Ver línea 770.

**P: ¿Por qué funciona con "get_base_path" si cambió el nombre?**  
R: Hay aliases de compatibilidad (línea ~131).

**P: ¿Cómo elimino un ciclo?**  
R: Usa `eliminar_ciclo(id)` con `cascade=True` si hay divisiones.

**P: ¿Dónde está la lógica de validación de horarios?**  
R: Búsqueda "validar" o línea ~1450. Mira `validar_conflictos_horario()`.

---

## 📝 CONVENCIONES DEL CÓDIGO

- **Funciones públicas**: `obtener_materias()` (sin prefijo `_`)
- **Funciones privadas**: `_recargar_materias_tree()` (con prefijo `_`)
- **Constantes**: `HORARIO_DIAS_BASE`, `ESPACIOS_POR_DEFECTO`
- **Clases**: `App`, `ToolTip` (CapitalCase)
- **Variables**: `materias_seleccionadas` (snake_case)

---

## 🎓 PRÓXIMOS PASOS

1. Lee el **encabezado** del archivo (primeras 80 líneas)
2. Lee **MAPA_ESTRUCTURA_REFACTORIZACION.md** para contexto completo
3. Busca la sección que te interesa
4. Lee docstrings para entender qué hace cada función
5. Usa búsqueda para encontrar dónde se llama cada función

---

**¡Bienvenido al código documentado! Espero que esta guía te ayude a navegarlo efectivamente.**

