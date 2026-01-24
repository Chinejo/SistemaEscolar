# MAPA DE ESTRUCTURA PARA REFACTORIZACIÓN
## SistemaEscolar_v1.py - Documento de Guía

**Fecha**: Enero 2026  
**Versión**: 1.0 - Monolito Documentado  
**Propósito**: Este documento guía la extracción de módulos del monolito hacia la estructura modular en version 2.0

---

## ÍNDICE DE CONTENIDOS

El archivo está estructurado en 24 secciones principales marcadas con comentarios `# ═══════...`:

### SECCIONES DE BASE DE DATOS (Líneas ~1-1800)

1. **Inicialización de BD y Conexión** (Líneas 95-145)
   - `obtener_ruta_base()` - Detecta ruta base (PyInstaller vs Script)
   - `obtener_conexion()` - Crea conexión SQLite con configuración segura
   - `operacion_bd` decorator - Automatiza conexión, commit y cierre

2. **Funciones Genéricas CRUD** (Líneas 205-285)
   - `crear_entidad()` - INSERT genérico
   - `obtener_entidades()` - SELECT genérico
   - `actualizar_entidad()` - UPDATE genérico
   - `eliminar_entidad()` - DELETE genérico
   - **Candidato para**: `database/crud.py` o `database/base.py`

3. **Constantes y Configuración Global** (Líneas 340-360)
   - `HORARIO_DIAS_BASE` - Días de la semana disponibles
   - `ESPACIOS_POR_DEFECTO` - Número de franjas horarias (8 default)
   - `_HOJA_CARACTERES_INVALIDOS` - Caracteres inválidos en Excel

4. **Módulo: Gestión de Materias** (Líneas 770-840)
   - `crear_materia(nombre, horas)`
   - `obtener_materias()` → Dict[id, nombre, horas_semanales]
   - `actualizar_materia(id, nombre, horas)`
   - `eliminar_materia(id)`
   - **Candidato para**: `database/materias.py`

5. **Módulo: Gestión de Profesores** (Líneas 848-915)
   - `crear_profesor(nombre)`
   - `obtener_profesores()` → Dict[id, nombre]
   - `actualizar_profesor(id, nombre)`
   - `eliminar_profesor(id)` - Con cascade DELETE en profesor_turno
   - **Candidato para**: `database/profesores.py`

6. **Módulo: Profesor-Turno** (Líneas 917-1000)
   - `asignar_turno_a_profesor(profesor_id, turno_id)`
   - `quitar_turno_a_profesor(profesor_id, turno_id)`
   - `obtener_turnos_de_profesor(profesor_id)` - JOIN con tabla turno
   - `obtener_profesores_por_turno(turno_id)` - JOIN inverso
   - `obtener_profesor_turnos()` - Todas las combinaciones
   - **Candidato para**: `database/profesor_turno.py`

7. **Módulo: Banca de Horas** (Líneas 1037-1110)
   - `asignar_banca_profesor(profesor_id, materia_id, banca_horas)`
   - `obtener_banca_profesor(profesor_id)` - Materias que enseña
   - `actualizar_banca_profesor(pm_id, banca_horas)`
   - `eliminar_banca_profesor(pm_id)`
   - **Candidato para**: `database/profesor_materia.py`

8. **Módulo: Gestión de Ciclos** (Líneas 1118-1350)
   - `crear_ciclo(nombre, plan_ids)` - Crear ciclo con planes asociados
   - `actualizar_ciclo(id, nombre, plan_ids)` - Actualizar con validaciones
   - `obtener_ciclos(plan_id)` - Ciclos de un plan
   - `obtener_ciclos_con_planes()` - Árbol completo ciclo→planes
   - `obtener_planes_de_ciclo(ciclo_id)`
   - `contar_dependencias_ciclo(ciclo_id)` - Verificar divisiones/horarios
   - `eliminar_ciclo(id, cascade=False)` - Con opción de cascade delete
   - **Candidato para**: `database/ciclos.py`

9. **Módulo: Ciclo-Materia** (Líneas ~1380-1430)
   - `agregar_materia_a_ciclo()`
   - `eliminar_materia_de_ciclo()`
   - `obtener_materias_de_ciclo(ciclo_id)`
   - **Candidato para**: `database/ciclo_materia.py`

