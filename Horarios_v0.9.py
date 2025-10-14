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
	style.configure('TCombobox', padding=4, fieldbackground='#e9ecef', background='#e9ecef', selectbackground='#ffffff', selectforeground='#222')
	style.map('TCombobox',
		fieldbackground=[('readonly', '#ffffff'), ('!readonly', '#e9ecef')],
		background=[('readonly', '#ffffff'), ('!readonly', '#e9ecef')],
		selectbackground=[('!focus', '#ffffff'), ('focus', '#ffffff')],
		selectforeground=[('!focus', '#222'), ('focus', '#222')]
	)
	style.configure('Treeview', font=('Segoe UI', 10), rowheight=26, fieldbackground='#ffffff', background='#ffffff')
	style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'), background='#e0e7ef', foreground='#222')
	style.map('Treeview', background=[('selected', '#b3d1ff')])
	style.map('Treeview', foreground=[('selected', '#222')])
# MODELOS Y LOGICA DE DATOS PARA GESTION DE HORARIOS ESCOLARES
import sqlite3
from typing import List, Optional, Dict, Any


# Inicialización de la base de datos
DB_NAME = 'horarios.db'

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
		FOREIGN KEY(division_id) REFERENCES division(id),
		FOREIGN KEY(materia_id) REFERENCES materia(id),
		FOREIGN KEY(profesor_id) REFERENCES profesor(id),
		UNIQUE(division_id, dia, espacio)
	)''')
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

def obtener_planes_de_turno(turno_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT p.id, p.nombre FROM plan_estudio p
                 JOIN turno_plan tp ON tp.plan_id = p.id
                 WHERE tp.turno_id = ?''', (turno_id,))
    planes = [{'id': row[0], 'nombre': row[1]} for row in c.fetchall()]
    conn.close()
    return planes

def obtener_planes_de_turno(turno_id: int) -> list:
	conn = get_connection()
	c = conn.cursor()
	c.execute('''SELECT p.id, p.nombre FROM plan_materia pm
				 JOIN plan_estudio p ON pm.plan_id = p.id
				 JOIN turno_plan tp ON tp.plan_id = p.id
				 WHERE tp.turno_id=?''', (turno_id,))
	rows = c.fetchall()
	conn.close()
	return [{'id': r[0], 'nombre': r[1]} for r in rows]

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
def crear_horario(division_id: int, dia: str, espacio: int, hora_inicio: str, hora_fin: str, materia_id: int, profesor_id: int):
	conn = get_connection()
	c = conn.cursor()
	# Obtener el turno de la división actual
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

	c.execute('''INSERT INTO horario (division_id, dia, espacio, hora_inicio, hora_fin, materia_id, profesor_id) VALUES (?, ?, ?, ?, ?, ?, ?)''',
			  (division_id, dia, espacio, hora_inicio_db, hora_fin_db, materia_id, profesor_id))

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

# Inicializar la base de datos al importar el módulo
init_db()

# ================= INTERFAZ GRAFICA BASE ===================

