def aplicar_estilos_ttk():
	style = ttk.Style()
	try:
		style.theme_use('clam')
	except Exception:
		pass
	style.configure('.', background='#f4f6fa', font=('Segoe UI', 10))
	style.configure('TLabel', background='#f4f6fa', font=('Segoe UI', 10))
	style.configure('TButton', font=('Segoe UI', 10, 'bold'), padding=6, relief='flat', background='#e0e7ef')
	style.map('TButton', background=[('active', '#d0d7e7')])
	style.configure('TEntry', relief='flat', padding=4)
	style.configure('TCombobox', padding=4, fieldbackground='#ffffff', background='#ffffff', selectbackground='#ffffff', selectforeground='#222')
	style.map('TCombobox',
		fieldbackground=[('disabled', '#e9ecef'), ('readonly', '#ffffff'), ('!readonly', '#ffffff')],
		background=[('disabled', '#e9ecef'), ('readonly', '#ffffff'), ('!readonly', '#ffffff')],
		selectbackground=[('!focus', '#ffffff'), ('focus', '#ffffff')],
		selectforeground=[('!focus', '#222'), ('focus', '#222')]
	)
	style.configure('Treeview', font=('Segoe UI', 10), rowheight=26, fieldbackground='#ffffff', background='#ffffff')
	style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'), background='#e0e7ef', foreground='#222')
	style.map('Treeview', background=[('selected', '#b3d1ff')])
	style.map('Treeview', foreground=[('selected', '#222')])
# MODELOS Y LOGICA DE DATOS PARA GESTION DE HORARIOS ESCOLARES
import sqlite3
import os
from typing import List, Optional, Dict, Any


# Inicialización de la base de datos
# Usar ruta absoluta basada en la ubicación del script
DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(DB_DIR, 'horarios.db')

def get_connection():
	return sqlite3.connect(DB_NAME)

# Decorador para centralizar manejo de conexión y commit
def db_operation(func):
	def wrapper(*args, **kwargs):
		conn = get_connection()
		try:
			result = func(conn, *args, **kwargs)
			conn.commit()
			return result
		except sqlite3.IntegrityError as e:
			raise Exception(str(e))
		finally:
			conn.close()
	return wrapper

# Funciones genéricas para CRUD simples
@db_operation
def crear_entidad(conn, tabla, campos, valores):
	placeholders = ','.join(['?']*len(valores))
	campos_str = ','.join(campos)
	conn.execute(f'INSERT INTO {tabla} ({campos_str}) VALUES ({placeholders})', valores)

@db_operation
def obtener_entidades(conn, tabla, campos):
	c = conn.cursor()
	c.execute(f'SELECT {','.join(campos)} FROM {tabla}')
	return [dict(zip(campos, row)) for row in c.fetchall()]

@db_operation
def actualizar_entidad(conn, tabla, campos, valores, id_campo, id_valor):
	set_str = ','.join([f'{campo}=?' for campo in campos])
	conn.execute(f'UPDATE {tabla} SET {set_str} WHERE {id_campo}=?', (*valores, id_valor))

@db_operation
def eliminar_entidad(conn, tabla, id_campo, id_valor):
	conn.execute(f'DELETE FROM {tabla} WHERE {id_campo}=?', (id_valor,))

def init_db():
	conn = get_connection()
	c = conn.cursor()
	# Años por plan
	c.execute('''CREATE TABLE IF NOT EXISTS anio (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		nombre TEXT NOT NULL,
		plan_id INTEGER,
		FOREIGN KEY(plan_id) REFERENCES plan_estudio(id),
		UNIQUE(nombre, plan_id)
	)''')
	# Materias por año
	c.execute('''CREATE TABLE IF NOT EXISTS anio_materia (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		anio_id INTEGER,
		materia_id INTEGER,
		FOREIGN KEY(anio_id) REFERENCES anio(id),
		FOREIGN KEY(materia_id) REFERENCES materia(id),
		UNIQUE(anio_id, materia_id)
	)''')
	# Plan de estudios
	c.execute('''CREATE TABLE IF NOT EXISTS plan_estudio (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		nombre TEXT UNIQUE NOT NULL
	)''')
	# Materias por plan de estudio
	c.execute('''CREATE TABLE IF NOT EXISTS plan_materia (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		plan_id INTEGER,
		materia_id INTEGER,
		FOREIGN KEY(plan_id) REFERENCES plan_estudio(id),
		FOREIGN KEY(materia_id) REFERENCES materia(id),
		UNIQUE(plan_id, materia_id)
	)''')
	# Turnos
	c.execute('''CREATE TABLE IF NOT EXISTS turno (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		nombre TEXT UNIQUE NOT NULL
	)''')
	# Turno-Plan (qué planes se ofrecen en cada turno)
	c.execute('''CREATE TABLE IF NOT EXISTS turno_plan (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		turno_id INTEGER,
		plan_id INTEGER,
		FOREIGN KEY(turno_id) REFERENCES turno(id),
		FOREIGN KEY(plan_id) REFERENCES plan_estudio(id),
		UNIQUE(turno_id, plan_id)
	)''')
	# Divisiones por turno, plan y año
	c.execute('''CREATE TABLE IF NOT EXISTS division (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		nombre TEXT NOT NULL,
		turno_id INTEGER,
		plan_id INTEGER,
		anio_id INTEGER,
		FOREIGN KEY(turno_id) REFERENCES turno(id),
		FOREIGN KEY(plan_id) REFERENCES plan_estudio(id),
		FOREIGN KEY(anio_id) REFERENCES anio(id),
		UNIQUE(nombre, turno_id, plan_id, anio_id)
	)''')
	# Materias
	c.execute('''CREATE TABLE IF NOT EXISTS materia (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		nombre TEXT UNIQUE NOT NULL,
		horas_semanales INTEGER NOT NULL
	)''')
	# Profesores
	c.execute('''CREATE TABLE IF NOT EXISTS profesor (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		nombre TEXT UNIQUE NOT NULL
	)''')
	# Banca de horas por materia para cada profesor
	c.execute('''CREATE TABLE IF NOT EXISTS profesor_materia (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		profesor_id INTEGER,
		materia_id INTEGER,
		banca_horas INTEGER NOT NULL,
		FOREIGN KEY(profesor_id) REFERENCES profesor(id),
		FOREIGN KEY(materia_id) REFERENCES materia(id),
		UNIQUE(profesor_id, materia_id)
	)''')
	# Turnos asignados a profesores
	c.execute('''CREATE TABLE IF NOT EXISTS profesor_turno (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		profesor_id INTEGER,
		turno_id INTEGER,
		FOREIGN KEY(profesor_id) REFERENCES profesor(id),
		FOREIGN KEY(turno_id) REFERENCES turno(id),
		UNIQUE(profesor_id, turno_id)
	)''')
	# Divisiones
	c.execute('''CREATE TABLE IF NOT EXISTS division (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		nombre TEXT UNIQUE NOT NULL
	)''')
	# Horarios: un espacio por día, hora, división
	c.execute('''CREATE TABLE IF NOT EXISTS horario (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		division_id INTEGER,
		dia TEXT,
		espacio INTEGER,
		hora_inicio TEXT,
		hora_fin TEXT,
		materia_id INTEGER,
		profesor_id INTEGER,
		turno_id INTEGER,
		FOREIGN KEY(division_id) REFERENCES division(id),
		FOREIGN KEY(materia_id) REFERENCES materia(id),
		FOREIGN KEY(profesor_id) REFERENCES profesor(id),
		FOREIGN KEY(turno_id) REFERENCES turno(id),
		UNIQUE(division_id, dia, espacio)
	)''')
	
	# Agregar columna turno_id a registros existentes si no existe
	try:
		c.execute('ALTER TABLE horario ADD COLUMN turno_id INTEGER REFERENCES turno(id)')
	except sqlite3.OperationalError:
		pass  # La columna ya existe
	# Horas por espacio/turno (valores por defecto para cada turno y espacio)
	c.execute('''CREATE TABLE IF NOT EXISTS turno_espacio_hora (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		turno_id INTEGER,
		espacio INTEGER,
		hora_inicio TEXT,
		hora_fin TEXT,
		FOREIGN KEY(turno_id) REFERENCES turno(id),
		UNIQUE(turno_id, espacio)
	)''')
	conn.commit()
	conn.close()


# CRUD Materia simplificado
def crear_materia(nombre: str, horas: int):
	try:
		crear_entidad('materia', ['nombre', 'horas_semanales'], [nombre, horas])
	except Exception:
		raise Exception('Ya existe una materia con ese nombre.')

def obtener_materias() -> List[Dict[str, Any]]:
	return obtener_entidades('materia', ['id', 'nombre', 'horas_semanales'])

def actualizar_materia(id_: int, nombre: str, horas: int):
	actualizar_entidad('materia', ['nombre', 'horas_semanales'], [nombre, horas], 'id', id_)

def eliminar_materia(id_: int):
	eliminar_entidad('materia', 'id', id_)


# CRUD Profesor simplificado
def crear_profesor(nombre: str):
	try:
		crear_entidad('profesor', ['nombre'], [nombre])
	except Exception:
		raise Exception('Ya existe un profesor con ese nombre.')

def obtener_profesores() -> List[Dict[str, Any]]:
	return obtener_entidades('profesor', ['id', 'nombre'])

def actualizar_profesor(id_: int, nombre: str):
	actualizar_entidad('profesor', ['nombre'], [nombre], 'id', id_)

def eliminar_profesor(id_: int):
	# Elimina también los turnos asignados
	@db_operation
	def _eliminar_profesor(conn, id_):
		conn.execute('DELETE FROM profesor_turno WHERE profesor_id=?', (id_,))
		conn.execute('DELETE FROM profesor WHERE id=?', (id_,))
	_eliminar_profesor(id_)

# CRUD Turnos de profesor
def asignar_turno_a_profesor(profesor_id: int, turno_id: int):
	try:
		conn = get_connection()
		c = conn.cursor()
		c.execute('INSERT INTO profesor_turno (profesor_id, turno_id) VALUES (?, ?)', (profesor_id, turno_id))
		conn.commit()
	except sqlite3.IntegrityError:
		raise Exception('El profesor ya tiene asignado ese turno.')
	finally:
		conn.close()

def quitar_turno_a_profesor(profesor_id: int, turno_id: int):
	conn = get_connection()
	c = conn.cursor()
	c.execute('DELETE FROM profesor_turno WHERE profesor_id=? AND turno_id=?', (profesor_id, turno_id))
	conn.commit()
	conn.close()

def obtener_turnos_de_profesor(profesor_id: int):
	conn = get_connection()
	c = conn.cursor()
	c.execute('''SELECT t.id, t.nombre FROM profesor_turno pt JOIN turno t ON pt.turno_id = t.id WHERE pt.profesor_id=?''', (profesor_id,))
	rows = c.fetchall()
	conn.close()
	return [{'id': r[0], 'nombre': r[1]} for r in rows]

def obtener_profesores_por_turno(turno_id: int):
	conn = get_connection()
	c = conn.cursor()
	c.execute('''SELECT p.id, p.nombre FROM profesor p JOIN profesor_turno pt ON p.id = pt.profesor_id WHERE pt.turno_id=?''', (turno_id,))
	rows = c.fetchall()
	conn.close()
	return [{'id': r[0], 'nombre': r[1]} for r in rows]

# CRUD Banca de horas por materia para profesor
def asignar_banca_profesor(profesor_id: int, materia_id: int, banca_horas: int):
	try:
		conn = get_connection()
		c = conn.cursor()
		c.execute('INSERT INTO profesor_materia (profesor_id, materia_id, banca_horas) VALUES (?, ?, ?)', (profesor_id, materia_id, banca_horas))
		conn.commit()
	except sqlite3.IntegrityError:
		raise Exception('El profesor ya tiene esa materia asignada.')
	finally:
		conn.close()

def obtener_banca_profesor(profesor_id: int) -> List[Dict[str, Any]]:
	conn = get_connection()
	c = conn.cursor()
	c.execute('''SELECT pm.id, m.nombre, pm.banca_horas FROM profesor_materia pm JOIN materia m ON pm.materia_id = m.id WHERE pm.profesor_id=?''', (profesor_id,))
	rows = c.fetchall()
	conn.close()
	return [{'id': r[0], 'materia': r[1], 'banca_horas': r[2]} for r in rows]

def actualizar_banca_profesor(pm_id: int, banca_horas: int):
	conn = get_connection()
	c = conn.cursor()
	c.execute('UPDATE profesor_materia SET banca_horas=? WHERE id=?', (banca_horas, pm_id))
	conn.commit()
	conn.close()

def eliminar_banca_profesor(pm_id: int):
	conn = get_connection()
	c = conn.cursor()
	c.execute('DELETE FROM profesor_materia WHERE id=?', (pm_id,))
	conn.commit()
	conn.close()

# CRUD División

# CRUD Año
def crear_anio(nombre: str, plan_id: int):
	try:
		conn = get_connection()
		c = conn.cursor()
		c.execute('INSERT INTO anio (nombre, plan_id) VALUES (?, ?)', (nombre, plan_id))
		conn.commit()
	except sqlite3.IntegrityError:
		raise Exception('Ya existe un año con ese nombre en el plan.')
	finally:
		conn.close()

def obtener_anios(plan_id: int) -> list:
	conn = get_connection()
	c = conn.cursor()
	c.execute('SELECT id, nombre FROM anio WHERE plan_id=?', (plan_id,))
	rows = c.fetchall()
	conn.close()
	return [{'id': r[0], 'nombre': r[1]} for r in rows]

def eliminar_anio(id_: int):
	conn = get_connection()
	c = conn.cursor()
	c.execute('DELETE FROM anio WHERE id=?', (id_,))
	conn.commit()
	conn.close()

# CRUD Materias por año
def agregar_materia_a_anio(anio_id: int, materia_id: int):
	try:
		conn = get_connection()
		c = conn.cursor()
		c.execute('INSERT INTO anio_materia (anio_id, materia_id) VALUES (?, ?)', (anio_id, materia_id))
		conn.commit()
	except sqlite3.IntegrityError:
		raise Exception('La materia ya está en el año.')
	finally:
		conn.close()

def quitar_materia_de_anio(anio_id: int, materia_id: int):
	conn = get_connection()
	c = conn.cursor()
	c.execute('DELETE FROM anio_materia WHERE anio_id=? AND materia_id=?', (anio_id, materia_id))
	conn.commit()
	conn.close()

def obtener_materias_de_anio(anio_id: int) -> list:
	conn = get_connection()
	c = conn.cursor()
	c.execute('''SELECT m.id, m.nombre FROM anio_materia am JOIN materia m ON am.materia_id = m.id WHERE am.anio_id=?''', (anio_id,))
	rows = c.fetchall()
	conn.close()
	return [{'id': r[0], 'nombre': r[1]} for r in rows]

# CRUD Plan de estudio
def crear_plan(nombre: str):
	try:
		conn = get_connection()
		c = conn.cursor()
		c.execute('INSERT INTO plan_estudio (nombre) VALUES (?)', (nombre,))
		conn.commit()
	except sqlite3.IntegrityError:
		raise Exception('Ya existe un plan de estudio con ese nombre.')
	finally:
		conn.close()

def obtener_planes() -> list:
	conn = get_connection()
	c = conn.cursor()
	c.execute('SELECT id, nombre FROM plan_estudio')
	rows = c.fetchall()
	conn.close()
	return [{'id': r[0], 'nombre': r[1]} for r in rows]

def eliminar_plan(id_: int):
	conn = get_connection()
	c = conn.cursor()
	c.execute('DELETE FROM plan_estudio WHERE id=?', (id_,))
	conn.commit()
	conn.close()

def agregar_materia_a_plan(plan_id: int, materia_id: int):
	try:
		conn = get_connection()
		c = conn.cursor()
		c.execute('INSERT INTO plan_materia (plan_id, materia_id) VALUES (?, ?)', (plan_id, materia_id))
		conn.commit()
	except sqlite3.IntegrityError:
		raise Exception('La materia ya está en el plan.')
	finally:
		conn.close()

def quitar_materia_de_plan(plan_id: int, materia_id: int):
	conn = get_connection()
	c = conn.cursor()
	c.execute('DELETE FROM plan_materia WHERE plan_id=? AND materia_id=?', (plan_id, materia_id))
	conn.commit()
	conn.close()

def obtener_materias_de_plan(plan_id: int) -> list:
	conn = get_connection()
	c = conn.cursor()
	c.execute('''SELECT m.id, m.nombre FROM plan_materia pm JOIN materia m ON pm.materia_id = m.id WHERE pm.plan_id=?''', (plan_id,))
	rows = c.fetchall()
	conn.close()
	return [{'id': r[0], 'nombre': r[1]} for r in rows]

# CRUD Turno
def crear_turno(nombre: str):
	try:
		conn = get_connection()
		c = conn.cursor()
		c.execute('INSERT INTO turno (nombre) VALUES (?)', (nombre,))
		conn.commit()
	except sqlite3.IntegrityError:
		raise Exception('Ya existe un turno con ese nombre.')
	finally:
		conn.close()

def obtener_turnos() -> list:
	conn = get_connection()
	c = conn.cursor()
	c.execute('SELECT id, nombre FROM turno')
	rows = c.fetchall()
	conn.close()
	return [{'id': r[0], 'nombre': r[1]} for r in rows]

def eliminar_turno(id_: int):
	conn = get_connection()
	c = conn.cursor()
	c.execute('DELETE FROM turno WHERE id=?', (id_,))
	conn.commit()
	conn.close()

def agregar_plan_a_turno(turno_id: int, plan_id: int):
	try:
		conn = get_connection()
		c = conn.cursor()
		c.execute('INSERT INTO turno_plan (turno_id, plan_id) VALUES (?, ?)', (turno_id, plan_id))
		conn.commit()
	except sqlite3.IntegrityError:
		raise Exception('El plan ya está en el turno.')
	finally:
		conn.close()

def quitar_plan_de_turno(turno_id: int, plan_id: int):
	conn = get_connection()
	c = conn.cursor()
	c.execute('DELETE FROM turno_plan WHERE turno_id=? AND plan_id=?', (turno_id, plan_id))
	conn.commit()
	conn.close()

def obtener_planes_de_turno(turno_id: int) -> list:
	"""Obtiene los planes de estudio asociados a un turno (sin duplicados)"""
	conn = get_connection()
	c = conn.cursor()
	c.execute('''SELECT DISTINCT p.id, p.nombre FROM plan_estudio p
				 JOIN turno_plan tp ON tp.plan_id = p.id
				 WHERE tp.turno_id = ?''', (turno_id,))
	rows = c.fetchall()
	conn.close()
	return [{'id': r[0], 'nombre': r[1]} for r in rows]

