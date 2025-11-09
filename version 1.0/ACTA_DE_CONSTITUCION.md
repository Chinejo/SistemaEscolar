# ACTA DE CONSTITUCIÓN DEL PROYECTO
## Sistema de Gestión de Horarios Escolares

---

## 1. INFORMACIÓN GENERAL DEL PROYECTO

### 1.1 Identificación del Proyecto
- **Nombre del Proyecto:** Sistema de Gestión de Horarios Escolares
- **Versión Actual:** 0.9
- **Fecha de Inicio:** 2024
- **Fecha del Acta:** 8 de Noviembre de 2025
- **Propietario del Proyecto:** Institución Educativa
- **Jefe del Proyecto:** [Nombre del responsable]
- **Patrocinador:** [Nombre de la institución]

### 1.2 Clasificación del Proyecto
- **Categoría:** Sistema de Información Educativa
- **Tipo:** Aplicación de Escritorio
- **Alcance:** Institucional
- **Criticidad:** Media-Alta

---

## 2. PROPÓSITO Y JUSTIFICACIÓN DEL PROYECTO

### 2.1 Propósito
Desarrollar e implementar un sistema informático integral para la gestión automatizada de horarios escolares, que permita planificar, asignar y controlar los horarios de clases, profesores, materias y divisiones de la institución educativa.

### 2.2 Justificación del Proyecto

#### Situación Actual (Problemática)
La institución educativa mantiene actualmente toda la información relacionada con horarios escolares en formato papel, lo que genera:

- **Problemas de Accesibilidad:** Dificultad para consultar información rápidamente
- **Riesgo de Pérdida:** Documentos físicos susceptibles a deterioro o extravío
- **Redundancia de Datos:** Información duplicada en múltiples documentos
- **Errores Manuales:** Superposición de horarios, asignación incorrecta de profesores
- **Dificultad de Actualización:** Cambios requieren reescribir documentos completos
- **Falta de Trazabilidad:** Sin historial de cambios o versiones anteriores
- **Coordinación Compleja:** Difícil visualizar disponibilidad de profesores y aulas
- **Tiempo Excesivo:** Horas dedicadas a organización manual de horarios

#### Beneficios Esperados
- ✅ **Modernización Institucional:** Transición de procesos manuales a digitales
- ✅ **Eficiencia Operativa:** Reducción del tiempo dedicado a gestión de horarios
- ✅ **Reducción de Errores:** Validaciones automáticas previenen conflictos
- ✅ **Acceso Rápido:** Consulta inmediata de información
- ✅ **Integridad de Datos:** Información centralizada y respaldada
- ✅ **Flexibilidad:** Facilidad para realizar cambios y ajustes
- ✅ **Trazabilidad:** Historial de cambios y versiones
- ✅ **Mejor Planificación:** Visualización integral de recursos

---

## 3. OBJETIVOS DEL PROYECTO

### 3.1 Objetivo General
Modernizar la gestión de horarios escolares mediante el desarrollo e implementación de un sistema informático que permita administrar de manera eficiente y centralizada todos los aspectos relacionados con la planificación académica de la institución.

### 3.2 Objetivos Específicos

1. **Gestión de Planes de Estudio**
   - Crear y mantener planes de estudio con sus materias asociadas
   - Organizar materias por año académico
   - Gestionar horas semanales por materia

2. **Gestión de Recursos Humanos**
   - Administrar información del personal docente
   - Asignar materias a profesores (banca de horas)
   - Controlar disponibilidad horaria de profesores por turno

3. **Gestión de Estructura Académica**
   - Administrar turnos escolares (mañana, tarde, noche)
   - Gestionar divisiones/cursos por turno, plan y año
   - Configurar horarios estándar por turno

4. **Gestión de Horarios**
   - Asignar horarios por división/curso
   - Asignar horarios por profesor
   - Validar automáticamente conflictos de horarios
   - Sincronización bidireccional entre vistas