10. **Módulo: Planes de Estudio** (Líneas ~1450-1550)
    - `crear_plan(nombre)`
    - `obtener_planes()`
    - `eliminar_plan(id)`
    - **Candidato para**: `database/planes.py`

11. **Módulo: Turnos** (Líneas ~1210-1300)
    - `crear_turno(nombre)`
    - `obtener_turnos()`
    - `actualizar_turno(id, nombre)`
    - `eliminar_turno(id)`
    - **Candidato para**: `database/turnos.py`

12. **Módulo: Divisiones** (Líneas ~1306-1400)
    - `crear_division(ciclo_id, plan_id, nombre)`
    - `obtener_divisiones(ciclo_id)`
    - `actualizar_division(id, nombre)`
    - `eliminar_division(id)`
    - **Candidato para**: `database/divisiones.py`

13. **Módulo: Horarios** (Líneas ~1427-1550)
    - `crear_horario(division_id, turno_id, dia, espacio, profesor_id, materia_id)`
    - `obtener_horarios(division_id)`
    - `obtener_horarios_por_profesor(profesor_id)`
    - `eliminar_horario(id)`
    - `validar_conflictos_horario()` - Importante para lógica de negocio
    - **Candidato para**: `database/horarios.py` + `controllers/validacion_horarios.py`

14. **Módulo: Turno-Espacio-Hora** (Líneas ~1500-1550)
    - `asignar_espacios_turno()`
    - `obtener_espacios_turno()`
    - **Candidato para**: `database/turno_espacios.py`

### SECCIONES DE UTILIDADES (Líneas ~1600-1900)

15. **Funciones de Exportación a Excel** (Líneas ~350-700)
    - `_obtener_dias_para_export()` - Consulta BD para días usados
    - `_obtener_max_espacios_para_export()` - Espacios máximos
    - `_sanitizar_nombre_hoja_excel()` - Limpia caracteres inválidos
    - Múltiples funciones de `_armar_*.py` para construir hojas
    - `exportar_horarios()` - Función principal de exportación
    - **Candidato para**: `utils/exportar_excel.py`

16. **Función Inicialización BD** (Líneas ~730-765)
    - `init_db()` - Crea todas las tablas si no existen
    - Define esquema completo con restricciones FK
    - **Candidato para**: `database/schema.py` o `database/init.py`

17. **Módulo: Respaldos (Backups)** (Líneas ~1600-1700)
    - `crear_backup(tipo="manual")`
    - `obtener_backups()`
    - `restaurar_backup(ruta_backup)`
    - `eliminar_backup(ruta_backup)`
    - **Candidato para**: `utils/respaldos.py`

18. **Módulo: Gestión de Usuarios del Sistema** (Líneas ~1750-1900)
    - `hashear_password(password)` - SHA256
    - `validar_usuario(usuario, password)` - Autenticación
    - `crear_usuario(usuario, password, es_admin=False)`
    - `obtener_usuarios()`
    - `eliminar_usuario(usuario)`
    - `hay_usuarios()` - Verifica si hay admin creado
    - `cambiar_password(usuario, password_vieja, password_nueva)`
    - **Candidato para**: `database/usuarios.py` + `auth/autenticacion.py`

19. **Clases y Utilidades GUI** (Líneas ~1950-1985)
    - `ToolTip` class - Tooltips personalizados
    - `aplicar_estilos_ttk()` - Configuración de estilos ttk
    - `crear_treeview()` - Helper para crear TreeView con scrollbars
    - `recargar_treeview()` - Actualiza datos en TreeView
    - `smart_combobox_autocomplete()` - Autocomplete en combobox
    - **Candidato para**: `gui/components.py` + `gui/estilos.py`

### SECCIÓN PRINCIPAL DE APLICACIÓN (Líneas ~1987-6829)

20. **Clase App: Principal** (Líneas 1987-2200)
    - `App` class hereda de `tk.Tk`
    - `__init__()` - Inicialización, check de usuarios, login
    - `_configurar_admin_inicial()` - Setup primer uso
    - `_mostrar_login()` - Pantalla de login
    - `_crear_menu_barrar()` - Barra de menú principal
    - `_crear_frame_principal()` - Frame para contenido dinámico
    - `limpiar_frame()` - Limpia y resetea frame principal
    - **Candidato para**: `gui/app.py` + `controllers/app_controller.py`

### SUBMÓDULOS DE LA CLASE App (Líneas 2257-6829)

