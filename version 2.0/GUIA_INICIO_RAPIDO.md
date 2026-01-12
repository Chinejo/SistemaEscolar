# Guía de Inicio Rápido - Refactorización v2.0

## 🎯 Objetivo

Esta guía te ayudará a comenzar con la refactorización del Sistema de Gestión de Horarios Escolares.

## 📚 Documentos Clave

Antes de comenzar, revisa estos documentos en orden:

1. **[PLAN_REFACTORIZACION.md](./PLAN_REFACTORIZACION.md)**  
   Plan completo con arquitectura y distribución de módulos

2. **[MAPEO_MIGRACION.md](./MAPEO_MIGRACION.md)**  
   Mapeo detallado de cada función del código original a su nueva ubicación

3. **[CHECKLIST_IMPLEMENTACION.md](./CHECKLIST_IMPLEMENTACION.md)**  
   Lista de tareas con progreso de implementación

4. **[README.md](./README.md)**  
   Descripción general del proyecto v2.0

## 🚀 Comenzar a Implementar

### Paso 1: Revisar la Estructura

La estructura de carpetas ya está creada:

```
version 2.0/
├── database/       ✅ Creado
├── models/         ✅ Creado
├── repositories/   ✅ Creado
├── services/       ✅ Creado
├── ui/
│   ├── components/ ✅ Creado
│   └── views/      ✅ Creado
└── utils/          ✅ Creado
```

Todos los archivos `__init__.py` están creados.

### Paso 2: Orden de Implementación

Sigue este orden para evitar problemas de dependencias:

#### **Fase 1: Fundamentos** (Empezar aquí)
```
1. config.py              ← Configuración global
2. database/connection.py ← Conexión a BD
3. database/schema.py     ← Esquema de BD
4. models/base.py         ← Modelo base
```

#### **Fase 2: Modelos**
```
5. models/materia.py
6. models/profesor.py
7. models/anio.py
8. models/plan.py
9. models/turno.py
10. models/division.py
11. models/horario.py
```

#### **Fase 3: Repositorios**
```
12. repositories/base_repository.py
13. repositories/materia_repository.py
14. repositories/profesor_repository.py
... (etc)
```

#### **Fase 4: Servicios**
```
services/validation_service.py
services/materia_service.py
services/profesor_service.py
services/horario_service.py
services/turno_service.py
services/plan_service.py
services/anio_service.py
services/division_service.py
```

#### **Fase 5: UI**
```
ui/styles.py
ui/components/...
ui/main_window.py
ui/views/...
```

#### **Fase 6: Integración**
```
main.py  ← Último archivo
```

### Paso 3: Template de Código

#### Template para Modelos

```python
"""
Modelo de [Entidad].
Representa [descripción de la entidad].
"""
from typing import Optional, Dict, Any


class NombreModelo:
    """Modelo para [entidad]."""
    
    def __init__(
        self,
        id: Optional[int] = None,
        atributo1: Optional[str] = None,
        atributo2: Optional[int] = None
    ):
        """
        Inicializa un nuevo [Modelo].
        
        Args:
            id: ID único del registro
            atributo1: Descripción
            atributo2: Descripción
        """
        self.id = id
        self.atributo1 = atributo1
        self.atributo2 = atributo2
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el modelo a diccionario.
        
        Returns:
            Diccionario con los atributos del modelo
        """
        return {
            'id': self.id,
            'atributo1': self.atributo1,
            'atributo2': self.atributo2
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'NombreModelo':
        """
        Crea una instancia desde un diccionario.
        
        Args:
            data: Diccionario con los datos del modelo
            
        Returns:
            Instancia del modelo
        """
        return NombreModelo(
            id=data.get('id'),
            atributo1=data.get('atributo1'),
            atributo2=data.get('atributo2')
        )
    
    def __repr__(self) -> str:
        """Representación del modelo."""
        return f"NombreModelo(id={self.id}, atributo1='{self.atributo1}')"
```

#### Template para Repositorios

```python
"""
Repositorio para [Entidad].
Gestiona el acceso a datos de [entidad].
"""
from typing import List, Optional, Dict, Any
from repositories.base_repository import BaseRepository
from models.nombre_modelo import NombreModelo


class NombreRepository(BaseRepository):
    """Repositorio para [Entidad]."""
    
    def __init__(self):
        """Inicializa el repositorio."""
        super().__init__('nombre_tabla')
    
    def crear(self, campo1: str, campo2: int) -> None:
        """
        Crea un nuevo registro.
        
        Args:
            campo1: Descripción
            campo2: Descripción
        """
        campos = ['campo1', 'campo2']
        valores = [campo1, campo2]
        self.create(campos, valores)
    
    def obtener_todos(self) -> List[NombreModelo]:
        """
        Obtiene todos los registros.
        
        Returns:
            Lista de modelos
        """
        campos = ['id', 'campo1', 'campo2']
        datos = self.find_all(campos)
        return [NombreModelo.from_dict(d) for d in datos]
    
    # Agregar métodos específicos según necesidad
```

#### Template para Vistas