5. **Interfaz de Usuario**
   - Proporcionar interfaz gráfica intuitiva
   - Implementar funcionalidad CRUD completa
   - Ofrecer múltiples vistas de la información

---

## 4. ALCANCE DEL PROYECTO

### 4.1 Dentro del Alcance

#### Funcionalidades Incluidas

**Gestión de Materias/Obligaciones:**
- Alta, baja, modificación y consulta de materias
- Control de horas semanales asignadas
- Filtros de búsqueda
- Contadores totales de materias y horas

**Gestión de Personal Docente:**
- Alta, baja, modificación y consulta de profesores
- Asignación de banca de horas por materia
- Asignación de turnos a profesores
- Filtros por turno y nombre

**Gestión de Planes de Estudio:**
- Creación de planes de estudio
- Asignación de materias al plan
- Gestión de años/cursos por plan
- Asignación de materias a años específicos

**Gestión de Turnos:**
- Creación de turnos escolares
- Asignación de planes a turnos
- Configuración de horarios estándar por turno

**Gestión de Divisiones/Cursos:**
- Alta y baja de divisiones
- Organización por turno, plan y año
- Filtros de búsqueda
- Edición de información

**Gestión de Horarios:**
- Vista por curso/división (grilla semanal)
- Vista por profesor (grilla semanal)
- Asignación de materia, profesor y horario por espacio
- Validación de conflictos
- Configuración de horas por turno
- Limpieza de horarios vacíos
- Sincronización automática entre vistas

**Características Técnicas:**
- Base de datos SQLite local
- Interfaz gráfica con Tkinter
- Validaciones de integridad
- Sistema de tooltips de ayuda
- Navegación por teclado
- Autocompletado inteligente

### 4.2 Fuera del Alcance

Lo siguiente NO está incluido en el alcance actual:

- ❌ Gestión de alumnos y matrículas
- ❌ Control de asistencia
- ❌ Sistema de calificaciones
- ❌ Comunicación con padres
- ❌ Reportes estadísticos complejos
- ❌ Integración con otros sistemas
- ❌ Aplicación móvil
- ❌ Acceso web/en línea
- ❌ Sistema multi-usuario con permisos
- ❌ Gestión de aulas físicas
- ❌ Reserva de recursos (proyectores, laboratorios)
- ❌ Exportación a formatos avanzados (PDF, Excel)
- ❌ Notificaciones automáticas
- ❌ Sincronización en la nube

---

## 5. ENTREGABLES DEL PROYECTO

### 5.1 Entregables de Software

1. **Aplicación Ejecutable**
   - Archivo `.exe` para Windows
   - Base de datos SQLite integrada
   - Sin necesidad de instalación de dependencias

2. **Base de Datos**
   - Esquema completo de base de datos
   - Tablas con relaciones definidas
   - Sistema de migraciones

3. **Código Fuente**
   - Código Python completo
   - Versión monolítica (v0.9): 3,307 líneas
   - Versión modular (v2.0): en desarrollo

### 5.2 Entregables de Documentación

1. **Documentación de Usuario**
   - Manual de Usuario completo
   - Guías de inicio rápido
   - Casos de uso

2. **Documentación Técnica**
   - Arquitectura del sistema
   - Modelo de base de datos
   - API de funciones

3. **Documentación de Proyecto**
   - Acta de constitución (este documento)
   - Documentación de cambios
   - Guía de compilación

---

## 6. REQUERIMIENTOS DE ALTO NIVEL

### 6.1 Requerimientos Funcionales

**RF-01: Gestión de Entidades Básicas**
- El sistema debe permitir operaciones CRUD sobre: Materias, Profesores, Planes de Estudio, Turnos, Divisiones

**RF-02: Asignaciones y Relaciones**
- El sistema debe permitir relacionar: Materias con Profesores, Profesores con Turnos, Materias con Planes, Planes con Turnos

**RF-03: Gestión de Horarios Dual**
- El sistema debe ofrecer dos vistas de horarios: Por Curso y Por Profesor
- Las vistas deben estar sincronizadas en tiempo real