21. **Módulo App: Gestión de Materias** (Líneas ~2257-2524)
    - `mostrar_materias()` - Vista principal de materias
    - `_recargar_materias_tree()` - Actualiza tabla
    - `_agregar_materia()` - Handler para crear
    - `_editar_materia()` - Handler para editar
    - `_eliminar_materia()` - Handler para eliminar
    - `_asignar_materias_a_plan()` - Diálogo para asignar a planes
    - `_on_select_materia()` - Handler de selección en tabla
    - **Candidato para**: `views/materias_view.py` + `controllers/materias_controller.py`

22. **Módulo App: Personal y Ciclos** (Líneas ~2540-3200)
    - `mostrar_personal_ciclos()` - Pantalla principal con 3 tabs
    - **Tab: Personal**
      - Tabla de profesores
      - Asignación de turnos (checkboxes)
      - Gestión de banca de horas
    - **Tab: Ciclos**
      - Tabla de ciclos
      - Diálogos para crear/editar ciclos
      - Asociación con planes
    - **Tab: Divisiones**
      - Tabla de divisiones por ciclo
      - Formulario de alta
    - **Candidato para**: `views/personal_view.py`, `views/ciclos_view.py`, `views/divisiones_view.py`

23. **Módulo App: Divisiones** (Líneas ~3200-3850)
    - `mostrar_divisiones()` - Gestión de divisiones
    - Filtro por ciclo
    - CRUD operations
    - **Candidato para**: `views/divisiones_view.py`

24. **Módulo App: Horarios por Curso** (Líneas ~3864-4290)
    - `mostrar_horarios_ciclo()` - Grilla de horarios por curso
    - Visualización de profesor-materia en división
    - Editor modal para cambiar asignaciones
    - Validación de conflictos
    - **Candidato para**: `views/horarios_curso_view.py`

25. **Módulo App: Horarios por Profesor** (Líneas ~4294-5070)
    - `mostrar_horarios_profesor()` - Grilla por profesor
    - Similar a horarios por curso pero agrupa diferente
    - **Candidato para**: `views/horarios_profesor_view.py`

26. **Módulo App: Configuración de Horas** (Líneas ~5077-5380)
    - Configuración de franjas horarias por turno
    - Editor modal
    - Aplicación masiva
    - **Candidato para**: `views/configuracion_horas_view.py`

27. **Módulo App: Turnos, Planes y Materias** (Líneas ~5390-5920)
    - `mostrar_turnos_planes_materias()` - Vista unificada
    - 3 tabs: Turnos, Planes, Materias
    - Cada uno con CRUD
    - **Candidato para**: `views/turnos_planes_view.py`

28. **Módulo App: Exportación** (Líneas ~5950-6360)
    - Múltiples funciones `exportar_*_a_excel()`
    - Diálogos de selección de datos
    - Llamadas a funciones de `utils/exportar_excel.py`
    - **Candidato para**: `controllers/exportacion_controller.py`

29. **Módulo App: Gestión de Usuarios** (Líneas ~6375-6700)
    - `mostrar_gestion_usuarios()` - Admin panel
    - Crear/eliminar usuarios
    - Cambiar permisos
    - `cambiar_mi_password()` - Para usuario actual
    - `cerrar_sesion()` - Logout
    - **Candidato para**: `views/usuarios_view.py` + `controllers/usuarios_controller.py`

30. **Módulo App: Respaldos** (Líneas ~6717-6829)
    - `crear_backup_manual()` - Triguer manual de backup
    - `mostrar_lista_backups()` - Gestión de backups
    - `_recargar_backups_tree()` - Actualiza lista
    - Opciones para restaurar/eliminar
    - **Candidato para**: `views/respaldos_view.py`

---

## PUNTO DE ENTRADA (Línea ~6850)

```python
if __name__ == "__main__":
    init_db()
    app = App()
    app.mainloop()
```

---

## ESTRUCTURA PROPUESTA PARA VERSION 2.0

Basado en la documentación anterior, la estructura modular debería ser:

