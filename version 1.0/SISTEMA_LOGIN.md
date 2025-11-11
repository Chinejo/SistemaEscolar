# Sistema de Login - Documentación

## Cambios Implementados

Se ha implementado un sistema completo de autenticación y gestión de usuarios en el sistema de horarios escolares.

### 1. Base de Datos

Se agregó una nueva tabla `usuarios` con los siguientes campos:
- `id`: Identificador único del usuario
- `username`: Nombre de usuario (único)
- `password`: Contraseña hasheada con SHA256
- `es_admin`: Indica si el usuario es administrador (1) o usuario normal (0)
- `fecha_creacion`: Fecha de creación del usuario

### 2. Primer Inicio del Sistema

Al ejecutar la aplicación por primera vez (cuando no existen usuarios en la base de datos):
- Se muestra una ventana de configuración inicial
- Se solicita crear las credenciales del administrador principal
- Validaciones:
  - Usuario debe tener al menos 3 caracteres
  - Contraseña debe tener al menos 4 caracteres
  - Las contraseñas deben coincidir
- No se puede cancelar o cerrar esta ventana sin crear el administrador

### 3. Login

En cada inicio posterior del sistema:
- Se muestra una ventana de login
- El usuario debe ingresar sus credenciales
- Las contraseñas se verifican contra el hash almacenado en la base de datos
- Si las credenciales son correctas, se accede al sistema
- El título de la ventana muestra el usuario actual

### 4. Menú del Sistema

Se agregó un nuevo menú "Sistema" con opciones diferentes según el tipo de usuario:

#### Para Administradores:
- **Gestionar Usuarios**: Acceso completo a la gestión de usuarios
- **Cambiar Contraseña**: Cambiar su propia contraseña
- **Cerrar Sesión**: Salir del sistema

#### Para Usuarios Normales:
- **Cambiar Contraseña**: Cambiar su propia contraseña
- **Cerrar Sesión**: Salir del sistema

### 5. Gestión de Usuarios (Solo Administradores)

Vista completa con las siguientes funcionalidades:

#### Crear Usuario
- Formulario para crear nuevos usuarios
- Opción para marcar como administrador
- Validaciones de usuario y contraseña
- No permite usuarios duplicados

#### Eliminar Usuario
- Seleccionar usuario de la tabla y eliminarlo
- Protecciones:
  - No permite eliminar el propio usuario
  - No permite eliminar el último administrador del sistema

#### Cambiar Contraseña de Usuario
- El administrador puede cambiar la contraseña de cualquier usuario
- Validaciones de contraseña

#### Tabla de Usuarios
Muestra:
- Nombre de usuario
- Tipo (Administrador o Usuario)
- Fecha de creación

### 6. Cambiar Mi Contraseña

Disponible para todos los usuarios:
- Requiere ingresar la contraseña actual
- Solicita la nueva contraseña dos veces
- Valida que la contraseña actual sea correcta
- Valida que las nuevas contraseñas coincidan

### 7. Cerrar Sesión

- Solicita confirmación
- Vuelve a la pantalla de login
- Limpia los datos de sesión actual

## Seguridad

- Las contraseñas se almacenan hasheadas con SHA256
- Nunca se muestra la contraseña en texto plano
- Las validaciones previenen contraseñas débiles
- El sistema garantiza que siempre exista al menos un administrador

## Diferencias de Permisos

### Administradores
- Acceso completo a todas las funcionalidades del sistema
- Pueden crear, editar y eliminar usuarios
- Pueden cambiar contraseñas de otros usuarios
- Ven la opción "Gestionar Usuarios" en el menú

### Usuarios Normales
- Acceso a todas las funcionalidades de horarios, materias, profesores, etc.
- NO pueden gestionar usuarios
- Solo pueden cambiar su propia contraseña
- NO ven la opción "Gestionar Usuarios"

## Uso del Sistema

### Primera Vez
1. Al ejecutar el programa por primera vez, aparecerá la pantalla de configuración inicial
2. Crear el usuario administrador con:
   - Usuario (mínimo 3 caracteres)
   - Contraseña (mínimo 4 caracteres)
   - Confirmar contraseña
3. Click en "Crear Administrador"

### Inicio de Sesión
1. Al abrir el programa, ingrese sus credenciales
2. Click en "Iniciar Sesión"

### Crear Usuarios Adicionales (Solo Admin)
1. Ir al menú "Sistema" → "Gestionar Usuarios"
2. Click en "Crear Usuario"
3. Completar el formulario
4. Marcar "Usuario Administrador" si desea otorgar privilegios de admin
5. Click en "Crear"

### Cambiar Contraseña
1. Ir al menú "Sistema" → "Cambiar Contraseña"
2. Ingresar contraseña actual
3. Ingresar nueva contraseña dos veces
4. Click en "Cambiar"

### Cerrar Sesión
1. Ir al menú "Sistema" → "Cerrar Sesión"
2. Confirmar la acción

## Notas Técnicas

- El hash de contraseña utiliza SHA256
- Los usuarios se almacenan en la tabla `usuarios` de la base de datos SQLite
- La sesión actual se mantiene en la variable `self.usuario_actual` de la clase `App`
- Al cerrar sesión, se limpia el menú y se vuelve a la pantalla de login
- El sistema no permite quedarse sin administradores