**RF-04: Validaciones Automáticas**
- El sistema debe prevenir: Superposición de horarios, Asignación de materias no autorizadas, Conflictos de disponibilidad

**RF-05: Búsqueda y Filtrado**
- El sistema debe permitir filtrar información por: Turno, Nombre, Plan de Estudios, Año

**RF-06: Configuración Flexible**
- El sistema debe permitir configurar horarios estándar por turno
- Aplicación individual o masiva de configuraciones

### 6.2 Requerimientos No Funcionales

**RNF-01: Usabilidad**
- Interfaz gráfica intuitiva con menús organizados
- Navegación completa por teclado
- Tooltips de ayuda contextual
- Autocompletado inteligente

**RNF-02: Rendimiento**
- Tiempo de respuesta < 2 segundos para operaciones comunes
- Carga inicial de la aplicación < 5 segundos
- Soporte para al menos 100 profesores y 500 materias

**RNF-03: Confiabilidad**
- Base de datos transaccional con rollback
- Validación de datos antes de guardar
- Mensajes de error claros

**RNF-04: Mantenibilidad**
- Código comentado y documentado
- Funciones modulares reutilizables
- Convenciones de nomenclatura consistentes

**RNF-05: Portabilidad**
- Ejecutable independiente para Windows
- Compatibilidad con Windows 7, 8, 10, 11
- Sin dependencias externas para el usuario final

**RNF-06: Seguridad de Datos**
- Base de datos local protegida
- Integridad referencial en BD
- Backup automático (opcional)

---

## 7. RESTRICCIONES

### 7.1 Restricciones Técnicas
- **Plataforma:** Windows únicamente (versión actual)
- **Lenguaje:** Python 3.9+
- **Framework UI:** Tkinter (estándar de Python)
- **Base de Datos:** SQLite3
- **Arquitectura:** Aplicación de escritorio monousuario

### 7.2 Restricciones de Recursos
- **Equipo de Desarrollo:** 1 desarrollador principal
- **Presupuesto:** Limitado (uso de herramientas gratuitas)
- **Hardware:** Equipos de escritorio estándar de la institución

### 7.3 Restricciones de Tiempo
- **Desarrollo Iterativo:** Versiones incrementales
- **Mantenimiento:** Continuo según necesidades

---

## 8. SUPUESTOS Y DEPENDENCIAS

### 8.1 Supuestos

1. **Acceso a Equipamiento**
   - La institución cuenta con computadoras para ejecutar el sistema
   - Los equipos cumplen requisitos mínimos (Windows 7+, 4GB RAM)

2. **Disponibilidad de Datos**
   - La información actual en papel puede ser digitalizada
   - Los datos son consistentes y completos

3. **Capacitación de Usuarios**
   - Personal administrativo puede ser capacitado en el uso del sistema
   - Disponibilidad de tiempo para capacitación

4. **Soporte Técnico**
   - Existe personal o proveedor para soporte técnico básico
   - Capacidad de realizar backups periódicos

### 8.2 Dependencias

1. **Dependencias Tecnológicas**
   - Python 3.9+ disponible para desarrollo
   - PyInstaller para compilación de ejecutables
   - SQLite3 (incluido en Python)

2. **Dependencias Organizacionales**
   - Aprobación de autoridades educativas
   - Colaboración de personal administrativo para definición de requerimientos
   - Disponibilidad de usuarios para pruebas

3. **Dependencias de Datos**
   - Estructura organizativa definida (turnos, planes, divisiones)
   - Información actualizada de profesores y materias

---

## 9. RIESGOS INICIALES

### Riesgos Identificados

