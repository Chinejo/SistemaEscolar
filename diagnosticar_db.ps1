# Script de diagnóstico para verificar qué base de datos está usando el ejecutable

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Diagnóstico de Base de Datos" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Primero, agregar algunos datos a la base de datos existente usando Python
Write-Host "1. Agregando datos de prueba a la base de datos con Python..." -ForegroundColor Yellow

$pythonScript = @"
import sqlite3
import os

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist', 'horarios.db')
print(f'Conectando a: {db_path}')

conn = sqlite3.connect(db_path)
c = conn.cursor()

# Verificar si ya existe algún turno de prueba
c.execute("SELECT COUNT(*) FROM turno WHERE nombre='TURNO_TEST'")
if c.fetchone()[0] == 0:
    c.execute("INSERT INTO turno (nombre) VALUES ('TURNO_TEST')")
    conn.commit()
    print('✓ Turno de prueba agregado')
else:
    print('✓ Turno de prueba ya existe')

# Mostrar todos los turnos
c.execute("SELECT id, nombre FROM turno")
turnos = c.fetchall()
print(f'\nTurnos en la base de datos:')
for turno in turnos:
    print(f'  - ID: {turno[0]}, Nombre: {turno[1]}')

conn.close()
print(f'\nRuta de la DB: {db_path}')
print(f'Tamaño: {os.path.getsize(db_path)} bytes')
"@

$pythonScript | Out-File -FilePath "temp_test_db.py" -Encoding UTF8

& ".\.venv\Scripts\python.exe" temp_test_db.py

Write-Host ""
Write-Host "2. Ahora abre el ejecutable y verifica si ves 'TURNO_TEST' en la lista de turnos." -ForegroundColor Cyan
Write-Host "   Presiona cualquier tecla cuando hayas verificado..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host ""
Write-Host "3. ¿Viste el turno 'TURNO_TEST' en el ejecutable? (S/N): " -ForegroundColor Yellow -NoNewline
$respuesta = Read-Host

if ($respuesta -eq "S" -or $respuesta -eq "s") {
    Write-Host ""
    Write-Host "✅ ¡EXCELENTE! El ejecutable SÍ está usando la base de datos correcta" -ForegroundColor Green
    Write-Host "   La base de datos se encuentra en: .\dist\horarios.db" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "❌ PROBLEMA CONFIRMADO: El ejecutable NO está usando la base de datos correcta" -ForegroundColor Red
    Write-Host ""
    Write-Host "Esto puede deberse a:" -ForegroundColor Yellow
    Write-Host "  1. El ejecutable está creando una DB en otra ubicación" -ForegroundColor Gray
    Write-Host "  2. Hay un problema con la detección de ruta en el código" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Voy a buscar todas las bases de datos horarios.db en el sistema..." -ForegroundColor Yellow
    Write-Host ""
    
    # Buscar archivos horarios.db en todo el directorio del proyecto
    $dbFiles = Get-ChildItem -Path "C:\Chino\Tecnicatura\Metodologia de sistemas\Programa horarios" -Recurse -Filter "horarios.db" -ErrorAction SilentlyContinue
    
    Write-Host "Bases de datos encontradas:" -ForegroundColor Cyan
    foreach ($file in $dbFiles) {
        $size = $file.Length
        $modified = $file.LastWriteTime
        Write-Host "  📁 $($file.FullName)" -ForegroundColor White
        Write-Host "     Tamaño: $size bytes | Modificado: $modified" -ForegroundColor Gray
        Write-Host ""
    }
}

# Limpiar archivo temporal
Remove-Item "temp_test_db.py" -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