```python
"""
Vista de [Sección].
Gestiona la interfaz de usuario para [descripción].
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional


class NombreView:
    """Vista para gestión de [sección]."""
    
    def __init__(self, parent, main_window):
        """
        Inicializa la vista.
        
        Args:
            parent: Frame padre donde se renderiza la vista
            main_window: Referencia a la ventana principal
        """
        self.parent = parent
        self.main_window = main_window
        self.tree = None
        self.seleccion_id = None
    
    def mostrar(self) -> None:
        """Renderiza la vista completa."""
        # Título
        ttk.Label(
            self.parent,
            text='Título de la Vista',
            font=('Arial', 14)
        ).pack(pady=10)
        
        # Tabla
        self._crear_tabla()
        
        # Botones
        self._crear_botones()
        
        # Cargar datos
        self._recargar_tree()
    
    def _crear_tabla(self) -> None:
        """Crea el Treeview."""
        # Implementar
        pass
    
    def _crear_botones(self) -> None:
        """Crea los botones de acción."""
        # Implementar
        pass
    
    def _recargar_tree(self) -> None:
        """Recarga los datos en el Treeview."""
        # Implementar
        pass
    
    def _on_select(self, event=None) -> None:
        """Maneja la selección en el tree."""
        # Implementar
        pass
```

### Paso 4: Copiar Código del Original

Para cada archivo que crees:

1. **Abre** `version 1.0/Horarios_v0.9.py`
2. **Consulta** el archivo `MAPEO_MIGRACION.md`
3. **Copia** el código correspondiente
4. **Adapta** al nuevo formato (clases, imports, etc.)
5. **Documenta** con docstrings
6. **Prueba** el módulo

### Paso 5: Actualizar Checklist

Después de completar cada archivo/módulo:

1. Marca la casilla en `CHECKLIST_IMPLEMENTACION.md`
2. Haz commit con mensaje descriptivo
3. Continúa con el siguiente módulo

## 📝 Convenciones Importantes

### Imports
```python
# Siempre en este orden:
# 1. Librerías estándar
import os
import sys
from typing import List, Optional, Dict, Any

# 2. Librerías de terceros
import tkinter as tk
from tkinter import ttk, messagebox

# 3. Imports locales
from config import DB_NAME
from database.connection import get_connection
from models.materia import Materia
```

### Nombres
- **Archivos:** `snake_case.py` (materia_repository.py)
- **Clases:** `PascalCase` (MateriaRepository)
- **Funciones:** `snake_case` (obtener_todas)
- **Constantes:** `UPPER_SNAKE_CASE` (DB_NAME)
- **Variables privadas:** `_nombre` (prefijo underscore)

### Docstrings
Usar formato Google:

```python
def funcion(param1: str, param2: int) -> bool:
    """
    Descripción breve de la función.
    
    Descripción más detallada si es necesaria.
    
    Args:
        param1: Descripción del parámetro 1
        param2: Descripción del parámetro 2
        
    Returns:
        Descripción del valor de retorno
        
    Raises:
        ValueError: Cuando param2 es negativo
    """
    pass
```

## ⚠️ Consideraciones Importantes

### ❌ Evitar

- Imports circulares
- Código duplicado
- Funciones muy largas (>50 líneas)
- Variables globales mutables
- Lógica de negocio en la UI
- Acceso directo a BD desde vistas

### ✅ Hacer

- Un módulo, una responsabilidad
- Funciones pequeñas y específicas
- Documentar todo con docstrings
- Validar inputs
- Manejar excepciones
- Escribir código legible

## 🧪 Testing

Aunque no hay tests formales aún, prueba cada módulo:

```python
# Al final de cada archivo, agregar:
if __name__ == '__main__':
    # Código de prueba
    # Ejemplo:
    repo = MateriaRepository()
    materias = repo.obtener_todas()
    print(f"Total materias: {len(materias)}")
```

## 🆘 Ayuda y Recursos

### Documentos de Referencia
- [PEP 8](https://pep8.org/) - Guía de estilo Python
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Real Python - Repository Pattern](https://realpython.com/python-sql-libraries/)

### En Caso de Duda
1. Consulta el código original en `version 1.0/`
2. Revisa el `MAPEO_MIGRACION.md`
3. Mira ejemplos en módulos ya implementados
4. Pregunta en el equipo

## 📊 Progreso Esperado

Tiempo estimado por fase (trabajando 2-3 horas/día):

- **Fase 1:** 1-2 días
- **Fase 2:** 2-3 días
- **Fase 3:** 2-3 días
- **Fase 4:** 1-2 días
- **Fase 5:** 5-7 días
- **Fase 6:** 2-3 días

**Total estimado:** 15-20 días

## 🎯 Siguiente Acción

**EMPEZAR AHORA:**

Crea el archivo `config.py` siguiendo el template y copiando el código de configuración del original.

```python
# config.py - Tu primer archivo
"""
Configuración global de la aplicación.
"""
import os
import sys

def get_base_path():
    """Obtiene la ruta base de la aplicación..."""
    # Copiar código del original
    pass

# Continuar con las demás configuraciones...
```

---

**¡Buena suerte con la refactorización! 🚀**

**Fecha de inicio:** [Tu fecha aquí]