```
SistemaEscolar_v2.0/
├── main.py                          # Punto de entrada
├── config.py                         # Configuración global
│
├── database/
│   ├── __init__.py
│   ├── conexion.py                  # obtener_conexion(), operacion_bd decorator
│   ├── schema.py                    # init_db(), definición de tablas
│   ├── crud.py                      # crear_entidad, obtener_entidades, etc
│   ├── materias.py                  # CRUD Materias
│   ├── profesores.py                # CRUD Profesores
│   ├── profesor_turno.py            # Relación profesor-turno
│   ├── profesor_materia.py          # Banca de horas
│   ├── ciclos.py                    # CRUD Ciclos
│   ├── ciclo_materia.py             # Relación ciclo-materia
│   ├── planes.py                    # CRUD Planes
│   ├── turnos.py                    # CRUD Turnos
│   ├── divisiones.py                # CRUD Divisiones
│   ├── horarios.py                  # CRUD Horarios
│   ├── turno_espacios.py            # Config de espacios por turno
│   └── usuarios.py                  # CRUD Usuarios
│
├── auth/
│   ├── __init__.py
│   └── autenticacion.py             # Validación, hashing, login
│
├── controllers/
│   ├── __init__.py
│   ├── validacion_horarios.py       # Lógica de conflictos
│   ├── exportacion_controller.py    # Control de exportación
│   └── usuarios_controller.py       # Control de usuarios
│
├── utils/
│   ├── __init__.py
│   ├── exportar_excel.py            # Funciones de Excel
│   └── respaldos.py                 # Gestión de backups
│
├── gui/
│   ├── __init__.py
│   ├── app.py                       # Clase App principal
│   ├── estilos.py                   # Estilos ttk, colores
│   ├── components.py                # ToolTip, TreeView helpers
│   │
│   └── views/
│       ├── __init__.py
│       ├── login_view.py            # Pantalla de login
│       ├── materias_view.py         # Gestión de materias
│       ├── personal_view.py         # Gestión de profesores
│       ├── ciclos_view.py           # Gestión de ciclos
│       ├── divisiones_view.py       # Gestión de divisiones
│       ├── horarios_curso_view.py   # Horarios por curso
│       ├── horarios_profesor_view.py# Horarios por profesor
│       ├── configuracion_horas_view.py
│       ├── turnos_planes_view.py    # Turnos, planes, materias
│       ├── usuarios_view.py         # Gestión de usuarios (admin)
│       └── respaldos_view.py        # Gestión de backups
│
└── tests/
    └── test_database.py
```

---

## NOTAS IMPORTANTES PARA LA REFACTORIZACIÓN

### 1. **Dependencias Críticas**
- `init_db()` debe ejecutarse primero (antes de cualquier operación)
- `obtener_conexion()` es usado por todas las funciones CRUD
- El decorador `operacion_bd` es fundamental para auto-commit

### 2. **Patrón de Transacciones**
Muchas funciones usan `@operacion_bd` que:
- Abre conexión
- Ejecuta función
- Hace commit automático
- Cierra conexión

Al refactorizar, mantener este patrón.

### 3. **Validaciones de Integridad Referencial**
- `ciclo` requiere `plan_ciclo` y `plan_estudio`
- `division` requiere `ciclo`
- `horario` requiere `division`, `profesor`, `materia`, `turno`
- Cuidado con eliminaciones en cascade

### 4. **Tabla de Hechos: horario**
La tabla `horario` es central:
```
horario(
  id, 
  division_id (FK), 
  turno_id (FK),
  dia, 
  espacio,
  profesor_id (FK),
  materia_id (FK)
)
```

Esta tabla cruza división, turno, profesor y materia.

### 5. **Métodos Privados (`_`) vs Públicos**
- `mostrar_*()` - Métodos públicos que renderean vistas
- `_*()` - Métodos privados (handlers, helpers)
- Considerar helpers comunes en `components.py`

### 6. **TODO REFACTOR Comments**
Se han marcado con comentarios `# TODO REFACTOR:` varias oportunidades:
- Código duplicado entre `_recargar_*_tree()` → Factory pattern
- Diálogos modales similares → Template pattern
- Validaciones repetidas → Extracted validators

---

## CHECKLIST PARA REFACTORIZACIÓN

- [ ] Extraer `database/` con todos los módulos CRUD
- [ ] Crear `gui/views/` con cada vista principal
- [ ] Implementar factory para TreeView + reload pattern
- [ ] Centralizar validaciones de horarios en `controllers/`
- [ ] Extraer Excel en `utils/exportar_excel.py`
- [ ] Implementar autenticación en `auth/`
- [ ] Crear `config.py` centralizado
- [ ] Implementar logging
- [ ] Escribir tests unitarios para CRUD
- [ ] Actualizar imports en punto de entrada

---

**Fin del documento**