| ID | Riesgo | Probabilidad | Impacto | Estrategia de Mitigación |
|----|--------|--------------|---------|--------------------------|
| R-01 | Resistencia al cambio por parte del personal | Media | Alto | Capacitación gradual, demostración de beneficios |
| R-02 | Pérdida de datos durante migración | Baja | Crítico | Backups múltiples, proceso de migración controlado |
| R-03 | Errores en validaciones de horarios | Media | Alto | Pruebas exhaustivas, validación con usuarios |
| R-04 | Incompatibilidad con equipos antiguos | Media | Medio | Verificación previa de requisitos, actualización de equipos |
| R-05 | Falta de mantenimiento futuro | Baja | Alto | Documentación completa, código limpio y comentado |
| R-06 | Cambios en estructura organizativa | Media | Medio | Sistema flexible y parametrizable |
| R-07 | Corrupción de base de datos | Baja | Crítico | Sistema de backups automáticos, validaciones de integridad |
| R-08 | Requerimientos no detectados | Media | Medio | Desarrollo iterativo, feedback continuo |

---

## 10. CRONOGRAMA DE HITOS

### Hitos Principales

| Hito | Descripción | Fecha Estimada | Estado |
|------|-------------|----------------|--------|
| M1 | Definición de requerimientos | Q1 2024 | ✅ Completado |
| M2 | Diseño de base de datos | Q1 2024 | ✅ Completado |
| M3 | Desarrollo de funcionalidades básicas | Q2 2024 | ✅ Completado |
| M4 | Implementación de horarios por curso | Q2 2024 | ✅ Completado |
| M5 | Implementación de horarios por profesor | Q3 2024 | ✅ Completado |
| M6 | Corrección de bugs y mejoras UX | Q4 2024 | ✅ Completado |
| M7 | Pruebas de usuario | Q4 2024 | 🔄 En progreso |
| M8 | Capacitación de usuarios | Q1 2025 | ⏳ Pendiente |
| M9 | Implementación en producción | Q1 2025 | ⏳ Pendiente |
| M10 | Refactorización a v2.0 (opcional) | Q2 2025 | 🔄 En desarrollo |

---

## 11. PRESUPUESTO PRELIMINAR

### 11.1 Costos de Desarrollo

| Concepto | Descripción | Costo Estimado |
|----------|-------------|----------------|
| Desarrollo de Software | 400+ horas de desarrollo | [Por definir] |
| Documentación | Manuales y guías | [Por definir] |
| Pruebas y QA | Testing y correcciones | [Por definir] |
| **Subtotal Desarrollo** | | [Por definir] |

### 11.2 Costos de Implementación

| Concepto | Descripción | Costo Estimado |
|----------|-------------|----------------|
| Capacitación | Training de usuarios | [Por definir] |
| Migración de Datos | Digitalización de datos actuales | [Por definir] |
| Licencias | N/A (software open source) | $0 |
| **Subtotal Implementación** | | [Por definir] |

### 11.3 Costos de Mantenimiento (Anual)

| Concepto | Descripción | Costo Estimado |
|----------|-------------|----------------|
| Soporte Técnico | Resolución de incidencias | [Por definir] |
| Actualizaciones | Mejoras y nuevas funcionalidades | [Por definir] |
| Backups | Almacenamiento y gestión | [Por definir] |
| **Subtotal Mantenimiento** | | [Por definir] |

**PRESUPUESTO TOTAL:** [Por definir]

---

## 12. ORGANIZACIÓN DEL PROYECTO

### 12.1 Estructura Organizacional

```
┌─────────────────────────────┐
│    PATROCINADOR             │
│  (Autoridad Educativa)      │
└──────────────┬──────────────┘
               │
┌──────────────▼──────────────┐
│    JEFE DE PROYECTO         │
│  (Coordinador Académico)    │
└──────────────┬──────────────┘
               │
       ┌───────┴───────┐
       │               │
┌──────▼──────┐ ┌─────▼──────┐
│  DESARROLLO │ │  USUARIOS  │
│  (Developer)│ │  (Personal)│
└─────────────┘ └────────────┘
```

### 12.2 Roles y Responsabilidades