import tkinter as tk
from tkinter import ttk, messagebox

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

		divisiones_menu = tk.Menu(menubar, tearoff=0)
		divisiones_menu.add_command(label='Gestionar Divisiones', command=self.mostrar_divisiones)
		menubar.add_cascade(label='Divisiones', menu=divisiones_menu)

		horarios_menu = tk.Menu(menubar, tearoff=0)
		horarios_menu.add_command(label='Gestionar Horarios', command=self.mostrar_horarios)
		menubar.add_cascade(label='Horarios', menu=horarios_menu)

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
			self._cargar_divisiones_en_tree()
			self.entry_nombre_division.delete(0, tk.END)
			self.cb_turno_division.set('')
			self.cb_plan_division.set('')
			self.cb_anio_division.set('')
			self.division_seleccionada_id = None
		except Exception as e:
			messagebox.showerror('Error', str(e))


	def mostrar_divisiones(self):
		self.limpiar_frame()
		ttk.Label(self.frame_principal, text='Gestión de Divisiones', font=('Arial', 14)).pack(pady=10)

		# Totales
		divisiones = obtener_divisiones()
		total_divisiones = len(divisiones)
		frame_tot = ttk.Frame(self.frame_principal)
		frame_tot.pack(pady=2)
		ttk.Label(frame_tot, text=f'Total de divisiones: {total_divisiones}').grid(row=0, column=0, padx=10)

		# Filtro
		frame_filtro = ttk.Frame(self.frame_principal)
		frame_filtro.pack(pady=2)
		ttk.Label(frame_filtro, text='Filtro:').grid(row=0, column=0, padx=5)
		self.filtro_division = tk.StringVar()
		entry_filtro = ttk.Entry(frame_filtro, textvariable=self.filtro_division)
		entry_filtro.grid(row=0, column=1, padx=5)

		# Selección de Turno, Plan, Año, División
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
		ttk.Label(frame_sel, text='División:').grid(row=0, column=6, padx=5)
		self.cb_division_horario = ttk.Combobox(frame_sel, values=[], state='disabled')
		self.cb_division_horario.grid(row=0, column=7, padx=5)

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
		self.cb_turno_division.bind('<<ComboboxSelected>>', on_turno_selected)
		self.cb_plan_division.bind('<<ComboboxSelected>>', on_plan_selected)

		# Tabla de divisiones usando helper
		frame_tabla = ttk.Frame(self.frame_principal)
		frame_tabla.pack(pady=10, fill='both', expand=True)
		self.tree_divisiones = crear_treeview(frame_tabla, ('Nombre', 'Turno', 'Plan', 'Año'), ('Nombre', 'Turno', 'Plan', 'Año'))
		self._recargar_divisiones_tree()

		def filtrar_divisiones(*args):
			filtro = self.filtro_division.get().lower()
			divisiones = obtener_divisiones()
			datos = []
			for c in divisiones:
				turno = next((t['nombre'] for t in obtener_turnos() if t['id'] == c['turno_id']), '')
				plan = next((p['nombre'] for p in obtener_planes() if p['id'] == c['plan_id']), '')
				anio = next((a['nombre'] for a in obtener_anios(c['plan_id']) if a['id'] == c['anio_id']), '')
				if filtro in c['nombre'].lower():
					datos.append({'id': c['id'], 'Nombre': c['nombre'], 'Turno': turno, 'Plan': plan, 'Año': anio})
			recargar_treeview(self.tree_divisiones, datos, ['Nombre', 'Turno', 'Plan', 'Año'])
		self.filtro_division.trace_add('write', filtrar_divisiones)

		# Formulario de alta/edición
		form = ttk.Frame(self.frame_principal)
		form.pack(pady=10)
		ttk.Label(form, text='Nombre:').grid(row=0, column=0, padx=5, pady=2)
		self.entry_nombre_division = ttk.Entry(form)
		self.entry_nombre_division.grid(row=0, column=1, padx=5, pady=2)

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
		datos = []
		for c in divisiones:
			turno = next((t['nombre'] for t in obtener_turnos() if t['id'] == c['turno_id']), '')
			plan = next((p['nombre'] for p in obtener_planes() if p['id'] == c['plan_id']), '')
			anio = next((a['nombre'] for a in obtener_anios(c['plan_id']) if a['id'] == c['anio_id']), '')
			datos.append({'id': c['id'], 'Nombre': c['nombre'], 'Turno': turno, 'Plan': plan, 'Año': anio})
		recargar_treeview(self.tree_divisiones, datos, ['Nombre', 'Turno', 'Plan', 'Año'])

	# Eliminada: _cargar_divisiones_en_tree (reemplazada por _recargar_divisiones_tree)

	def _agregar_division(self):
		nombre = self.entry_nombre_division.get().strip()
		if not nombre:
			messagebox.showerror('Error', 'Ingrese un nombre válido.')
			return
		turno_nombre = self.cb_turno_division.get()
		plan_nombre = self.cb_plan_division.get()
		anio_nombre = self.cb_anio_division.get()
		if not (turno_nombre and plan_nombre and anio_nombre):
			messagebox.showerror('Error', 'Seleccione turno, plan y año.')
			return
		turno_id = self.turnos_dict[turno_nombre]
		plan_id = self.planes_dict[plan_nombre]
		anios = obtener_anios(plan_id)
		anio_id = next((a['id'] for a in anios if a['nombre'] == anio_nombre), None)
		if not anio_id:
			messagebox.showerror('Error', 'Año inválido.')
			return
		try:
			conn = get_connection()
			c = conn.cursor()
			c.execute('INSERT INTO division (nombre, turno_id, plan_id, anio_id) VALUES (?, ?, ?, ?)', (nombre, turno_id, plan_id, anio_id))
			conn.commit()
			conn.close()
			self._cargar_divisiones_en_tree()
			self.entry_nombre_division.delete(0, tk.END)
		except Exception as e:
			if 'UNIQUE constraint failed' in str(e):
				messagebox.showerror('Error', 'Ya existe una división con ese nombre, turno, plan y año.')
			else:
				messagebox.showerror('Error', str(e))

	def _editar_division(self):
		if not self.division_seleccionada_id:
			messagebox.showerror('Error', 'Seleccione una división para editar.')
			return
		nombre = self.entry_nombre_division.get().strip()
		turno_nombre = self.cb_turno_division.get()
		plan_nombre = self.cb_plan_division.get()
		anio_nombre = self.cb_anio_division.get()
		if not (nombre and turno_nombre and plan_nombre and anio_nombre):
			messagebox.showerror('Error', 'Complete todos los campos.')
			return
		turno_id = self.turnos_dict[turno_nombre]
		plan_id = self.planes_dict[plan_nombre]
		anios = obtener_anios(plan_id)
		anio_id = next((a['id'] for a in anios if a['nombre'] == anio_nombre), None)
		if not anio_id:
			messagebox.showerror('Error', 'Año inválido.')
			return
		try:
			conn = get_connection()
			c = conn.cursor()
			c.execute('UPDATE division SET nombre=?, turno_id=?, plan_id=?, anio_id=? WHERE id=?', (nombre, turno_id, plan_id, anio_id, self.division_seleccionada_id))
			conn.commit()
			conn.close()
			self._cargar_divisiones_en_tree()
		except Exception as e:
			messagebox.showerror('Error', str(e))

	def _on_select_division(self, event=None):
		sel = self.tree_divisiones.selection()
		if not sel:
			self.division_seleccionada_id = None
			return
		cid = sel[0]
		self.division_seleccionada_id = cid
		divisiones = obtener_divisiones()
		c = next((x for x in divisiones if str(x['id']) == str(cid)), None)
		if c:
			self.entry_nombre_division.delete(0, tk.END)
			self.entry_nombre_division.insert(0, c['nombre'])
			# Set turno, plan, año in comboboxes
			turno = next((t['nombre'] for t in obtener_turnos() if t['id'] == c['turno_id']), '')
			self.cb_turno_division.set(turno)
			# Trigger plan loading
			self.cb_turno_division.event_generate('<<ComboboxSelected>>')
			plan = next((p['nombre'] for p in obtener_planes() if p['id'] == c['plan_id']), '')
			self.cb_plan_division.set(plan)
			# Trigger año loading
			self.cb_plan_division.event_generate('<<ComboboxSelected>>')
			anio = next((a['nombre'] for a in obtener_anios(c['plan_id']) if a['id'] == c['anio_id']), '')
			self.cb_anio_division.set(anio)

	def mostrar_horarios(self):
		self.limpiar_frame()
		ttk.Label(self.frame_principal, text='Gestión de Horarios', font=('Arial', 14)).pack(pady=10)

		# Selección paso a paso: Turno → Plan → Año → División
		frame_sel = ttk.Frame(self.frame_principal)
		frame_sel.pack(pady=5)
		ttk.Label(frame_sel, text='Turno:').grid(row=0, column=0, padx=5)
		turnos = obtener_turnos()
		self.turnos_dict_horario = {t['nombre']: t['id'] for t in turnos}
		self.cb_turno_horario = ttk.Combobox(frame_sel, values=list(self.turnos_dict_horario.keys()), state='readonly')
		self.cb_turno_horario.grid(row=0, column=1, padx=5)
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
			self.cb_plan_horario['values'] = list(self.planes_dict_horario.keys())
			self.cb_plan_horario.set('')
			self.cb_plan_horario.config(state='readonly' if planes else 'disabled')
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
			self.cb_anio_horario['values'] = list(self.anios_dict_horario.keys())
			self.cb_anio_horario.set('')
			self.cb_anio_horario.config(state='readonly' if anios else 'disabled')
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
			self.cb_division_horario['values'] = list(self.divisiones_dict_horario.keys())
			self.cb_division_horario.set('')
			self.cb_division_horario.config(state='readonly' if divisiones else 'disabled')
		def on_division_selected(event=None):
			self._dibujar_grilla_horario()
		self.cb_turno_horario.bind('<<ComboboxSelected>>', on_turno_selected)
		self.cb_plan_horario.bind('<<ComboboxSelected>>', on_plan_selected)
		self.cb_anio_horario.bind('<<ComboboxSelected>>', on_anio_selected)
		self.cb_division_horario.bind('<<ComboboxSelected>>', on_division_selected)

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
		ttk.Button(frame_bottom_btns, text='Configurar horas por turno', command=self._configurar_horas_por_turno).pack()

	def _dibujar_grilla_horario(self):
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
								command=lambda d=dia, e=esp: self._editar_espacio_horario(d, e))
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

	def _editar_espacio_horario(self, dia, espacio):
		division_nombre = getattr(self, 'cb_division_horario', None)
		if not division_nombre or not self.cb_division_horario.get():
			return
		division_id = self.divisiones_dict_horario[self.cb_division_horario.get()]
		win = tk.Toplevel(self)
		win.configure(bg='#f4f6fa')
		sufijo = 'ª'
		win.title(f'{dia} - {espacio}{sufijo} hora')
		win.geometry('450x450')
		win.minsize(400, 400)
		win.transient(self)
		win.grab_set()
		win.focus_force()
		win.configure(bg='#f4f6fa')
		ttk.Label(win, text=f'{dia} - {espacio}{sufijo} hora', font=('Segoe UI', 13, 'bold'), background='#e0e7ef', foreground='#2a3a4a').pack(pady=10, fill='x')

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
					cb_profesor['values'] = nombres_profesores
					cb_profesor.set('')
					cb_profesor.config(state='readonly' if nombres_profesores else 'disabled')
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
				crear_horario(division_id, dia, espacio, hora_inicio, hora_fin, mid, pid)
				self._dibujar_grilla_horario()
				win.destroy()
			except Exception as e:
				if datos_previos:
					try:
						crear_horario(division_id, dia, espacio, datos_previos['hora_inicio'], datos_previos['hora_fin'], datos_previos['materia_id'], datos_previos['profesor_id'])
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
						self._dibujar_grilla_horario()
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
		win.geometry('550x550')
		win.minsize(500, 500)
		win.transient(self)
		win.grab_set()
		win.focus_force()
		frame = ttk.Frame(win)
		frame.pack(padx=10, pady=10, fill='both', expand=True)
		ttk.Label(frame, text='Turno:').grid(row=0, column=0, padx=5, pady=5, sticky='w')
		turnos = obtener_turnos()
		turnos_dict = {t['nombre']: t['id'] for t in turnos}
		cb_turno = ttk.Combobox(frame, values=list(turnos_dict.keys()), state='readonly')
		cb_turno.grid(row=0, column=1, padx=5, pady=5, sticky='w')

		# Tabla simple para espacios
		entries = {}
		for esp in range(1, 9):
			ttk.Label(frame, text=f'{esp}ª:').grid(row=esp, column=0, padx=5, pady=2, sticky='e')
			e_inicio = ttk.Entry(frame, width=8)
			e_inicio.grid(row=esp, column=1, padx=5, pady=2, sticky='w')
			e_fin = ttk.Entry(frame, width=8)
			e_fin.grid(row=esp, column=2, padx=5, pady=2, sticky='w')
			entries[esp] = (e_inicio, e_fin)

		apply_var = tk.IntVar(value=0)
		chk_apply = ttk.Checkbutton(frame, text='Aplicar a horarios existentes', variable=apply_var)
		chk_apply.grid(row=9, column=0, columnspan=3, pady=8, sticky='w')

		def cargar_defaults(event=None):
			nombre = cb_turno.get()
			if not nombre:
				for esp in entries:
					entries[esp][0].delete(0, tk.END)
					entries[esp][1].delete(0, tk.END)
				return
			turno_id = turnos_dict[nombre]
			for esp in entries:
				d = obtener_turno_espacio_hora(turno_id, esp)
				entries[esp][0].delete(0, tk.END)
				entries[esp][1].delete(0, tk.END)
				if d:
					if d.get('hora_inicio'):
						entries[esp][0].insert(0, d.get('hora_inicio'))
					if d.get('hora_fin'):
						entries[esp][1].insert(0, d.get('hora_fin'))

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
				set_turno_espacio_hora(turno_id, esp, hi if hi else None, hf if hf else None)
			# Aplicar a horarios existentes si se pidió
			if apply_var.get():
				conn = get_connection()
				c = conn.cursor()
				# Obtener divisiones del turno
				c.execute('SELECT id FROM division WHERE turno_id=?', (turno_id,))
				divs = [r[0] for r in c.fetchall()]
				dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
				for esp in entries:
					hi = entries[esp][0].get().strip() or None
					hf = entries[esp][1].get().strip() or None
					if hi is None and hf is None:
						continue
					for div in divs:
						for dia in dias:
							# Si existe fila para division+dia+espacio, actualizar donde falte
							c.execute('SELECT id FROM horario WHERE division_id=? AND espacio=? AND dia=?', (div, esp, dia))
							row = c.fetchone()
							if row:
								# Sobrescribir las horas existentes con los nuevos valores
								c.execute('UPDATE horario SET hora_inicio = ?, hora_fin = ? WHERE id=?', (hi, hf, row[0]))
							else:
								# Insertar nuevo horario con materia y profesor NULL para que la casilla muestre las horas
								c.execute('INSERT INTO horario (division_id, dia, espacio, hora_inicio, hora_fin, materia_id, profesor_id) VALUES (?, ?, ?, ?, ?, NULL, NULL)', (div, dia, esp, hi, hf))
				conn.commit()
				conn.close()
			messagebox.showinfo('OK', 'Valores guardados.')
			win.destroy()

		btns = ttk.Frame(frame)
		btns.grid(row=10, column=0, columnspan=3, pady=10)
		ttk.Button(btns, text='Guardar', command=guardar).pack(side='left', padx=5)
		ttk.Button(btns, text='Cancelar', command=win.destroy).pack(side='left', padx=5)

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
