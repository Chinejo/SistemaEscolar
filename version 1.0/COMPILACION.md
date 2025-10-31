# Instrucciones para Compilar el Sistema de Gestión de Horarios Escolares

## Requisitos Previos
- Python 3.x instalado en el sistema

## Pasos para Compilar

### 1. Instalar PyInstaller
```powershell
pip install -r requirements.txt
```

### 2. Compilar el Ejecutable

#### Opción A: Usando el archivo .spec (Recomendado)
```powershell
pyinstaller SistemaHorarios.spec
```

#### Opción B: Comando directo (alternativa)
```powershell
pyinstaller --onefile --windowed --name SistemaHorarios Horarios_v0.9.py
```

### 3. Ubicación del Ejecutable
Después de la compilación, encontrarás el ejecutable en:
```
dist/SistemaHorarios.exe
```

## Opciones de Compilación

### Compilación Básica (Un solo archivo)
```powershell
pyinstaller --onefile --windowed --name SistemaHorarios Horarios_v0.9.py
```

### Compilación con Ícono Personalizado
Si tienes un archivo .ico, usa:
```powershell
pyinstaller --onefile --windowed --icon=icono.ico --name SistemaHorarios Horarios_v0.9.py
```

### Compilación en Carpeta (Más rápido al iniciar)
```powershell
pyinstaller --windowed --name SistemaHorarios Horarios_v0.9.py
```

## Parámetros Explicados

- `--onefile`: Crea un solo archivo ejecutable (más fácil de distribuir)
- `--windowed` o `-w`: No muestra la consola de comandos (para aplicaciones GUI)
- `--name`: Nombre del ejecutable resultante
- `--icon`: Archivo .ico para el ícono del ejecutable
- `--noconsole`: Alternativa a --windowed

## Distribución

### El ejecutable es completamente standalone y puede:
- ✅ Ejecutarse en cualquier PC con Windows sin necesidad de Python
- ✅ Crear su propia base de datos SQLite automáticamente
- ✅ Funcionar de forma independiente

### Para distribuir:
1. Copia el archivo `dist/SistemaHorarios.exe`
2. Opcionalmente, incluye el archivo `horarios.db` si quieres distribuir datos precargados
3. El programa creará automáticamente la base de datos si no existe

## Limpieza
Para limpiar archivos temporales de compilación:
```powershell
Remove-Item -Recurse -Force build, dist, *.spec
```

## Solución de Problemas

### Error: "Failed to execute script"
- Verifica que todas las dependencias estén instaladas
- Ejecuta con `--debug` para más información:
  ```powershell
  pyinstaller --onefile --windowed --debug all --name SistemaHorarios Horarios_v0.9.py
  ```

### La base de datos no se crea o no guarda los datos
**SOLUCIÓN IMPLEMENTADA**: El código ya está corregido para usar `sys.executable` cuando se ejecuta desde PyInstaller.

La base de datos se creará en el mismo directorio donde está el ejecutable.

Si aún tienes problemas:
1. Verifica que tienes permisos de escritura en la carpeta del ejecutable
2. Ejecuta el .exe como administrador
3. Verifica que no haya otro proceso bloqueando el archivo

### Probar que el ejecutable funciona correctamente
```powershell
.\probar_ejecutable.ps1
```

Este script verifica que:
- El ejecutable existe y es del tamaño correcto
- Se puede ejecutar sin errores
- La base de datos se crea correctamente en la carpeta del .exe

### Antivirus bloquea el ejecutable
- Es común con ejecutables creados por PyInstaller
- Agrégalo a las excepciones del antivirus
- Considera firmar digitalmente el ejecutable para distribución profesional

### Ejecutable muy grande
- Usa compilación en carpeta en lugar de `--onefile`
- El tamaño típico es 10-20 MB debido a Python embebido

## Notas Importantes

1. **Base de datos**: El archivo `horarios.db` se crea automáticamente en el mismo directorio del ejecutable
2. **Primera ejecución**: El programa iniciará con base de datos vacía (sin turnos, planes, etc.)
3. **Compatibilidad**: El .exe compilado en Windows solo funciona en Windows
4. **Versión de Python**: El ejecutable incluye la versión de Python con la que fue compilado

## Compilación para Otros Sistemas Operativos

- **Linux**: Compila en Linux, genera un ejecutable para Linux
- **macOS**: Compila en macOS, genera un ejecutable para macOS
- No es posible compilar para múltiples plataformas desde un solo sistema