**Patrocinador del Proyecto**
- Aprobar presupuesto y recursos
- Tomar decisiones estratégicas
- Resolver conflictos organizacionales

**Jefe del Proyecto**
- Coordinar desarrollo e implementación
- Gestionar stakeholders
- Reportar avances
- Validar entregables

**Equipo de Desarrollo**
- Diseñar y desarrollar el software
- Realizar pruebas
- Crear documentación técnica
- Brindar soporte técnico

**Usuarios Finales**
- Proporcionar requerimientos
- Participar en pruebas
- Validar funcionalidades
- Adoptar el sistema

---

## 13. CRITERIOS DE ÉXITO

### 13.1 Criterios de Aceptación del Proyecto

El proyecto se considerará exitoso si cumple con los siguientes criterios:

1. **Funcionalidad Completa**
   - ✅ Todas las funcionalidades CRUD implementadas y funcionando
   - ✅ Sincronización bidireccional entre vistas de horarios
   - ✅ Validaciones automáticas operativas

2. **Calidad del Software**
   - ✅ Menos de 5 bugs críticos en producción
   - ✅ Tiempo de respuesta menor a 2 segundos
   - ✅ Interfaz intuitiva según feedback de usuarios

3. **Documentación**
   - ✅ Manual de usuario completo
   - ✅ Documentación técnica disponible
   - ✅ Guías de instalación y uso

4. **Adopción por Usuarios**
   - ⏳ Al menos 80% del personal capacitado
   - ⏳ Uso diario del sistema para gestión de horarios
   - ⏳ Reducción de 50% en tiempo de gestión manual

5. **Integridad de Datos**
   - ✅ Toda la información histórica migrada correctamente
   - ✅ Sistema de backup implementado
   - ✅ Cero pérdida de datos en 3 meses de operación

---

## 14. APROBACIONES

### 14.1 Firmas de Aprobación

Este documento establece la base para el inicio formal del proyecto y debe ser aprobado por las siguientes partes:

| Rol | Nombre | Firma | Fecha |
|-----|--------|-------|-------|
| **Patrocinador del Proyecto** | [Nombre] | __________ | __/__/____ |
| **Jefe del Proyecto** | [Nombre] | __________ | __/__/____ |
| **Representante de Usuarios** | [Nombre] | __________ | __/__/____ |
| **Equipo de Desarrollo** | [Nombre] | __________ | __/__/____ |

---

## 15. CONTROL DE CAMBIOS

### Historial de Versiones del Acta

| Versión | Fecha | Autor | Descripción de Cambios |
|---------|-------|-------|------------------------|
| 1.0 | 08/11/2025 | [Autor] | Creación inicial del acta de constitución |
| | | | |

---

## 16. ANEXOS

### Anexo A: Glosario de Términos

- **Materia/Obligación:** Asignatura del plan de estudios
- **Banca de Horas:** Cantidad de horas asignadas a un profesor para una materia
- **Turno:** Horario escolar (mañana, tarde, noche)
- **División:** Grupo/curso de alumnos
- **Espacio:** Módulo horario dentro de un turno (1ª, 2ª, 3ª hora, etc.)
- **Plan de Estudios:** Conjunto de materias que conforman una carrera/nivel
- **Año/Curso:** Nivel académico dentro de un plan de estudios
- **Grilla:** Visualización semanal de horarios (lunes a viernes)

### Anexo B: Referencias

- Código fuente: `version 1.0/Horarios_v0.9.py`
- Documentación de cambios: `version 1.0/DOCUMENTACION_CAMBIOS.md`
- Plan de refactorización: `version 2.0/PLAN_REFACTORIZACION.md`
- Base de datos: `horarios.db` (SQLite)

---

**Documento preparado por:** [Nombre del responsable]  
**Fecha de elaboración:** 8 de Noviembre de 2025  
**Próxima revisión:** [Fecha]

---

_Este documento constituye el acta de constitución oficial del proyecto Sistema de Gestión de Horarios Escolares y establece la base formal para su planificación, ejecución y control._