# Función helper para autocompletar comboboxes con una sola opción
def autocompletar_combobox(combobox, valores, incluir_vacio=True):
	"""
	Configura un combobox con los valores dados.
	
	Args:
		combobox: El widget ttk.Combobox a configurar
		valores: Lista de valores para el combobox
		incluir_vacio: Si True, incluye una opción vacía al inicio
	
	Returns:
		bool: Siempre retorna False (autocompletado deshabilitado)
	"""
	if incluir_vacio:
		combobox['values'] = [''] + valores
	else:
		combobox['values'] = valores
	
	# Configurar estado según disponibilidad de valores
	if len(valores) >= 1:
		if not incluir_vacio:
			combobox.set('')
		combobox.config(state='readonly')
		return False
	else:
		combobox.set('')
		combobox.config(state='disabled')
		return False

# CRUD División
def crear_division(nombre: str):
	# Nuevo: requiere turno_id, plan_id, anio_id
	raise Exception('La función crear_division debe ser llamada con turno_id, plan_id y anio_id.')

def obtener_divisiones() -> List[Dict[str, Any]]:
	conn = get_connection()
	c = conn.cursor()
	c.execute('SELECT id, nombre, turno_id, plan_id, anio_id FROM division')
	rows = c.fetchall()
	conn.close()
	return [{'id': r[0], 'nombre': r[1], 'turno_id': r[2], 'plan_id': r[3], 'anio_id': r[4]} for r in rows]

def actualizar_division(id_: int, nombre: str):
	conn = get_connection()
	c = conn.cursor()
	c.execute('UPDATE division SET nombre=? WHERE id=?', (nombre, id_))
	conn.commit()
	conn.close()

def eliminar_division(id_: int):
	conn = get_connection()
	c = conn.cursor()
	c.execute('DELETE FROM division WHERE id=?', (id_,))
	conn.commit()
	conn.close()

# CRUD Horario
def crear_horario(division_id: int, dia: str, espacio: int, hora_inicio: str, hora_fin: str, materia_id: int, profesor_id: int, turno_id: int = None):
	conn = get_connection()
	c = conn.cursor()
	# Obtener el turno de la división actual si no se proporciona
	if turno_id is None:
		c.execute('SELECT turno_id FROM division WHERE id=?', (division_id,))
		row = c.fetchone()
		if not row:
			conn.close()
			raise Exception('División no encontrada.')
		turno_id = row[0]

	# Si se proporcionó profesor, validar superposición solo entonces
	if profesor_id is not None:
		c.execute('''
			SELECT h.id FROM horario h
			JOIN division d ON h.division_id = d.id
			WHERE h.dia=? AND h.espacio=? AND h.profesor_id=? AND d.turno_id=? AND h.division_id != ?
		''', (dia, espacio, profesor_id, turno_id, division_id))
		if c.fetchone():
			conn.close()
			raise Exception('El profesor ya está asignado en ese horario en otra división del mismo turno.')

	# Validar que el profesor tenga la materia asignada solo si ambos ids están presentes
	if profesor_id is not None and materia_id is not None:
		c.execute('SELECT 1 FROM profesor_materia WHERE profesor_id=? AND materia_id=?', (profesor_id, materia_id))
		if not c.fetchone():
			conn.close()
			raise Exception('El profesor no tiene asignada la materia seleccionada.')

	# Permitir hora_inicio/hora_fin vacías (NULL)
	hora_inicio_db = hora_inicio if hora_inicio else None
	hora_fin_db = hora_fin if hora_fin else None

	c.execute('''INSERT INTO horario (division_id, dia, espacio, hora_inicio, hora_fin, materia_id, profesor_id, turno_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
			  (division_id, dia, espacio, hora_inicio_db, hora_fin_db, materia_id, profesor_id, turno_id))

	# Sumar horas a materia y banca de profesor
	# Sumar horas a materia y banca de profesor si corresponde
	if materia_id is not None:
		c.execute('UPDATE materia SET horas_semanales = horas_semanales + 1 WHERE id=?', (materia_id,))
	if profesor_id is not None and materia_id is not None:
		c.execute('UPDATE profesor_materia SET banca_horas = banca_horas + 1 WHERE profesor_id=? AND materia_id=?', (profesor_id, materia_id))
	conn.commit()
	conn.close()

def obtener_horarios(division_id: int) -> List[Dict[str, Any]]:
	conn = get_connection()
	c = conn.cursor()
	c.execute('''SELECT h.id, h.dia, h.espacio, h.hora_inicio, h.hora_fin, m.nombre, p.nombre FROM horario h
				 LEFT JOIN materia m ON h.materia_id = m.id
				 LEFT JOIN profesor p ON h.profesor_id = p.id
				 WHERE h.division_id=?''', (division_id,))
	rows = c.fetchall()
	conn.close()
	return [{'id': r[0], 'dia': r[1], 'espacio': r[2], 'hora_inicio': r[3], 'hora_fin': r[4], 'materia': r[5], 'profesor': r[6]} for r in rows]

def eliminar_horario(id_: int):
	conn = get_connection()
	c = conn.cursor()
	# Al eliminar, restar horas a materia y profesor
	c.execute('SELECT materia_id, profesor_id FROM horario WHERE id=?', (id_,))
	row = c.fetchone()
	if row:
		materia_id, profesor_id = row
		if materia_id is not None:
			c.execute('UPDATE materia SET horas_semanales = horas_semanales - 1 WHERE id=?', (materia_id,))
		if profesor_id is not None and materia_id is not None:
			c.execute('UPDATE profesor_materia SET banca_horas = banca_horas - 1 WHERE profesor_id=? AND materia_id=?', (profesor_id, materia_id))
	c.execute('DELETE FROM horario WHERE id=?', (id_,))
	conn.commit()
	conn.close()

# Helpers para horas por turno/espacio (turno_espacio_hora)
def obtener_turno_espacio_hora(turno_id: int, espacio: int):
	conn = get_connection()
	c = conn.cursor()
	c.execute('SELECT hora_inicio, hora_fin FROM turno_espacio_hora WHERE turno_id=? AND espacio=?', (turno_id, espacio))
	row = c.fetchone()
	conn.close()
	if row:
		return {'hora_inicio': row[0], 'hora_fin': row[1]}
	return None

def set_turno_espacio_hora(turno_id: int, espacio: int, hora_inicio: str, hora_fin: str):
	conn = get_connection()
	c = conn.cursor()
	# Si ambos vacíos, eliminar registro existente
	if not hora_inicio and not hora_fin:
		c.execute('DELETE FROM turno_espacio_hora WHERE turno_id=? AND espacio=?', (turno_id, espacio))
	else:
		# Insertar o actualizar (usamos INSERT OR REPLACE sobre la clave única turno_id+espacio)
		c.execute('INSERT OR REPLACE INTO turno_espacio_hora (turno_id, espacio, hora_inicio, hora_fin) VALUES (?, ?, ?, ?)',
				  (turno_id, espacio, hora_inicio if hora_inicio else None, hora_fin if hora_fin else None))
	conn.commit()
	conn.close()

def eliminar_turno_espacio_hora(turno_id: int, espacio: int):
	conn = get_connection()
	c = conn.cursor()
	c.execute('DELETE FROM turno_espacio_hora WHERE turno_id=? AND espacio=?', (turno_id, espacio))
	conn.commit()
	conn.close()

# CRUD Horario por Profesor (usa la misma tabla 'horario' que la vista por curso)
def crear_horario_profesor(profesor_id: int, turno_id: int, dia: str, espacio: int, hora_inicio: str, hora_fin: str, division_id: int = None, materia_id: int = None):
	"""
	Crea un horario para un profesor. Si division_id se proporciona, valida que pertenezca al turno.
	Los datos se guardan en la tabla 'horario' para que se sincronicen con la vista por curso.
	"""
	conn = get_connection()
	c = conn.cursor()
	
	# Validar que el profesor esté asignado al turno
	c.execute('SELECT 1 FROM profesor_turno WHERE profesor_id=? AND turno_id=?', (profesor_id, turno_id))
	if not c.fetchone():
		conn.close()
		raise Exception('El profesor no está asignado a este turno.')
	
	# Validar que el profesor tenga la materia asignada solo si ambos están presentes
	if materia_id is not None and profesor_id is not None:
		c.execute('SELECT 1 FROM profesor_materia WHERE profesor_id=? AND materia_id=?', (profesor_id, materia_id))
		if not c.fetchone():
			conn.close()
			raise Exception('El profesor no tiene asignada esta materia.')
	
	# Si se especifica división, validar que pertenezca al turno
	if division_id is not None:
		c.execute('SELECT turno_id FROM division WHERE id=?', (division_id,))
		row = c.fetchone()
		if not row:
			conn.close()
			raise Exception('División no encontrada.')
		if row[0] != turno_id:
			conn.close()
			raise Exception('La división no pertenece al turno seleccionado.')
		
		# Si hay división, validar que no exista ya un horario para esa división en ese día/espacio
		c.execute('''SELECT 1 FROM horario 
					 WHERE division_id=? AND dia=? AND espacio=?''', 
				  (division_id, dia, espacio))
		if c.fetchone():
			conn.close()
			raise Exception('Ya existe un horario asignado para esta división en este día y espacio.')
	
	# Validar que no haya superposición en el horario del profesor (mismo turno, día y espacio)
	c.execute('''SELECT 1 FROM horario 
				 WHERE profesor_id=? AND turno_id=? AND dia=? AND espacio=?''', 
			  (profesor_id, turno_id, dia, espacio))
	if c.fetchone():
		conn.close()
		raise Exception('El profesor ya tiene un horario asignado en este día y espacio en este turno.')
	
	# Permitir hora_inicio/hora_fin vacías (NULL)
	hora_inicio_db = hora_inicio if hora_inicio else None
	hora_fin_db = hora_fin if hora_fin else None
	
	c.execute('''INSERT INTO horario (division_id, dia, espacio, hora_inicio, hora_fin, materia_id, profesor_id, turno_id) 
				 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
			  (division_id, dia, espacio, hora_inicio_db, hora_fin_db, materia_id, profesor_id, turno_id))
	
	conn.commit()
	conn.close()

def obtener_horarios_profesor(profesor_id: int, turno_id: int) -> List[Dict[str, Any]]:
	"""
	Obtiene todos los horarios de un profesor en un turno específico.
	Lee de la tabla 'horario', por lo que incluye asignaciones hechas desde cualquier vista.
	"""
	conn = get_connection()
	c = conn.cursor()
	c.execute('''SELECT h.id, h.dia, h.espacio, h.hora_inicio, h.hora_fin, 
				 m.nombre as materia, d.nombre as division
				 FROM horario h
				 LEFT JOIN materia m ON h.materia_id = m.id
				 LEFT JOIN division d ON h.division_id = d.id
				 WHERE h.profesor_id=? AND h.turno_id=?''', (profesor_id, turno_id))
	rows = c.fetchall()
	conn.close()
	return [{'id': r[0], 'dia': r[1], 'espacio': r[2], 'hora_inicio': r[3], 'hora_fin': r[4], 'materia': r[5], 'division': r[6]} for r in rows]

def eliminar_horario_profesor(id_: int):
	"""
	Elimina un horario por su ID. Como usa la tabla 'horario', 
	el cambio se refleja automáticamente en ambas vistas.
	"""
	# Usamos la misma función eliminar_horario que ya existe
	eliminar_horario(id_)

# Inicializar la base de datos al importar el módulo
init_db()

# ================= INTERFAZ GRAFICA BASE ===================

import tkinter as tk
from tkinter import ttk, messagebox

# === Clase para Tooltips ===
class ToolTip:
	"""Crear un tooltip para un widget dado"""
	def __init__(self, widget, text):
		self.widget = widget
		self.text = text
		self.tip_window = None
		self.widget.bind("<Enter>", self.show_tip)
		self.widget.bind("<Leave>", self.hide_tip)
	
	def show_tip(self, event=None):
		if self.tip_window or not self.text:
			return
		x, y, cx, cy = self.widget.bbox("insert")
		x = x + self.widget.winfo_rootx() + 25
		y = y + cy + self.widget.winfo_rooty() + 25
		self.tip_window = tw = tk.Toplevel(self.widget)
		tw.wm_overrideredirect(True)
		tw.wm_geometry(f"+{x}+{y}")
		label = tk.Label(tw, text=self.text, justify='left',
						background="#ffffe0", relief='solid', borderwidth=1,
						font=("Segoe UI", 9, "normal"), padx=8, pady=6)
		label.pack(ipadx=1)
	
	def hide_tip(self, event=None):
		if self.tip_window:
			self.tip_window.destroy()
			self.tip_window = None

# === Helpers para interfaz gráfica ===
def crear_treeview(parent, columnas, headings, height=10):
	tree = ttk.Treeview(parent, columns=columnas, show='headings', height=height)
	for col, head in zip(columnas, headings):
		tree.heading(col, text=head)
	vsb = ttk.Scrollbar(parent, orient='vertical', command=tree.yview)
	hsb = ttk.Scrollbar(parent, orient='horizontal', command=tree.xview)
	tree.configure(yscroll=vsb.set, xscroll=hsb.set)
	tree.grid(row=0, column=0, sticky='nsew')
	vsb.grid(row=0, column=1, sticky='ns')
	hsb.grid(row=1, column=0, sticky='ew')
	parent.grid_rowconfigure(0, weight=1)
	parent.grid_columnconfigure(0, weight=1)
	return tree

def recargar_treeview(tree, datos, campos):
	for row in tree.get_children():
		tree.delete(row)
	for d in datos:
		tree.insert('', 'end', iid=d['id'], values=tuple(d[c] for c in campos))

