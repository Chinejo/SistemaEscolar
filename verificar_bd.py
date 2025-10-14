import sqlite3
import os

db_path = 'horarios.db'
print(f"Verificando estructura de la base de datos...")
print(f"Ruta: {os.path.abspath(db_path)}")

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Verificar tabla horario
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='horario'")
    if c.fetchone():
        print("\n✓ Tabla 'horario' encontrada")
        
        # Mostrar estructura
        c.execute("PRAGMA table_info(horario)")
        columnas = c.fetchall()
        print("\nColumnas de la tabla horario:")
        for col in columnas:
            print(f"  - {col[1]} ({col[2]})")
        
        # Contar registros
        c.execute('SELECT COUNT(*) FROM horario')
        print(f"\nTotal registros en horario: {c.fetchone()[0]}")
        
        # Contar por tipo
        c.execute('SELECT COUNT(*) FROM horario WHERE division_id IS NOT NULL')
        print(f"  - Con división (vista por curso): {c.fetchone()[0]}")
        
        c.execute('SELECT COUNT(*) FROM horario WHERE profesor_id IS NOT NULL AND turno_id IS NOT NULL')
        print(f"  - Con profesor y turno (sincronizados): {c.fetchone()[0]}")
    else:
        print("\n✗ Tabla 'horario' NO encontrada")
    
    # Verificar si existe horario_profesor (debería haber sido eliminada)
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='horario_profesor'")
    if c.fetchone():
        print("\n⚠ Tabla 'horario_profesor' todavía existe (debería haberse eliminado)")
    else:
        print("\n✓ Tabla 'horario_profesor' eliminada correctamente")
    
    conn.close()
    print("\n✓ Verificación completa")
else:
    print("✗ Base de datos no encontrada")
