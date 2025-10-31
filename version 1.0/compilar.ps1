# Script de Compilación Automática para Sistema de Horarios
# Este script instala PyInstaller si no está instalado y compila el ejecutable

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Sistema de Gestión de Horarios" -ForegroundColor Cyan
Write-Host "  Script de Compilación Automática" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si PyInstaller está instalado
Write-Host "Verificando PyInstaller..." -ForegroundColor Yellow
$pyinstallerInstalled = pip list | Select-String "pyinstaller"

if (-not $pyinstallerInstalled) {
    Write-Host "PyInstaller no encontrado. Instalando..." -ForegroundColor Yellow
    pip install pyinstaller
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error al instalar PyInstaller. Abortando." -ForegroundColor Red
        exit 1
    }
    Write-Host "PyInstaller instalado correctamente." -ForegroundColor Green
} else {
    Write-Host "PyInstaller ya está instalado." -ForegroundColor Green
}

Write-Host ""
Write-Host "Limpiando compilaciones anteriores..." -ForegroundColor Yellow
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
Write-Host "Limpieza completada." -ForegroundColor Green

Write-Host ""
Write-Host "Iniciando compilación..." -ForegroundColor Yellow
Write-Host "Esto puede tomar algunos minutos..." -ForegroundColor Gray

# Compilar usando el archivo .spec
pyinstaller SistemaHorarios.spec --clean

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  ✅ COMPILACIÓN EXITOSA" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "El ejecutable se encuentra en:" -ForegroundColor Cyan
    Write-Host "  $(Get-Location)\dist\SistemaHorarios.exe" -ForegroundColor White
    Write-Host ""
    Write-Host "Tamaño del ejecutable:" -ForegroundColor Cyan
    $size = (Get-Item "dist\SistemaHorarios.exe").Length / 1MB
    Write-Host "  $([math]::Round($size, 2)) MB" -ForegroundColor White
    Write-Host ""
    Write-Host "Puedes distribuir este archivo a cualquier PC con Windows." -ForegroundColor Green
    Write-Host "No requiere Python instalado." -ForegroundColor Green
    Write-Host ""
    
    # Preguntar si desea abrir la carpeta
    $respuesta = Read-Host "¿Deseas abrir la carpeta del ejecutable? (S/N)"
    if ($respuesta -eq "S" -or $respuesta -eq "s") {
        explorer "$(Get-Location)\dist"
    }
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "  ❌ ERROR EN LA COMPILACIÓN" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Revisa los mensajes de error anteriores." -ForegroundColor Yellow
    Write-Host "Verifica que el archivo Horarios_v0.9.py existe y no tiene errores." -ForegroundColor Yellow
    exit 1
}
