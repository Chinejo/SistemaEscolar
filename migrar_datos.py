import sqlite3
import os

db_path = 'horarios.db'
print(f"Migrando datos existentes...")
print(f"Ruta: {os.path.abspath(db_path)}")

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Actualizar turno_id de los horarios existentes basándose en la división
    print("\nActualizando turno_id de horarios existentes...")
    c.execute('''
        UPDATE horario
        SET turno_id = (
            SELECT d.turno_id
            FROM division d
            WHERE d.id = horario.division_id
        )
        WHERE division_id IS NOT NULL AND turno_id IS NULL
    ''')
    
    registros_actualizados = c.rowcount
    conn.commit()
    
    print(f"✓ {registros_actualizados} registros actualizados con turno_id")
    
    # Verificar
    c.execute('SELECT COUNT(*) FROM horario WHERE turno_id IS NOT NULL')
    print(f"✓ Total registros con turno_id: {c.fetchone()[0]}")
    
    c.execute('SELECT COUNT(*) FROM horario WHERE turno_id IS NULL')
    print(f"  Registros sin turno_id: {c.fetchone()[0]}")
    
    conn.close()
    print("\n✓ Migración completa")
else:
    print("✗ Base de datos no encontrada")