class App(tk.Tk):
	def __init__(self):
		super().__init__()
		aplicar_estilos_ttk()
		self.title('Gestión de Horarios Escolares')
		self.geometry('900x650')
		self.configure(bg='#f4f6fa')
		self._crear_menu()
		self._crear_frame_principal()

	def _crear_menu(self):
		menubar = tk.Menu(self)
		self.config(menu=menubar)

		planes_menu = tk.Menu(menubar, tearoff=0)
		planes_menu.add_command(label='Gestionar Materias', command=self.mostrar_materias)
		planes_menu.add_separator()
		planes_menu.add_command(label='Gestionar Planes de Estudio', command=self.mostrar_planes)
		menubar.add_cascade(label='Plan de estudios', menu=planes_menu)

		turnos_menu = tk.Menu(menubar, tearoff=0)
		turnos_menu.add_command(label='Gestionar Turnos', command=self.mostrar_turnos)
		menubar.add_cascade(label='Turnos', menu=turnos_menu)

		profesores_menu = tk.Menu(menubar, tearoff=0)
		profesores_menu.add_command(label='Gestionar Profesores', command=self.mostrar_profesores)
		menubar.add_cascade(label='Profesores', menu=profesores_menu)

		cursos_menu = tk.Menu(menubar, tearoff=0)
		cursos_menu.add_command(label='Gestionar Cursos', command=self.mostrar_divisiones)
		menubar.add_cascade(label='Cursos', menu=cursos_menu)

		horarios_menu = tk.Menu(menubar, tearoff=0)
		horarios_menu.add_command(label='Por curso', command=self.mostrar_horarios_curso)
		horarios_menu.add_command(label='Por profesor', command=self.mostrar_horarios_profesor)
		menubar.add_cascade(label='Gestión de horarios', menu=horarios_menu)

	def _crear_frame_principal(self):
		self.frame_principal = ttk.Frame(self)
		self.frame_principal.pack(fill='both', expand=True)
		self.label_bienvenida = ttk.Label(
			self.frame_principal,
			text='Bienvenido al sistema de gestión de horarios escolares',
			font=('Segoe UI', 18, 'bold'),
			background='#f4f6fa',
			foreground='#2a3a4a')
		self.label_bienvenida.pack(pady=50)

	def limpiar_frame(self):
		for widget in self.frame_principal.winfo_children():
			widget.destroy()


	def mostrar_materias(self):
		self.limpiar_frame()
		ttk.Label(self.frame_principal, text='Gestión de Materias', font=('Arial', 14)).pack(pady=10)

		# Totales
		materias = obtener_materias()
		total_materias = len(materias)
		total_horas = sum(m['horas_semanales'] for m in materias)
		frame_tot = ttk.Frame(self.frame_principal)
		frame_tot.pack(pady=2)
		ttk.Label(frame_tot, text=f'Total de materias: {total_materias}').grid(row=0, column=0, padx=10)
		ttk.Label(frame_tot, text=f'Total de horas institucionales: {total_horas}').grid(row=0, column=1, padx=10)

		# Filtro
		frame_filtro = ttk.Frame(self.frame_principal)
		frame_filtro.pack(pady=2)
		ttk.Label(frame_filtro, text='Filtro:').grid(row=0, column=0, padx=5)
		self.filtro_materia = tk.StringVar()
		entry_filtro = ttk.Entry(frame_filtro, textvariable=self.filtro_materia)
		entry_filtro.grid(row=0, column=1, padx=5)

		# Tabla de materias usando helper
		frame_tabla = ttk.Frame(self.frame_principal)
		frame_tabla.pack(pady=10, fill='both', expand=True)
		self.tree_materias = crear_treeview(frame_tabla, ('Nombre', 'Horas'), ('Nombre', 'Horas asignadas'))
		self._recargar_materias_tree()

		def filtrar_materias(*args):
			filtro = self.filtro_materia.get().lower()
			materias_filtradas = [m for m in obtener_materias() if filtro in m['nombre'].lower()]
			recargar_treeview(self.tree_materias, materias_filtradas, ['nombre', 'horas_semanales'])
		self.filtro_materia.trace_add('write', filtrar_materias)

		# Formulario de alta/edición
		form = ttk.Frame(self.frame_principal)
		form.pack(pady=10)
		ttk.Label(form, text='Nombre:').grid(row=0, column=0, padx=5, pady=2)
		self.entry_nombre_materia = ttk.Entry(form)
		self.entry_nombre_materia.grid(row=0, column=1, padx=5, pady=2)

		# Botones
		btns = ttk.Frame(self.frame_principal)
		btns.pack(pady=5)
		ttk.Button(btns, text='Agregar', command=self._agregar_materia).grid(row=0, column=0, padx=5)
		ttk.Button(btns, text='Editar', command=self._editar_materia).grid(row=0, column=1, padx=5)
		ttk.Button(btns, text='Eliminar', command=self._eliminar_materia).grid(row=0, column=2, padx=5)

		# Selección en tabla
		self.tree_materias.bind('<<TreeviewSelect>>', self._on_select_materia)
		self.materia_seleccionada_id = None

	def _recargar_materias_tree(self):
		materias_ordenadas = sorted(obtener_materias(), key=lambda m: m['nombre'].lower())
		recargar_treeview(self.tree_materias, materias_ordenadas, ['nombre', 'horas_semanales'])

	# Eliminada: _cargar_materias_en_tree (reemplazada por _recargar_materias_tree)

	def _agregar_materia(self):
		nombre = self.entry_nombre_materia.get().strip()
		if not nombre:
			messagebox.showerror('Error', 'Ingrese un nombre válido.')
			return
		try:
			crear_materia(nombre, 0)
			self._recargar_materias_tree()
			self.entry_nombre_materia.delete(0, tk.END)
		except Exception as e:
			messagebox.showerror('Error', str(e))

	def _on_select_materia(self, event):
		sel = self.tree_materias.selection()
		if sel:
			mid = sel[0]
			vals = self.tree_materias.item(mid, 'values')
			self.entry_nombre_materia.delete(0, tk.END)
			self.entry_nombre_materia.insert(0, vals[0])
			self.materia_seleccionada_id = int(mid)
		else:
			self.materia_seleccionada_id = None

	def _editar_materia(self):
		if not self.materia_seleccionada_id:
			messagebox.showwarning('Atención', 'Seleccione una materia para editar.')
			return
		nombre = self.entry_nombre_materia.get().strip()
		if not nombre:
			messagebox.showerror('Error', 'Ingrese un nombre válido.')
			return
		try:
			horas_actual = [m['horas_semanales'] for m in obtener_materias() if m['id'] == self.materia_seleccionada_id][0]
			actualizar_materia(self.materia_seleccionada_id, nombre, horas_actual)
			self._recargar_materias_tree()
		except Exception as e:
			messagebox.showerror('Error', str(e))

	def _eliminar_materia(self):
		if not self.materia_seleccionada_id:
			messagebox.showwarning('Atención', 'Seleccione una materia para eliminar.')
			return
		if messagebox.askyesno('Confirmar', '¿Está seguro de eliminar la materia seleccionada?'):
			try:
				eliminar_materia(self.materia_seleccionada_id)
				self._recargar_materias_tree()
				self.entry_nombre_materia.delete(0, tk.END)
				self.materia_seleccionada_id = None
			except Exception as e:
				messagebox.showerror('Error', str(e))


	def mostrar_profesores(self):
		self.limpiar_frame()
		ttk.Label(self.frame_principal, text='Gestión de Profesores', font=('Arial', 14)).pack(pady=10)

		# Totales (se actualiza dinámicamente)
		self.label_total_profesores = ttk.Label(self.frame_principal, text='')
		self.label_total_profesores.pack()

		# Filtro por turno
		frame_filtro = ttk.Frame(self.frame_principal)
		frame_filtro.pack(pady=2)
		ttk.Label(frame_filtro, text='Filtro:').grid(row=0, column=0, padx=5)
		self.filtro_profesor = tk.StringVar()
		entry_filtro = ttk.Entry(frame_filtro, textvariable=self.filtro_profesor)
		entry_filtro.grid(row=0, column=1, padx=5)
		ttk.Label(frame_filtro, text='Turno:').grid(row=0, column=2, padx=5)
		turnos = obtener_turnos()
		self.turnos_dict_prof = {t['nombre']: t['id'] for t in turnos}
		self.cb_turno_profesor = ttk.Combobox(frame_filtro, values=['Todos'] + list(self.turnos_dict_prof.keys()), state='readonly')
		self.cb_turno_profesor.set('Todos')
		self.cb_turno_profesor.grid(row=0, column=3, padx=5)

		# Tabla de profesores usando helper
		frame_tabla = ttk.Frame(self.frame_principal)
		frame_tabla.pack(pady=10, fill='both', expand=True)
		self.tree_profesores = crear_treeview(frame_tabla, ('Nombre',), ('Nombre',))
		self._recargar_profesores_tree()

		def filtrar_profesores(*args):
			filtro = self.filtro_profesor.get().lower()
			turno_nombre = self.cb_turno_profesor.get()
			if turno_nombre == 'Todos':
				profesores = obtener_profesores()
			else:
				turno_id = self.turnos_dict_prof[turno_nombre]
				profesores = obtener_profesores_por_turno(turno_id)
			profesores_filtrados = [p for p in profesores if filtro in p['nombre'].lower()]
			recargar_treeview(self.tree_profesores, profesores_filtrados, ['nombre'])
			self.label_total_profesores.config(text=f'Total de profesores: {len(profesores_filtrados)}')
		self.filtro_profesor.trace_add('write', filtrar_profesores)
		self.cb_turno_profesor.bind('<<ComboboxSelected>>', lambda e: filtrar_profesores())
		# Inicializar el total
		self.after(100, filtrar_profesores)

		# Formulario de alta/edición
		form = ttk.Frame(self.frame_principal)
		form.pack(pady=10)
		ttk.Label(form, text='Nombre:').grid(row=0, column=0, padx=5, pady=2)
		self.entry_nombre_profesor = ttk.Entry(form)
		self.entry_nombre_profesor.grid(row=0, column=1, padx=5, pady=2)

		# Botones
		btns = ttk.Frame(self.frame_principal)
		btns.pack(pady=5)
		ttk.Button(btns, text='Agregar', command=self._agregar_profesor).grid(row=0, column=0, padx=5)
		ttk.Button(btns, text='Editar', command=self._editar_profesor).grid(row=0, column=1, padx=5)
		ttk.Button(btns, text='Eliminar', command=self._eliminar_profesor).grid(row=0, column=2, padx=5)
		ttk.Button(btns, text='Banca de horas', command=self._gestionar_banca_profesor).grid(row=0, column=3, padx=5)
		ttk.Button(btns, text='Turnos del profesor', command=self._gestionar_turnos_profesor).grid(row=0, column=4, padx=5)

		# Selección en tabla
		self.tree_profesores.bind('<<TreeviewSelect>>', self._on_select_profesor)
		self.profesor_seleccionado_id = None

	def _recargar_profesores_tree(self):
		profesores_ordenados = sorted(obtener_profesores(), key=lambda p: p['nombre'].lower())
		recargar_treeview(self.tree_profesores, profesores_ordenados, ['nombre'])

	# Eliminada: _cargar_profesores_en_tree (reemplazada por _recargar_profesores_tree)

	def _agregar_profesor(self):
		nombre = self.entry_nombre_profesor.get().strip()
		if not nombre:
			messagebox.showerror('Error', 'Ingrese un nombre válido.')
			return
		try:
			crear_profesor(nombre)
			self._recargar_profesores_tree()
			self.entry_nombre_profesor.delete(0, tk.END)
		except Exception as e:
			messagebox.showerror('Error', str(e))

	def _on_select_profesor(self, event):
		sel = self.tree_profesores.selection()
		if sel:
			pid = sel[0]
			vals = self.tree_profesores.item(pid, 'values')
			self.entry_nombre_profesor.delete(0, tk.END)
			self.entry_nombre_profesor.insert(0, vals[0])
			self.profesor_seleccionado_id = int(pid)
		else:
			self.profesor_seleccionado_id = None

	def _editar_profesor(self):
		if not self.profesor_seleccionado_id:
			messagebox.showwarning('Atención', 'Seleccione un profesor para editar.')
			return
		nombre = self.entry_nombre_profesor.get().strip()
		if not nombre:
			messagebox.showerror('Error', 'Ingrese un nombre válido.')
			return
		try:
			actualizar_profesor(self.profesor_seleccionado_id, nombre)
			self._recargar_profesores_tree()
		except Exception as e:
			messagebox.showerror('Error', str(e))

	def _eliminar_profesor(self):
		if not self.profesor_seleccionado_id:
			messagebox.showwarning('Atención', 'Seleccione un profesor para eliminar.')
			return
		if messagebox.askyesno('Confirmar', '¿Está seguro de eliminar el profesor seleccionado?'):
			try:
				eliminar_profesor(self.profesor_seleccionado_id)
				self._recargar_profesores_tree()
				self.entry_nombre_profesor.delete(0, tk.END)
				self.profesor_seleccionado_id = None
			except Exception as e:
				messagebox.showerror('Error', str(e))

	def _gestionar_banca_profesor(self):
		if not self.profesor_seleccionado_id:
			messagebox.showwarning('Atención', 'Seleccione un profesor para ver sus horas asignadas.')
			return
		self._abrir_ventana_banca_profesor(self.profesor_seleccionado_id)

	def _abrir_ventana_banca_profesor(self, profesor_id):
		win = tk.Toplevel(self)
		win.configure(bg='#f4f6fa')
		win.title('Materias asignadas al profesor')
		win.geometry('550x450')
		win.minsize(550, 450)
		win.transient(self)
		win.grab_set()
		win.focus_force()
		ttk.Label(win, text='Materias asignadas y horas ocupadas', font=('Arial', 12)).pack(pady=8)

		# Tabla de banca con frame para expansión
		frame_tabla = ttk.Frame(win)
		frame_tabla.pack(pady=5, padx=10, fill='both', expand=True)
		
		tree_banca = ttk.Treeview(frame_tabla, columns=('Materia', 'Horas'), show='headings')
		tree_banca.heading('Materia', text='Materia')
		tree_banca.heading('Horas', text='Horas asignadas')
		tree_banca.pack(side='left', fill='both', expand=True)
		
		# Scrollbar para la tabla
		vsb = ttk.Scrollbar(frame_tabla, orient='vertical', command=tree_banca.yview)
		tree_banca.configure(yscroll=vsb.set)
		vsb.pack(side='right', fill='y')

		def cargar_banca():
			for row in tree_banca.get_children():
				tree_banca.delete(row)
			for b in obtener_banca_profesor(profesor_id):
				tree_banca.insert('', 'end', iid=b['id'], values=(b['materia'], b['banca_horas']))

		cargar_banca()

		# Formulario para asignar materia
		form = ttk.Frame(win)
		form.pack(pady=5)
		ttk.Label(form, text='Materia:').grid(row=0, column=0, padx=5, pady=2)
		materias = obtener_materias()
		materia_nombres = [m['nombre'] for m in materias]
		materia_ids = {m['nombre']: m['id'] for m in materias}
		cb_materia = ttk.Combobox(form, values=materia_nombres, state='normal')
		cb_materia.grid(row=0, column=1, padx=5, pady=2)
		cb_materia.focus_set()
		def filtrar_materias(event):
			typed = cb_materia.get().lower()
			filtradas = [m for m in materia_nombres if typed in m.lower()]
			cb_materia['values'] = filtradas if filtradas else materia_nombres
		cb_materia.bind('<KeyRelease>', filtrar_materias)

		def agregar_materia(event=None):
			materia = cb_materia.get()
			if not materia:
				messagebox.showerror('Error', 'Seleccione una materia.')
				return
			try:
				# Asignar con horas 0 (se irán sumando por horario)
				asignar_banca_profesor(profesor_id, materia_ids[materia], 0)
				cargar_banca()
			except Exception as e:
				messagebox.showerror('Error', str(e))

		def eliminar_materia(event=None):
			sel = tree_banca.selection()
			if not sel:
				messagebox.showwarning('Atención', 'Seleccione una materia para eliminar.')
				return
			if messagebox.askyesno('Confirmar', '¿Eliminar materia asignada al profesor?'):
				try:
					eliminar_banca_profesor(int(sel[0]))
					cargar_banca()
				except Exception as e:
					messagebox.showerror('Error', str(e))

		btns = ttk.Frame(win)
		btns.pack(pady=5)
		btn_agregar = ttk.Button(btns, text='Agregar materia', command=agregar_materia)
		btn_agregar.grid(row=0, column=0, padx=5)
		btn_eliminar = ttk.Button(btns, text='Eliminar materia', command=eliminar_materia)
		btn_eliminar.grid(row=0, column=1, padx=5)
		# Accesibilidad con Enter
		cb_materia.bind('<Return>', agregar_materia)
		btn_agregar.bind('<Return>', lambda e: agregar_materia())
		btn_eliminar.bind('<Return>', lambda e: eliminar_materia())

	def _eliminar_division(self):
		if not self.division_seleccionada_id:
			messagebox.showerror('Error', 'Seleccione una división para eliminar.')
			return
		if not messagebox.askyesno('Confirmar', '¿Está seguro de eliminar la división seleccionada?'):
			return
		try:
			eliminar_division(self.division_seleccionada_id)
			self._recargar_divisiones_tree()
			self.division_seleccionada_id = None
		except Exception as e:
			messagebox.showerror('Error', str(e))


	def mostrar_divisiones(self):
		self.limpiar_frame()
		ttk.Label(self.frame_principal, text='Gestión de Cursos', font=('Arial', 14)).pack(pady=10)

		# Totales
		divisiones = obtener_divisiones()
		total_divisiones = len(divisiones)
		frame_tot = ttk.Frame(self.frame_principal)
		frame_tot.pack(pady=2)
		self.label_total_divisiones = ttk.Label(frame_tot, text=f'Total de divisiones: {total_divisiones}')
		self.label_total_divisiones.grid(row=0, column=0, padx=10)

		# Selección de Turno, Plan, Año
		frame_sel = ttk.Frame(self.frame_principal)
		frame_sel.pack(pady=5)
		ttk.Label(frame_sel, text='Turno:').grid(row=0, column=0, padx=5)
		turnos = obtener_turnos()
		self.turnos_dict = {t['nombre']: t['id'] for t in turnos}
		self.cb_turno_division = ttk.Combobox(frame_sel, values=list(self.turnos_dict.keys()), state='readonly')
		self.cb_turno_division.grid(row=0, column=1, padx=5)
		ttk.Label(frame_sel, text='Plan:').grid(row=0, column=2, padx=5)
		self.cb_plan_division = ttk.Combobox(frame_sel, values=[], state='disabled')
		self.cb_plan_division.grid(row=0, column=3, padx=5)
		ttk.Label(frame_sel, text='Año:').grid(row=0, column=4, padx=5)
		self.cb_anio_division = ttk.Combobox(frame_sel, values=[], state='disabled')
		self.cb_anio_division.grid(row=0, column=5, padx=5)

		def on_turno_selected(event=None):
			turno_nombre = self.cb_turno_division.get()
			if not turno_nombre:
				self.cb_plan_division['values'] = []
				self.cb_plan_division.set('')
				self.cb_plan_division.config(state='disabled')
				self.cb_anio_division['values'] = []
				self.cb_anio_division.set('')
				self.cb_anio_division.config(state='disabled')
				return
			turno_id = self.turnos_dict[turno_nombre]
			planes = obtener_planes_de_turno(turno_id)
			self.planes_dict = {p['nombre']: p['id'] for p in planes}
			self.cb_plan_division['values'] = list(self.planes_dict.keys())
			self.cb_plan_division.set('')
			self.cb_plan_division.config(state='readonly' if planes else 'disabled')
			self.cb_anio_division['values'] = []
			self.cb_anio_division.set('')
			self.cb_anio_division.config(state='disabled')
			# Pasar focus a Plan
			if planes:
				self.cb_plan_division.focus_set()
			self._recargar_divisiones_tree()
		def on_plan_selected(event=None):
			plan_nombre = self.cb_plan_division.get()
			if not plan_nombre:
				self.cb_anio_division['values'] = []
				self.cb_anio_division.set('')
				self.cb_anio_division.config(state='disabled')
				return
			plan_id = self.planes_dict[plan_nombre]
			anios = obtener_anios(plan_id)
			self.cb_anio_division['values'] = [a['nombre'] for a in anios]
			self.cb_anio_division.set('')
			self.cb_anio_division.config(state='readonly' if anios else 'disabled')
			# Pasar focus a Año
			if anios:
				self.cb_anio_division.focus_set()
			self._recargar_divisiones_tree()
		def on_anio_selected(event=None):
			self._recargar_divisiones_tree()
		self.cb_turno_division.bind('<<ComboboxSelected>>', on_turno_selected)
		self.cb_plan_division.bind('<<ComboboxSelected>>', on_plan_selected)
		self.cb_anio_division.bind('<<ComboboxSelected>>', on_anio_selected)
		
		# Focus inicial en Turno
		self.cb_turno_division.focus_set()

		# Tabla de divisiones usando helper
		frame_tabla = ttk.Frame(self.frame_principal)
		frame_tabla.pack(pady=10, fill='both', expand=True)
		self.tree_divisiones = crear_treeview(frame_tabla, ('Turno', 'Plan', 'Año', 'División'), ('Turno', 'Plan', 'Año', 'División'))
		self._recargar_divisiones_tree()

		# Botones
		btns = ttk.Frame(self.frame_principal)
		btns.pack(pady=5)
		ttk.Button(btns, text='Agregar', command=self._agregar_division).grid(row=0, column=0, padx=5)
		ttk.Button(btns, text='Editar', command=self._editar_division).grid(row=0, column=1, padx=5)
		ttk.Button(btns, text='Eliminar', command=self._eliminar_division).grid(row=0, column=2, padx=5)

		# Selección en tabla
		self.tree_divisiones.bind('<<TreeviewSelect>>', self._on_select_division)
		self.division_seleccionada_id = None

	def _recargar_divisiones_tree(self):
		divisiones = obtener_divisiones()
		
		# Obtener filtros seleccionados
		turno_nombre = self.cb_turno_division.get()
		plan_nombre = self.cb_plan_division.get()
		anio_nombre = self.cb_anio_division.get()
		
		datos = []
		for c in divisiones:
			turno = next((t['nombre'] for t in obtener_turnos() if t['id'] == c['turno_id']), '')
			plan = next((p['nombre'] for p in obtener_planes() if p['id'] == c['plan_id']), '')
			anio = next((a['nombre'] for a in obtener_anios(c['plan_id']) if a['id'] == c['anio_id']), '')
			
			# Aplicar filtros
			if turno_nombre and turno != turno_nombre:
				continue
			if plan_nombre and plan != plan_nombre:
				continue
			if anio_nombre and anio != anio_nombre:
				continue
			
			datos.append({'id': c['id'], 'Turno': turno, 'Plan': plan, 'Año': anio, 'División': c['nombre']})
		
		recargar_treeview(self.tree_divisiones, datos, ['Turno', 'Plan', 'Año', 'División'])
		
		# Actualizar contador de divisiones
		self.label_total_divisiones.config(text=f'Total de divisiones: {len(datos)}')

	# Eliminada: _cargar_divisiones_en_tree (reemplazada por _recargar_divisiones_tree)

	def _agregar_division(self):
		win = tk.Toplevel(self)
		win.configure(bg='#f4f6fa')
		win.title('Agregar División')
		win.geometry('450x250')
		win.minsize(450, 250)
		win.transient(self)
		win.grab_set()
		win.focus_force()
		
		ttk.Label(win, text='Nueva División', font=('Arial', 12)).pack(pady=10)
		
		# Formulario
		form = ttk.Frame(win)
		form.pack(pady=10)
		
		ttk.Label(form, text='Turno:').grid(row=0, column=0, padx=5, pady=5, sticky='e')
		turnos = obtener_turnos()
		turnos_dict = {t['nombre']: t['id'] for t in turnos}
		cb_turno = ttk.Combobox(form, values=list(turnos_dict.keys()), state='readonly', width=25)
		cb_turno.grid(row=0, column=1, padx=5, pady=5)
		cb_turno.focus_set()
		
		ttk.Label(form, text='Plan:').grid(row=1, column=0, padx=5, pady=5, sticky='e')
		cb_plan = ttk.Combobox(form, values=[], state='disabled', width=25)
		cb_plan.grid(row=1, column=1, padx=5, pady=5)
		
		ttk.Label(form, text='Año:').grid(row=2, column=0, padx=5, pady=5, sticky='e')
		cb_anio = ttk.Combobox(form, values=[], state='disabled', width=25)
		cb_anio.grid(row=2, column=1, padx=5, pady=5)
		
		ttk.Label(form, text='División:').grid(row=3, column=0, padx=5, pady=5, sticky='e')
		entry_division = ttk.Entry(form, width=27)
		entry_division.grid(row=3, column=1, padx=5, pady=5)
		
		planes_dict = {}
		anios_list = []
		
		def on_turno_selected(event=None):
			turno_nombre = cb_turno.get()
			if not turno_nombre:
				cb_plan['values'] = []
				cb_plan.set('')
				cb_plan.config(state='disabled')
				cb_anio['values'] = []
				cb_anio.set('')
				cb_anio.config(state='disabled')
				return
			turno_id = turnos_dict[turno_nombre]
			planes = obtener_planes_de_turno(turno_id)
			planes_dict.clear()
			planes_dict.update({p['nombre']: p['id'] for p in planes})
			cb_plan['values'] = list(planes_dict.keys())
			cb_plan.set('')
			cb_plan.config(state='readonly' if planes else 'disabled')
			cb_anio['values'] = []
			cb_anio.set('')
			cb_anio.config(state='disabled')
			if planes:
				cb_plan.focus_set()
		
		def on_plan_selected(event=None):
			plan_nombre = cb_plan.get()
			if not plan_nombre:
				cb_anio['values'] = []
				cb_anio.set('')
				cb_anio.config(state='disabled')
				return
			plan_id = planes_dict[plan_nombre]
			anios = obtener_anios(plan_id)
			anios_list.clear()
			anios_list.extend(anios)
			cb_anio['values'] = [a['nombre'] for a in anios]
			cb_anio.set('')
			cb_anio.config(state='readonly' if anios else 'disabled')
			if anios:
				cb_anio.focus_set()
		
		def on_anio_selected(event=None):
			entry_division.focus_set()
		
		cb_turno.bind('<<ComboboxSelected>>', on_turno_selected)
		cb_plan.bind('<<ComboboxSelected>>', on_plan_selected)
		cb_anio.bind('<<ComboboxSelected>>', on_anio_selected)
		
		def guardar(event=None):
			nombre = entry_division.get().strip()
			if not nombre:
				messagebox.showerror('Error', 'Ingrese un nombre de división válido.', parent=win)
				return
			turno_nombre = cb_turno.get()
			plan_nombre = cb_plan.get()
			anio_nombre = cb_anio.get()
			if not (turno_nombre and plan_nombre and anio_nombre):
				messagebox.showerror('Error', 'Seleccione turno, plan y año.', parent=win)
				return
			turno_id = turnos_dict[turno_nombre]
			plan_id = planes_dict[plan_nombre]
			anio_id = next((a['id'] for a in anios_list if a['nombre'] == anio_nombre), None)
			if not anio_id:
				messagebox.showerror('Error', 'Año inválido.', parent=win)
				return
			try:
				conn = get_connection()
				c = conn.cursor()
				c.execute('INSERT INTO division (nombre, turno_id, plan_id, anio_id) VALUES (?, ?, ?, ?)', 
						  (nombre, turno_id, plan_id, anio_id))
				conn.commit()
				conn.close()
				self._recargar_divisiones_tree()
				win.destroy()
			except Exception as e:
				if 'UNIQUE constraint failed' in str(e):
					messagebox.showerror('Error', 'Ya existe una división con ese nombre, turno, plan y año.', parent=win)
				else:
					messagebox.showerror('Error', str(e), parent=win)
		
		# Botones
		btns = ttk.Frame(win)
		btns.pack(pady=10)
		ttk.Button(btns, text='Guardar', command=guardar).grid(row=0, column=0, padx=5)
		ttk.Button(btns, text='Cancelar', command=win.destroy).grid(row=0, column=1, padx=5)
		
		entry_division.bind('<Return>', guardar)

	def _editar_division(self):
		if not self.division_seleccionada_id:
			messagebox.showerror('Error', 'Seleccione una división para editar.')
			return
		
		# Obtener datos de la división seleccionada
		divisiones = obtener_divisiones()
		division_actual = next((x for x in divisiones if str(x['id']) == str(self.division_seleccionada_id)), None)
		if not division_actual:
			messagebox.showerror('Error', 'División no encontrada.')
			return
		
		win = tk.Toplevel(self)
		win.configure(bg='#f4f6fa')
		win.title('Editar División')
		win.geometry('450x250')
		win.minsize(450, 250)
		win.transient(self)
		win.grab_set()
		win.focus_force()
		
		ttk.Label(win, text='Editar División', font=('Arial', 12)).pack(pady=10)
		
		# Formulario
		form = ttk.Frame(win)
		form.pack(pady=10)
		
		ttk.Label(form, text='Turno:').grid(row=0, column=0, padx=5, pady=5, sticky='e')
		turnos = obtener_turnos()
		turnos_dict = {t['nombre']: t['id'] for t in turnos}
		cb_turno = ttk.Combobox(form, values=list(turnos_dict.keys()), state='readonly', width=25)
		cb_turno.grid(row=0, column=1, padx=5, pady=5)
		
		ttk.Label(form, text='Plan:').grid(row=1, column=0, padx=5, pady=5, sticky='e')
		cb_plan = ttk.Combobox(form, values=[], state='disabled', width=25)
		cb_plan.grid(row=1, column=1, padx=5, pady=5)
		
		ttk.Label(form, text='Año:').grid(row=2, column=0, padx=5, pady=5, sticky='e')
		cb_anio = ttk.Combobox(form, values=[], state='disabled', width=25)
		cb_anio.grid(row=2, column=1, padx=5, pady=5)
		
		ttk.Label(form, text='División:').grid(row=3, column=0, padx=5, pady=5, sticky='e')
		entry_division = ttk.Entry(form, width=27)
		entry_division.grid(row=3, column=1, padx=5, pady=5)
		entry_division.insert(0, division_actual['nombre'])
		
		planes_dict = {}
		anios_list = []
		
		def on_turno_selected(event=None):
			turno_nombre = cb_turno.get()
			if not turno_nombre:
				cb_plan['values'] = []
				cb_plan.set('')
				cb_plan.config(state='disabled')
				cb_anio['values'] = []
				cb_anio.set('')
				cb_anio.config(state='disabled')
				return
			turno_id = turnos_dict[turno_nombre]
			planes = obtener_planes_de_turno(turno_id)
			planes_dict.clear()
			planes_dict.update({p['nombre']: p['id'] for p in planes})
			cb_plan['values'] = list(planes_dict.keys())
			cb_plan.config(state='readonly' if planes else 'disabled')
			# Mantener selección si es el mismo turno
			if event is None:
				plan_actual = next((p['nombre'] for p in obtener_planes() if p['id'] == division_actual['plan_id']), '')
				if plan_actual in planes_dict:
					cb_plan.set(plan_actual)
					cb_plan.event_generate('<<ComboboxSelected>>')
			else:
				cb_plan.set('')
				cb_anio['values'] = []
				cb_anio.set('')
				cb_anio.config(state='disabled')
		
		def on_plan_selected(event=None):
			plan_nombre = cb_plan.get()
			if not plan_nombre:
				cb_anio['values'] = []
				cb_anio.set('')
				cb_anio.config(state='disabled')
				return
			plan_id = planes_dict[plan_nombre]
			anios = obtener_anios(plan_id)
			anios_list.clear()
			anios_list.extend(anios)
			cb_anio['values'] = [a['nombre'] for a in anios]
			cb_anio.config(state='readonly' if anios else 'disabled')
			# Mantener selección si es el mismo plan
			if event is None:
				anio_actual = next((a['nombre'] for a in obtener_anios(division_actual['plan_id']) if a['id'] == division_actual['anio_id']), '')
				if anio_actual in [a['nombre'] for a in anios]:
					cb_anio.set(anio_actual)
			else:
				cb_anio.set('')
		
		cb_turno.bind('<<ComboboxSelected>>', on_turno_selected)
		cb_plan.bind('<<ComboboxSelected>>', on_plan_selected)
		
		# Precargar datos actuales
		turno_actual = next((t['nombre'] for t in turnos if t['id'] == division_actual['turno_id']), '')
		cb_turno.set(turno_actual)
		on_turno_selected()
		
		def guardar(event=None):
			nombre = entry_division.get().strip()
			if not nombre:
				messagebox.showerror('Error', 'Ingrese un nombre de división válido.', parent=win)
				return
			turno_nombre = cb_turno.get()
			plan_nombre = cb_plan.get()
			anio_nombre = cb_anio.get()
			if not (turno_nombre and plan_nombre and anio_nombre):
				messagebox.showerror('Error', 'Complete todos los campos.', parent=win)
				return
			turno_id = turnos_dict[turno_nombre]
			plan_id = planes_dict[plan_nombre]
			anio_id = next((a['id'] for a in anios_list if a['nombre'] == anio_nombre), None)
			if not anio_id:
				messagebox.showerror('Error', 'Año inválido.', parent=win)
				return
			try:
				conn = get_connection()
				c = conn.cursor()
				c.execute('UPDATE division SET nombre=?, turno_id=?, plan_id=?, anio_id=? WHERE id=?', 
						  (nombre, turno_id, plan_id, anio_id, self.division_seleccionada_id))
				conn.commit()
				conn.close()
				self._recargar_divisiones_tree()
				win.destroy()
			except Exception as e:
				if 'UNIQUE constraint failed' in str(e):
					messagebox.showerror('Error', 'Ya existe una división con ese nombre, turno, plan y año.', parent=win)
				else:
					messagebox.showerror('Error', str(e), parent=win)
		
		# Botones
		btns = ttk.Frame(win)
		btns.pack(pady=10)
		ttk.Button(btns, text='Guardar', command=guardar).grid(row=0, column=0, padx=5)
		ttk.Button(btns, text='Cancelar', command=win.destroy).grid(row=0, column=1, padx=5)
		
		entry_division.bind('<Return>', guardar)
		entry_division.focus_set()

	def _on_select_division(self, event=None):
		sel = self.tree_divisiones.selection()
		if not sel:
			self.division_seleccionada_id = None
			return
		cid = sel[0]
		self.division_seleccionada_id = cid

	def mostrar_horarios_curso(self):
		self.limpiar_frame()
		ttk.Label(self.frame_principal, text='Gestión de Horarios por Curso', font=('Arial', 14)).pack(pady=10)

		# Selección paso a paso: Turno → Plan → Año → División
		frame_sel = ttk.Frame(self.frame_principal)
		frame_sel.pack(pady=5)
		ttk.Label(frame_sel, text='Turno:').grid(row=0, column=0, padx=5)
		turnos = obtener_turnos()
		self.turnos_dict_horario = {t['nombre']: t['id'] for t in turnos}
		self.cb_turno_horario = ttk.Combobox(frame_sel, values=list(self.turnos_dict_horario.keys()), state='readonly')
		self.cb_turno_horario.grid(row=0, column=1, padx=5)
		# Autocompletar turno si solo hay uno
		turno_autocompletado = autocompletar_combobox(self.cb_turno_horario, list(self.turnos_dict_horario.keys()), incluir_vacio=False)
		ttk.Label(frame_sel, text='Plan:').grid(row=0, column=2, padx=5)
		self.cb_plan_horario = ttk.Combobox(frame_sel, values=[], state='disabled')
		self.cb_plan_horario.grid(row=0, column=3, padx=5)
		ttk.Label(frame_sel, text='Año:').grid(row=0, column=4, padx=5)
		self.cb_anio_horario = ttk.Combobox(frame_sel, values=[], state='disabled')
		self.cb_anio_horario.grid(row=0, column=5, padx=5)
		ttk.Label(frame_sel, text='División:').grid(row=0, column=6, padx=5)
		self.cb_division_horario = ttk.Combobox(frame_sel, values=[], state='disabled')
		self.cb_division_horario.grid(row=0, column=7, padx=5)

		def on_turno_selected(event=None):
			turno_nombre = self.cb_turno_horario.get()
			if not turno_nombre:
				self.cb_plan_horario['values'] = []
				self.cb_plan_horario.set('')
				self.cb_plan_horario.config(state='disabled')
				self.cb_anio_horario['values'] = []
				self.cb_anio_horario.set('')
				self.cb_anio_horario.config(state='disabled')
				self.cb_division_horario['values'] = []
				self.cb_division_horario.set('')
				self.cb_division_horario.config(state='disabled')
				return
			turno_id = self.turnos_dict_horario[turno_nombre]
			planes = obtener_planes_de_turno(turno_id)
			self.planes_dict_horario = {p['nombre']: p['id'] for p in planes}
			plan_nombres = list(self.planes_dict_horario.keys())
			autocompletar_combobox(self.cb_plan_horario, plan_nombres, incluir_vacio=False)
			# Enfocar el siguiente combobox
			self.cb_plan_horario.focus_set()
			self.cb_anio_horario['values'] = []
			self.cb_anio_horario.set('')
			self.cb_anio_horario.config(state='disabled')
			self.cb_division_horario['values'] = []
			self.cb_division_horario.set('')
			self.cb_division_horario.config(state='disabled')
		def on_plan_selected(event=None):
			plan_nombre = self.cb_plan_horario.get()
			if not plan_nombre:
				self.cb_anio_horario['values'] = []
				self.cb_anio_horario.set('')
				self.cb_anio_horario.config(state='disabled')
				self.cb_division_horario['values'] = []
				self.cb_division_horario.set('')
				self.cb_division_horario.config(state='disabled')
				return
			plan_id = self.planes_dict_horario[plan_nombre]
			anios = obtener_anios(plan_id)
			self.anios_dict_horario = {a['nombre']: a['id'] for a in anios}
			anio_nombres = list(self.anios_dict_horario.keys())
			autocompletar_combobox(self.cb_anio_horario, anio_nombres, incluir_vacio=False)
			# Enfocar el siguiente combobox
			self.cb_anio_horario.focus_set()
			self.cb_division_horario['values'] = []
			self.cb_division_horario.set('')
			self.cb_division_horario.config(state='disabled')
		def on_anio_selected(event=None):
			anio_nombre = self.cb_anio_horario.get()
			if not anio_nombre:
				self.cb_division_horario['values'] = []
				self.cb_division_horario.set('')
				self.cb_division_horario.config(state='disabled')
				return
			anio_id = self.anios_dict_horario[anio_nombre]
			# Filtrar divisiones por turno, plan y año
			turno_nombre = self.cb_turno_horario.get()
			plan_nombre = self.cb_plan_horario.get()
			if not (turno_nombre and plan_nombre):
				self.cb_division_horario['values'] = []
				self.cb_division_horario.set('')
				self.cb_division_horario.config(state='disabled')
				return
			turno_id = self.turnos_dict_horario[turno_nombre]
			plan_id = self.planes_dict_horario[plan_nombre]
			divisiones = [c for c in obtener_divisiones() if c['turno_id'] == turno_id and c['plan_id'] == plan_id and c['anio_id'] == anio_id]
			self.divisiones_dict_horario = {c['nombre']: c['id'] for c in divisiones}
			division_nombres = list(self.divisiones_dict_horario.keys())
			autocompletar_combobox(self.cb_division_horario, division_nombres, incluir_vacio=False)
			# Enfocar el siguiente combobox
			self.cb_division_horario.focus_set()
		def on_division_selected(event=None):
			self._dibujar_grilla_horario_curso()
		self.cb_turno_horario.bind('<<ComboboxSelected>>', on_turno_selected)
		self.cb_plan_horario.bind('<<ComboboxSelected>>', on_plan_selected)
		self.cb_anio_horario.bind('<<ComboboxSelected>>', on_anio_selected)
		self.cb_division_horario.bind('<<ComboboxSelected>>', on_division_selected)
		
		# Si el turno se autocompletó, trigger inicial
		if turno_autocompletado:
			on_turno_selected()

		self.espacios_por_dia = 8
		
		# Frame contenedor con Canvas y Scrollbar para la grilla de horarios
		container_grilla = ttk.Frame(self.frame_principal)
		container_grilla.pack(pady=10, expand=True, fill='both')
		
		# Canvas con scrollbar
		self.canvas_horario = tk.Canvas(container_grilla, bg='#f4f6fa', highlightthickness=0)
		scrollbar_horario = ttk.Scrollbar(container_grilla, orient='vertical', command=self.canvas_horario.yview)
		self.canvas_horario.configure(yscrollcommand=scrollbar_horario.set)
		
		scrollbar_horario.pack(side='right', fill='y')
		self.canvas_horario.pack(side='left', fill='both', expand=True)
		
		# Frame dentro del canvas para la grilla
		self.frame_grilla_horario = ttk.Frame(self.canvas_horario)
		self.canvas_window = self.canvas_horario.create_window((0, 0), window=self.frame_grilla_horario, anchor='nw')
		
		# Actualizar scroll region cuando cambie el tamaño del frame
		def actualizar_scroll_region(event=None):
			self.canvas_horario.update_idletasks()
			self.canvas_horario.configure(scrollregion=(0, 0, self.frame_grilla_horario.winfo_reqwidth(), self.frame_grilla_horario.winfo_reqheight()))
		self.frame_grilla_horario.bind('<Configure>', actualizar_scroll_region)
		
		# Ajustar el ancho del frame al canvas
		def ajustar_ancho_canvas(event):
			canvas_width = event.width
			self.canvas_horario.itemconfig(self.canvas_window, width=canvas_width)
		self.canvas_horario.bind('<Configure>', ajustar_ancho_canvas)
		
		# Permitir scroll con la rueda del mouse solo cuando el cursor está sobre el canvas
		def on_mousewheel(event):
			self.canvas_horario.yview_scroll(int(-1*(event.delta/120)), "units")
		
		def bind_mousewheel(event):
			self.canvas_horario.bind_all("<MouseWheel>", on_mousewheel)
		
		def unbind_mousewheel(event):
			self.canvas_horario.unbind_all("<MouseWheel>")
		
		self.canvas_horario.bind('<Enter>', bind_mousewheel)
		self.canvas_horario.bind('<Leave>', unbind_mousewheel)

		# Botón para configurar horas por turno en la parte baja (siempre visible)
		frame_bottom_btns = ttk.Frame(self.frame_principal)
		frame_bottom_btns.pack(pady=6)
		ttk.Button(frame_bottom_btns, text='Configurar horas por turno', command=self._configurar_horas_por_turno).pack(side='left', padx=5)
		ttk.Button(frame_bottom_btns, text='Limpiar horarios vacíos', command=self._limpiar_horarios_vacios_curso).pack(side='left', padx=5)
		
		# Enfocar el primer combobox al entrar
		self.cb_turno_horario.focus_set()

	def _dibujar_grilla_horario_curso(self):
		for widget in self.frame_grilla_horario.winfo_children():
			widget.destroy()
		division_nombre = getattr(self, 'cb_division_horario', None)
		if not division_nombre or not self.cb_division_horario.get():
			return
		division_id = self.divisiones_dict_horario[self.cb_division_horario.get()]
		dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
		horarios = obtener_horarios(division_id)
		matriz = {(h['dia'], h['espacio']): h for h in horarios}
		
		# Configurar columnas: la primera (índices) sin weight, las demás con weight igual
		for col, dia in enumerate([''] + dias):
			if col == 0:
				# Primera columna: tamaño fijo, sin expandir
				self.frame_grilla_horario.grid_columnconfigure(col, weight=0, minsize=50)
			else:
				# Columnas de días: mismo weight para ancho uniforme
				self.frame_grilla_horario.grid_columnconfigure(col, weight=1, minsize=120)
			
			if col == 0:
				ttk.Label(self.frame_grilla_horario, text='', font=('Segoe UI', 10, 'bold'), background='#f4f6fa').grid(row=0, column=col, padx=(0,0), pady=2, sticky='nsew')
			else:
				ttk.Label(self.frame_grilla_horario, text=dia, font=('Segoe UI', 10, 'bold'), background='#e0e7ef', foreground='#2a3a4a').grid(row=0, column=col, padx=(0,0), pady=2, sticky='nsew')

		# Guardar referencias a los botones para poder actualizar su wraplength dinámicamente
		self._grilla_botones = []
		for esp in range(1, self.espacios_por_dia+1):
			self.frame_grilla_horario.grid_rowconfigure(esp, weight=1, minsize=38)
			etiqueta = f"{esp}ª"
			ttk.Label(self.frame_grilla_horario, text=etiqueta, font=('Segoe UI', 10, 'bold'), background='#e0e7ef', foreground='#2a3a4a', anchor='center').grid(row=esp, column=0, padx=(0,0), pady=2, sticky='nsew')
			fila_botones = []
			for col, dia in enumerate(dias, start=1):
				h = matriz.get((dia, esp))
				texto = ''
				if h:
					texto = f"{h['materia'] or ''}\n{h['profesor'] or ''}\n{h['hora_inicio'] or ''}-{h['hora_fin'] or ''}"
				btn = tk.Button(self.frame_grilla_horario, text=texto, wraplength=100, anchor='w', justify='left',
								bg='#ffffff', relief='ridge', bd=1,
								command=lambda d=dia, e=esp: self._editar_espacio_horario_curso(d, e))
				btn.grid(row=esp, column=col, padx=1, pady=1, sticky='nsew')
				fila_botones.append(btn)
			self._grilla_botones.append(fila_botones)

		# Función para actualizar el wraplength de los botones según el tamaño de la celda
		def actualizar_wraplength(event=None):
			for esp, fila in enumerate(self._grilla_botones):
				for col, btn in enumerate(fila):
					info = btn.grid_info()
					col_idx = info['column']
					# Obtener el ancho real de la celda
					width = self.frame_grilla_horario.grid_bbox(col_idx, esp+1)[2]
					# Dejar un pequeño margen
					btn.config(wraplength=max(width-8, 60))
		self.frame_grilla_horario.bind('<Configure>', actualizar_wraplength)
		self.after(100, lambda: self.frame_grilla_horario.event_generate('<Configure>'))
		
		# Actualizar la región de scroll después de dibujar la grilla
		def actualizar_scroll():
			self.frame_grilla_horario.update_idletasks()
			self.canvas_horario.configure(scrollregion=(0, 0, self.frame_grilla_horario.winfo_reqwidth(), self.frame_grilla_horario.winfo_reqheight()))
			self.canvas_horario.yview_moveto(0)  # Resetear scroll a la parte superior
		self.after(150, actualizar_scroll)

	def _limpiar_horarios_vacios_curso(self):
		"""Elimina horarios que solo tienen hora de inicio y fin, sin materia ni profesor"""
		division_nombre = getattr(self, 'cb_division_horario', None)
		if not division_nombre or not self.cb_division_horario.get():
			messagebox.showwarning('Advertencia', 'Seleccione una división primero.')
			return
		
		division_id = self.divisiones_dict_horario[self.cb_division_horario.get()]
		
		if not messagebox.askyesno('Confirmar', '¿Eliminar todos los horarios que solo contengan hora de inicio y fin?\n\nLos horarios con materia o profesor asignados no serán eliminados.'):
			return
		
		try:
			conn = get_connection()
			c = conn.cursor()
			# Eliminar horarios que solo tengan horas pero no materia ni profesor
			c.execute('''DELETE FROM horario 
						WHERE division_id = ? 
						AND (materia_id IS NULL OR materia_id = '') 
						AND (profesor_id IS NULL OR profesor_id = '')
						AND (hora_inicio IS NOT NULL OR hora_fin IS NOT NULL)''', (division_id,))
			eliminados = c.rowcount
			conn.commit()
			conn.close()
			
			messagebox.showinfo('Éxito', f'Se eliminaron {eliminados} horarios vacíos.')
			self._dibujar_grilla_horario_curso()
		except Exception as e:
			messagebox.showerror('Error', f'Error al limpiar horarios: {str(e)}')

	def _editar_espacio_horario_curso(self, dia, espacio):
		division_nombre = getattr(self, 'cb_division_horario', None)
		if not division_nombre or not self.cb_division_horario.get():
			return
		division_id = self.divisiones_dict_horario[self.cb_division_horario.get()]
		win = tk.Toplevel(self)
		win.configure(bg='#f4f6fa')
		sufijo = 'ª'
		win.title(f'{dia} - {espacio}{sufijo} hora')
		win.geometry('330x270')
		win.resizable(False, False)
		win.transient(self)
		win.grab_set()
		win.focus_force()
		ttk.Label(win, text=f'{dia} - {espacio}{sufijo} hora', font=('Segoe UI', 13, 'bold'), background='#e0e7ef', foreground='#2a3a4a', anchor='center').pack(pady=10, fill='x')

		# Horario
		form = ttk.Frame(win)
		form.pack(pady=10, padx=10, fill='x')
		ttk.Label(form, text='Hora inicio:', background='#f4f6fa').grid(row=0, column=0, padx=5, pady=4, sticky='e')
		entry_inicio = ttk.Entry(form, width=8)
		entry_inicio.grid(row=0, column=1, padx=5, pady=4, sticky='w')
		ttk.Label(form, text='Hora fin:', background='#f4f6fa').grid(row=1, column=0, padx=5, pady=4, sticky='e')
		entry_fin = ttk.Entry(form, width=8)
		entry_fin.grid(row=1, column=1, padx=5, pady=4, sticky='w')

		# Autoinsertar ':' tras dos dígitos y navegación automática
		def autoinsert_colon(event, entry, next_widget=None):
			val = entry.get()
			if len(val) == 2 and ':' not in val:
				entry.insert(2, ':')
			if len(val) > 4:
				entry.delete(5, tk.END)
			if len(val.replace(':','')) == 4 and next_widget:
				next_widget.focus_set()
		entry_inicio.bind('<KeyRelease>', lambda e: autoinsert_colon(e, entry_inicio, entry_fin))
		entry_fin.bind('<KeyRelease>', lambda e: autoinsert_colon(e, entry_fin, None))

		# Materia
		ttk.Label(form, text='Materia:', background='#f4f6fa').grid(row=2, column=0, padx=5, pady=4, sticky='e')
		materias = obtener_materias()
		materia_nombres = [m['nombre'] for m in materias]
		materia_ids = {m['nombre']: m['id'] for m in materias}
		cb_materia = ttk.Combobox(form, values=materia_nombres, state='readonly')
		cb_materia.grid(row=2, column=1, padx=5, pady=4, sticky='w')
		def materia_autofilter(event):
			typed = cb_materia.get().lower()
			filtered = [m for m in materia_nombres if typed in m.lower()]
			cb_materia['values'] = filtered if filtered else materia_nombres
		cb_materia.bind('<KeyRelease>', materia_autofilter)
		# Autocompletar si solo hay una materia
		autocompletar_combobox(cb_materia, materia_nombres, incluir_vacio=False)

		# Profesor
		ttk.Label(form, text='Profesor:', background='#f4f6fa').grid(row=3, column=0, padx=5, pady=4, sticky='e')
		cb_profesor = ttk.Combobox(form, values=[], state='readonly')
		cb_profesor.grid(row=3, column=1, padx=5, pady=4, sticky='w')
		cb_profesor.config(state='disabled')

		def get_profesor_ids():
			return {p['nombre']: p['id'] for p in obtener_profesores()}
		profesor_ids = get_profesor_ids()

		def habilitar_profesor(event=None):
			materia_nombre = cb_materia.get()
			if materia_nombre:
				materia_id = None
				for m in obtener_materias():
					if m['nombre'] == materia_nombre:
						materia_id = m['id']
						break
				if materia_id is not None:
					conn = get_connection()
					cur = conn.cursor()
					cur.execute('''SELECT p.nombre, p.id FROM profesor p JOIN profesor_materia pm ON p.id = pm.profesor_id WHERE pm.materia_id = ?''', (materia_id,))
					rows = cur.fetchall()
					nombres_profesores = sorted([row[0] for row in rows], key=lambda n: n.lower())
					nonlocal profesor_ids
					profesor_ids = {row[0]: row[1] for row in rows}
					conn.close()
					# Autocompletar si solo hay un profesor
					autocompletar_combobox(cb_profesor, nombres_profesores, incluir_vacio=True)
				else:
					cb_profesor['values'] = []
					cb_profesor.set('')
					cb_profesor.config(state='disabled')
			else:
				cb_profesor['values'] = []
				cb_profesor.set('')
				cb_profesor.config(state='disabled')
		cb_materia.bind('<<ComboboxSelected>>', habilitar_profesor)

		# Cargar datos existentes si hay
		horarios = obtener_horarios(division_id)
		h_existente = None
		for h in horarios:
			if h['dia'] == dia and h['espacio'] == espacio:
				h_existente = h
				break
		if h_existente:
			if h_existente['hora_inicio']:
				entry_inicio.insert(0, h_existente['hora_inicio'])
			if h_existente['hora_fin']:
				entry_fin.insert(0, h_existente['hora_fin'])
			if h_existente['materia']:
				cb_materia.set(h_existente['materia'])
			if h_existente['profesor']:
				cb_profesor.set(h_existente['profesor'])

		# Navegación con Enter
		entry_inicio.bind('<Return>', lambda e: entry_fin.focus_set())
		entry_fin.bind('<Return>', lambda e: cb_materia.focus_set())
		cb_materia.bind('<Return>', lambda e: cb_profesor.focus_set())

		def guardar(event=None):
			hora_inicio = entry_inicio.get().strip()
			hora_fin = entry_fin.get().strip()
			materia = cb_materia.get()
			profesor = cb_profesor.get()
			if profesor and not materia:
				messagebox.showerror('Error', 'Si asigna profesor, también seleccione la materia.')
				return
			if not hora_inicio or not hora_fin:
				conn_tmp = get_connection()
				cur_tmp = conn_tmp.cursor()
				cur_tmp.execute('SELECT turno_id FROM division WHERE id=?', (division_id,))
				r = cur_tmp.fetchone()
				conn_tmp.close()
				if r:
					turno_id_tmp = r[0]
					default_h = obtener_turno_espacio_hora(turno_id_tmp, espacio)
					if default_h:
						if not hora_inicio:
							hora_inicio = default_h.get('hora_inicio') or ''
						if not hora_fin:
							hora_fin = default_h.get('hora_fin') or ''
			datos_previos = None
			if h_existente:
				datos_previos = {
					'id': h_existente['id'],
					'hora_inicio': h_existente['hora_inicio'],
					'hora_fin': h_existente['hora_fin'],
					'materia_id': materia_ids.get(h_existente['materia'], None),
					'profesor_id': profesor_ids.get(h_existente['profesor'], None)
				}
			try:
				if h_existente:
					eliminar_horario(h_existente['id'])
				mid = materia_ids.get(materia) if materia else None
				pid = profesor_ids.get(profesor) if profesor else None
				# Obtener turno_id de la división
				turno_nombre = self.cb_turno_horario.get()
				turno_id = self.turnos_dict_horario[turno_nombre]
				crear_horario(division_id, dia, espacio, hora_inicio, hora_fin, mid, pid, turno_id)
				self._dibujar_grilla_horario_curso()
				win.destroy()
			except Exception as e:
				if datos_previos:
					try:
						turno_nombre = self.cb_turno_horario.get()
						turno_id = self.turnos_dict_horario[turno_nombre]
						crear_horario(division_id, dia, espacio, datos_previos['hora_inicio'], datos_previos['hora_fin'], datos_previos['materia_id'], datos_previos['profesor_id'], turno_id)
					except Exception:
						pass
				msg = str(e)
				if 'ya está asignado en ese horario en otra división' in msg or 'no tiene asignada la materia' in msg:
					messagebox.showerror('Error', msg)
				else:
					messagebox.showerror('Error', msg)

		def eliminar_espacio(event=None):
			if h_existente:
				if messagebox.askyesno('Confirmar', '¿Eliminar asignación de este espacio?'):
					try:
						eliminar_horario(h_existente['id'])
						self._dibujar_grilla_horario_curso()
						win.destroy()
					except Exception as e:
						messagebox.showerror('Error', str(e))
			else:
				win.destroy()

		btns = ttk.Frame(win)
		btns.pack(pady=15)
		btn_guardar = ttk.Button(btns, text='Guardar', command=guardar)
		btn_guardar.grid(row=0, column=0, padx=8)
		btn_eliminar = ttk.Button(btns, text='Eliminar', command=eliminar_espacio)
		btn_eliminar.grid(row=0, column=1, padx=8)
		btn_guardar.bind('<Return>', guardar)
		btn_eliminar.bind('<Return>', eliminar_espacio)
		entry_inicio.focus_set()

	# ============== VISTA DE HORARIOS POR PROFESOR ==============
	
	def mostrar_horarios_profesor(self):
		self.limpiar_frame()
		ttk.Label(self.frame_principal, text='Gestión de Horarios por Profesor', font=('Arial', 14)).pack(pady=10)

		# Selección paso a paso: Turno → Profesor
		frame_sel = ttk.Frame(self.frame_principal)
		frame_sel.pack(pady=5)
		ttk.Label(frame_sel, text='Turno:').grid(row=0, column=0, padx=5)
		turnos = obtener_turnos()
		self.turnos_dict_horario_prof = {t['nombre']: t['id'] for t in turnos}
		self.cb_turno_horario_prof = ttk.Combobox(frame_sel, values=list(self.turnos_dict_horario_prof.keys()), state='readonly')
		self.cb_turno_horario_prof.grid(row=0, column=1, padx=5)
		
		# Label "Buscar agente:" con tooltip
		lbl_buscar = ttk.Label(frame_sel, text='Buscar agente:')
		lbl_buscar.grid(row=0, column=2, padx=5)
		ToolTip(lbl_buscar, 
				"Buscar agente:\n"
				"• Escribe para filtrar\n"
				"• Enter: selecciona primera coincidencia\n"
				"• Esc / Backspace: limpiar campo")
		
		self.cb_profesor_horario = ttk.Combobox(frame_sel, values=[], state='disabled')
		self.cb_profesor_horario.grid(row=0, column=3, padx=5)
		
		# Autocompletar turno si solo hay uno
		turno_autocompletado_prof = autocompletar_combobox(self.cb_turno_horario_prof, list(self.turnos_dict_horario_prof.keys()), incluir_vacio=False)

		# Lista completa de profesores para filtrado
		self.profesores_lista_completa = []
		# Variable para rastrear si hay un profesor seleccionado
		self.profesor_seleccionado = False
		
		def ajustar_ancho_combobox(nombre=''):
			# Ajustar el ancho del combobox según el texto
			if nombre:
				# Calcular ancho basado en la longitud del texto (aprox 1 char = 10 px en ancho)
				ancho = max(20, min(len(nombre) + 5, 60))  # Min 20, Max 60
			else:
				ancho = 20  # Ancho por defecto
			self.cb_profesor_horario.config(width=ancho)

		def on_turno_selected_prof(event=None):
			turno_nombre = self.cb_turno_horario_prof.get()
			if not turno_nombre:
				self.cb_profesor_horario['values'] = []
				self.cb_profesor_horario.set('')
				self.cb_profesor_horario.config(state='disabled')
				self.profesores_lista_completa = []
				self.profesor_seleccionado = False
				ajustar_ancho_combobox()
				return
			turno_id = self.turnos_dict_horario_prof[turno_nombre]
			profesores = obtener_profesores_por_turno(turno_id)
			# Ordenar alfabéticamente
			profesores_ordenados = sorted(profesores, key=lambda p: p['nombre'].lower())
			self.profesores_dict_horario = {p['nombre']: p['id'] for p in profesores_ordenados}
			self.profesores_lista_completa = list(self.profesores_dict_horario.keys())
			autocompletar_combobox(self.cb_profesor_horario, self.profesores_lista_completa, incluir_vacio=False)
			self.cb_profesor_horario.config(state='normal' if profesores else 'disabled')
			self.profesor_seleccionado = False
			# Ajustar ancho si se autocompletó
			if self.cb_profesor_horario.get():
				ajustar_ancho_combobox(self.cb_profesor_horario.get())
			# Enfocar el combobox de profesor si hay opciones
			if profesores:
				self.cb_profesor_horario.focus_set()

		def on_profesor_selected(event=None):
			# Solo dibujar si el profesor está en la lista válida
			nombre = self.cb_profesor_horario.get()
			if nombre in self.profesores_dict_horario:
				self.profesor_seleccionado = True
				ajustar_ancho_combobox(nombre)
				self._dibujar_grilla_horario_profesor()
			else:
				self.profesor_seleccionado = False

		def filtrar_profesor(event=None):
			# Filtrar profesores mientras se tipea
			typed = self.cb_profesor_horario.get().lower()
			if typed == '':
				self.cb_profesor_horario['values'] = self.profesores_lista_completa
			else:
				filtered = [p for p in self.profesores_lista_completa if typed in p.lower()]
				self.cb_profesor_horario['values'] = filtered if filtered else self.profesores_lista_completa

		def seleccionar_primera_coincidencia(event=None):
			# Al presionar Enter, selecciona la primera coincidencia del filtro
			typed = self.cb_profesor_horario.get().lower()
			if typed:
				# Buscar coincidencias
				filtered = [p for p in self.profesores_lista_completa if typed in p.lower()]
				if filtered:
					# Seleccionar la primera coincidencia
					self.cb_profesor_horario.set(filtered[0])
					# Disparar el evento de selección
					on_profesor_selected()
					return 'break'  # Prevenir el comportamiento por defecto de Enter

		def limpiar_y_enfocar(event=None):
			# Al presionar Esc o Backspace, limpiar el combobox y enfocarlo
			self.cb_profesor_horario.set('')
			self.profesor_seleccionado = False
			ajustar_ancho_combobox()
			self.cb_profesor_horario.focus_set()
			# Limpiar la grilla
			for widget in self.frame_grilla_horario_prof.winfo_children():
				widget.destroy()
			return 'break'

		self.cb_turno_horario_prof.bind('<<ComboboxSelected>>', on_turno_selected_prof)
		self.cb_profesor_horario.bind('<<ComboboxSelected>>', on_profesor_selected)
		self.cb_profesor_horario.bind('<KeyRelease>', filtrar_profesor)
		self.cb_profesor_horario.bind('<Return>', seleccionar_primera_coincidencia)
		self.cb_profesor_horario.bind('<Escape>', limpiar_y_enfocar)
		self.cb_profesor_horario.bind('<BackSpace>', limpiar_y_enfocar)
		
		# Si el turno se autocompletó, trigger inicial
		if turno_autocompletado_prof:
			on_turno_selected_prof()

		self.espacios_por_dia_prof = 8
		
		# Frame contenedor con Canvas y Scrollbar para la grilla de horarios
		container_grilla = ttk.Frame(self.frame_principal)
		container_grilla.pack(pady=10, expand=True, fill='both')
		
		# Canvas con scrollbar
		self.canvas_horario_prof = tk.Canvas(container_grilla, bg='#f4f6fa', highlightthickness=0)
		scrollbar_horario_prof = ttk.Scrollbar(container_grilla, orient='vertical', command=self.canvas_horario_prof.yview)
		self.canvas_horario_prof.configure(yscrollcommand=scrollbar_horario_prof.set)
		
		scrollbar_horario_prof.pack(side='right', fill='y')
		self.canvas_horario_prof.pack(side='left', fill='both', expand=True)
		
		# Frame dentro del canvas para la grilla
		self.frame_grilla_horario_prof = ttk.Frame(self.canvas_horario_prof)
		self.canvas_window_prof = self.canvas_horario_prof.create_window((0, 0), window=self.frame_grilla_horario_prof, anchor='nw')
		
		# Actualizar scroll region cuando cambie el tamaño del frame
		def actualizar_scroll_region_prof(event=None):
			self.canvas_horario_prof.update_idletasks()
			self.canvas_horario_prof.configure(scrollregion=(0, 0, self.frame_grilla_horario_prof.winfo_reqwidth(), self.frame_grilla_horario_prof.winfo_reqheight()))
		self.frame_grilla_horario_prof.bind('<Configure>', actualizar_scroll_region_prof)
		
		# Ajustar el ancho del frame al canvas
		def ajustar_ancho_canvas_prof(event):
			canvas_width = event.width
			self.canvas_horario_prof.itemconfig(self.canvas_window_prof, width=canvas_width)
		self.canvas_horario_prof.bind('<Configure>', ajustar_ancho_canvas_prof)
		
		# Permitir scroll con la rueda del mouse
		def on_mousewheel_prof(event):
			self.canvas_horario_prof.yview_scroll(int(-1*(event.delta/120)), "units")
		
		def bind_mousewheel_prof(event):
			self.canvas_horario_prof.bind_all("<MouseWheel>", on_mousewheel_prof)
		
		def unbind_mousewheel_prof(event):
			self.canvas_horario_prof.unbind_all("<MouseWheel>")
		
		self.canvas_horario_prof.bind('<Enter>', bind_mousewheel_prof)
		self.canvas_horario_prof.bind('<Leave>', unbind_mousewheel_prof)

		# Botón para configurar horas por turno en la parte baja (siempre visible)
		frame_bottom_btns = ttk.Frame(self.frame_principal)
		frame_bottom_btns.pack(pady=6)
		ttk.Button(frame_bottom_btns, text='Configurar horas por turno', command=self._configurar_horas_por_turno).pack(side='left', padx=5)
		ttk.Button(frame_bottom_btns, text='Limpiar horarios vacíos', command=self._limpiar_horarios_vacios_profesor).pack(side='left', padx=5)
		
		# Enfocar el primer combobox al entrar
		self.cb_turno_horario_prof.focus_set()

	def _dibujar_grilla_horario_profesor(self):
		for widget in self.frame_grilla_horario_prof.winfo_children():
			widget.destroy()
		profesor_nombre = getattr(self, 'cb_profesor_horario', None)
		if not profesor_nombre or not self.cb_profesor_horario.get():
			return
		turno_nombre = self.cb_turno_horario_prof.get()
		if not turno_nombre:
			return
		profesor_id = self.profesores_dict_horario[self.cb_profesor_horario.get()]
		turno_id = self.turnos_dict_horario_prof[turno_nombre]

		# Obtener horarios del profesor
		horarios = obtener_horarios_profesor(profesor_id, turno_id)

		dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
		# Encabezados - igual que en vista por curso
		# Celda vacía en esquina superior izquierda
		ttk.Label(self.frame_grilla_horario_prof, text='', font=('Segoe UI', 10, 'bold'), background='#f4f6fa').grid(row=0, column=0, padx=(0,0), pady=2, sticky='nsew')
		# Días de la semana
		for col, dia in enumerate(dias, start=1):
			ttk.Label(self.frame_grilla_horario_prof, text=dia, font=('Segoe UI', 10, 'bold'), background='#e0e7ef', foreground='#2a3a4a').grid(row=0, column=col, padx=(0,0), pady=2, sticky='nsew')

		# Configuración de columnas igual que en vista por curso
		self.frame_grilla_horario_prof.columnconfigure(0, weight=0, minsize=52)
		for c in range(1, 6):
			self.frame_grilla_horario_prof.columnconfigure(c, weight=1, minsize=150)

		self._grilla_botones_prof = []
		for esp in range(1, self.espacios_por_dia_prof + 1):
			# Etiqueta igual que en vista por curso
			etiqueta = f"{esp}ª"
			ttk.Label(self.frame_grilla_horario_prof, text=etiqueta, font=('Segoe UI', 10, 'bold'), background='#e0e7ef', foreground='#2a3a4a', anchor='center').grid(row=esp, column=0, padx=(0,0), pady=2, sticky='nsew')
			self.frame_grilla_horario_prof.rowconfigure(esp, weight=1, minsize=38)

			fila_botones = []
			for col, dia in enumerate(dias, start=1):
				h = next((ho for ho in horarios if ho['dia'] == dia and ho['espacio'] == esp), None)
				texto = ''
				if h:
					texto = f"{h['materia'] or ''}\n{h['division'] or ''}\n{h['hora_inicio'] or ''}-{h['hora_fin'] or ''}"
				btn = tk.Button(self.frame_grilla_horario_prof, text=texto, wraplength=100, anchor='w', justify='left',
								bg='#ffffff', relief='ridge', bd=1,
								command=lambda d=dia, e=esp: self._editar_espacio_horario_profesor(d, e))
				btn.grid(row=esp, column=col, padx=1, pady=1, sticky='nsew')
				fila_botones.append(btn)
			self._grilla_botones_prof.append(fila_botones)

		# Ajustar wraplength dinámicamente
		def actualizar_wraplength_prof(event=None):
			for esp, fila in enumerate(self._grilla_botones_prof):
				for col, btn in enumerate(fila):
					info = btn.grid_info()
					col_idx = info['column']
					width = self.frame_grilla_horario_prof.grid_bbox(col_idx, esp+1)[2]
					btn.config(wraplength=max(width-8, 60))
		self.frame_grilla_horario_prof.bind('<Configure>', actualizar_wraplength_prof)
		self.after(100, lambda: self.frame_grilla_horario_prof.event_generate('<Configure>'))
		
		# Actualizar la región de scroll
		def actualizar_scroll_prof():
			self.frame_grilla_horario_prof.update_idletasks()
			self.canvas_horario_prof.configure(scrollregion=(0, 0, self.frame_grilla_horario_prof.winfo_reqwidth(), self.frame_grilla_horario_prof.winfo_reqheight()))
			self.canvas_horario_prof.yview_moveto(0)
		self.after(150, actualizar_scroll_prof)

	def _limpiar_horarios_vacios_profesor(self):
		"""Elimina horarios de profesor que solo tienen hora de inicio y fin, sin división ni materia"""
		profesor_nombre = getattr(self, 'cb_profesor_horario', None)
		turno_nombre = getattr(self, 'cb_turno_horario_prof', None)
		
		if not profesor_nombre or not self.cb_profesor_horario.get() or not turno_nombre or not self.cb_turno_horario_prof.get():
			messagebox.showwarning('Advertencia', 'Seleccione un turno y un profesor primero.')
			return
		
		profesor_id = self.profesores_dict_horario[self.cb_profesor_horario.get()]
		turno_id = self.turnos_dict_horario_prof[self.cb_turno_horario_prof.get()]
		
		if not messagebox.askyesno('Confirmar', '¿Eliminar todos los horarios que solo contengan hora de inicio y fin?\n\nLos horarios con división o materia asignados no serán eliminados.'):
			return
		
		try:
			conn = get_connection()
			c = conn.cursor()
			# Eliminar horarios que solo tengan horas pero no división ni materia
			c.execute('''DELETE FROM horario 
						WHERE profesor_id = ? 
						AND turno_id = ?
						AND (division_id IS NULL OR division_id = '') 
						AND (materia_id IS NULL OR materia_id = '')
						AND (hora_inicio IS NOT NULL OR hora_fin IS NOT NULL)''', (profesor_id, turno_id))
			eliminados = c.rowcount
			conn.commit()
			conn.close()
			
			messagebox.showinfo('Éxito', f'Se eliminaron {eliminados} horarios vacíos.')
			self._dibujar_grilla_horario_profesor()
		except Exception as e:
			messagebox.showerror('Error', f'Error al limpiar horarios: {str(e)}')

	def _editar_espacio_horario_profesor(self, dia, espacio):
		if not self.cb_profesor_horario.get() or not self.cb_turno_horario_prof.get():
			messagebox.showwarning('Advertencia', 'Selecciona un turno y un profesor.')
			return
		
		profesor_id = self.profesores_dict_horario[self.cb_profesor_horario.get()]
		turno_id = self.turnos_dict_horario_prof[self.cb_turno_horario_prof.get()]
		
		# Obtener horario existente si hay
		horarios = obtener_horarios_profesor(profesor_id, turno_id)
		h_existente = next((h for h in horarios if h['dia'] == dia and h['espacio'] == espacio), None)
		
		# Ventana de edición - estilo similar a por curso
		win = tk.Toplevel(self)
		win.configure(bg='#f4f6fa')
		sufijo = 'ª'
		win.title(f'{dia} - {espacio}{sufijo} hora')
		win.geometry('330x360')
		win.resizable(False, False)
		win.transient(self)
		win.grab_set()
		win.focus_force()
		ttk.Label(win, text=f'{dia} - {espacio}{sufijo} hora', font=('Segoe UI', 13, 'bold'), background='#e0e7ef', foreground='#2a3a4a', anchor='center').pack(pady=10, fill='x')

		# Horario
		form = ttk.Frame(win)
		form.pack(pady=10, padx=10, fill='x')
		ttk.Label(form, text='Hora inicio:', background='#f4f6fa').grid(row=0, column=0, padx=5, pady=4, sticky='e')
		entry_inicio = ttk.Entry(form, width=8)
		entry_inicio.grid(row=0, column=1, padx=5, pady=4, sticky='w')
		ttk.Label(form, text='Hora fin:', background='#f4f6fa').grid(row=1, column=0, padx=5, pady=4, sticky='e')
		entry_fin = ttk.Entry(form, width=8)
		entry_fin.grid(row=1, column=1, padx=5, pady=4, sticky='w')

		# Autoinsertar ':' tras dos dígitos y navegación automática
		def autoinsert_colon(event, entry, next_widget=None):
			val = entry.get()
			if len(val) == 2 and ':' not in val:
				entry.insert(2, ':')
			if len(val) > 5:
				entry.delete(5, tk.END)
			if len(val.replace(':','')) == 4 and next_widget:
				next_widget.focus_set()
		entry_inicio.bind('<KeyRelease>', lambda e: autoinsert_colon(e, entry_inicio, entry_fin))
		entry_fin.bind('<KeyRelease>', lambda e: autoinsert_colon(e, entry_fin, None))

		# Materia - Obtener solo las materias que tiene asignadas el profesor
		ttk.Label(form, text='Materia:', background='#f4f6fa').grid(row=2, column=0, padx=5, pady=4, sticky='e')
		banca = obtener_banca_profesor(profesor_id)
		materia_nombres = [b['materia'] for b in banca]
		
		# Necesitamos obtener los IDs de las materias
		todas_materias = obtener_materias()
		materia_ids = {m['nombre']: m['id'] for m in todas_materias}
		
		cb_materia = ttk.Combobox(form, values=materia_nombres, state='readonly')
		cb_materia.grid(row=2, column=1, padx=5, pady=4, sticky='w')
		# Autocompletar si solo hay una materia
		autocompletar_combobox(cb_materia, materia_nombres, incluir_vacio=False)

		# Plan de estudios
		ttk.Label(form, text='Plan:', background='#f4f6fa').grid(row=3, column=0, padx=5, pady=4, sticky='e')
		planes = obtener_planes_de_turno(turno_id)
		plan_nombres = [p['nombre'] for p in planes]
		plan_ids = {p['nombre']: p['id'] for p in planes}
		cb_plan = ttk.Combobox(form, values=[], state='disabled')
		cb_plan.grid(row=3, column=1, padx=5, pady=4, sticky='w')
		
		# Año (se actualiza al seleccionar plan)
		ttk.Label(form, text='Año:', background='#f4f6fa').grid(row=4, column=0, padx=5, pady=4, sticky='e')
		cb_anio = ttk.Combobox(form, values=[], state='disabled')
		cb_anio.grid(row=4, column=1, padx=5, pady=4, sticky='w')
		anios_dict = {}

		# División (se actualiza al seleccionar año)
		ttk.Label(form, text='División:', background='#f4f6fa').grid(row=5, column=0, padx=5, pady=4, sticky='e')
		cb_division = ttk.Combobox(form, values=[], state='disabled')
		cb_division.grid(row=5, column=1, padx=5, pady=4, sticky='w')
		division_ids = {}
		
		def on_plan_selected(event=None):
			nonlocal anios_dict
			plan_nombre = cb_plan.get()
			if not plan_nombre:
				cb_anio['values'] = []
				cb_anio.set('')
				cb_anio.config(state='disabled')
				cb_division['values'] = []
				cb_division.set('')
				cb_division.config(state='disabled')
				return
			
			plan_id = plan_ids[plan_nombre]
			anios = obtener_anios(plan_id)
			anios_list = [a['nombre'] for a in anios]
			anios_dict = {a['nombre']: a['id'] for a in anios}
			
			# Autocompletar año si solo hay uno
			if autocompletar_combobox(cb_anio, anios_list, incluir_vacio=True):
				on_anio_selected()  # Trigger automático si se autocompletó
		
		def on_anio_selected(event=None):
			nonlocal division_ids
			anio_nombre = cb_anio.get()
			if not anio_nombre:
				cb_division['values'] = []
				cb_division.set('')
				cb_division.config(state='disabled')
				return
			
			plan_nombre = cb_plan.get()
			if not plan_nombre:
				return
			
			anio_id = anios_dict[anio_nombre]
			plan_id = plan_ids[plan_nombre]
			
			# Obtener divisiones del turno, plan y año seleccionados
			divisiones = obtener_divisiones()
			divisiones_filtradas = [d for d in divisiones 
								  if d['turno_id'] == turno_id 
								  and d['plan_id'] == plan_id
								  and d['anio_id'] == anio_id]
			division_nombres = [d['nombre'] for d in divisiones_filtradas]
			division_ids = {d['nombre']: d['id'] for d in divisiones_filtradas}
			
			# Autocompletar división si solo hay una
			autocompletar_combobox(cb_division, division_nombres, incluir_vacio=True)
		
		cb_plan.bind('<<ComboboxSelected>>', on_plan_selected)
		cb_anio.bind('<<ComboboxSelected>>', on_anio_selected)
		
		# Configurar plan inicial y autocompletar si solo hay uno
		if autocompletar_combobox(cb_plan, plan_nombres, incluir_vacio=True):
			on_plan_selected()  # Trigger automático si se autocompletó

		# Cargar datos existentes
		if h_existente:
			entry_inicio.insert(0, h_existente['hora_inicio'] or '')
			entry_fin.insert(0, h_existente['hora_fin'] or '')
			cb_materia.set(h_existente['materia'] or '')
			
			# Cargar plan, año y división si existen
			if h_existente['division']:
				# Buscar el plan, año y división
				divisiones = obtener_divisiones()
				div_encontrada = next((d for d in divisiones if d['nombre'] == h_existente['division']), None)
				if div_encontrada:
					# Encontrar el plan
					plan_encontrado = next((p for p in plan_nombres if plan_ids[p] == div_encontrada['plan_id']), None)
					if plan_encontrado:
						cb_plan.set(plan_encontrado)
						on_plan_selected()  # Actualizar años
						
						# Encontrar el año
						anios_disponibles = obtener_anios(div_encontrada['plan_id'])
						anio_encontrado = next((a['nombre'] for a in anios_disponibles if a['id'] == div_encontrada['anio_id']), None)
						if anio_encontrado:
							cb_anio.set(anio_encontrado)
							on_anio_selected()  # Actualizar divisiones
							cb_division.set(h_existente['division'])

		# Guardar cambios previos para rollback en caso de error
		datos_previos = None
		if h_existente:
			# Buscar los IDs originales
			div_id = None
			if h_existente['division']:
				divisiones = obtener_divisiones()
				div_encontrada = next((d for d in divisiones if d['nombre'] == h_existente['division']), None)
				if div_encontrada:
					div_id = div_encontrada['id']
			mat_id = materia_ids.get(h_existente['materia']) if h_existente['materia'] else None
			datos_previos = {
				'hora_inicio': h_existente['hora_inicio'],
				'hora_fin': h_existente['hora_fin'],
				'division_id': div_id,
				'materia_id': mat_id
			}

		def guardar(event=None):
			hora_inicio = entry_inicio.get().strip()
			hora_fin = entry_fin.get().strip()
			division = cb_division.get().strip()
			materia = cb_materia.get().strip()

			try:
				if h_existente:
					eliminar_horario_profesor(h_existente['id'])
				
				div_id = division_ids.get(division) if division else None
				mat_id = materia_ids.get(materia) if materia else None
				
				crear_horario_profesor(profesor_id, turno_id, dia, espacio, hora_inicio, hora_fin, div_id, mat_id)
				self._dibujar_grilla_horario_profesor()
				win.destroy()
			except Exception as e:
				# Rollback en caso de error
				if datos_previos:
					try:
						crear_horario_profesor(profesor_id, turno_id, dia, espacio, 
											 datos_previos['hora_inicio'], datos_previos['hora_fin'], 
											 datos_previos['division_id'], datos_previos['materia_id'])
					except Exception:
						pass
				messagebox.showerror('Error', str(e))

		def eliminar_espacio(event=None):
			if h_existente:
				if messagebox.askyesno('Confirmar', '¿Eliminar asignación de este espacio?'):
					try:
						eliminar_horario_profesor(h_existente['id'])
						self._dibujar_grilla_horario_profesor()
						win.destroy()
					except Exception as e:
						messagebox.showerror('Error', str(e))
			else:
				win.destroy()

		btns = ttk.Frame(win)
		btns.pack(pady=15)
		btn_guardar = ttk.Button(btns, text='Guardar', command=guardar)
		btn_guardar.grid(row=0, column=0, padx=8)
		btn_eliminar = ttk.Button(btns, text='Eliminar', command=eliminar_espacio)
		btn_eliminar.grid(row=0, column=1, padx=8)
		btn_guardar.bind('<Return>', guardar)
		btn_eliminar.bind('<Return>', eliminar_espacio)
		entry_inicio.focus_set()

	# --- Paneles agregados: Plan de estudios y Turnos ---

	def _configurar_horas_por_turno(self):
		# Dialogo para configurar horas por turno para espacios 1..8
		win = tk.Toplevel(self)
		win.configure(bg='#f4f6fa')
		win.title('Configurar horas por turno')
		win.geometry('280x480')
		win.resizable(False, False)
		win.transient(self)
		win.grab_set()
		win.focus_force()
		frame = ttk.Frame(win)
		frame.pack(padx=15, pady=15, fill='both', expand=True)
		
		ttk.Label(frame, text='Turno:', font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, padx=5, pady=8, sticky='w')
		turnos = obtener_turnos()
		turnos_dict = {t['nombre']: t['id'] for t in turnos}
		cb_turno = ttk.Combobox(frame, values=list(turnos_dict.keys()), state='readonly', width=15)
		cb_turno.grid(row=0, column=1, columnspan=4, padx=5, pady=8, sticky='w')

		# Función de validación de horas (copiada de edición de horarios)
		def autoinsert_colon(event, entry, next_widget=None):
			val = entry.get()
			if len(val) == 2 and ':' not in val:
				entry.insert(2, ':')
			if len(val) > 5:
				entry.delete(5, tk.END)
			if len(val.replace(':','')) == 4 and next_widget:
				next_widget.focus_set()

		# Tabla con labels mejorados
		entries = {}
		for esp in range(1, 9):
			ttk.Label(frame, text=f'{esp}ª:', font=('Segoe UI', 9, 'bold')).grid(row=esp, column=0, padx=5, pady=3, sticky='e')
			
			e_inicio = ttk.Entry(frame, width=7)
			e_inicio.insert(0, 'hh:mm')
			e_inicio.config(foreground='gray')
			e_inicio.grid(row=esp, column=1, padx=2, pady=3)
			
			ttk.Label(frame, text='Hs  a', font=('Segoe UI', 9)).grid(row=esp, column=2, padx=2, pady=3)
			
			e_fin = ttk.Entry(frame, width=7)
			e_fin.insert(0, 'hh:mm')
			e_fin.config(foreground='gray')
			e_fin.grid(row=esp, column=3, padx=2, pady=3)
			
			ttk.Label(frame, text='Hs', font=('Segoe UI', 9)).grid(row=esp, column=4, padx=2, pady=3, sticky='w')
			
			entries[esp] = (e_inicio, e_fin)
			
			# Placeholder functionality
			def on_focus_in(event, entry):
				if entry.get() == 'hh:mm':
					entry.delete(0, tk.END)
					entry.config(foreground='black')
			
			def on_focus_out(event, entry):
				if entry.get() == '':
					entry.insert(0, 'hh:mm')
					entry.config(foreground='gray')
			
			e_inicio.bind('<FocusIn>', lambda e, ent=e_inicio: on_focus_in(e, ent))
			e_inicio.bind('<FocusOut>', lambda e, ent=e_inicio: on_focus_out(e, ent))
			e_fin.bind('<FocusIn>', lambda e, ent=e_fin: on_focus_in(e, ent))
			e_fin.bind('<FocusOut>', lambda e, ent=e_fin: on_focus_out(e, ent))
			
			# Autocompletado de ':'
			if esp < 8:
				next_e = entries.get(esp+1, (None, None))[0]
			else:
				next_e = None
			e_inicio.bind('<KeyRelease>', lambda e, ent=e_inicio, nxt=e_fin: autoinsert_colon(e, ent, nxt))
			e_fin.bind('<KeyRelease>', lambda e, ent=e_fin, nxt=next_e: autoinsert_colon(e, ent, nxt))

		# Checkboxes para aplicar a horarios existentes
		apply_actual_var = tk.IntVar(value=0)
		apply_todos_var = tk.IntVar(value=0)
		
		chk_apply_actual = ttk.Checkbutton(frame, text='Aplicar a horario actual', variable=apply_actual_var)
		chk_apply_actual.grid(row=9, column=0, columnspan=5, pady=5, sticky='w')
		
		chk_apply_todos = ttk.Checkbutton(frame, text='Aplicar a todos los horarios del turno', variable=apply_todos_var)
		chk_apply_todos.grid(row=10, column=0, columnspan=5, pady=5, sticky='w')

		def cargar_defaults(event=None):
			nombre = cb_turno.get()
			if not nombre:
				for esp in entries:
					e_i, e_f = entries[esp]
					e_i.delete(0, tk.END)
					e_i.insert(0, 'hh:mm')
					e_i.config(foreground='gray')
					e_f.delete(0, tk.END)
					e_f.insert(0, 'hh:mm')
					e_f.config(foreground='gray')
				return
			turno_id = turnos_dict[nombre]
			for esp in entries:
				d = obtener_turno_espacio_hora(turno_id, esp)
				e_i, e_f = entries[esp]
				e_i.delete(0, tk.END)
				e_f.delete(0, tk.END)
				if d and d.get('hora_inicio'):
					e_i.insert(0, d.get('hora_inicio'))
					e_i.config(foreground='black')
				else:
					e_i.insert(0, 'hh:mm')
					e_i.config(foreground='gray')
				if d and d.get('hora_fin'):
					e_f.insert(0, d.get('hora_fin'))
					e_f.config(foreground='black')
				else:
					e_f.insert(0, 'hh:mm')
					e_f.config(foreground='gray')

		cb_turno.bind('<<ComboboxSelected>>', cargar_defaults)

		def guardar():
			nombre = cb_turno.get()
			if not nombre:
				messagebox.showerror('Error', 'Seleccione un turno.')
				return
			turno_id = turnos_dict[nombre]
			# Guardar cada espacio
			for esp in entries:
				hi = entries[esp][0].get().strip()
				hf = entries[esp][1].get().strip()
				# Ignorar placeholders
				if hi == 'hh:mm':
					hi = ''
				if hf == 'hh:mm':
					hf = ''
				set_turno_espacio_hora(turno_id, esp, hi if hi else None, hf if hf else None)
			
			# Aplicar a horarios existentes si se pidió
			if apply_actual_var.get() or apply_todos_var.get():
				conn = get_connection()
				c = conn.cursor()
				dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
				
				# Verificar si estamos en la vista de horarios por profesor con un profesor seleccionado
				# Debemos verificar que exista cb_turno_horario_prof (específico de vista profesor)
				# y NO solo cb_turno_horario (que es de vista curso)
				en_vista_profesor = (hasattr(self, 'cb_turno_horario_prof') and 
									hasattr(self, 'cb_profesor_horario') and 
									hasattr(self, 'profesores_dict_horario') and 
									self.cb_turno_horario_prof.winfo_exists() and
									self.cb_profesor_horario.get() and 
									self.cb_profesor_horario.get() in self.profesores_dict_horario)
				
				# Verificar si estamos en la vista de horarios por curso con una división seleccionada
				en_vista_curso = (hasattr(self, 'cb_turno_horario') and 
								hasattr(self, 'cb_division_horario') and 
								hasattr(self, 'divisiones_dict_horario') and
								self.cb_turno_horario.winfo_exists() and
								self.cb_division_horario.get() and 
								self.cb_division_horario.get() in self.divisiones_dict_horario)
				
				if apply_actual_var.get():
					# Aplicar solo al horario actual (profesor o división seleccionada)
					if en_vista_profesor:
						# Aplicar solo al profesor seleccionado
						profesor_id = self.profesores_dict_horario[self.cb_profesor_horario.get()]
						for esp in entries:
							hi = entries[esp][0].get().strip()
							hf = entries[esp][1].get().strip()
							# Ignorar placeholders
							if hi == 'hh:mm':
								hi = None
							if hf == 'hh:mm':
								hf = None
							if hi is None and hf is None:
								continue
							
							for dia in dias:
								# Si existe fila para profesor+dia+espacio+turno, actualizar
								c.execute('SELECT id FROM horario WHERE profesor_id=? AND turno_id=? AND espacio=? AND dia=?', (profesor_id, turno_id, esp, dia))
								row = c.fetchone()
								if row:
									# Sobrescribir las horas existentes con los nuevos valores
									c.execute('UPDATE horario SET hora_inicio = ?, hora_fin = ? WHERE id=?', (hi, hf, row[0]))
								else:
									# Insertar nuevo horario con division y materia NULL
									c.execute('INSERT INTO horario (profesor_id, turno_id, dia, espacio, hora_inicio, hora_fin, division_id, materia_id) VALUES (?, ?, ?, ?, ?, ?, NULL, NULL)', (profesor_id, turno_id, dia, esp, hi, hf))
					
					elif en_vista_curso:
						# Aplicar solo a la división seleccionada
						division_id = self.divisiones_dict_horario[self.cb_division_horario.get()]
						for esp in entries:
							hi = entries[esp][0].get().strip()
							hf = entries[esp][1].get().strip()
							# Ignorar placeholders
							if hi == 'hh:mm':
								hi = None
							if hf == 'hh:mm':
								hf = None
							if hi is None and hf is None:
								continue
							
							for dia in dias:
								# Si existe fila para division+dia+espacio, actualizar
								c.execute('SELECT id FROM horario WHERE division_id=? AND espacio=? AND dia=?', (division_id, esp, dia))
								row = c.fetchone()
								if row:
									# Sobrescribir las horas existentes con los nuevos valores
									c.execute('UPDATE horario SET hora_inicio = ?, hora_fin = ? WHERE id=?', (hi, hf, row[0]))
								else:
									# Insertar nuevo horario con materia y profesor NULL
									c.execute('INSERT INTO horario (division_id, dia, espacio, hora_inicio, hora_fin, materia_id, profesor_id) VALUES (?, ?, ?, ?, ?, NULL, NULL)', (division_id, dia, esp, hi, hf))
				
				if apply_todos_var.get():
					# Aplicar a todos los horarios del turno
					if en_vista_profesor:
						# Aplicar a todos los profesores del turno
						c.execute('SELECT profesor_id FROM profesor_turno WHERE turno_id=?', (turno_id,))
						profesores_turno = [r[0] for r in c.fetchall()]
						for prof_id in profesores_turno:
							for esp in entries:
								hi = entries[esp][0].get().strip()
								hf = entries[esp][1].get().strip()
								# Ignorar placeholders
								if hi == 'hh:mm':
									hi = None
								if hf == 'hh:mm':
									hf = None
								if hi is None and hf is None:
									continue
								
								for dia in dias:
									# Si existe fila para profesor+dia+espacio+turno, actualizar
									c.execute('SELECT id FROM horario WHERE profesor_id=? AND turno_id=? AND espacio=? AND dia=?', (prof_id, turno_id, esp, dia))
									row = c.fetchone()
									if row:
										# Sobrescribir las horas existentes con los nuevos valores
										c.execute('UPDATE horario SET hora_inicio = ?, hora_fin = ? WHERE id=?', (hi, hf, row[0]))
									else:
										# Insertar nuevo horario con division y materia NULL
										c.execute('INSERT INTO horario (profesor_id, turno_id, dia, espacio, hora_inicio, hora_fin, division_id, materia_id) VALUES (?, ?, ?, ?, ?, ?, NULL, NULL)', (prof_id, turno_id, dia, esp, hi, hf))
					elif en_vista_curso:
						# Aplicar a todas las divisiones del turno (vista por curso)
						c.execute('SELECT id FROM division WHERE turno_id=?', (turno_id,))
						divs = [r[0] for r in c.fetchall()]
						for div in divs:
							for esp in entries:
								hi = entries[esp][0].get().strip()
								hf = entries[esp][1].get().strip()
								# Ignorar placeholders
								if hi == 'hh:mm':
									hi = None
								if hf == 'hh:mm':
									hf = None
								if hi is None and hf is None:
									continue
								
								for dia in dias:
									# Si existe fila para division+dia+espacio, actualizar
									c.execute('SELECT id FROM horario WHERE division_id=? AND espacio=? AND dia=?', (div, esp, dia))
									row = c.fetchone()
									if row:
										# Sobrescribir las horas existentes con los nuevos valores
										c.execute('UPDATE horario SET hora_inicio = ?, hora_fin = ? WHERE id=?', (hi, hf, row[0]))
									else:
										# Insertar nuevo horario con materia y profesor NULL
										c.execute('INSERT INTO horario (division_id, dia, espacio, hora_inicio, hora_fin, materia_id, profesor_id) VALUES (?, ?, ?, ?, ?, NULL, NULL)', (div, dia, esp, hi, hf))
				
				conn.commit()
				conn.close()
			
			# Refrescar la grilla dependiendo de la vista activa
			if hasattr(self, 'cb_profesor_horario') and hasattr(self, 'cb_turno_horario_prof') and self.cb_turno_horario_prof.winfo_exists() and self.cb_profesor_horario.get():
				self._dibujar_grilla_horario_profesor()
			elif hasattr(self, 'cb_division_horario') and hasattr(self, 'cb_turno_horario') and self.cb_turno_horario.winfo_exists() and self.cb_division_horario.get():
				self._dibujar_grilla_horario_curso()
			
			messagebox.showinfo('OK', 'Valores guardados.')
			win.destroy()

		btns = ttk.Frame(frame)
		btns.grid(row=11, column=0, columnspan=5, pady=15)
		ttk.Button(btns, text='Guardar', command=guardar, width=12).pack(side='left', padx=5)
		ttk.Button(btns, text='Cancelar', command=win.destroy, width=12).pack(side='left', padx=5)

	def mostrar_planes(self):
		self.limpiar_frame()
		ttk.Label(self.frame_principal, text='Gestión de Planes de Estudio', font=('Arial', 14)).pack(pady=10)
		frame_tabla = ttk.Frame(self.frame_principal)
		frame_tabla.pack(pady=10, fill='both', expand=True)
		self.tree_planes = crear_treeview(frame_tabla, ('Nombre',), ('Nombre',))
		self._recargar_planes_tree()

		form = ttk.Frame(self.frame_principal)
		form.pack(pady=10)
		ttk.Label(form, text='Nombre:').grid(row=0, column=0, padx=5, pady=2)
		self.entry_nombre_plan = ttk.Entry(form)
		self.entry_nombre_plan.grid(row=0, column=1, padx=5, pady=2)
		btns = ttk.Frame(self.frame_principal)
		btns.pack(pady=5)
		ttk.Button(btns, text='Agregar', command=self._agregar_plan).grid(row=0, column=0, padx=5)
		ttk.Button(btns, text='Eliminar', command=self._eliminar_plan).grid(row=0, column=1, padx=5)
		ttk.Button(btns, text='Materias del plan', command=self._gestionar_materias_plan).grid(row=0, column=2, padx=5)
		ttk.Button(btns, text='Años del plan', command=self._gestionar_anios_plan).grid(row=0, column=3, padx=5)
		self.tree_planes.bind('<<TreeviewSelect>>', self._on_select_plan)
		self.plan_seleccionado_id = None

	def _recargar_planes_tree(self):
		planes_ordenados = sorted(obtener_planes(), key=lambda p: p['nombre'].lower())
		recargar_treeview(self.tree_planes, planes_ordenados, ['nombre'])

	# Eliminada: _cargar_planes_en_tree (reemplazada por _recargar_planes_tree)

	def _agregar_plan(self):
		nombre = self.entry_nombre_plan.get().strip()
		if not nombre:
			messagebox.showerror('Error', 'Ingrese un nombre válido.')
			return
		try:
			crear_plan(nombre)
			self._cargar_planes_en_tree()
			self.entry_nombre_plan.delete(0, tk.END)
		except Exception as e:
			messagebox.showerror('Error', str(e))

	def _eliminar_plan(self):
		if not self.plan_seleccionado_id:
			messagebox.showerror('Error', 'Seleccione un plan.')
			return
		try:
			eliminar_plan(self.plan_seleccionado_id)
			self._cargar_planes_en_tree()
			self.plan_seleccionado_id = None
		except Exception as e:
			messagebox.showerror('Error', str(e))

	def _on_select_plan(self, event):
		sel = self.tree_planes.selection()
		if sel:
			self.plan_seleccionado_id = int(sel[0])
		else:
			self.plan_seleccionado_id = None

	def _gestionar_materias_plan(self):
		if not self.plan_seleccionado_id:
			messagebox.showerror('Error', 'Seleccione un plan.')
			return
		win = tk.Toplevel(self)
		win.configure(bg='#f4f6fa')
		win.title('Materias del plan')
		win.geometry('450x480')
		win.minsize(400, 420)
		win.transient(self)
		win.grab_set()
		win.focus_force()
		materias_plan = obtener_materias_de_plan(self.plan_seleccionado_id)
		todas_materias = sorted(obtener_materias(), key=lambda m: m['nombre'].lower())
		frame = ttk.Frame(win)
		frame.pack(fill='both', expand=True, padx=10, pady=10)
		tree = ttk.Treeview(frame, columns=('Nombre',), show='headings', height=10)
		tree.heading('Nombre', text='Nombre')
		tree.pack(side='left', fill='both', expand=True)
		vsb = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
		tree.configure(yscroll=vsb.set)
		vsb.pack(side='right', fill='y')
		def cargar():
			for row in tree.get_children():
				tree.delete(row)
			for m in materias_plan:
				tree.insert('', 'end', iid=m['id'], values=(m['nombre'],))
		cargar()
		def agregar():
			opciones = [p for p in todas_materias if p not in materias_plan]
			if not opciones:
				messagebox.showinfo('Info', 'No hay materias para agregar.')
				return
			win2 = tk.Toplevel(win)
			win2.configure(bg='#f4f6fa')
			win2.title('Agregar materia')
			win2.geometry('350x180')
			win2.minsize(320, 160)
			win2.transient(win)
			win2.grab_set()
			win2.focus_force()
			cb = ttk.Combobox(win2, values=[m['nombre'] for m in opciones], state='readonly')
			cb.pack(pady=10)
			def aceptar():
				nombre = cb.get()
				if not nombre:
					return
				materia = next((m for m in opciones if m['nombre'] == nombre), None)
				if materia:
					try:
						agregar_materia_a_plan(self.plan_seleccionado_id, materia['id'])
						materias_plan.append(materia)
						cargar()
						win2.destroy()
					except Exception as e:
						messagebox.showerror('Error', str(e))
			ttk.Button(win2, text='Agregar', command=aceptar).pack(pady=5)
			cb.bind('<Return>', lambda e: aceptar())
		def quitar():
			sel = tree.selection()
			if not sel:
				return
			materia_id = int(sel[0])
			try:
				quitar_materia_de_plan(self.plan_seleccionado_id, materia_id)
				materias_plan[:] = [m for m in materias_plan if m['id'] != materia_id]
				cargar()
			except Exception as e:
				messagebox.showerror('Error', str(e))
		btns = ttk.Frame(win)
		btns.pack(pady=5)
		ttk.Button(btns, text='Agregar materia', command=agregar).pack(side='left', padx=5)
		ttk.Button(btns, text='Quitar materia', command=quitar).pack(side='left', padx=5)
		# La accesibilidad con Enter se configura dentro de la función agregar


	def mostrar_turnos(self):
		self.limpiar_frame()
		ttk.Label(self.frame_principal, text='Gestión de Turnos', font=('Arial', 14)).pack(pady=10)
		frame_tabla = ttk.Frame(self.frame_principal)
		frame_tabla.pack(pady=10, fill='both', expand=True)
		self.tree_turnos = crear_treeview(frame_tabla, ('Nombre',), ('Nombre',))
		self._recargar_turnos_tree()

		form = ttk.Frame(self.frame_principal)
		form.pack(pady=10)
		ttk.Label(form, text='Nombre:').grid(row=0, column=0, padx=5, pady=2)
		self.entry_nombre_turno = ttk.Entry(form)
		self.entry_nombre_turno.grid(row=0, column=1, padx=5, pady=2)
		btns = ttk.Frame(self.frame_principal)
		btns.pack(pady=5)
		ttk.Button(btns, text='Agregar', command=self._agregar_turno).grid(row=0, column=0, padx=5)
		ttk.Button(btns, text='Eliminar', command=self._eliminar_turno).grid(row=0, column=1, padx=5)
		ttk.Button(btns, text='Planes del turno', command=self._gestionar_planes_turno).grid(row=0, column=2, padx=5)
		self.tree_turnos.bind('<<TreeviewSelect>>', self._on_select_turno)
		self.turno_seleccionado_id = None

	def _recargar_turnos_tree(self):
		turnos_ordenados = sorted(obtener_turnos(), key=lambda t: t['nombre'].lower())
		recargar_treeview(self.tree_turnos, turnos_ordenados, ['nombre'])

	# Eliminada: _cargar_turnos_en_tree (reemplazada por _recargar_turnos_tree)

	def _agregar_turno(self):
		nombre = self.entry_nombre_turno.get().strip()
		if not nombre:
			messagebox.showerror('Error', 'Ingrese un nombre válido.')
			return
		try:
			crear_turno(nombre)
			self._cargar_turnos_en_tree()
			self.entry_nombre_turno.delete(0, tk.END)
		except Exception as e:
			messagebox.showerror('Error', str(e))

	def _eliminar_turno(self):
		if not self.turno_seleccionado_id:
			messagebox.showerror('Error', 'Seleccione un turno.')
			return
		try:
			eliminar_turno(self.turno_seleccionado_id)
			self._cargar_turnos_en_tree()
			self.turno_seleccionado_id = None
		except Exception as e:
			messagebox.showerror('Error', str(e))

	def _on_select_turno(self, event):
		sel = self.tree_turnos.selection()
		if sel:
			self.turno_seleccionado_id = int(sel[0])
		else:
			self.turno_seleccionado_id = None

	def _gestionar_planes_turno(self):
		if not self.turno_seleccionado_id:
			messagebox.showerror('Error', 'Seleccione un turno.')
			return
		win = tk.Toplevel(self)
		win.configure(bg='#f4f6fa')
		win.title('Planes del turno')
		win.geometry('450x480')
		win.minsize(400, 420)
		win.transient(self)
		win.grab_set()
		win.focus_force()
		# Siempre obtener la lista actualizada desde la base
		def get_planes_turno():
			return obtener_planes_de_turno(self.turno_seleccionado_id)
		todos_planes = sorted(obtener_planes(), key=lambda p: p['nombre'].lower())
		frame = ttk.Frame(win)
		frame.pack(fill='both', expand=True, padx=10, pady=10)
		tree = ttk.Treeview(frame, columns=('Nombre',), show='headings', height=10)
		tree.heading('Nombre', text='Nombre')
		tree.pack(side='left', fill='both', expand=True)
		vsb = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
		tree.configure(yscroll=vsb.set)
		vsb.pack(side='right', fill='y')
		def cargar():
			for row in tree.get_children():
				tree.delete(row)
			# Usar set para evitar duplicados por error
			ids_insertados = set()
			for p in get_planes_turno():
				if p['id'] not in ids_insertados:
					tree.insert('', 'end', iid=p['id'], values=(p['nombre'],))
					ids_insertados.add(p['id'])
		cargar()
		def agregar():
			planes_turno_actual = get_planes_turno()
			opciones = [p for p in todos_planes if p not in planes_turno_actual]
			if not opciones:
				messagebox.showinfo('Info', 'No hay planes para agregar.')
				return
			win2 = tk.Toplevel(win)
			win2.configure(bg='#f4f6fa')
			win2.title('Agregar plan')
			win2.geometry('350x180')
			win2.minsize(320, 160)
			win2.transient(win)
			win2.grab_set()
			win2.focus_force()
			cb = ttk.Combobox(win2, values=[p['nombre'] for p in opciones], state='readonly')
			cb.pack(pady=10)
			def aceptar():
				nombre = cb.get()
				if not nombre:
					return
				plan = next((p for p in opciones if p['nombre'] == nombre), None)
				if plan:
					try:
						agregar_plan_a_turno(self.turno_seleccionado_id, plan['id'])
						cargar()
						win2.destroy()
					except Exception as e:
						messagebox.showerror('Error', str(e))
			ttk.Button(win2, text='Agregar', command=aceptar).pack(pady=5)
			cb.bind('<Return>', lambda e: aceptar())
		def quitar():
			sel = tree.selection()
			if not sel:
				return
			plan_id = int(sel[0])
			try:
				quitar_plan_de_turno(self.turno_seleccionado_id, plan_id)
				cargar()
			except Exception as e:
				messagebox.showerror('Error', str(e))
		btns = ttk.Frame(win)
		btns.pack(pady=5)
		ttk.Button(btns, text='Agregar plan', command=agregar).pack(side='left', padx=5)
		ttk.Button(btns, text='Quitar plan', command=quitar).pack(side='left', padx=5)

	def _gestionar_anios_plan(self):
		if not self.plan_seleccionado_id:
			messagebox.showerror('Error', 'Seleccione un plan.')
			return
		win = tk.Toplevel(self)
		win.configure(bg='#f4f6fa')
		win.title('Años del plan')
		win.geometry('450x480')
		win.minsize(400, 420)
		win.transient(self)
		win.grab_set()
		win.focus_force()
		anios_plan = obtener_anios(self.plan_seleccionado_id)
		frame = ttk.Frame(win)
		frame.pack(fill='both', expand=True, padx=10, pady=10)
		tree = ttk.Treeview(frame, columns=('Nombre',), show='headings', height=10)
		tree.heading('Nombre', text='Nombre')
		tree.pack(side='left', fill='both', expand=True)
		vsb = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
		tree.configure(yscroll=vsb.set)
		vsb.pack(side='right', fill='y')
		def cargar():
			for row in tree.get_children():
				tree.delete(row)
			for a in anios_plan:
				tree.insert('', 'end', iid=a['id'], values=(a['nombre'],))
		cargar()
		def agregar():
			win2 = tk.Toplevel(win)
			win2.configure(bg='#f4f6fa')
			win2.title('Agregar año')
			win2.geometry('350x180')
			win2.minsize(320, 160)
			ttk.Label(win2, text='Nombre:').pack(pady=5)
			entry = ttk.Entry(win2)
			entry.pack(pady=5)
			def aceptar():
				nombre = entry.get().strip()
				if not nombre:
					return
				try:
					crear_anio(nombre, self.plan_seleccionado_id)
					anios_plan.append({'id': obtener_anios(self.plan_seleccionado_id)[-1]['id'], 'nombre': nombre})
					cargar()
					win2.destroy()
				except Exception as e:
					messagebox.showerror('Error', str(e))
			ttk.Button(win2, text='Agregar', command=aceptar).pack(pady=5)
		def quitar():
			sel = tree.selection()
			if not sel:
				return
			anio_id = int(sel[0])
			try:
				eliminar_anio(anio_id)
				anios_plan[:] = [a for a in anios_plan if a['id'] != anio_id]
				cargar()
			except Exception as e:
				messagebox.showerror('Error', str(e))
		def materias():
			sel = tree.selection()
			if not sel:
				messagebox.showerror('Error', 'Seleccione un año.')
				return
			anio_id = int(sel[0])
			win3 = tk.Toplevel(win)
			win3.configure(bg='#f4f6fa')
			win3.title('Materias del año')
			win3.geometry('450x480')
			win3.minsize(400, 420)
			win3.transient(win)
			win3.grab_set()
			win3.focus_force()
			materias_anio = obtener_materias_de_anio(anio_id)
			materias_plan = obtener_materias_de_plan(self.plan_seleccionado_id)
			frame3 = ttk.Frame(win3)
			frame3.pack(fill='both', expand=True, padx=10, pady=10)
			tree3 = ttk.Treeview(frame3, columns=('Nombre',), show='headings', height=10)
			tree3.heading('Nombre', text='Nombre')
			tree3.pack(side='left', fill='both', expand=True)
			vsb3 = ttk.Scrollbar(frame3, orient='vertical', command=tree3.yview)
			tree3.configure(yscroll=vsb3.set)
			vsb3.pack(side='right', fill='y')
			def cargar3():
				for row in tree3.get_children():
					tree3.delete(row)
				for m in materias_anio:
					tree3.insert('', 'end', iid=m['id'], values=(m['nombre'],))
			cargar3()
			def agregar3():
				opciones = [m for m in materias_plan if m not in materias_anio]
				if not opciones:
					messagebox.showinfo('Info', 'No hay materias para agregar.')
					return
				win4 = tk.Toplevel(win3)
				win4.configure(bg='#f4f6fa')
				win4.title('Agregar materia')
				win4.geometry('350x180')
				win4.minsize(320, 160)
				win4.transient(win3)
				win4.grab_set()
				win4.focus_force()
				cb = ttk.Combobox(win4, values=[m['nombre'] for m in opciones], state='normal')
				cb.pack(pady=10)
				cb.focus_set()
				def filtrar_materias(event):
					typed = cb.get().lower()
					filtradas = [m['nombre'] for m in opciones if typed in m['nombre'].lower()]
					cb['values'] = filtradas if filtradas else [m['nombre'] for m in opciones]
				cb.bind('<KeyRelease>', filtrar_materias)
				def aceptar():
					nombre = cb.get()
					if not nombre:
						return
					materia = next((m for m in opciones if m['nombre'] == nombre), None)
					if materia:
						try:
							agregar_materia_a_anio(anio_id, materia['id'])
							materias_anio.append(materia)
							cargar3()
							win4.destroy()
						except Exception as e:
							messagebox.showerror('Error', str(e))
				ttk.Button(win4, text='Agregar', command=aceptar).pack(pady=5)
				cb.bind('<Return>', lambda e: aceptar())
			def quitar3():
				sel3 = tree3.selection()
				if not sel3:
					return
				materia_id = int(sel3[0])
				try:
					quitar_materia_de_anio(anio_id, materia_id)
					materias_anio[:] = [m for m in materias_anio if m['id'] != materia_id]
					cargar3()
				except Exception as e:
					messagebox.showerror('Error', str(e))
			btns3 = ttk.Frame(win3)
			btns3.pack(pady=5)
			ttk.Button(btns3, text='Agregar materia', command=agregar3).pack(side='left', padx=5)
			ttk.Button(btns3, text='Quitar materia', command=quitar3).pack(side='left', padx=5)
		btns = ttk.Frame(win)
		btns.pack(pady=5)
		ttk.Button(btns, text='Agregar año', command=agregar).pack(side='left', padx=5)
		ttk.Button(btns, text='Quitar año', command=quitar).pack(side='left', padx=5)
		ttk.Button(btns, text='Materias del año', command=materias).pack(side='left', padx=5)

	def _gestionar_turnos_profesor(self):
		if not self.profesor_seleccionado_id:
			messagebox.showwarning('Atención', 'Seleccione un profesor para gestionar sus turnos.')
			return
		profesor_id = self.profesor_seleccionado_id
		win = tk.Toplevel(self)
		win.configure(bg='#f4f6fa')
		win.title('Turnos del profesor')
		win.geometry('450x500')
		win.minsize(400, 450)
		win.transient(self)
		win.grab_set()
		win.focus_force()
		ttk.Label(win, text='Turnos asignados', font=('Arial', 12)).pack(pady=8)
		frame = ttk.Frame(win)
		frame.pack(fill='both', expand=True, padx=10, pady=10)
		tree_asignados = ttk.Treeview(frame, columns=('Nombre',), show='headings', height=6)
		tree_asignados.heading('Nombre', text='Turno')
		tree_asignados.pack(side='left', fill='both', expand=True)
		vsb = ttk.Scrollbar(frame, orient='vertical', command=tree_asignados.yview)
		tree_asignados.configure(yscroll=vsb.set)
		vsb.pack(side='right', fill='y')
		def cargar_turnos_asignados():
			for row in tree_asignados.get_children():
				tree_asignados.delete(row)
			for t in obtener_turnos_de_profesor(profesor_id):
				tree_asignados.insert('', 'end', iid=t['id'], values=(t['nombre'],))
		cargar_turnos_asignados()
		ttk.Label(win, text='Agregar turno').pack(pady=5)
		turnos = obtener_turnos()
		turnos_asignados = [t['id'] for t in obtener_turnos_de_profesor(profesor_id)]
		turnos_disponibles = [t for t in turnos if t['id'] not in turnos_asignados]
		cb_turno = ttk.Combobox(win, values=[t['nombre'] for t in turnos_disponibles], state='readonly')
		cb_turno.pack(pady=5)
		def cargar_turnos_disponibles():
			turnos = obtener_turnos()
			turnos_asignados = [t['id'] for t in obtener_turnos_de_profesor(profesor_id)]
			turnos_disponibles = [t for t in turnos if t['id'] not in turnos_asignados]
			cb_turno['values'] = [t['nombre'] for t in turnos_disponibles]
			cb_turno.set('')
		def agregar_turno():
			nombre = cb_turno.get()
			if not nombre:
				return
			turno = next((t for t in obtener_turnos() if t['nombre'] == nombre), None)
			if turno:
				try:
					asignar_turno_a_profesor(profesor_id, turno['id'])
					cargar_turnos_asignados()
					cargar_turnos_disponibles()
				except Exception as e:
					messagebox.showerror('Error', str(e))
		frame = ttk.Frame(win)
		frame.pack(pady=5)
		ttk.Button(frame, text='Agregar', command=agregar_turno).grid(row=0, column=0, padx=2)
		def quitar_turno():
			sel = tree_asignados.selection()
			if not sel:
				return
			turno_id = int(sel[0])
			if messagebox.askyesno('Confirmar', '¿Quitar turno del profesor?'):
				try:
					quitar_turno_a_profesor(profesor_id, turno_id)
					cargar_turnos_asignados()
					cargar_turnos_disponibles()
				except Exception as e:
					messagebox.showerror('Error', str(e))
		ttk.Button(frame, text='Quitar turno', command=quitar_turno).grid(row=0, column=1, padx=2)

if __name__ == "__main__":
    import tkinter as tk
    from tkinter import ttk, messagebox
    init_db()
    app = App()
    app.mainloop()
