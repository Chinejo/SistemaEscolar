################################################################################
# SISTEMA DE GESTIÓN DE HORARIOS ESCOLARES - VERSION 1.0
################################################################################
#
# DESCRIPCIÓN GENERAL:
#   Aplicación de escritorio desarrollada en Python con Tkinter para la gestión
#   integral de horarios escolares. El sistema maneja la asignación de profesores
#   a diferentes turnos, ciclos, divisiones y materias, generando horarios
#   optimizados con validación de conflictos y capacidad de exportación a Excel.
#
# DEPENDENCIAS PRINCIPALES:
#   - sqlite3: Persistencia de datos en base de datos relacional
#   - tkinter: Interfaz gráfica de usuario (GUI)
#   - xlwt: Exportación de horarios a formato Excel
#   - hashlib: Hash seguro de contraseñas
#   - datetime: Manejo de fechas y horas
#
# ESTRUCTURA DE DATOS PRINCIPALES:
#   - Materia/Obligación: Asignaturas con carga horaria semanal
#   - Profesor: Personal educativo asignable a turnos
#   - Ciclo: Niveles educativos (1er año, 2do año, etc.) con planes de estudio
#   - Plan de Estudio: Conjuntos de materias por ciclo y turno
#   - Turno: Jornadas (Mañana, Tarde, Noche)
#   - División: Cursos/secciones dentro de ciclos
#   - Horario: Asignación de profesor-materia a división en día/hora específico
#   - Usuario: Credenciales de acceso (Administrador, Usuario regular)
#
# TABLA DE CONTENIDOS:
#   1. IMPORTS Y CONFIGURACIÓN GLOBAL (líneas ~1-13)
#   2. FUNCIONES DE INICIALIZACIÓN Y CONEXIÓN BD (líneas ~15-35)
#   3. DECORADOR Y FUNCIONES GENÉRICAS CRUD (líneas ~36-78)
#   4. FUNCIONES AUXILIARES DE BASE DE DATOS (líneas ~79-115)
#   5. CONSTANTES Y VARIABLES GLOBALES (líneas ~116-120)
#   6. FUNCIONES DE EXPORTACIÓN A EXCEL (líneas ~121-290)
#   7. FUNCIÓN DE INICIALIZACIÓN DE ESQUEMA BD (líneas ~291-400)
#   8. MÓDULO: GESTIÓN DE MATERIAS (líneas ~401-500)
#   9. MÓDULO: GESTIÓN DE PROFESORES (líneas ~501-600)
#   10. MÓDULO: GESTIÓN DE PROFESOR-TURNO (líneas ~601-650)
#   11. MÓDULO: BANCA DE HORAS (líneas ~651-700)
#   12. MÓDULO: GESTIÓN DE CICLOS (líneas ~701-800)
#   13. MÓDULO: GESTIÓN DE CICLO-MATERIA (líneas ~801-850)
#   14. MÓDULO: GESTIÓN DE PLANES DE ESTUDIO (líneas ~851-950)
#   15. MÓDULO: GESTIÓN DE TURNOS (líneas ~951-1050)
#   16. MÓDULO: GESTIÓN DE DIVISIONES (líneas ~1051-1150)
#   17. MÓDULO: GESTIÓN DE HORARIOS (líneas ~1151-1300)
#   18. MÓDULO: GESTIÓN DE USUARIO-TURNO-HORA (líneas ~1301-1350)
#   19. MÓDULO: GESTIÓN DE USUARIO (líneas ~1351-1400)
#   20. MÓDULO: RESPALDOS (BACKUPS) (líneas ~1401-1450)
#   21. MÓDULO: GESTIÓN DE USUARIOS DEL SISTEMA (líneas ~1451-1550)
#   22. MÓDULO: CLASES BASE Y UTILIDADES GUI (líneas ~1551-1650)
#   23. CLASE PRINCIPAL App: APLICACIÓN TKINTER (líneas ~1651-6200)
#       23.1. INICIALIZACIÓN Y AUTENTICACIÓN
#       23.2. GESTIÓN DE MATERIAS
#       23.3. GESTIÓN DE PERSONAL Y CICLOS
#       23.4. GESTIÓN DE DIVISIONES
#       23.5. GESTIÓN DE HORARIOS POR CURSO
#       23.6. GESTIÓN DE HORARIOS POR PROFESOR
#       23.7. CONFIGURACIÓN DE HORAS POR TURNO
#       23.8. GESTIÓN DE TURNOS, PLANES Y MATERIAS
#       23.9. EXPORTACIÓN DE HORARIOS
#       23.10. GESTIÓN DE USUARIOS DEL SISTEMA
#       23.11. GESTIÓN DE RESPALDOS (BACKUPS)
#   24. PUNTO DE ENTRADA PRINCIPAL (línea ~6250)
#
# GLOSARIO DE TÉRMINOS:
#   - Materia: Asignatura curricular (Matemáticas, Lengua, etc.)
#   - Profesor: Docente asignado a las materias
#   - Ciclo: Nivel educativo (Primero, Segundo, Tercero)
#   - Plan de Estudio: Conjunto de materias de un ciclo en un turno
#   - Turno: Jornada educativa (Mañana, Tarde, Noche)
#   - División: Sección de un ciclo (1°A, 1°B, etc.)
#   - Horario: Asignación de profesor-materia a división en día/hora
#   - Banca de Horas: Cantidad de horas que puede enseñar un profesor
#   - Espacio Horario: Franja de tiempo en un turno (8:00-8:45, etc.)
#
# NOTA DE REFACTORIZACIÓN:
#   Este código es un monolito funcional diseñado para futuras refactorizaciones.
#   Los comentarios de sección y subsección indican los módulos que serán
#   extraídos en version 2.0 a una estructura modular separada.
#
################################################################################

import hashlib
import os
import shutil
import sqlite3
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import xlwt


# ═══════════════════════════════════════════════════════════════════════════════
# 2. INICIALIZACIÓN DE BASE DE DATOS Y CONEXIÓN
# ═══════════════════════════════════════════════════════════════════════════════
# Funciones para obtener la ruta de la aplicación, crear conexiones a la BD
# y gestionar el ciclo de vida de la conexión a SQLite.
# ───────────────────────────────────────────────────────────────────────────────

def obtener_ruta_base():
	"""
	Obtiene la ruta base de la aplicación.
	
	Detecta si se ejecuta desde un script Python o desde un ejecutable compilado
	con PyInstaller, devolviendo la ruta correcta en cada caso.
	
	Retorna:
		str: Ruta del directorio base de la aplicación
		
	Notas:
		- En desarrollo: devuelve el directorio del archivo .py
		- En PyInstaller: devuelve el directorio del ejecutable .exe
	"""
	if getattr(sys, 'frozen', False):
		# Ejecutando desde PyInstaller compilado
		return os.path.dirname(sys.executable)
	else:
		# Ejecutando desde script Python normal en desarrollo
		return os.path.dirname(os.path.abspath(__file__))


# Configuración global de la base de datos
RUTA_BD_DIR = obtener_ruta_base()
RUTA_BD_COMPLETA = os.path.join(RUTA_BD_DIR, 'institucion.db')

# Mantener referencias globales para compatibilidad con código existente
DB_DIR = RUTA_BD_DIR
DB_NAME = RUTA_BD_COMPLETA

# Aliases de compatibilidad para nombres anteriores en inglés
get_base_path = obtener_ruta_base

def obtener_conexion():
	"""
	Obtiene una conexión a la base de datos SQLite.
	
	Crea una conexión con configuración segura para:
	- Mantener restricciones de clave foránea (PRAGMA foreign_keys)
	- Evitar bloqueos por lecturas prolongadas (busy_timeout)
	- Permitir múltiples operaciones concurrentes
	
	Retorna:
		sqlite3.Connection: Conexión abierta a la base de datos
		
	Notas:
		- El timeout de 15 segundos previene bloqueos indefinidos
		- La restricción foreign_keys = ON mantiene la integridad referencial
	"""
	conn = sqlite3.connect(RUTA_BD_COMPLETA, timeout=15)
	# Mantener restricciones referenciales para integridad de datos
	conn.execute('PRAGMA foreign_keys = ON')
	# Evitar bloqueos por lecturas prolongadas (timeout: 15 segundos)
	conn.execute('PRAGMA busy_timeout = 15000')
	return conn

# Mantener compatibilidad con código existente
get_connection = obtener_conexion

# ───────────────────────────────────────────────────────────────────────────────
# DECORADOR: Automatización de conexión y transacciones
# ───────────────────────────────────────────────────────────────────────────────

def operacion_bd(funcion):
	"""
	Decorador que centraliza la gestión de conexiones a base de datos.
	
	Automáticamente:
	- Obtiene una conexión a la BD antes de ejecutar la función
	- Realiza un commit si la función completa sin errores
	- Cierra la conexión al finalizar (éxito o error)
	- Captura y re-lanza excepciones de integridad
	
	Uso:
		@operacion_bd
		def mi_funcion(conn, parametro1, parametro2):
			# La función recibe 'conn' como primer argumento
			# El resto de parámetros se pasan normalmente
			pass
		
	Notas:
		- La función decorada debe aceptar 'conn' como primer parámetro
		- Los cambios se confirman automáticamente (auto-commit)
		- Las excepciones de integridad se envuelven en Exception
	"""
	def envoltorio(*args, **kwargs):
		conn = obtener_conexion()
		try:
			resultado = funcion(conn, *args, **kwargs)
			conn.commit()
			return resultado
		except sqlite3.IntegrityError as e:
			# Violación de restricción de integridad (ej: clave foránea, clave única)
			raise Exception(str(e))
		finally:
			conn.close()
	return envoltorio

# Compatibilidad con nombre anterior en inglés
db_operation = operacion_bd

# ───────────────────────────────────────────────────────────────────────────────
# FUNCIONES GENÉRICAS CRUD
# ───────────────────────────────────────────────────────────────────────────────
# Operaciones básicas Create, Read, Update, Delete para entidades genéricas
# Utilizadas por funciones específicas de cada módulo de negocio.
# ............................................................................

@operacion_bd
def crear_entidad(conn, tabla, campos, valores):
	"""
	Inserta una nueva fila en una tabla (operación Create).
	
	Parámetros:
		conn: Conexión a BD (inyectada por decorador)
		tabla (str): Nombre de la tabla donde insertar
		campos (list): Lista de nombres de columnas
		valores (tuple): Tupla de valores en el mismo orden que campos
		
	Retorna:
		None (pero confirma cambios en BD)
		
	Ejemplo:
		crear_entidad('materias', ['nombre', 'horas_semanales'], ['Matemática', 3])
	"""
	placeholders = ','.join(['?']*len(valores))
	campos_str = ','.join(campos)
	conn.execute(f'INSERT INTO {tabla} ({campos_str}) VALUES ({placeholders})', valores)

@operacion_bd
def obtener_entidades(conn, tabla, campos):
	"""
	Recupera todas las filas de una tabla (operación Read/Get).
	
	Parámetros:
		conn: Conexión a BD (inyectada por decorador)
		tabla (str): Nombre de la tabla
		campos (list): Lista de nombres de columnas a recuperar
		
	Retorna:
		list: Lista de diccionarios con estructura {campo: valor, ...}
		
	Ejemplo:
		resultado = obtener_entidades('materias', ['id', 'nombre', 'horas_semanales'])
		# Retorna: [{'id': 1, 'nombre': 'Matemática', 'horas_semanales': 3}, ...]
	"""
	c = conn.cursor()
	c.execute(f'SELECT {','.join(campos)} FROM {tabla}')
	return [dict(zip(campos, row)) for row in c.fetchall()]

@operacion_bd
def actualizar_entidad(conn, tabla, campos, valores, id_campo, id_valor):
	"""
	Actualiza una fila existente en una tabla (operación Update).
	
	Parámetros:
		conn: Conexión a BD (inyectada por decorador)
		tabla (str): Nombre de la tabla
		campos (list): Lista de columnas a actualizar
		valores (tuple): Nuevos valores en el mismo orden que campos
		id_campo (str): Nombre del campo ID para identificar la fila
		id_valor: Valor del ID de la fila a actualizar
		
	Retorna:
		None (pero confirma cambios en BD)
		
	Ejemplo:
		actualizar_entidad('materias', ['nombre', 'horas'], ['Álgebra', 4], 'id', 1)
	"""
	set_str = ','.join([f'{campo}=?' for campo in campos])
	conn.execute(f'UPDATE {tabla} SET {set_str} WHERE {id_campo}=?', (*valores, id_valor))

@operacion_bd
def eliminar_entidad(conn, tabla, id_campo, id_valor):
	"""
	Elimina una fila de una tabla (operación Delete).
	
	Parámetros:
		conn: Conexión a BD (inyectada por decorador)
		tabla (str): Nombre de la tabla
		id_campo (str): Nombre del campo ID para identificar la fila
		id_valor: Valor del ID de la fila a eliminar
		
	Retorna:
		None (pero confirma cambios en BD)
		
	Ejemplo:
		eliminar_entidad('materias', 'id', 5)
	"""
	conn.execute(f'DELETE FROM {tabla} WHERE {id_campo}=?', (id_valor,))

# ───────────────────────────────────────────────────────────────────────────────
# FUNCIONES AUXILIARES DE BASE DE DATOS
# ───────────────────────────────────────────────────────────────────────────────

def _tabla_existe(conn, nombre_tabla: str) -> bool:
	"""
	Verifica si una tabla existe en la base de datos.
	
	Parámetros:
		conn: Conexión a BD
		nombre_tabla (str): Nombre de la tabla a verificar
		
	Retorna:
		bool: True si la tabla existe, False en caso contrario
	"""
	c = conn.cursor()
	c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (nombre_tabla,))
	return c.fetchone() is not None

# Compatibilidad con nombre anterior
_table_exists = _tabla_existe


# ═══════════════════════════════════════════════════════════════════════════════
# 3. CONSTANTES Y CONFIGURACIÓN GLOBAL
# ═══════════════════════════════════════════════════════════════════════════════
# Constantes de configuración para horarios, espacios y exportación a Excel.
# ───────────────────────────────────────────────────────────────────────────────

# Días de la semana base en el calendario escolar
HORARIO_DIAS_BASE = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']

# Número de espacios horarios (franjas de tiempo) por defecto en un turno
# Ej: 8 espacios = 8 bloques de 45 minutos cada uno (8:00-8:45, 8:45-9:30, ...)
ESPACIOS_POR_DEFECTO = 8

# Caracteres inválidos en nombres de hojas Excel según formato XLSX
# Estos caracteres causan error si se usan en nombres de hojas
_HOJA_CARACTERES_INVALIDOS = set('[]:*?/\\')


# ═══════════════════════════════════════════════════════════════════════════════
# 4. FUNCIONES AUXILIARES PARA EXPORTACIÓN A EXCEL
# ═══════════════════════════════════════════════════════════════════════════════
# Funciones helper para consultar información de horarios, días y espacios que
# será exportada a planillas Excel. Estas se utilizan en el módulo de exportación.
# ───────────────────────────────────────────────────────────────────────────────


def _obtener_dias_para_export() -> List[str]:
	"""Obtiene los días en orden para construir las planillas, admitiendo días nuevos."""
	dias_base = HORARIO_DIAS_BASE.copy()
	conn = get_connection()
	try:
		if not _table_exists(conn, 'horario'):
			return dias_base
		c = conn.cursor()
		c.execute("SELECT DISTINCT dia FROM horario WHERE dia IS NOT NULL AND dia <> ''")
		extras = []
		for row in c.fetchall():
			dia = row[0]
			if not dia:
				continue
			if dia not in dias_base and dia not in extras:
				extras.append(dia)
		extras.sort(key=lambda x: x.lower())
		return dias_base + extras
	finally:
		conn.close()


def _obtener_max_espacios_para_export() -> int:
	"""Calcula la cantidad máxima de espacios a exportar considerando la base."""
	max_espacio = ESPACIOS_POR_DEFECTO
	conn = get_connection()
	try:
		c = conn.cursor()
		if _table_exists(conn, 'horario'):
			c.execute('SELECT MAX(espacio) FROM horario')
			row = c.fetchone()
			if row and row[0]:
				max_espacio = max(max_espacio, int(row[0]))
		if _table_exists(conn, 'turno_espacio_hora'):
			c.execute('SELECT MAX(espacio) FROM turno_espacio_hora')
			row = c.fetchone()
			if row and row[0]:
				max_espacio = max(max_espacio, int(row[0]))
	finally:
			conn.close()
	return max_espacio


def _crear_estilos_xls() -> Dict[str, xlwt.XFStyle]:
	"""Crea estilos reutilizables para las planillas XLS."""
	def _bordes():
		b = xlwt.Borders()
		b.left = xlwt.Borders.THIN
		b.right = xlwt.Borders.THIN
		b.top = xlwt.Borders.THIN
		b.bottom = xlwt.Borders.THIN
		return b

	head_font = xlwt.Font()
	head_font.bold = True
	head_align = xlwt.Alignment()
	head_align.horz = xlwt.Alignment.HORZ_CENTER
	head_align.vert = xlwt.Alignment.VERT_CENTER
	head_style = xlwt.XFStyle()
	head_style.font = head_font
	head_style.alignment = head_align
	head_style.borders = _bordes()

	index_style = xlwt.XFStyle()
	index_font = xlwt.Font()
	index_font.bold = True
	index_align = xlwt.Alignment()
	index_align.horz = xlwt.Alignment.HORZ_CENTER
	index_align.vert = xlwt.Alignment.VERT_CENTER
	index_style.font = index_font
	index_style.alignment = index_align
	index_style.borders = _bordes()

	cell_style = xlwt.XFStyle()
	cell_align = xlwt.Alignment()
	cell_align.horz = xlwt.Alignment.HORZ_LEFT
	cell_align.vert = xlwt.Alignment.VERT_TOP
	cell_align.wrap = xlwt.Alignment.WRAP_AT_RIGHT
	cell_style.alignment = cell_align
	cell_style.borders = _bordes()

	return {
		'header': head_style,
		'index': index_style,
		'cell': cell_style
	}


def _componer_texto_celda(linea_superior: Optional[str], linea_intermedia: Optional[str],
						  hora_inicio: Optional[str], hora_fin: Optional[str]) -> str:
	"""Replica el formato de texto mostrado en la UI para cada celda."""
	if not any([linea_superior, linea_intermedia, hora_inicio, hora_fin]):
		return ''
	return f"{linea_superior or ''}\n{linea_intermedia or ''}\n{(hora_inicio or '')}-{(hora_fin or '')}"


def _texto_horario_curso(registro: Dict[str, Any]) -> str:
	return _componer_texto_celda(registro.get('materia'), registro.get('profesor'),
							  registro.get('hora_inicio'), registro.get('hora_fin'))


def _texto_horario_profesor(registro: Dict[str, Any]) -> str:
	return _componer_texto_celda(registro.get('materia'), registro.get('division'),
							  registro.get('hora_inicio'), registro.get('hora_fin'))


def _construir_matriz_horario(dias: List[str], espacios: int, registros: List[Dict[str, Any]],
							   formateador) -> Dict[tuple, str]:
	"""Convierte la lista de horarios en una matriz indexada por (día, espacio)."""
	matriz = {(dia, esp): '' for dia in dias for esp in range(1, espacios + 1)}
	for registro in registros:
		dia = registro.get('dia')
		if dia not in dias:
			continue
		espacio = registro.get('espacio')
		try:
			espacio = int(espacio)
		except (TypeError, ValueError):
			continue
		if espacio < 1 or espacio > espacios:
			continue
		matriz[(dia, espacio)] = formateador(registro)
	return matriz


def _sanear_nombre_hoja(nombre: str) -> str:
	if not nombre:
		nombre = 'Hoja'
	limpio = ''.join('_' if ch in _HOJA_CARACTERES_INVALIDOS else ch for ch in nombre.strip())
	if not limpio:
		limpio = 'Hoja'
	return limpio[:31]


def _asegurar_nombre_unico(nombre: str, existentes: set) -> str:
	"""Garantiza que el nombre de hoja sea único respetando el límite de 31 caracteres."""
	base = nombre
	contador = 2
	while nombre in existentes:
		sufijo = f" ({contador})"
		truncado = base
		if len(truncado) + len(sufijo) > 31:
			truncado = truncado[:31 - len(sufijo)]
		nombre = truncado + sufijo
		contador += 1
	existentes.add(nombre)
	return nombre


def _normalizar_ruta_xls(ruta: str) -> str:
	if not ruta:
		return ''
	base, ext = os.path.splitext(ruta)
	if ext.lower() == '.xls':
		return ruta
	if ext:
		return f"{base}.xls"
	return f"{ruta}.xls"


def _escribir_matriz_en_hoja(hoja: xlwt.Worksheet, dias: List[str], espacios: int,
							 matriz: Dict[tuple, str], estilos: Dict[str, xlwt.XFStyle]):
	"""Escribe encabezados y celdas respetando las dimensiones solicitadas."""
	# Encabezados
	for col, dia in enumerate([''] + dias):
		style = estilos['header'] if col == 0 else estilos['header']
		hoja.write(0, col, dia, style)
		if col == 0:
			hoja.col(col).width = 256 * 6
		else:
			hoja.col(col).width = 256 * 22

	# Filas de espacios
	for esp in range(1, espacios + 1):
		row = esp
		indice = f"{esp}ª"
		hoja.write(row, 0, indice, estilos['index'])
		for col, dia in enumerate(dias, start=1):
			valor = matriz.get((dia, esp), '')
			hoja.write(row, col, valor, estilos['cell'])


def exportar_planillas_horario(hojas: List[Dict[str, Any]], ruta_archivo: str) -> str:
	"""Genera un archivo XLS con múltiples hojas de horarios.

	Args:
		hojas: Lista de dicts con claves 'nombre', 'horarios' y 'construir_texto'.
		ruta_archivo: Ruta destino (se forzará extensión .xls).
	"""
	if not hojas:
		raise Exception('No hay horarios para exportar.')
	ruta_final = _normalizar_ruta_xls(ruta_archivo)
	if not ruta_final:
		raise Exception('Ruta de exportación inválida.')
	dias_default = _obtener_dias_para_export()
	espacios_default = _obtener_max_espacios_para_export()
	estilos = _crear_estilos_xls()
	workbook = xlwt.Workbook()
	nombres_hojas = set()
	for hoja in hojas:
		nombre = _sanear_nombre_hoja(hoja.get('nombre', 'Hoja'))
		nombre = _asegurar_nombre_unico(nombre, nombres_hojas)
		ws = workbook.add_sheet(nombre, cell_overwrite_ok=True)
		dias = hoja.get('dias') or dias_default
		espacios = hoja.get('espacios') or espacios_default
		horarios = hoja.get('horarios', [])
		formateador = hoja.get('construir_texto')
		if formateador is None:
			raise Exception('Falta formateador de texto para la hoja de exportación.')
		matriz = _construir_matriz_horario(dias, espacios, horarios, formateador)
		_escribir_matriz_en_hoja(ws, dias, espacios, matriz, estilos)

	directorio = os.path.dirname(ruta_final)
	if directorio and not os.path.exists(directorio):
		os.makedirs(directorio, exist_ok=True)
	workbook.save(ruta_final)
	return ruta_final


def _ensure_ciclo_schema(conn):
	"""Garantiza que la tabla ciclo soporte asociación multi-plan."""
	c = conn.cursor()
	info = []
	if _table_exists(conn, 'ciclo'):
		c.execute('PRAGMA table_info(ciclo)')
		info = c.fetchall()
	else:
		c.execute('''CREATE TABLE ciclo (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			nombre TEXT UNIQUE NOT NULL
		)''')

	has_plan_column = any(col[1] == 'plan_id' for col in info)
	if has_plan_column:
		_migrar_ciclos_multi_plan(conn)

	# Tabla puente plan-ciclo
	c.execute('''CREATE TABLE IF NOT EXISTS plan_ciclo (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		plan_id INTEGER NOT NULL,
		ciclo_id INTEGER NOT NULL,
		FOREIGN KEY(plan_id) REFERENCES plan_estudio(id) ON DELETE CASCADE,
		FOREIGN KEY(ciclo_id) REFERENCES ciclo(id) ON DELETE CASCADE,
		UNIQUE(plan_id, ciclo_id)
	)''')


def _migrar_ciclos_multi_plan(conn):
	"""Migra la tabla ciclo antigua (con plan_id) al nuevo esquema multi-plan."""
	c = conn.cursor()
	conn.execute('PRAGMA foreign_keys = OFF')
	c.execute('ALTER TABLE ciclo RENAME TO ciclo_old')
	c.execute('''CREATE TABLE ciclo (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		nombre TEXT UNIQUE NOT NULL
	)''')
	# Asegurar que la tabla puente exista antes de poblarla
	c.execute('''CREATE TABLE IF NOT EXISTS plan_ciclo (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		plan_id INTEGER NOT NULL,
		ciclo_id INTEGER NOT NULL,
		FOREIGN KEY(plan_id) REFERENCES plan_estudio(id) ON DELETE CASCADE,
		FOREIGN KEY(ciclo_id) REFERENCES ciclo(id) ON DELETE CASCADE,
		UNIQUE(plan_id, ciclo_id)
	)''')
	old_rows = c.execute('SELECT id, nombre, plan_id FROM ciclo_old').fetchall()
	nombre_to_new_id = {}
	id_map = {}
	for old_id, nombre, plan_id in old_rows:
		if nombre not in nombre_to_new_id:
			c.execute('INSERT INTO ciclo (nombre) VALUES (?)', (nombre,))
			nombre_to_new_id[nombre] = c.lastrowid
		new_id = nombre_to_new_id[nombre]
		id_map[old_id] = new_id
		if plan_id is not None:
			c.execute('INSERT OR IGNORE INTO plan_ciclo (plan_id, ciclo_id) VALUES (?, ?)', (plan_id, new_id))

	for table_name in ('division', 'ciclo_materia'):
		if not _table_exists(conn, table_name):
			continue
		for old_id, new_id in id_map.items():
			c.execute(f'UPDATE {table_name} SET ciclo_id=? WHERE ciclo_id=?', (new_id, old_id))
		if table_name == 'ciclo_materia':
			c.execute('''DELETE FROM ciclo_materia WHERE rowid NOT IN (
				SELECT MIN(rowid) FROM ciclo_materia GROUP BY ciclo_id, materia_id
			)''')

	c.execute('DROP TABLE ciclo_old')
	conn.execute('PRAGMA foreign_keys = ON')

def init_db():
	conn = get_connection()
	c = conn.cursor()
	
	# Tabla de usuarios para login
	c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		username TEXT UNIQUE NOT NULL,
		password TEXT NOT NULL,
		es_admin INTEGER NOT NULL DEFAULT 0,
		fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP
	)''')
	
	# Plan de estudios
	c.execute('''CREATE TABLE IF NOT EXISTS plan_estudio (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		nombre TEXT UNIQUE NOT NULL
	)''')

	# Ciclos multi-plan
	_ensure_ciclo_schema(conn)

	# Obligaciones por ciclo
	c.execute('''CREATE TABLE IF NOT EXISTS ciclo_materia (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		ciclo_id INTEGER,
		materia_id INTEGER,
		FOREIGN KEY(ciclo_id) REFERENCES ciclo(id),
		FOREIGN KEY(materia_id) REFERENCES materia(id),
		UNIQUE(ciclo_id, materia_id)
	)''')
	# Obligaciones por plan de estudio
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
	# Divisiones por turno, plan y ciclo
	c.execute('''CREATE TABLE IF NOT EXISTS division (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		nombre TEXT NOT NULL,
		turno_id INTEGER,
		plan_id INTEGER,
		ciclo_id INTEGER,
		FOREIGN KEY(turno_id) REFERENCES turno(id),
		FOREIGN KEY(plan_id) REFERENCES plan_estudio(id),
		FOREIGN KEY(ciclo_id) REFERENCES ciclo(id),
		UNIQUE(nombre, turno_id, plan_id, ciclo_id)
	)''')
	# Obligaciones
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
	# Banca de horas por obligación para cada profesor
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


# ═══════════════════════════════════════════════════════════════════════════════
# 5. MÓDULO: GESTIÓN DE MATERIAS/OBLIGACIONES
# ═══════════════════════════════════════════════════════════════════════════════
# Operaciones CRUD para materias (asignaturas curriculares con carga horaria).
# Candidato para módulo: database/materias.py
# ───────────────────────────────────────────────────────────────────────────────

def crear_materia(nombre: str, horas: int):
	"""
	Crea una nueva materia/obligación en el sistema.
	
	Parámetros:
		nombre (str): Nombre de la materia (ej: "Matemática", "Lengua")
		horas (int): Horas semanales de carga docente
		
	Lanza:
		Exception: Si ya existe una materia con el mismo nombre
		
	Dependencias:
		- Tabla: materia
		- Requerida por: crear_ciclo, mostrar_materias (App)
		
	Candidato para: database/materias.py
	"""
	try:
		crear_entidad('materia', ['nombre', 'horas_semanales'], [nombre, horas])
	except Exception:
		raise Exception('Ya existe una materia con ese nombre.')

def obtener_materias() -> List[Dict[str, Any]]:
	"""
	Obtiene la lista completa de materias del sistema.
	
	Retorna:
		list: Lista de diccionarios con estructura {'id': int, 'nombre': str, 'horas_semanales': int}
		
	Ejemplo:
		materias = obtener_materias()
		# Retorna: [{'id': 1, 'nombre': 'Matemática', 'horas_semanales': 4}, ...]
		
	Candidato para: database/materias.py
	"""
	return obtener_entidades('materia', ['id', 'nombre', 'horas_semanales'])

def actualizar_materia(id_: int, nombre: str, horas: int):
	"""
	Actualiza los datos de una materia existente.
	
	Parámetros:
		id_ (int): ID de la materia a actualizar
		nombre (str): Nuevo nombre de la materia
		horas (int): Nuevas horas semanales
		
	Retorna:
		None (pero realiza commit en BD)
		
	Candidato para: database/materias.py
	"""
	actualizar_entidad('materia', ['nombre', 'horas_semanales'], [nombre, horas], 'id', id_)

def eliminar_materia(id_: int):
	"""
	Elimina una materia del sistema.
	
	Parámetros:
		id_ (int): ID de la materia a eliminar
		
	Nota:
		Esto puede fallar si hay referencias en ciclos o planes de estudio
		debido a restricciones de clave foránea.
		
	Candidato para: database/materias.py
	"""
	eliminar_entidad('materia', 'id', id_)


# ═══════════════════════════════════════════════════════════════════════════════
# 6. MÓDULO: GESTIÓN DE PROFESORES
# ═══════════════════════════════════════════════════════════════════════════════
# Operaciones CRUD para profesores (docentes del sistema).
# Candidato para módulo: database/profesores.py
# ───────────────────────────────────────────────────────────────────────────────

def crear_profesor(nombre: str):
	"""
	Crea un nuevo profesor en el sistema.
	
	Parámetros:
		nombre (str): Nombre completo del docente
		
	Lanza:
		Exception: Si ya existe un profesor con el mismo nombre
		
	Dependencias:
		- Tabla: profesor
		- Requerida por: gestión de profesores, asignación de turnos
		
	Candidato para: database/profesores.py
	"""
	try:
		crear_entidad('profesor', ['nombre'], [nombre])
	except Exception:
		raise Exception('Ya existe un profesor con ese nombre.')

def obtener_profesores() -> List[Dict[str, Any]]:
	"""
	Obtiene la lista completa de profesores.
	
	Retorna:
		list: Lista de diccionarios {'id': int, 'nombre': str}
		
	Candidato para: database/profesores.py
	"""
	return obtener_entidades('profesor', ['id', 'nombre'])

def actualizar_profesor(id_: int, nombre: str):
	"""
	Actualiza los datos de un profesor.
	
	Parámetros:
		id_ (int): ID del profesor
		nombre (str): Nuevo nombre
		
	Candidato para: database/profesores.py
	"""
	actualizar_entidad('profesor', ['nombre'], [nombre], 'id', id_)

def eliminar_profesor(id_: int):
	"""
	Elimina un profesor del sistema junto con sus asignaciones.
	
	Parámetros:
		id_ (int): ID del profesor a eliminar
		
	Notas:
		- Elimina automáticamente las referencias en profesor_turno
		- Esto puede fallar si hay horarios asignados (restricción FK)
		
	Candidato para: database/profesores.py
	"""
	# TODO REFACTOR: Usar transacción explícita para garantizar consistencia
	# Elimina también los turnos asignados
	@db_operation
	def _eliminar_profesor(conn, id_):
		conn.execute('DELETE FROM profesor_turno WHERE profesor_id=?', (id_,))
		conn.execute('DELETE FROM profesor WHERE id=?', (id_,))
	_eliminar_profesor(id_)

# ═══════════════════════════════════════════════════════════════════════════════
# 7. MÓDULO: GESTIÓN DE PROFESOR-TURNO (RELACIÓN MUCHOS A MUCHOS)
# ═══════════════════════════════════════════════════════════════════════════════
# Operaciones para asignar/desasignar turnos (jornadas) a profesores.
# Candidato para módulo: database/profesor_turno.py
# ───────────────────────────────────────────────────────────────────────────────

def asignar_turno_a_profesor(profesor_id: int, turno_id: int):
	"""
	Asigna un turno (jornada) a un profesor.
	
	Parámetros:
		profesor_id (int): ID del profesor
		turno_id (int): ID del turno (Mañana, Tarde, Noche)
		
	Lanza:
		Exception: Si el profesor ya tiene asignado ese turno (violación de clave única)
		
	Dependencias:
		- Tablas: profesor, turno, profesor_turno
		- Requerida por: mostrar_personal_y_ciclos, gestión de horarios
		
	Candidato para: database/profesor_turno.py
	"""
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
	"""
	Desasigna un turno de un profesor.
	
	Parámetros:
		profesor_id (int): ID del profesor
		turno_id (int): ID del turno
		
	Nota:
		Se elimina la relación profesor_turno, pero no el profesor ni el turno.
		
	Candidato para: database/profesor_turno.py
	"""
	conn = get_connection()
	c = conn.cursor()
	c.execute('DELETE FROM profesor_turno WHERE profesor_id=? AND turno_id=?', (profesor_id, turno_id))
	conn.commit()
	conn.close()

def obtener_turnos_de_profesor(profesor_id: int):
	"""
	Obtiene los turnos asignados a un profesor.
	
	Parámetros:
		profesor_id (int): ID del profesor
		
	Retorna:
		list: Lista de diccionarios {'id': int, 'nombre': str}
		
	Ejemplo:
		turnos = obtener_turnos_de_profesor(1)
		# Retorna: [{'id': 1, 'nombre': 'Mañana'}, {'id': 2, 'nombre': 'Tarde'}]
		
	Candidato para: database/profesor_turno.py
	"""
	conn = get_connection()
	c = conn.cursor()
	c.execute('''SELECT t.id, t.nombre FROM profesor_turno pt JOIN turno t ON pt.turno_id = t.id WHERE pt.profesor_id=?''', (profesor_id,))
	rows = c.fetchall()
	conn.close()
	return [{'id': r[0], 'nombre': r[1]} for r in rows]

def obtener_profesores_por_turno(turno_id: int):
	"""
	Obtiene los profesores asignados a un turno.
	
	Parámetros:
		turno_id (int): ID del turno
		
	Retorna:
		list: Lista de diccionarios {'id': int, 'nombre': str}
		
	Candidato para: database/profesor_turno.py
	"""
	conn = get_connection()
	c = conn.cursor()
	c.execute('''SELECT p.id, p.nombre FROM profesor p JOIN profesor_turno pt ON p.id = pt.profesor_id WHERE pt.turno_id=?''', (turno_id,))
	rows = c.fetchall()
	conn.close()
	return [{'id': r[0], 'nombre': r[1]} for r in rows]


def obtener_profesor_turnos() -> List[Dict[str, Any]]:
	"""
	Obtiene todas las combinaciones profesor-turno del sistema.
	
	Retorna:
		list: Lista de diccionarios {'profesor_id': int, 'profesor': str, 'turno_id': int, 'turno': str}
		
	Candidato para: database/profesor_turno.py
	"""
	conn = get_connection()
	c = conn.cursor()
	c.execute('''SELECT p.id, p.nombre, t.id, t.nombre
			 FROM profesor_turno pt
			 JOIN profesor p ON p.id = pt.profesor_id
			 JOIN turno t ON t.id = pt.turno_id
			 ORDER BY p.nombre, t.nombre''')
	rows = c.fetchall()
	conn.close()
	return [
		{'profesor_id': r[0], 'profesor': r[1], 'turno_id': r[2], 'turno': r[3]}
		for r in rows
	]

# ═══════════════════════════════════════════════════════════════════════════════
# 8. MÓDULO: BANCA DE HORAS POR PROFESOR-MATERIA
# ═══════════════════════════════════════════════════════════════════════════════
# Operaciones para gestionar la carga horaria disponible de cada profesor
# en cada materia que puede impartir.
# Candidato para módulo: database/profesor_materia.py
# ───────────────────────────────────────────────────────────────────────────────

def asignar_banca_profesor(profesor_id: int, materia_id: int, banca_horas: int):
	"""
	Asigna una banca horaria (carga) a un profesor para una materia.
	
	Parámetros:
		profesor_id (int): ID del profesor
		materia_id (int): ID de la materia
		banca_horas (int): Cantidad de horas que puede enseñar
		
	Lanza:
		Exception: Si el profesor ya tiene esa materia asignada
		
	Candidato para: database/profesor_materia.py
	"""
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
	"""
	Obtiene la banca horaria de un profesor.
	
	Parámetros:
		profesor_id (int): ID del profesor
		
	Retorna:
		list: Lista de diccionarios {'id': int, 'materia': str, 'banca_horas': int}
		
	Candidato para: database/profesor_materia.py
	"""
	conn = get_connection()
	c = conn.cursor()
	c.execute('''SELECT pm.id, m.nombre, pm.banca_horas FROM profesor_materia pm JOIN materia m ON pm.materia_id = m.id WHERE pm.profesor_id=?''', (profesor_id,))
	rows = c.fetchall()
	conn.close()
	return [{'id': r[0], 'materia': r[1], 'banca_horas': r[2]} for r in rows]

def actualizar_banca_profesor(pm_id: int, banca_horas: int):
	"""
	Actualiza la banca horaria de un profesor para una materia.
	
	Parámetros:
		pm_id (int): ID del registro profesor_materia
		banca_horas (int): Nueva cantidad de horas
		
	Candidato para: database/profesor_materia.py
	"""
	conn = get_connection()
	c = conn.cursor()
	c.execute('UPDATE profesor_materia SET banca_horas=? WHERE id=?', (banca_horas, pm_id))
	conn.commit()
	conn.close()

def eliminar_banca_profesor(pm_id: int):
	"""
	Elimina la asignación de una materia de un profesor.
	
	Parámetros:
		pm_id (int): ID del registro profesor_materia
		
	Candidato para: database/profesor_materia.py
	"""
	conn = get_connection()
	c = conn.cursor()
	c.execute('DELETE FROM profesor_materia WHERE id=?', (pm_id,))
	conn.commit()
	conn.close()

# ═══════════════════════════════════════════════════════════════════════════════
# 9. MÓDULO: GESTIÓN DE CICLOS (NIVELES EDUCATIVOS)
# ═══════════════════════════════════════════════════════════════════════════════
# Operaciones CRUD para ciclos (años/niveles educativos con planes asociados).
# Un ciclo puede tener múltiples planes de estudio.
# Candidato para módulo: database/ciclos.py
# ───────────────────────────────────────────────────────────────────────────────

def crear_ciclo(nombre: str, plan_ids: List[int]) -> int:
	"""
	Crea un nuevo ciclo (nivel educativo) y lo asocia con planes de estudio.
	
	Parámetros:
		nombre (str): Nombre del ciclo (ej: "Primer Año", "Segundo Año")
		plan_ids (list): Lista de IDs de planes de estudio a asociar
		
	Retorna:
		int: ID del ciclo creado
		
	Lanza:
		Exception: Si ya existe un ciclo con ese nombre o si no hay planes
		
	Dependencias:
		- Tablas: ciclo, plan_ciclo, plan
		- Requerida por: gestión de divisiones, horarios
		
	Candidato para: database/ciclos.py
	"""
	if not plan_ids:
		raise Exception('Debe seleccionar al menos un plan de estudio.')
	conn = get_connection()
	try:
		c = conn.cursor()
		c.execute('INSERT INTO ciclo (nombre) VALUES (?)', (nombre,))
		ciclo_id = c.lastrowid
		for plan_id in plan_ids:
			c.execute('INSERT INTO plan_ciclo (plan_id, ciclo_id) VALUES (?, ?)', (plan_id, ciclo_id))
		conn.commit()
		return ciclo_id
	except sqlite3.IntegrityError:
		raise Exception('Ya existe un ciclo con ese nombre.')
	finally:
		conn.close()


def actualizar_ciclo(id_: int, nombre: str, plan_ids: List[int]):
	"""
	Actualiza un ciclo existente y sus asociaciones con planes de estudio.
	
	Parámetros:
		id_ (int): ID del ciclo a actualizar
		nombre (str): Nuevo nombre del ciclo
		plan_ids (list): Nueva lista de IDs de planes asociados
		
	Lanza:
		Exception: Si no hay planes, ya existe un ciclo con ese nombre,
				   o hay divisiones asociadas a planes que se desvinculan
		
	Candidato para: database/ciclos.py
	"""
	if not plan_ids:
		raise Exception('Debe seleccionar al menos un plan de estudio.')
	conn = get_connection()
	try:
		c = conn.cursor()
		try:
			c.execute('UPDATE ciclo SET nombre=? WHERE id=?', (nombre, id_))
		except sqlite3.IntegrityError:
			raise Exception('Ya existe un ciclo con ese nombre.')
		existing = {row[0] for row in c.execute('SELECT plan_id FROM plan_ciclo WHERE ciclo_id=?', (id_,))}
		new_set = set(plan_ids)
		to_add = new_set - existing
		to_remove = existing - new_set
		if to_remove and _tabla_existe(conn, 'division'):
			for plan_id in to_remove:
				c.execute('SELECT COUNT(*) FROM division WHERE ciclo_id=? AND plan_id=?', (id_, plan_id))
				if c.fetchone()[0] > 0:
					raise Exception('No se puede desvincular el plan seleccionado porque existen divisiones asociadas.')
		for plan_id in to_remove:
			c.execute('DELETE FROM plan_ciclo WHERE ciclo_id=? AND plan_id=?', (id_, plan_id))
		for plan_id in to_add:
			c.execute('INSERT INTO plan_ciclo (plan_id, ciclo_id) VALUES (?, ?)', (plan_id, id_))
		conn.commit()
	finally:
		conn.close()


def obtener_ciclos(plan_id: int) -> list:
	"""
	Obtiene los ciclos asociados a un plan de estudio.
	
	Parámetros:
		plan_id (int): ID del plan de estudio
		
	Retorna:
		list: Lista de diccionarios {'id': int, 'nombre': str}
		
	Candidato para: database/ciclos.py
	"""
	conn = get_connection()
	c = conn.cursor()
	c.execute('''SELECT c.id, c.nombre FROM ciclo c
			 JOIN plan_ciclo pc ON pc.ciclo_id = c.id
			 WHERE pc.plan_id=?
			 ORDER BY c.nombre''', (plan_id,))
	rows = c.fetchall()
	conn.close()
	return [{'id': r[0], 'nombre': r[1]} for r in rows]


def obtener_ciclos_con_planes() -> List[Dict[str, Any]]:
	"""
	Obtiene todos los ciclos con sus planes asociados.
	
	Retorna:
		list: Lista de diccionarios con estructura:
			  {'id': int, 'nombre': str, 'planes': [{'id': int, 'nombre': str}, ...]}
		
	Candidato para: database/ciclos.py
	"""
	conn = get_connection()
	c = conn.cursor()
	c.execute('''SELECT c.id, c.nombre, p.id, p.nombre
			 FROM ciclo c
			 LEFT JOIN plan_ciclo pc ON pc.ciclo_id = c.id
			 LEFT JOIN plan_estudio p ON p.id = pc.plan_id
			 ORDER BY c.nombre, p.nombre''')
	rows = c.fetchall()
	conn.close()
	result: Dict[int, Dict[str, Any]] = {}
	for ciclo_id, ciclo_nombre, plan_id, plan_nombre in rows:
		if ciclo_id not in result:
			result[ciclo_id] = {'id': ciclo_id, 'nombre': ciclo_nombre, 'planes': []}
		if plan_id is not None:
			result[ciclo_id]['planes'].append({'id': plan_id, 'nombre': plan_nombre})
	return list(result.values())


def obtener_planes_de_ciclo(ciclo_id: int) -> List[Dict[str, Any]]:
	"""
	Obtiene los planes de estudio asociados a un ciclo.
	
	Parámetros:
		ciclo_id (int): ID del ciclo
		
	Retorna:
		list: Lista de diccionarios {'id': int, 'nombre': str}
		
	Candidato para: database/ciclos.py
	"""
	conn = get_connection()
	c = conn.cursor()
	c.execute('''SELECT p.id, p.nombre FROM plan_ciclo pc
			 JOIN plan_estudio p ON p.id = pc.plan_id
			 WHERE pc.ciclo_id=?
			 ORDER BY p.nombre''', (ciclo_id,))
	rows = c.fetchall()
	conn.close()
	return [{'id': r[0], 'nombre': r[1]} for r in rows]


def contar_dependencias_ciclo(ciclo_id: int) -> Dict[str, int]:
	"""
	Cuenta las dependencias (divisiones y horarios) de un ciclo.
	
	Parámetros:
		ciclo_id (int): ID del ciclo
		
	Retorna:
		dict: {'divisiones': int, 'horarios': int}
		
	Notas:
		Se utiliza antes de eliminar un ciclo para verificar posibles conflictos.
		
	Candidato para: database/ciclos.py
	"""
	conn = get_connection()
	c = conn.cursor()
	divisiones = horarios = 0
	if _tabla_existe(conn, 'division'):
		c.execute('SELECT COUNT(*) FROM division WHERE ciclo_id=?', (ciclo_id,))
		divisiones = c.fetchone()[0]
	if divisiones and _tabla_existe(conn, 'horario'):
		c.execute('''SELECT COUNT(*) FROM horario
				 WHERE division_id IN (SELECT id FROM division WHERE ciclo_id=?)''', (ciclo_id,))
		horarios = c.fetchone()[0]
	conn.close()
	return {'divisiones': divisiones, 'horarios': horarios}


def eliminar_ciclo(id_: int, cascade: bool = False):
	"""
	Elimina un ciclo del sistema.
	
	Parámetros:
		id_ (int): ID del ciclo a eliminar
		cascade (bool): Si True, elimina también divisiones y horarios asociados
		
	Lanza:
		Exception: Si hay dependencias y cascade=False
		
	Notas:
		- Si hay divisiones u horarios y cascade=False, lanza una excepción
		- Si cascade=True, elimina todo en orden: horarios, divisiones, plan_ciclo, ciclo
		
	Candidato para: database/ciclos.py
	"""
	conn = get_connection()
	try:
		c = conn.cursor()
		deps = contar_dependencias_ciclo(id_)
		if (deps['divisiones'] or deps['horarios']) and not cascade:
			raise Exception('El ciclo tiene divisiones y/o horarios asociados.')
		if cascade and deps['divisiones']:
			if _table_exists(conn, 'horario'):
				c.execute('DELETE FROM horario WHERE division_id IN (SELECT id FROM division WHERE ciclo_id=?)', (id_,))
			if _table_exists(conn, 'division'):
				c.execute('DELETE FROM division WHERE ciclo_id=?', (id_,))
		if _table_exists(conn, 'ciclo_materia'):
			c.execute('DELETE FROM ciclo_materia WHERE ciclo_id=?', (id_,))
		c.execute('DELETE FROM plan_ciclo WHERE ciclo_id=?', (id_,))
		c.execute('DELETE FROM ciclo WHERE id=?', (id_,))
		conn.commit()
	finally:
		conn.close()

# CRUD Obligaciones por ciclo
def agregar_materia_a_ciclo(ciclo_id: int, materia_id: int):
	try:
		conn = get_connection()
		c = conn.cursor()
		c.execute('INSERT INTO ciclo_materia (ciclo_id, materia_id) VALUES (?, ?)', (ciclo_id, materia_id))
		conn.commit()
	except sqlite3.IntegrityError:
		raise Exception('La materia ya está en el ciclo.')
	finally:
		conn.close()

def quitar_materia_de_ciclo(ciclo_id: int, materia_id: int):
	conn = get_connection()
	c = conn.cursor()
	c.execute('DELETE FROM ciclo_materia WHERE ciclo_id=? AND materia_id=?', (ciclo_id, materia_id))
	conn.commit()
	conn.close()

def obtener_materias_de_ciclo(ciclo_id: int) -> list:
	conn = get_connection()
	c = conn.cursor()
	c.execute('''SELECT m.id, m.nombre FROM ciclo_materia am JOIN materia m ON am.materia_id = m.id WHERE am.ciclo_id=?''', (ciclo_id,))
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

def obtener_turnos_de_plan(plan_id: int) -> list:
	"""Obtiene los turnos asociados a un plan de estudio"""
	conn = get_connection()
	c = conn.cursor()
	c.execute('''SELECT DISTINCT t.id, t.nombre FROM turno t
				 JOIN turno_plan tp ON tp.turno_id = t.id
				 WHERE tp.plan_id = ?''', (plan_id,))
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
	# Nuevo: requiere turno_id, plan_id, ciclo_id
	raise Exception('La función crear_division debe ser llamada con turno_id, plan_id y ciclo_id.')

def obtener_divisiones() -> List[Dict[str, Any]]:
	conn = get_connection()
	c = conn.cursor()
	c.execute('SELECT id, nombre, turno_id, plan_id, ciclo_id FROM division')
	rows = c.fetchall()
	conn.close()
	return [{'id': r[0], 'nombre': r[1], 'turno_id': r[2], 'plan_id': r[3], 'ciclo_id': r[4]} for r in rows]

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

# ==== Helpers internos para la tabla de horarios ====

def _obtener_turno_de_division(conn, division_id: int) -> int:
	c = conn.cursor()
	c.execute('SELECT turno_id FROM division WHERE id=?', (division_id,))
	row = c.fetchone()
	if not row:
		raise Exception('División no encontrada.')
	return row[0]


def _obtener_slot_horario(conn, division_id: int, dia: str, espacio: int):
	c = conn.cursor()
	c.execute('SELECT id, materia_id, profesor_id FROM horario WHERE division_id=? AND dia=? AND espacio=?',
		  (division_id, dia, espacio))
	row = c.fetchone()
	if row:
		return {'id': row[0], 'materia_id': row[1], 'profesor_id': row[2]}
	return None


def _ajustar_contadores(conn, old_profesor_id: Optional[int], old_materia_id: Optional[int],
					   new_profesor_id: Optional[int], new_materia_id: Optional[int]):
	if old_profesor_id == new_profesor_id and old_materia_id == new_materia_id:
		return  # No hay cambios
	c = conn.cursor()
	if old_materia_id and old_materia_id != new_materia_id:
		c.execute('UPDATE materia SET horas_semanales = horas_semanales - 1 WHERE id=?', (old_materia_id,))
	if new_materia_id and new_materia_id != old_materia_id:
		c.execute('UPDATE materia SET horas_semanales = horas_semanales + 1 WHERE id=?', (new_materia_id,))

	if old_profesor_id and old_materia_id and (old_profesor_id != new_profesor_id or old_materia_id != new_materia_id):
		c.execute('UPDATE profesor_materia SET banca_horas = banca_horas - 1 WHERE profesor_id=? AND materia_id=?',
				  (old_profesor_id, old_materia_id))
	if new_profesor_id and new_materia_id and (old_profesor_id != new_profesor_id or old_materia_id != new_materia_id):
		c.execute('UPDATE profesor_materia SET banca_horas = banca_horas + 1 WHERE profesor_id=? AND materia_id=?',
				  (new_profesor_id, new_materia_id))


def _validar_profesor_para_slot(conn, profesor_id: int, turno_id: int, materia_id: Optional[int],
								 dia: str, espacio: int, division_id: int, horario_existente_id: Optional[int]):
	c = conn.cursor()
	c.execute('SELECT 1 FROM profesor_turno WHERE profesor_id=? AND turno_id=?', (profesor_id, turno_id))
	if not c.fetchone():
		raise Exception('El profesor no está asignado al turno seleccionado.')

	if materia_id is not None:
		c.execute('SELECT 1 FROM profesor_materia WHERE profesor_id=? AND materia_id=?', (profesor_id, materia_id))
		if not c.fetchone():
			raise Exception('El profesor no tiene asignada la materia seleccionada.')

	slot_id = horario_existente_id if horario_existente_id is not None else -1
	c.execute('''SELECT h.id FROM horario h
			 JOIN division d ON h.division_id = d.id
			 WHERE h.profesor_id=? AND h.dia=? AND h.espacio=? AND d.turno_id=? AND h.id != ?''',
		  (profesor_id, dia, espacio, turno_id, slot_id))
	if c.fetchone():
		raise Exception('El profesor ya está asignado en ese horario en otra división del mismo turno.')


def _upsert_horario(conn, division_id: int, dia: str, espacio: int,
				   hora_inicio: Optional[str], hora_fin: Optional[str],
				   materia_id: Optional[int], profesor_id: Optional[int], turno_id: Optional[int]):
	c = conn.cursor()
	div_turno_id = _obtener_turno_de_division(conn, division_id)
	if turno_id is None:
		turno_id = div_turno_id
	elif turno_id != div_turno_id:
		raise Exception('La división seleccionada no pertenece al turno indicado.')

	slot = _obtener_slot_horario(conn, division_id, dia, espacio)
	horario_id = slot['id'] if slot else None
	old_materia = slot['materia_id'] if slot else None
	old_profesor = slot['profesor_id'] if slot else None

	if profesor_id is not None:
		_validar_profesor_para_slot(conn, profesor_id, turno_id, materia_id, dia, espacio, division_id, horario_id)

	_ajustar_contadores(conn, old_profesor, old_materia, profesor_id, materia_id)

	hora_inicio_db = hora_inicio if hora_inicio else None
	hora_fin_db = hora_fin if hora_fin else None

	if horario_id:
		c.execute('''UPDATE horario SET hora_inicio=?, hora_fin=?, materia_id=?, profesor_id=?, turno_id=?
				  WHERE id=?''',
			  (hora_inicio_db, hora_fin_db, materia_id, profesor_id, turno_id, horario_id))
		return horario_id
	else:
		c.execute('''INSERT INTO horario (division_id, dia, espacio, hora_inicio, hora_fin, materia_id, profesor_id, turno_id)
				  VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
			  (division_id, dia, espacio, hora_inicio_db, hora_fin_db, materia_id, profesor_id, turno_id))
		return c.lastrowid

# CRUD Horario
def crear_horario(division_id: int, dia: str, espacio: int, hora_inicio: str, hora_fin: str, materia_id: int, profesor_id: int, turno_id: int = None):
	conn = get_connection()
	try:
		_upsert_horario(conn, division_id, dia, espacio, hora_inicio, hora_fin, materia_id, profesor_id, turno_id)
		conn.commit()
	except Exception:
		conn.rollback()
		raise
	finally:
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

# CRUD Horario por Profesor (usa la misma tabla 'horario' que la vista por ciclo)
def crear_horario_profesor(profesor_id: int, turno_id: int, dia: str, espacio: int,
						  hora_inicio: str, hora_fin: str,
						  division_id: int = None, materia_id: int = None):
	"""Sincroniza las cargas desde la vista por profesor usando la misma lógica que la vista por ciclo."""
	if division_id is None:
		raise Exception('Seleccione el ciclo/división antes de guardar el horario del profesor.')
	if materia_id is None:
		raise Exception('Seleccione la materia dictada por el profesor.')

	conn = get_connection()
	try:
		_upsert_horario(conn, division_id, dia, espacio, hora_inicio, hora_fin, materia_id, profesor_id, turno_id)
		conn.commit()
	except Exception:
		conn.rollback()
		raise
	finally:
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

# ============== FUNCIONES DE BACKUP ==============

def crear_backup_db(manual=False) -> str:
	"""
	Crea una copia de seguridad de la base de datos.
	
	Args:
		manual: Si es True, crea un backup con timestamp detallado.
				Si es False, crea/sobreescribe el backup automático.
	
	Returns:
		Ruta del archivo de backup creado
	"""
	if not os.path.exists(DB_NAME):
		raise Exception('La base de datos no existe.')
	
	if manual:
		# Backup manual con timestamp completo
		timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
		backup_name = f'institucion_backup_{timestamp}.bak'
	else:
		# Backup automático - siempre sobrescribe el mismo archivo
		backup_name = 'institucion.bak'
	
	backup_path = os.path.join(DB_DIR, backup_name)
	
	try:
		shutil.copy2(DB_NAME, backup_path)
		return backup_path
	except Exception as e:
		raise Exception(f'Error al crear backup: {str(e)}')

def listar_backups() -> list:
	"""Lista todos los archivos de backup en el directorio de la base de datos"""
	backups = []
	if os.path.exists(DB_DIR):
		for filename in os.listdir(DB_DIR):
			if filename.endswith('.bak'):
				filepath = os.path.join(DB_DIR, filename)
				stat = os.stat(filepath)
				backups.append({
					'nombre': filename,
					'ruta': filepath,
					'tamaño': stat.st_size,
					'fecha': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
				})
	# Ordenar por fecha, más reciente primero
	backups.sort(key=lambda x: x['fecha'], reverse=True)
	return backups

# ============== FUNCIONES DE GESTION DE USUARIOS ==============

def hash_password(password: str) -> str:
	"""Genera un hash SHA256 de la contraseña"""
	return hashlib.sha256(password.encode()).hexdigest()

def verificar_usuario(username: str, password: str) -> dict:
	"""Verifica las credenciales de un usuario y retorna sus datos si son correctas"""
	conn = get_connection()
	c = conn.cursor()
	password_hash = hash_password(password)
	c.execute('SELECT id, username, es_admin FROM usuarios WHERE username=? AND password=?', 
			  (username, password_hash))
	row = c.fetchone()
	conn.close()
	if row:
		return {'id': row[0], 'username': row[1], 'es_admin': bool(row[2])}
	return None

def crear_usuario(username: str, password: str, es_admin: bool = False):
	"""Crea un nuevo usuario en el sistema"""
	conn = get_connection()
	c = conn.cursor()
	password_hash = hash_password(password)
	try:
		c.execute('INSERT INTO usuarios (username, password, es_admin) VALUES (?, ?, ?)',
				  (username, password_hash, 1 if es_admin else 0))
		conn.commit()
	except sqlite3.IntegrityError:
		conn.close()
		raise Exception('Ya existe un usuario con ese nombre.')
	conn.close()

def obtener_usuarios() -> list:
	"""Obtiene la lista de todos los usuarios (sin contraseñas)"""
	conn = get_connection()
	c = conn.cursor()
	c.execute('SELECT id, username, es_admin, fecha_creacion FROM usuarios')
	rows = c.fetchall()
	conn.close()
	return [{'id': r[0], 'username': r[1], 'es_admin': bool(r[2]), 'fecha_creacion': r[3]} for r in rows]

def eliminar_usuario(user_id: int):
	"""Elimina un usuario del sistema"""
	conn = get_connection()
	c = conn.cursor()
	# No permitir eliminar si es el único admin
	c.execute('SELECT COUNT(*) FROM usuarios WHERE es_admin=1')
	admin_count = c.fetchone()[0]
	c.execute('SELECT es_admin FROM usuarios WHERE id=?', (user_id,))
	row = c.fetchone()
	if row and row[0] == 1 and admin_count <= 1:
		conn.close()
		raise Exception('No se puede eliminar el único administrador del sistema.')
	c.execute('DELETE FROM usuarios WHERE id=?', (user_id,))
	conn.commit()
	conn.close()

def hay_usuarios() -> bool:
	"""Verifica si existen usuarios en el sistema"""
	conn = get_connection()
	c = conn.cursor()
	c.execute('SELECT COUNT(*) FROM usuarios')
	count = c.fetchone()[0]
	conn.close()
	return count > 0

def cambiar_password(user_id: int, nueva_password: str):
	"""Cambia la contraseña de un usuario"""
	conn = get_connection()
	c = conn.cursor()
	password_hash = hash_password(nueva_password)
	c.execute('UPDATE usuarios SET password=? WHERE id=?', (password_hash, user_id))
	conn.commit()
	conn.close()

# Inicializar la base de datos al importar el módulo
init_db()

# Crear backup automático al inicio (si existe la base de datos)
try:
	if os.path.exists(DB_NAME):
		crear_backup_db(manual=False)
except Exception:
	pass  # Si falla el backup automático, continuar igualmente

# ================= INTERFAZ GRAFICA BASE ===================

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
	
def aplicar_estilos_ttk():
	"""Configura estilos base para todos los widgets ttk."""
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

# === Helpers para interfaz gráfica ===
def crear_treeview(parent, columnas, headings, height=3, column_config=None):
	"""Crea un Treeview con altura mínima de 3 líneas y scrollable
	
	Args:
		parent: Frame padre
		columnas: Lista de nombres de columnas
		headings: Lista de encabezados de columnas
		height: Altura mínima en líneas
		column_config: Diccionario opcional con configuración de columnas
			Ejemplo: {'#0': {'width': 50, 'anchor': 'center'}, 'col1': {'width': 100, 'anchor': 'center'}}
	"""
	tree = ttk.Treeview(parent, columns=columnas, show='headings', height=height)
	
	# Configurar encabezados
	for col, head in zip(columnas, headings):
		tree.heading(col, text=head)
	
	# Configurar columnas si se proporciona configuración
	if column_config:
		for col_name, config in column_config.items():
			if col_name in ['#0'] + list(columnas):
				tree.column(col_name, **config)
	
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

# ═══════════════════════════════════════════════════════════════════════════════
# 20. CLASE PRINCIPAL: APP - APLICACIÓN TKINTER
# ═══════════════════════════════════════════════════════════════════════════════
# Clase principal que implementa la interfaz gráfica (GUI) de la aplicación.
# Utiliza Tkinter para crear ventanas, diálogos y controles interactivos.
#
# Módulos funcionales dentro de App:
#   - Inicialización y Autenticación
#   - Gestión de Materias
#   - Gestión de Personal y Ciclos
#   - Gestión de Divisiones
#   - Gestión de Horarios por Curso
#   - Gestión de Horarios por Profesor
#   - Configuración de Horas
#   - Gestión de Turnos, Planes y Materias
#   - Exportación de Horarios
#   - Gestión de Usuarios del Sistema
#   - Gestión de Respaldos
#
# Candidato para refactorización modular: views/, controllers/
# ───────────────────────────────────────────────────────────────────────────────

class App(tk.Tk):
	"""
	Aplicación principal de Gestión de Horarios Escolares.
	
	Hereda de tk.Tk para crear la ventana raíz de la aplicación.
	Gestiona toda la interfaz de usuario, autenticación y flujo de navegación.
	"""
	
	def __init__(self):
		"""
		Inicializa la aplicación Tkinter.
		
		Configura:
		- Estilos visuales (ttk styles)
		- Ventana principal (título, tamaño, color)
		- Verificación de primer inicio (sin usuarios)
		- Pantalla de login o configuración inicial
		
		Atributos de instancia:
		- self.usuario_actual: Información del usuario logueado (dict o None)
		- self.current_*: Campos para almacenar selecciones temporales en UI
		- self.frame_principal: Frame principal para contenido dinámico
		"""
		super().__init__()
		aplicar_estilos_ttk()
		self.title('Gestión de Horarios Escolares - Login')
		self.geometry('900x650')
		self.configure(bg='#f4f6fa')
		
		# Datos del usuario logueado
		self.usuario_actual = None
		
		# Verificar si es el primer inicio (no hay usuarios)
		if not hay_usuarios():
			self._configurar_admin_inicial()
		else:
			self._mostrar_login()

	def _configurar_admin_inicial(self):
		"""Configuración inicial del administrador en el primer inicio"""
		self.withdraw()  # Ocultar ventana principal
		
		win = tk.Toplevel(self)
		win.title('Configuración Inicial')
		win.geometry('450x380')
		win.resizable(False, False)
		win.configure(bg='#f4f6fa')
		win.protocol('WM_DELETE_WINDOW', lambda: sys.exit())  # Cerrar app si se cancela
		
		# Centrar ventana
		win.update_idletasks()
		x = (win.winfo_screenwidth() // 2) - (win.winfo_width() // 2)
		y = (win.winfo_screenheight() // 2) - (win.winfo_height() // 2)
		win.geometry(f'+{x}+{y}')
		
		ttk.Label(win, text='Bienvenido al Sistema', 
				 font=('Arial', 16, 'bold'), background='#f4f6fa').pack(pady=20)
		
		ttk.Label(win, text='Este es el primer inicio del sistema.\nPor favor, cree las credenciales del administrador:', 
				 font=('Arial', 10), background='#f4f6fa', justify='center').pack(pady=10)
		
		# Formulario
		form = ttk.Frame(win)
		form.pack(pady=20, padx=40)
		
		ttk.Label(form, text='Usuario:', background='#f4f6fa').grid(row=0, column=0, sticky='e', padx=5, pady=8)
		entry_username = ttk.Entry(form, width=25)
		entry_username.grid(row=0, column=1, padx=5, pady=8)
		entry_username.focus_set()
		
		ttk.Label(form, text='Contraseña:', background='#f4f6fa').grid(row=1, column=0, sticky='e', padx=5, pady=8)
		entry_password = ttk.Entry(form, show='*', width=25)
		entry_password.grid(row=1, column=1, padx=5, pady=8)
		
		ttk.Label(form, text='Confirmar:', background='#f4f6fa').grid(row=2, column=0, sticky='e', padx=5, pady=8)
		entry_confirm = ttk.Entry(form, show='*', width=25)
		entry_confirm.grid(row=2, column=1, padx=5, pady=8)
		
		def crear_admin():
			username = entry_username.get().strip()
			password = entry_password.get()
			confirm = entry_confirm.get()
			
			if not username:
				messagebox.showerror('Error', 'El nombre de usuario no puede estar vacío.', parent=win)
				return
			
			if len(username) < 3:
				messagebox.showerror('Error', 'El nombre de usuario debe tener al menos 3 caracteres.', parent=win)
				return
			
			if not password:
				messagebox.showerror('Error', 'La contraseña no puede estar vacía.', parent=win)
				return
			
			if len(password) < 4:
				messagebox.showerror('Error', 'La contraseña debe tener al menos 4 caracteres.', parent=win)
				return
			
			if password != confirm:
				messagebox.showerror('Error', 'Las contraseñas no coinciden.', parent=win)
				return
			
			try:
				crear_usuario(username, password, es_admin=True)
				messagebox.showinfo('Éxito', f'Administrador "{username}" creado correctamente.', parent=win)
				win.destroy()
				self.deiconify()  # Mostrar ventana principal
				self._mostrar_login()
			except Exception as e:
				messagebox.showerror('Error', str(e), parent=win)
		
		# Botones
		frame_btn = ttk.Frame(win)
		frame_btn.pack(pady=20)
		ttk.Button(frame_btn, text='Crear Administrador', command=crear_admin, width=20).pack()
		
		# Bindings de Enter
		entry_username.bind('<Return>', lambda e: entry_password.focus_set())
		entry_password.bind('<Return>', lambda e: entry_confirm.focus_set())
		entry_confirm.bind('<Return>', lambda e: crear_admin())

	def _mostrar_login(self):
		"""Muestra la ventana de login"""
		self.withdraw()  # Ocultar ventana principal
		
		win = tk.Toplevel(self)
		win.title('Inicio de Sesión')
		win.geometry('420x320')
		win.resizable(False, False)
		win.configure(bg='#f4f6fa')
		win.protocol('WM_DELETE_WINDOW', lambda: sys.exit())  # Cerrar app si se cancela
		
		# Centrar ventana
		win.update_idletasks()
		x = (win.winfo_screenwidth() // 2) - (win.winfo_width() // 2)
		y = (win.winfo_screenheight() // 2) - (win.winfo_height() // 2)
		win.geometry(f'+{x}+{y}')
		
		ttk.Label(win, text='Sistema de Gestión de Horarios', 
				 font=('Arial', 14, 'bold'), background='#f4f6fa').pack(pady=20)
		
		ttk.Label(win, text='Ingrese sus credenciales:', 
				 font=('Arial', 10), background='#f4f6fa').pack(pady=5)
		
		# Formulario
		form = ttk.Frame(win)
		form.pack(pady=20, padx=40)
		
		ttk.Label(form, text='Usuario:', background='#f4f6fa').grid(row=0, column=0, sticky='e', padx=5, pady=10)
		entry_username = ttk.Entry(form, width=25)
		entry_username.grid(row=0, column=1, padx=5, pady=10)
		entry_username.focus_set()
		
		ttk.Label(form, text='Contraseña:', background='#f4f6fa').grid(row=1, column=0, sticky='e', padx=5, pady=10)
		entry_password = ttk.Entry(form, show='*', width=25)
		entry_password.grid(row=1, column=1, padx=5, pady=10)
		
		def iniciar_sesion():
			username = entry_username.get().strip()
			password = entry_password.get()
			
			if not username or not password:
				messagebox.showerror('Error', 'Complete todos los campos.', parent=win)
				return
			
			usuario = verificar_usuario(username, password)
			if usuario:
				self.usuario_actual = usuario
				win.destroy()
				self.deiconify()  # Mostrar ventana principal
				self.title(f'Gestión de Horarios Escolares - Usuario: {usuario["username"]}')
				self._crear_menu()
				self._crear_frame_principal()
			else:
				messagebox.showerror('Error', 'Usuario o contraseña incorrectos.', parent=win)
				entry_password.delete(0, tk.END)
		
		# Botones
		frame_btn = ttk.Frame(win)
		frame_btn.pack(pady=20)
		ttk.Button(frame_btn, text='Iniciar Sesión', command=iniciar_sesion, width=18).pack()
		
		# Bindings de Enter
		entry_username.bind('<Return>', lambda e: entry_password.focus_set())
		entry_password.bind('<Return>', lambda e: iniciar_sesion())

	def _crear_menu(self):
		menubar = tk.Menu(self)
		self.config(menu=menubar)

		# Turnos, Planes y Materias (enlace directo)
		menubar.add_command(label='Turnos, Planes y Materias', command=self.mostrar_turnos_planes_materias)

		# Gestión de Personal y Ciclos (enlace directo)
		menubar.add_command(label='Personal y Cursos', command=self.mostrar_personal_ciclos)

		# Gestión de horarios (único con cascada)
		horarios_menu = tk.Menu(menubar, tearoff=0)
		horarios_menu.add_command(label='Por curso', command=self.mostrar_horarios_ciclo)
		horarios_menu.add_command(label='Por profesor', command=self.mostrar_horarios_profesor)
		menubar.add_cascade(label='Gestión de horarios', menu=horarios_menu)
		
		# Menú de Sistema
		sistema_menu = tk.Menu(menubar, tearoff=0)
		
		# Solo administradores ven Gestionar Usuarios
		if self.usuario_actual and self.usuario_actual.get('es_admin'):
			sistema_menu.add_command(label='Gestionar Usuarios', command=self.mostrar_gestion_usuarios)
			sistema_menu.add_separator()
		
		# Backups disponibles para todos los usuarios
		sistema_menu.add_command(label='Crear Backup Manual', command=self.crear_backup_manual)
		
		# Ver backups solo para administradores (incluye eliminar)
		if self.usuario_actual and self.usuario_actual.get('es_admin'):
			sistema_menu.add_command(label='Ver Backups', command=self.mostrar_lista_backups)
		
		sistema_menu.add_separator()
		sistema_menu.add_command(label='Cambiar Contraseña', command=self.cambiar_mi_password)
		sistema_menu.add_command(label='Cerrar Sesión', command=self.cerrar_sesion)
		menubar.add_cascade(label='Sistema', menu=sistema_menu)

	def _crear_frame_principal(self):
		if hasattr(self, 'frame_principal') and self.frame_principal.winfo_exists():
			self.frame_principal.destroy()
		
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
		if hasattr(self, 'frame_principal') and self.frame_principal.winfo_exists():
			for widget in self.frame_principal.winfo_children():
				widget.destroy()
			# Resetear el frame para evitar desplazamientos
			self.frame_principal.pack_forget()
			self.frame_principal.destroy()
			self.frame_principal = ttk.Frame(self)
			self.frame_principal.pack(fill='both', expand=True)


	# ───────────────────────────────────────────────────────────────────────────────
	# MÓDULO: GESTIÓN DE MATERIAS
	# ───────────────────────────────────────────────────────────────────────────────
	# Métodos para crear, editar, eliminar y listar materias/obligaciones curriculares.
	# Vista principal con tabla filtrable, formulario de entrada y acciones CRUD.
	# Candidato para refactorización: views/materias_view.py

	def mostrar_materias(self):
		"""
		Muestra la pantalla de gestión de materias/obligaciones.
		
		Funcionalidades:
		- Tabla de materias con nombre y horas semanales
		- Filtro por nombre (búsqueda en tiempo real)
		- Botones: Agregar, Editar, Eliminar, Asignar a Plan
		- Totales de materias y horas institucionales
		
		Requiere:
		- obtener_materias() - para cargar lista inicial
		- crear_materia() - para crear nuevas materias
		- actualizar_materia() - para editar existentes
		- eliminar_materia() - para borrar materias
		"""
		self.limpiar_frame()
		ttk.Label(self.frame_principal, text='Gestión de Materias/Obligaciones', font=('Arial', 14)).pack(pady=10)

		# Totales
		materias = obtener_materias()
		total_materias = len(materias)
		total_horas = sum(m['horas_semanales'] for m in materias)
		frame_tot = ttk.Frame(self.frame_principal)
		frame_tot.pack(pady=2)
		ttk.Label(frame_tot, text=f'Total de materias/obligaciones: {total_materias}').grid(row=0, column=0, padx=10)
		ttk.Label(frame_tot, text=f'Total de horas institucionales: {total_horas}').grid(row=0, column=1, padx=10)

		# Filtro
		frame_filtro = ttk.Frame(self.frame_principal)
		frame_filtro.pack(pady=2)
		ttk.Label(frame_filtro, text='Filtro:').grid(row=0, column=0, padx=5)
		self.filtro_materia = tk.StringVar()
		entry_filtro = ttk.Entry(frame_filtro, textvariable=self.filtro_materia)
		entry_filtro.grid(row=0, column=1, padx=5)

		# Tabla de obligaciones usando helper
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
		ttk.Button(btns, text='Asignar a Plan de Estudio', command=self._asignar_materias_a_plan).grid(row=0, column=3, padx=5)

		# Selección en tabla
		self.tree_materias.bind('<<TreeviewSelect>>', self._on_select_materia)
		self.materia_seleccionada_id = None

	def _recargar_materias_tree(self):
		materias_ordenadas = sorted(obtener_materias(), key=lambda m: m['nombre'].lower())
		recargar_treeview(self.tree_materias, materias_ordenadas, ['nombre', 'horas_semanales'])

	# Eliminada: _cargar_obligaciones_en_tree (reemplazada por _recargar_materias_tree)

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
	
	def _asignar_materias_a_plan(self):
		"""Ventana para asignar múltiples materias a un plan de estudio"""
		planes = obtener_planes()
		if not planes:
			messagebox.showinfo('Información', 'No hay planes de estudio creados.\nPor favor, cree al menos un plan primero.')
			return
		
		materias = obtener_materias()
		if not materias:
			messagebox.showinfo('Información', 'No hay materias creadas para asignar.')
			return
		
		win = tk.Toplevel(self)
		win.configure(bg='#f4f6fa')
		win.title('Asignar Materias a Plan de Estudio')
		win.geometry('550x500')
		win.minsize(550, 500)
		win.transient(self)
		win.grab_set()
		win.focus_force()
		
		ttk.Label(win, text='Asignar Materias a Plan de Estudio', font=('Arial', 12, 'bold')).pack(pady=10)
		
		# Selección de plan
		frame_plan = ttk.Frame(win)
		frame_plan.pack(pady=10, padx=20, fill='x')
		ttk.Label(frame_plan, text='Plan de Estudio:', font=('Segoe UI', 10)).grid(row=0, column=0, sticky='w', pady=5)
		
		plan_nombres = [p['nombre'] for p in sorted(planes, key=lambda x: x['nombre'].lower())]
		plan_ids = {p['nombre']: p['id'] for p in planes}
		
		cb_plan = ttk.Combobox(frame_plan, values=plan_nombres, state='readonly', width=40)
		cb_plan.grid(row=0, column=1, sticky='ew', pady=5, padx=(10, 0))
		frame_plan.columnconfigure(1, weight=1)
		cb_plan.focus_set()
		
		# Frame para lista de materias con checkboxes
		frame_materias = ttk.Frame(win)
		frame_materias.pack(pady=10, padx=20, fill='both', expand=True)
		ttk.Label(frame_materias, text='Seleccionar materias a asignar:', font=('Segoe UI', 10)).pack(anchor='w', pady=(0, 5))
		
		# Canvas con scrollbar
		canvas_frame = ttk.Frame(frame_materias)
		canvas_frame.pack(fill='both', expand=True)
		
		canvas = tk.Canvas(canvas_frame, bg='#ffffff', highlightthickness=1, highlightbackground='#cccccc')
		scrollbar = ttk.Scrollbar(canvas_frame, orient='vertical', command=canvas.yview)
		scrollable_frame = ttk.Frame(canvas)
		
		scrollable_frame.bind(
			"<Configure>",
			lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
		)
		
		canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
		canvas.configure(yscrollcommand=scrollbar.set)
		
		canvas.pack(side='left', fill='both', expand=True)
		scrollbar.pack(side='right', fill='y')
		
		# Variables para checkboxes
		materias_vars = {}
		materias_checkbuttons = []
		
		def actualizar_lista_materias(*args):
			"""Actualiza la lista de materias según el plan seleccionado"""
			# Limpiar checkboxes anteriores
			for widget in scrollable_frame.winfo_children():
				widget.destroy()
			materias_vars.clear()
			materias_checkbuttons.clear()
			
			plan_nombre = cb_plan.get()
			if not plan_nombre:
				ttk.Label(scrollable_frame, text='Seleccione un plan primero', foreground='gray').pack(pady=20)
				return
			
			plan_id = plan_ids[plan_nombre]
			materias_plan = obtener_materias_de_plan(plan_id)
			materias_plan_ids = [m['id'] for m in materias_plan]
			
			# Crear checkboxes para materias no asignadas
			materias_disponibles = [m for m in materias if m['id'] not in materias_plan_ids]
			materias_disponibles_ordenadas = sorted(materias_disponibles, key=lambda x: x['nombre'].lower())
			
			if not materias_disponibles_ordenadas:
				ttk.Label(scrollable_frame, text='Todas las materias ya están asignadas a este plan', 
						 foreground='gray', font=('Segoe UI', 9, 'italic')).pack(pady=20)
				return
			
			# Frame de selección general
			frame_sel_todos = ttk.Frame(scrollable_frame)
			frame_sel_todos.pack(fill='x', pady=(5, 10), padx=5)
			
			var_todos = tk.IntVar(value=0)
			
			def seleccionar_todos():
				estado = var_todos.get()
				for var in materias_vars.values():
					var.set(estado)
			
			chk_todos = ttk.Checkbutton(frame_sel_todos, text='Seleccionar todas', 
									   variable=var_todos, command=seleccionar_todos)
			chk_todos.pack(anchor='w')
			
			ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=5)
			
			# Crear checkboxes para cada materia
			for materia in materias_disponibles_ordenadas:
				var = tk.IntVar(value=0)
				texto = f"{materia['nombre']} ({materia['horas_semanales']} hs)"
				chk = ttk.Checkbutton(scrollable_frame, text=texto, variable=var)
				chk.pack(anchor='w', pady=2, padx=5)
				materias_vars[materia['id']] = var
				materias_checkbuttons.append(chk)
		
		cb_plan.bind('<<ComboboxSelected>>', actualizar_lista_materias)
		
		# Botones
		frame_btns = ttk.Frame(win)
		frame_btns.pack(pady=15)
		
		def asignar():
			plan_nombre = cb_plan.get()
			if not plan_nombre:
				messagebox.showerror('Error', 'Seleccione un plan de estudio.', parent=win)
				return
			
			materias_seleccionadas = [mid for mid, var in materias_vars.items() if var.get() == 1]
			if not materias_seleccionadas:
				messagebox.showwarning('Atención', 'No ha seleccionado ninguna materia.', parent=win)
				return
			
			plan_id = plan_ids[plan_nombre]
			
			try:
				# Asignar cada materia seleccionada
				for materia_id in materias_seleccionadas:
					agregar_materia_a_plan(plan_id, materia_id)
				
				messagebox.showinfo('Éxito', 
								   f'Se asignaron {len(materias_seleccionadas)} materia(s) al plan "{plan_nombre}".', 
								   parent=win)
				
				# Actualizar la lista para reflejar los cambios
				actualizar_lista_materias()
				
			except Exception as e:
				messagebox.showerror('Error', str(e), parent=win)
		
		ttk.Button(frame_btns, text='Asignar Seleccionadas', command=asignar, width=20).grid(row=0, column=0, padx=5)
		ttk.Button(frame_btns, text='Cerrar', command=win.destroy, width=15).grid(row=0, column=1, padx=5)


	# ───────────────────────────────────────────────────────────────────────────────
	# MÓDULO: GESTIÓN DE PERSONAL Y CICLOS
	# ───────────────────────────────────────────────────────────────────────────────
	# Vista consolidada con tabs para gestionar profesores, ciclos y divisiones.
	# Candidato para refactorización: views/personal_ciclos_view.py
	
	def mostrar_personal_ciclos(self):
		"""
		Muestra la pantalla de gestión de personal, ciclos y divisiones.
		
		Estructura:
		- Tab 1: Personal (Profesores, asignación de turnos, banca de horas)
		- Tab 2: Ciclos (Crear, editar, eliminar ciclos con planes asociados)
		- Tab 3: Divisiones (Secciones dentro de ciclos)
		
		Cada tab tiene su propia tabla y botones de acción.
		"""
		self.limpiar_frame()
		
		# Título principal
		ttk.Label(self.frame_principal, text='Gestión de Personal, Ciclos y Divisiones', 
				 font=('Arial', 14)).pack(pady=10)
		
		# Crear notebook para tabs
		notebook = ttk.Notebook(self.frame_principal)
		notebook.pack(fill='both', expand=True, padx=10, pady=5)
		
		# Crear tabs
		tab_personal = ttk.Frame(notebook)
		tab_ciclos = ttk.Frame(notebook)
		tab_divisiones = ttk.Frame(notebook)
		
		notebook.add(tab_personal, text='Personal')
		notebook.add(tab_ciclos, text='Ciclos')
		notebook.add(tab_divisiones, text='Divisiones')
		
		# Crear contenido de cada tab
		self._crear_tab_personal(tab_personal)
		self._crear_tab_ciclos(tab_ciclos)
		self._crear_tab_divisiones(tab_divisiones)
	
	def _crear_tab_personal(self, parent):
		"""Crea el tab de Personal con layout lateral"""
		# Frame principal con dos columnas: aside y contenido
		main_frame = ttk.Frame(parent)
		main_frame.pack(fill='both', expand=True, padx=10, pady=10)
		main_frame.columnconfigure(1, weight=1)
		main_frame.rowconfigure(0, weight=1)
		
		# ===== ASIDE IZQUIERDO =====
		aside = ttk.Frame(main_frame)
		aside.grid(row=0, column=0, sticky='ns', padx=(0, 10))
		
		ttk.Label(aside, text='Acciones', font=('Segoe UI', 11, 'bold')).pack(pady=(0, 10))
		
		# Formulario de entrada
		ttk.Label(aside, text='Nombre:').pack(pady=(5, 2))
		entry_prof_frame = ttk.Frame(aside)
		entry_prof_frame.pack(pady=(0, 10))
		self.entry_nombre_profesor = ttk.Entry(entry_prof_frame, width=23)
		self.entry_nombre_profesor.pack(side='left')
		def _clear_prof_entry():
			self.entry_nombre_profesor.delete(0, tk.END)
			self.entry_nombre_profesor.focus_set()
		ttk.Button(entry_prof_frame, text='🧹', width=3, command=_clear_prof_entry).pack(side='left', padx=(5, 0))
		
		# Botones verticales
		ttk.Button(aside, text='Agregar', command=self._agregar_profesor, width=22).pack(pady=3)
		ttk.Button(aside, text='Editar', command=self._editar_profesor, width=22).pack(pady=3)
		ttk.Button(aside, text='Eliminar', command=self._eliminar_profesor, width=22).pack(pady=3)
		
		ttk.Separator(aside, orient='horizontal').pack(fill='x', pady=10)
		
		ttk.Button(aside, text='Banca de horas', command=self._gestionar_banca_profesor, width=22).pack(pady=3)
		ttk.Button(aside, text='Turnos del agente', command=self._gestionar_turnos_profesor, width=22).pack(pady=3)
		
		# ===== CONTENIDO DERECHO =====
		content = ttk.Frame(main_frame)
		content.grid(row=0, column=1, sticky='nsew')
		
		# Totales
		self.label_total_profesores = ttk.Label(content, text='', font=('Arial', 10))
		self.label_total_profesores.pack(pady=(0, 5))
		
		# Filtros
		frame_filtro = ttk.Frame(content)
		frame_filtro.pack(pady=5)
		
		ttk.Label(frame_filtro, text='Filtro:').grid(row=0, column=0, padx=5)
		self.filtro_profesor = tk.StringVar()
		entry_filtro_frame = ttk.Frame(frame_filtro)
		entry_filtro_frame.grid(row=0, column=1, padx=5)
		entry_filtro = ttk.Entry(entry_filtro_frame, textvariable=self.filtro_profesor, width=18)
		entry_filtro.pack(side='left')
		def _clear_filtro_prof():
			self.filtro_profesor.set('')
			entry_filtro.focus_set()
		ttk.Button(entry_filtro_frame, text='🧹', width=3, command=_clear_filtro_prof).pack(side='left', padx=(5, 0))
		
		ttk.Label(frame_filtro, text='Turno:').grid(row=0, column=2, padx=5)
		turnos = obtener_turnos()
		self.turnos_dict_prof = {t['nombre']: t['id'] for t in turnos}
		self.cb_turno_profesor = ttk.Combobox(frame_filtro, values=['Todos'] + list(self.turnos_dict_prof.keys()), 
									 state='readonly', width=18)
		self.cb_turno_profesor.set('Todos')
		self.cb_turno_profesor.grid(row=0, column=3, padx=5)
		
		# Tabla de profesores
		frame_tabla = ttk.Frame(content)
		frame_tabla.pack(pady=10, fill='both', expand=True)
		self.tree_profesores = crear_treeview(frame_tabla, ('Nombre',), ('Nombre',))
		self._recargar_profesores_tree()
		
		# Eventos de filtrado
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
			self.label_total_profesores.config(text=f'Total de agentes: {len(profesores_filtrados)}')
		
		self.filtro_profesor.trace_add('write', filtrar_profesores)
		self.cb_turno_profesor.bind('<<ComboboxSelected>>', lambda e: filtrar_profesores())
		self.after(100, filtrar_profesores)
		
		# Selección en tabla
		self.tree_profesores.bind('<<TreeviewSelect>>', self._on_select_profesor)
		self.profesor_seleccionado_id = None

	def _crear_tab_ciclos(self, parent):
		"""Crea el tab de Ciclos con CRUD y asociación a planes."""
		main_frame = ttk.Frame(parent)
		main_frame.pack(fill='both', expand=True, padx=10, pady=10)
		main_frame.columnconfigure(1, weight=1)
		main_frame.rowconfigure(0, weight=1)

		# Aside con acciones
		aside = ttk.Frame(main_frame)
		aside.grid(row=0, column=0, sticky='ns', padx=(0, 10))
		ttk.Label(aside, text='Acciones', font=('Segoe UI', 11, 'bold')).pack(pady=(0, 10))
		ttk.Button(aside, text='Agregar', command=self._agregar_ciclo, width=22).pack(pady=3)
		ttk.Button(aside, text='Editar', command=self._editar_ciclo, width=22).pack(pady=3)
		ttk.Button(aside, text='Eliminar', command=self._eliminar_ciclo_tab, width=22).pack(pady=3)

		# Contenido principal
		content = ttk.Frame(main_frame)
		content.grid(row=0, column=1, sticky='nsew')

		self.label_total_ciclos = ttk.Label(content, text='Total de ciclos: 0', font=('Arial', 10))
		self.label_total_ciclos.pack(pady=(0, 5))

		frame_tabla = ttk.Frame(content)
		frame_tabla.pack(pady=10, fill='both', expand=True)
		column_config = {
			'Ciclo': {'width': 200, 'anchor': 'w'},
			'Planes': {'width': 260, 'anchor': 'w'}
		}
		self.tree_ciclos = crear_treeview(frame_tabla, ('Ciclo', 'Planes'), ('Ciclo', 'Planes'), column_config=column_config)
		self.tree_ciclos.bind('<<TreeviewSelect>>', self._on_select_ciclo)
		self.ciclo_seleccionado_id = None
		self._recargar_ciclos_tree()
	
	def _crear_tab_divisiones(self, parent):
		"""Crea el tab de Divisiones con layout lateral"""
		# Frame principal con dos columnas: aside y contenido
		main_frame = ttk.Frame(parent)
		main_frame.pack(fill='both', expand=True, padx=10, pady=10)
		main_frame.columnconfigure(1, weight=1)
		main_frame.rowconfigure(0, weight=1)
		
		# ===== ASIDE IZQUIERDO =====
		aside = ttk.Frame(main_frame)
		aside.grid(row=0, column=0, sticky='ns', padx=(0, 10))
		
		ttk.Label(aside, text='Acciones', font=('Segoe UI', 11, 'bold')).pack(pady=(0, 10))
		
		# Botones verticales
		ttk.Button(aside, text='Agregar', command=self._agregar_division, width=22).pack(pady=3)
		ttk.Button(aside, text='Editar', command=self._editar_division, width=22).pack(pady=3)
		ttk.Button(aside, text='Eliminar', command=self._eliminar_division, width=22).pack(pady=3)
		
		# ===== CONTENIDO DERECHO =====
		content = ttk.Frame(main_frame)
		content.grid(row=0, column=1, sticky='nsew')
		
		# Totales
		divisiones = obtener_divisiones()
		total_divisiones = len(divisiones)
		self.label_total_divisiones = ttk.Label(content, text=f'Total de divisiones: {total_divisiones}', 
											   font=('Arial', 10))
		self.label_total_divisiones.pack(pady=(0, 5))
		
		# Selectores de filtro
		frame_sel = ttk.Frame(content)
		frame_sel.pack(pady=5)
		
		ttk.Label(frame_sel, text='Turno:').grid(row=0, column=0, padx=5)
		turnos = obtener_turnos()
		self.turnos_dict = {t['nombre']: t['id'] for t in turnos}
		self.cb_turno_division = ttk.Combobox(frame_sel, values=list(self.turnos_dict.keys()), 
											 state='readonly', width=15)
		self.cb_turno_division.grid(row=0, column=1, padx=5)
		
		ttk.Label(frame_sel, text='Plan:').grid(row=0, column=2, padx=5)
		self.cb_plan_division = ttk.Combobox(frame_sel, values=[], state='disabled', width=15)
		self.cb_plan_division.grid(row=0, column=3, padx=5)
		
		ttk.Label(frame_sel, text='Ciclo:').grid(row=0, column=4, padx=5)
		self.cb_ciclo_division = ttk.Combobox(frame_sel, values=[], state='disabled', width=15)
		self.cb_ciclo_division.grid(row=0, column=5, padx=5)
		
		# Eventos de selección
		def on_turno_selected(event=None):
			turno_nombre = self.cb_turno_division.get()
			if not turno_nombre:
				self.cb_plan_division['values'] = []
				self.cb_plan_division.set('')
				self.cb_plan_division.config(state='disabled')
				self.cb_ciclo_division['values'] = []
				self.cb_ciclo_division.set('')
				self.cb_ciclo_division.config(state='disabled')
				return
			turno_id = self.turnos_dict[turno_nombre]
			planes = obtener_planes_de_turno(turno_id)
			self.planes_dict = {p['nombre']: p['id'] for p in planes}
			self.cb_plan_division['values'] = list(self.planes_dict.keys())
			self.cb_plan_division.set('')
			self.cb_plan_division.config(state='readonly' if planes else 'disabled')
			self.cb_ciclo_division['values'] = []
			self.cb_ciclo_division.set('')
			self.cb_ciclo_division.config(state='disabled')
			if planes:
				self.cb_plan_division.focus_set()
			self._recargar_divisiones_tree()
		
		def on_plan_selected(event=None):
			plan_nombre = self.cb_plan_division.get()
			if not plan_nombre:
				self.cb_ciclo_division['values'] = []
				self.cb_ciclo_division.set('')
				self.cb_ciclo_division.config(state='disabled')
				return
			plan_id = self.planes_dict[plan_nombre]
			ciclos = obtener_ciclos(plan_id)
			self.cb_ciclo_division['values'] = [a['nombre'] for a in ciclos]
			self.cb_ciclo_division.set('')
			self.cb_ciclo_division.config(state='readonly' if ciclos else 'disabled')
			if ciclos:
				self.cb_ciclo_division.focus_set()
			self._recargar_divisiones_tree()
		
		def on_ciclo_selected(event=None):
			self._recargar_divisiones_tree()
		
		self.cb_turno_division.bind('<<ComboboxSelected>>', on_turno_selected)
		self.cb_plan_division.bind('<<ComboboxSelected>>', on_plan_selected)
		self.cb_ciclo_division.bind('<<ComboboxSelected>>', on_ciclo_selected)
		self.cb_turno_division.focus_set()
		
		# Tabla de divisiones
		frame_tabla = ttk.Frame(content)
		frame_tabla.pack(pady=10, fill='both', expand=True)
		
		# Configuración de columnas para el Treeview de Ciclos
		column_config = {
			'Turno': {'width': 100, 'anchor': 'center'},
			'Plan': {'width': 150, 'anchor': 'center'},
			'Ciclo': {'width': 100, 'anchor': 'center'},
			'División': {'width': 120, 'anchor': 'center'}
		}
		
		self.tree_divisiones = crear_treeview(frame_tabla, 
											 ('Turno', 'Plan', 'Ciclo', 'División'), 
											 ('Turno', 'Plan', 'Ciclo', 'División'),
											 column_config=column_config)
		self._recargar_divisiones_tree()
		
		# Selección en tabla
		self.tree_divisiones.bind('<<TreeviewSelect>>', self._on_select_division)
		self.division_seleccionada_id = None

	def _recargar_ciclos_tree(self):
		ciclos = obtener_ciclos_con_planes()
		self.ciclos_cache = ciclos
		datos_tree = []
		for ciclo in ciclos:
			planes_ordenados = sorted([p['nombre'] for p in ciclo['planes']], key=lambda x: x.lower())
			planes_text = ', '.join(planes_ordenados)
			planes_text = planes_text if planes_text else 'Sin planes asociados'
			datos_tree.append({'id': ciclo['id'], 'nombre': ciclo['nombre'], 'planes': planes_text})
		tree = getattr(self, 'tree_ciclos', None)
		if tree:
			recargar_treeview(tree, datos_tree, ['nombre', 'planes'])
		if hasattr(self, 'label_total_ciclos'):
			self.label_total_ciclos.config(text=f'Total de ciclos: {len(datos_tree)}')
		if not any(c['id'] == self.ciclo_seleccionado_id for c in ciclos):
			self.ciclo_seleccionado_id = None
		self._sincronizar_comboboxes_ciclos()

	def _on_select_ciclo(self, event=None):
		seleccion = self.tree_ciclos.selection()
		self.ciclo_seleccionado_id = int(seleccion[0]) if seleccion else None

	def _agregar_ciclo(self):
		self._abrir_modal_ciclo(modo='agregar')

	def _editar_ciclo(self):
		if not self.ciclo_seleccionado_id:
			messagebox.showerror('Error', 'Seleccione un ciclo para editar.')
			return
		self._abrir_modal_ciclo(modo='editar')

	def _eliminar_ciclo_tab(self):
		if not self.ciclo_seleccionado_id:
			messagebox.showerror('Error', 'Seleccione un ciclo para eliminar.')
			return
		deps = contar_dependencias_ciclo(self.ciclo_seleccionado_id)
		mensaje = (
			f"Se eliminarán {deps['divisiones']} divisiones y {deps['horarios']} horarios asociados al ciclo seleccionado. "
			'¿Desea continuar?'
		)
		if not messagebox.askyesno('Confirmar eliminación', mensaje):
			return
		try:
			eliminar_ciclo(self.ciclo_seleccionado_id, cascade=True)
			self.ciclo_seleccionado_id = None
			self._recargar_ciclos_tree()
			self._recargar_divisiones_tree()
		except Exception as e:
			messagebox.showerror('Error', str(e))

	def _abrir_modal_ciclo(self, modo: str):
		editar = modo == 'editar'
		ciclo_id = self.ciclo_seleccionado_id if editar else None
		if editar and not ciclo_id:
			messagebox.showerror('Error', 'Seleccione un ciclo para editar.')
			return
		planes = obtener_planes()
		if not planes:
			messagebox.showinfo('Información', 'Debe crear al menos un plan de estudio antes de gestionar ciclos.')
			return
		ciclo_actual = None
		if editar:
			ciclo_actual = next((c for c in getattr(self, 'ciclos_cache', []) if c['id'] == ciclo_id), None)
			if not ciclo_actual:
				messagebox.showerror('Error', 'No se pudo cargar la información del ciclo seleccionado.')
				return
		planes_seleccionados = {p['id'] for p in ciclo_actual['planes']} if ciclo_actual else set()
		win = tk.Toplevel(self)
		win.configure(bg='#f4f6fa')
		titulo = 'Editar ciclo' if editar else 'Agregar ciclo'
		win.title(titulo)
		win.geometry('420x440')
		win.minsize(400, 380)
		win.transient(self)
		win.grab_set()
		win.focus_force()

		ttk.Label(win, text=titulo, font=('Arial', 12, 'bold')).pack(pady=10)
		ttk.Label(win, text='Nombre del ciclo:', font=('Segoe UI', 10)).pack(anchor='w', padx=20)
		entry_nombre = ttk.Entry(win)
		entry_nombre.pack(fill='x', padx=20, pady=(0, 10))
		if ciclo_actual:
			entry_nombre.insert(0, ciclo_actual['nombre'])

		ttk.Label(win, text='Planes de estudio asociados:', font=('Segoe UI', 10)).pack(anchor='w', padx=20)
		planes_frame = ttk.Frame(win)
		planes_frame.pack(fill='both', expand=True, padx=20, pady=10)
		plan_vars = {}
		planes_sorted = sorted(planes, key=lambda p: p['nombre'].lower())
		if len(planes_sorted) > 5:
			canvas = tk.Canvas(planes_frame, highlightthickness=0, bg='#f4f6fa')
			scrollbar = ttk.Scrollbar(planes_frame, orient='vertical', command=canvas.yview)
			inner = ttk.Frame(canvas)
			inner.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
			canvas.create_window((0, 0), window=inner, anchor='nw')
			canvas.configure(yscrollcommand=scrollbar.set)
			canvas.pack(side='left', fill='both', expand=True)
			scrollbar.pack(side='right', fill='y')
			checkbox_parent = inner
		else:
			checkbox_parent = planes_frame
		for plan in planes_sorted:
			var = tk.IntVar(value=1 if plan['id'] in planes_seleccionados else 0)
			ttk.Checkbutton(checkbox_parent, text=plan['nombre'], variable=var).pack(anchor='w', pady=2)
			plan_vars[plan['id']] = var

		def guardar():
			nombre = entry_nombre.get().strip()
			if not nombre:
				messagebox.showerror('Error', 'Ingrese un nombre para el ciclo.', parent=win)
				return
			seleccionados = [plan_id for plan_id, var in plan_vars.items() if var.get() == 1]
			if not seleccionados:
				messagebox.showerror('Error', 'Seleccione al menos un plan de estudio.', parent=win)
				return
			try:
				if editar:
					actualizar_ciclo(ciclo_id, nombre, seleccionados)
				else:
					crear_ciclo(nombre, seleccionados)
				self._recargar_ciclos_tree()
				self._recargar_divisiones_tree()
				win.destroy()
			except Exception as e:
				messagebox.showerror('Error', str(e), parent=win)

		btns = ttk.Frame(win)
		btns.pack(pady=10)
		ttk.Button(btns, text='Guardar', command=guardar).pack(side='left', padx=5)
		ttk.Button(btns, text='Cancelar', command=win.destroy).pack(side='left', padx=5)
		entry_nombre.focus_set()
		win.bind('<Return>', lambda e: guardar())

	def _sincronizar_comboboxes_ciclos(self):
		self._actualizar_ciclos_en_divisiones_tab()
		self._actualizar_ciclos_en_horarios_curso()

	def _actualizar_ciclos_en_divisiones_tab(self):
		plan_combo = getattr(self, 'cb_plan_division', None)
		ciclo_combo = getattr(self, 'cb_ciclo_division', None)
		if not plan_combo or not ciclo_combo:
			return
		if not plan_combo.winfo_exists() or not ciclo_combo.winfo_exists():
			return
		try:
			plan_nombre = plan_combo.get()
		except tk.TclError:
			return
		planes_dict = getattr(self, 'planes_dict', {})
		if not plan_nombre or plan_nombre not in planes_dict:
			return
		plan_id = planes_dict[plan_nombre]
		ciclos = obtener_ciclos(plan_id)
		ciclo_nombres = [c['nombre'] for c in ciclos]
		try:
			seleccion = ciclo_combo.get()
		except tk.TclError:
			return
		ciclo_combo['values'] = ciclo_nombres
		ciclo_combo.config(state='readonly' if ciclo_nombres else 'disabled')
		if seleccion in ciclo_nombres:
			ciclo_combo.set(seleccion)
		else:
			ciclo_combo.set('')

	def _actualizar_ciclos_en_horarios_curso(self):
		plan_combo = getattr(self, 'cb_plan_horario', None)
		ciclo_combo = getattr(self, 'cb_ciclo_horario', None)
		if not plan_combo or not ciclo_combo:
			return
		if not plan_combo.winfo_exists() or not ciclo_combo.winfo_exists():
			return
		try:
			plan_nombre = plan_combo.get()
		except tk.TclError:
			return
		planes_dict = getattr(self, 'planes_dict_horario', {})
		if not plan_nombre or plan_nombre not in planes_dict:
			return
		plan_id = planes_dict[plan_nombre]
		ciclos = obtener_ciclos(plan_id)
		self.ciclos_dict_horario = {c['nombre']: c['id'] for c in ciclos}
		ciclo_nombres = list(self.ciclos_dict_horario.keys())
		try:
			seleccion = ciclo_combo.get()
		except tk.TclError:
			return
		ciclo_combo['values'] = ciclo_nombres
		ciclo_combo.config(state='readonly' if ciclo_nombres else 'disabled')
		if seleccion in ciclo_nombres:
			ciclo_combo.set(seleccion)
		else:
			ciclo_combo.set('')
	
	# ============================================================
	# FUNCIONES ANTIGUAS (mantenidas para compatibilidad)
	# ============================================================
	
	def mostrar_profesores(self):
		self.limpiar_frame()
		ttk.Label(self.frame_principal, text='Gestión de personal', font=('Arial', 14)).pack(pady=10)

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
			self.label_total_profesores.config(text=f'Total de agentes: {len(profesores_filtrados)}')
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
		ttk.Button(btns, text='Turnos del agente', command=self._gestionar_turnos_profesor).grid(row=0, column=4, padx=5)

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
		# Obtener nombre del profesor
		profesores = obtener_profesores()
		profesor = next((p for p in profesores if p['id'] == profesor_id), None)
		nombre_profesor = profesor['nombre'] if profesor else 'Agente'
		
		win = tk.Toplevel(self)
		win.configure(bg='#f4f6fa')
		win.title(f'Obligaciones de {nombre_profesor}')
		win.geometry('550x450')
		win.minsize(550, 450)
		win.transient(self)
		win.grab_set()
		win.focus_force()
		ttk.Label(win, text='Obligaciones asignadas y horas ocupadas', font=('Arial', 12)).pack(pady=8)

		# Tabla de banca con frame para expansión
		frame_tabla = ttk.Frame(win)
		frame_tabla.pack(pady=5, padx=10, fill='both', expand=True)
		
		tree_banca = ttk.Treeview(frame_tabla, columns=('Obligación', 'Horas'), show='headings', height=3)
		tree_banca.heading('Obligación', text='Obligación')
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
		ttk.Label(form, text='Obligación:').grid(row=0, column=0, padx=5, pady=2)
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
		btn_agregar = ttk.Button(btns, text='Agregar obligación', command=agregar_materia)
		btn_agregar.grid(row=0, column=0, padx=5)
		btn_eliminar = ttk.Button(btns, text='Eliminar obligación', command=eliminar_materia)
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
		ttk.Label(self.frame_principal, text='Gestión de Divisiones', font=('Arial', 14)).pack(pady=10)

		# Totales
		divisiones = obtener_divisiones()
		total_divisiones = len(divisiones)
		frame_tot = ttk.Frame(self.frame_principal)
		frame_tot.pack(pady=2)
		self.label_total_divisiones = ttk.Label(frame_tot, text=f'Total de divisiones: {total_divisiones}')
		self.label_total_divisiones.grid(row=0, column=0, padx=10)

		# Selección de Turno, Plan, Ciclo
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
		ttk.Label(frame_sel, text='Ciclo:').grid(row=0, column=4, padx=5)
		self.cb_ciclo_division = ttk.Combobox(frame_sel, values=[], state='disabled')
		self.cb_ciclo_division.grid(row=0, column=5, padx=5)

		def on_turno_selected(event=None):
			turno_nombre = self.cb_turno_division.get()
			if not turno_nombre:
				self.cb_plan_division['values'] = []
				self.cb_plan_division.set('')
				self.cb_plan_division.config(state='disabled')
				self.cb_ciclo_division['values'] = []
				self.cb_ciclo_division.set('')
				self.cb_ciclo_division.config(state='disabled')
				return
			turno_id = self.turnos_dict[turno_nombre]
			planes = obtener_planes_de_turno(turno_id)
			self.planes_dict = {p['nombre']: p['id'] for p in planes}
			self.cb_plan_division['values'] = list(self.planes_dict.keys())
			self.cb_plan_division.set('')
			self.cb_plan_division.config(state='readonly' if planes else 'disabled')
			self.cb_ciclo_division['values'] = []
			self.cb_ciclo_division.set('')
			self.cb_ciclo_division.config(state='disabled')
			# Pasar focus a Plan
			if planes:
				self.cb_plan_division.focus_set()
			self._recargar_divisiones_tree()
		def on_plan_selected(event=None):
			plan_nombre = self.cb_plan_division.get()
			if not plan_nombre:
				self.cb_ciclo_division['values'] = []
				self.cb_ciclo_division.set('')
				self.cb_ciclo_division.config(state='disabled')
				return
			plan_id = self.planes_dict[plan_nombre]
			ciclos = obtener_ciclos(plan_id)
			ciclo_actual = self.cb_ciclo_division.get()
			ciclo_nombres = [a['nombre'] for a in ciclos]
			self.cb_ciclo_division['values'] = ciclo_nombres
			if ciclo_actual in ciclo_nombres:
				self.cb_ciclo_division.set(ciclo_actual)
			else:
				self.cb_ciclo_division.set('')
			self.cb_ciclo_division.config(state='readonly' if ciclos else 'disabled')
			if ciclos and ciclo_actual not in ciclo_nombres:
				self.cb_ciclo_division.focus_set()
			self._recargar_divisiones_tree()
		def on_ciclo_selected(event=None):
			self._recargar_divisiones_tree()
		self.cb_turno_division.bind('<<ComboboxSelected>>', on_turno_selected)
		self.cb_plan_division.bind('<<ComboboxSelected>>', on_plan_selected)
		self.cb_ciclo_division.bind('<<ComboboxSelected>>', on_ciclo_selected)
		
		# Focus inicial en Turno
		self.cb_turno_division.focus_set()

		# Tabla de divisiones usando helper
		frame_tabla = ttk.Frame(self.frame_principal)
		frame_tabla.pack(pady=10, fill='both', expand=True)
		self.tree_divisiones = crear_treeview(frame_tabla, ('Turno', 'Plan', 'Ciclo', 'División'), ('Turno', 'Plan', 'Ciclo', 'División'))
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
		turnos_map = {t['id']: t['nombre'] for t in obtener_turnos()}
		planes_map = {p['id']: p['nombre'] for p in obtener_planes()}
		ciclos_map = {c['id']: c['nombre'] for c in obtener_ciclos_con_planes()}
		turno_nombre = self.cb_turno_division.get() if hasattr(self, 'cb_turno_division') else ''
		plan_nombre = self.cb_plan_division.get() if hasattr(self, 'cb_plan_division') else ''
		ciclo_nombre = self.cb_ciclo_division.get() if hasattr(self, 'cb_ciclo_division') else ''
		datos = []
		for division in divisiones:
			turno = turnos_map.get(division['turno_id'], '')
			plan = planes_map.get(division['plan_id'], '')
			ciclo = ciclos_map.get(division['ciclo_id'], '')
			if turno_nombre and turno != turno_nombre:
				continue
			if plan_nombre and plan != plan_nombre:
				continue
			if ciclo_nombre and ciclo != ciclo_nombre:
				continue
			datos.append({'id': division['id'], 'Turno': turno, 'Plan': plan, 'Ciclo': ciclo, 'División': division['nombre']})
		datos.sort(key=lambda d: (d['Turno'], d['Plan'], d['Ciclo'], d['División']))
		if hasattr(self, 'tree_divisiones'):
			recargar_treeview(self.tree_divisiones, datos, ['Turno', 'Plan', 'Ciclo', 'División'])
		if hasattr(self, 'label_total_divisiones'):
			self.label_total_divisiones.config(text=f'Total de divisiones: {len(datos)}')
		
		# Actualizar contador de divisiones
		self.label_total_divisiones.config(text=f'Total de divisiones: {len(datos)}')

	# Eliminada: _cargar_divisiones_en_tree (reemplazada por _recargar_divisiones_tree)

	def _agregar_division(self):
		win = tk.Toplevel(self)
		win.configure(bg='#f4f6fa')
		win.title('Agregar División')
		win.geometry('350x300')
		win.minsize(350, 300)
		win.transient(self)
		win.resizable(False, False)
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
		
		ttk.Label(form, text='Ciclo:').grid(row=2, column=0, padx=5, pady=5, sticky='e')
		cb_ciclo = ttk.Combobox(form, values=[], state='disabled', width=25)
		cb_ciclo.grid(row=2, column=1, padx=5, pady=5)
		
		ttk.Label(form, text='División:').grid(row=3, column=0, padx=5, pady=5, sticky='e')
		entry_division = ttk.Entry(form, width=27)
		entry_division.grid(row=3, column=1, padx=5, pady=5)
		
		planes_dict = {}
		ciclos_list = []
		
		def on_turno_selected(event=None):
			turno_nombre = cb_turno.get()
			if not turno_nombre:
				cb_plan['values'] = []
				cb_plan.set('')
				cb_plan.config(state='disabled')
				cb_ciclo['values'] = []
				cb_ciclo.set('')
				cb_ciclo.config(state='disabled')
				return
			turno_id = turnos_dict[turno_nombre]
			planes = obtener_planes_de_turno(turno_id)
			planes_dict.clear()
			planes_dict.update({p['nombre']: p['id'] for p in planes})
			cb_plan['values'] = list(planes_dict.keys())
			cb_plan.set('')
			cb_plan.config(state='readonly' if planes else 'disabled')
			cb_ciclo['values'] = []
			cb_ciclo.set('')
			cb_ciclo.config(state='disabled')
			if planes:
				cb_plan.focus_set()
		
		def on_plan_selected(event=None):
			plan_nombre = cb_plan.get()
			if not plan_nombre:
				cb_ciclo['values'] = []
				cb_ciclo.set('')
				cb_ciclo.config(state='disabled')
				return
			plan_id = planes_dict[plan_nombre]
			ciclos = obtener_ciclos(plan_id)
			ciclos_list.clear()
			ciclos_list.extend(ciclos)
			cb_ciclo['values'] = [a['nombre'] for a in ciclos]
			cb_ciclo.set('')
			cb_ciclo.config(state='readonly' if ciclos else 'disabled')
			if ciclos:
				cb_ciclo.focus_set()
		
		def on_ciclo_selected(event=None):
			entry_division.focus_set()
		
		cb_turno.bind('<<ComboboxSelected>>', on_turno_selected)
		cb_plan.bind('<<ComboboxSelected>>', on_plan_selected)
		cb_ciclo.bind('<<ComboboxSelected>>', on_ciclo_selected)
		
		def guardar(event=None):
			nombre = entry_division.get().strip()
			if not nombre:
				messagebox.showerror('Error', 'Ingrese un nombre de división válido.', parent=win)
				return
			turno_nombre = cb_turno.get()
			plan_nombre = cb_plan.get()
			ciclo_nombre = cb_ciclo.get()
			if not (turno_nombre and plan_nombre and ciclo_nombre):
				messagebox.showerror('Error', 'Seleccione turno, plan y ciclo.', parent=win)
				return
			turno_id = turnos_dict[turno_nombre]
			plan_id = planes_dict[plan_nombre]
			ciclo_id = next((a['id'] for a in ciclos_list if a['nombre'] == ciclo_nombre), None)
			if not ciclo_id:
				messagebox.showerror('Error', 'Ciclo inválido.', parent=win)
				return
			try:
				conn = get_connection()
				c = conn.cursor()
				c.execute('INSERT INTO division (nombre, turno_id, plan_id, ciclo_id) VALUES (?, ?, ?, ?)', 
						  (nombre, turno_id, plan_id, ciclo_id))
				conn.commit()
				conn.close()
				self._recargar_divisiones_tree()
				win.destroy()
			except Exception as e:
				if 'UNIQUE constraint failed' in str(e):
					messagebox.showerror('Error', 'Ya existe una división con ese nombre, turno, plan y ciclo.', parent=win)
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
		win.geometry('350x300')
		win.minsize(350, 300)
		win.transient(self)
		win.resizable(False, False)
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
		
		ttk.Label(form, text='Ciclo:').grid(row=2, column=0, padx=5, pady=5, sticky='e')
		cb_ciclo = ttk.Combobox(form, values=[], state='disabled', width=25)
		cb_ciclo.grid(row=2, column=1, padx=5, pady=5)
		
		ttk.Label(form, text='División:').grid(row=3, column=0, padx=5, pady=5, sticky='e')
		entry_division = ttk.Entry(form, width=27)
		entry_division.grid(row=3, column=1, padx=5, pady=5)
		entry_division.insert(0, division_actual['nombre'])
		
		planes_dict = {}
		ciclos_list = []
		
		def on_turno_selected(event=None):
			turno_nombre = cb_turno.get()
			if not turno_nombre:
				cb_plan['values'] = []
				cb_plan.set('')
				cb_plan.config(state='disabled')
				cb_ciclo['values'] = []
				cb_ciclo.set('')
				cb_ciclo.config(state='disabled')
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
				cb_ciclo['values'] = []
				cb_ciclo.set('')
				cb_ciclo.config(state='disabled')
		
		def on_plan_selected(event=None):
			plan_nombre = cb_plan.get()
			if not plan_nombre:
				cb_ciclo['values'] = []
				cb_ciclo.set('')
				cb_ciclo.config(state='disabled')
				return
			plan_id = planes_dict[plan_nombre]
			ciclos = obtener_ciclos(plan_id)
			ciclos_list.clear()
			ciclos_list.extend(ciclos)
			cb_ciclo['values'] = [a['nombre'] for a in ciclos]
			cb_ciclo.config(state='readonly' if ciclos else 'disabled')
			# Mantener selección si es el mismo plan
			if event is None:
				ciclo_actual = next((a['nombre'] for a in obtener_ciclos(division_actual['plan_id']) if a['id'] == division_actual['ciclo_id']), '')
				if ciclo_actual in [a['nombre'] for a in ciclos]:
					cb_ciclo.set(ciclo_actual)
			else:
				cb_ciclo.set('')
		
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
			ciclo_nombre = cb_ciclo.get()
			if not (turno_nombre and plan_nombre and ciclo_nombre):
				messagebox.showerror('Error', 'Complete todos los campos.', parent=win)
				return
			turno_id = turnos_dict[turno_nombre]
			plan_id = planes_dict[plan_nombre]
			ciclo_id = next((a['id'] for a in ciclos_list if a['nombre'] == ciclo_nombre), None)
			if not ciclo_id:
				messagebox.showerror('Error', 'Ciclo inválido.', parent=win)
				return
			try:
				conn = get_connection()
				c = conn.cursor()
				c.execute('UPDATE division SET nombre=?, turno_id=?, plan_id=?, ciclo_id=? WHERE id=?', 
						  (nombre, turno_id, plan_id, ciclo_id, self.division_seleccionada_id))
				conn.commit()
				conn.close()
				self._recargar_divisiones_tree()
				win.destroy()
			except Exception as e:
				if 'UNIQUE constraint failed' in str(e):
					messagebox.showerror('Error', 'Ya existe una división con ese nombre, turno, plan y ciclo.', parent=win)
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

	def _generar_nombre_archivo(self, prefijo: str) -> str:
		"""Genera un nombre seguro con timestamp para sugerir en el guardado."""
		limpio = ''.join(ch if ch.isalnum() or ch in ('_', '-') else '_' for ch in prefijo.strip()) if prefijo else 'horarios'
		limpio = limpio or 'horarios'
		timestamp = datetime.now().strftime('%Y%m%d_%H%M')
		return f"{limpio}_{timestamp}.xls"

	def _solicitar_ruta_exportacion(self, nombre_sugerido: str) -> Optional[str]:
		return filedialog.asksaveasfilename(
			parent=self,
			title='Guardar horarios como',
			initialfile=nombre_sugerido,
			defaultextension='.xls',
			filetypes=[('Libro Excel 97-2003', '*.xls')]
		)

	def _mostrar_dialogo_seleccion_multiple(self, titulo: str, descripcion: str,
											items: List[Dict[str, Any]], on_confirm) -> None:
		"""Muestra un diálogo genérico para seleccionar múltiples elementos."""
		if not items:
			messagebox.showinfo('Sin datos', 'No hay elementos disponibles para exportar.', parent=self)
			return
		ordenados = sorted(items, key=lambda x: x.get('label', '').lower())
		win = tk.Toplevel(self)
		win.title(titulo)
		win.transient(self)
		win.grab_set()
		win.resizable(False, False)
		frame = ttk.Frame(win, padding=12)
		frame.pack(fill='both', expand=True)
		ttk.Label(frame, text=descripcion, font=('Segoe UI', 10, 'bold')).pack(anchor='w')
		search_var = tk.StringVar()
		filtro_row = ttk.Frame(frame)
		filtro_row.pack(fill='x', pady=(6, 10))
		ttk.Label(filtro_row, text='Filtro:', font=('Segoe UI', 10, 'bold')).pack(side='left', padx=(0, 6))
		search_entry = ttk.Entry(filtro_row, textvariable=search_var)
		search_entry.pack(side='left', fill='x', expand=True)
		list_container = ttk.Frame(frame)
		list_container.pack(fill='both', expand=True)
		listbox = tk.Listbox(list_container, selectmode='multiple', height=14, exportselection=False)
		listbox.pack(side='left', fill='both', expand=True)
		scrollbar = ttk.Scrollbar(list_container, orient='vertical', command=listbox.yview)
		scrollbar.pack(side='right', fill='y')
		listbox.configure(yscrollcommand=scrollbar.set)
		lista_filtrada: List[Dict[str, Any]] = []

		def refrescar_lista(*_):
			filtro = search_var.get().strip().lower()
			listbox.delete(0, tk.END)
			lista_filtrada.clear()
			for item in ordenados:
				etiqueta = item.get('label', '')
				if filtro and filtro not in etiqueta.lower():
					continue
				lista_filtrada.append(item)
				listbox.insert(tk.END, etiqueta)
		refrescar_lista()
		search_var.trace_add('write', refrescar_lista)

		btn_sel = ttk.Frame(frame)
		btn_sel.pack(fill='x', pady=6)
		ttk.Button(btn_sel, text='Seleccionar todo', command=lambda: listbox.select_set(0, tk.END)).pack(side='left', padx=2)
		ttk.Button(btn_sel, text='Limpiar selección', command=lambda: listbox.selection_clear(0, tk.END)).pack(side='left', padx=2)

		acciones = ttk.Frame(frame)
		acciones.pack(fill='x', pady=(6, 0))

		def confirmar():
			indices = listbox.curselection()
			if not indices:
				messagebox.showwarning('Seleccionar', 'Seleccione al menos un elemento.', parent=win)
				return
			if not lista_filtrada:
				messagebox.showwarning('Sin resultados', 'No hay elementos que coincidan con el filtro.', parent=win)
				return
			valores = [lista_filtrada[i]['value'] for i in indices if i < len(lista_filtrada)]
			try:
				cerrar = on_confirm(valores)
			except Exception as exc:
				messagebox.showerror('Error', str(exc), parent=win)
				return
			if cerrar:
				win.destroy()

		ttk.Button(acciones, text='Exportar', command=confirmar).pack(side='left', padx=5)
		ttk.Button(acciones, text='Cancelar', command=win.destroy).pack(side='right', padx=5)
		search_entry.focus_set()

	def _exportar_horario_curso_actual(self):
		if not getattr(self, 'cb_division_horario', None) or not self.cb_division_horario.get():
			messagebox.showwarning('Seleccionar división', 'Seleccione una división antes de exportar.', parent=self)
			return
		division_nombre = self.cb_division_horario.get()
		division_id = self.divisiones_dict_horario.get(division_nombre)
		if division_id is None:
			messagebox.showerror('División inválida', 'La división seleccionada no es válida.', parent=self)
			return
		horarios = obtener_horarios(division_id)
		turno_nombre = self.cb_turno_horario.get() if getattr(self, 'cb_turno_horario', None) else ''
		hoja_nombre = f"{division_nombre} - {turno_nombre}".strip(' -')
		ruta = self._solicitar_ruta_exportacion(self._generar_nombre_archivo(division_nombre))
		if not ruta:
			return
		try:
			destino = exportar_planillas_horario([
				{'nombre': hoja_nombre, 'horarios': horarios, 'construir_texto': _texto_horario_curso}
			], ruta)
		except Exception as exc:
			messagebox.showerror('Error al exportar', str(exc), parent=self)
			return
		messagebox.showinfo('Exportación completada', f'Archivo generado en:\n{destino}', parent=self)

	def _exportar_multiples_cursos(self):
		divisiones = obtener_divisiones()
		if not divisiones:
			messagebox.showinfo('Sin divisiones', 'No hay divisiones registradas para exportar.', parent=self)
			return
		turnos_map = {t['id']: t['nombre'] for t in obtener_turnos()}
		planes_map = {p['id']: p['nombre'] for p in obtener_planes()}
		ciclos_map = {c['id']: c['nombre'] for c in obtener_ciclos_con_planes()}
		items = []
		div_lookup = {d['id']: d for d in divisiones}
		for division in divisiones:
			label = (
				f"{division['nombre']}  |  Turno: {turnos_map.get(division['turno_id'], 'Sin turno')}  |  "
				f"Plan: {planes_map.get(division['plan_id'], 'Sin plan')}  |  "
				f"Ciclo: {ciclos_map.get(division['ciclo_id'], 'Sin ciclo')}"
			)
			items.append({'label': label, 'value': division['id']})

		def on_confirm(ids):
			hojas = []
			for division_id in ids:
				division = div_lookup.get(division_id)
				if not division:
					continue
				horarios = obtener_horarios(division_id)
				turno_nombre = turnos_map.get(division['turno_id'], '')
				hoja_nombre = f"{division['nombre']} - {turno_nombre}".strip(' -')
				hojas.append({'nombre': hoja_nombre, 'horarios': horarios, 'construir_texto': _texto_horario_curso})
			if not hojas:
				messagebox.showwarning('Sin datos', 'Las divisiones seleccionadas no poseen horarios para exportar.', parent=self)
				return False
			ruta = self._solicitar_ruta_exportacion(self._generar_nombre_archivo('cursos'))
			if not ruta:
				return False
			try:
				destino = exportar_planillas_horario(hojas, ruta)
			except Exception as exc:
				messagebox.showerror('Error al exportar', str(exc), parent=self)
				return False
			messagebox.showinfo('Exportación completada', f'Se generó el archivo:\n{destino}', parent=self)
			return True

		self._mostrar_dialogo_seleccion_multiple(
			'Exportar horarios de cursos',
			'Seleccione las divisiones a exportar:',
			items,
			on_confirm
		)

	def _exportar_horario_profesor_actual(self):
		if not getattr(self, 'cb_profesor_horario', None) or not getattr(self, 'cb_turno_horario_prof', None):
			messagebox.showwarning('Seleccionar profesor', 'Seleccione un turno y un profesor antes de exportar.', parent=self)
			return
		profesor_nombre = self.cb_profesor_horario.get()
		turno_nombre = self.cb_turno_horario_prof.get()
		if not profesor_nombre or not turno_nombre:
			messagebox.showwarning('Seleccionar profesor', 'Seleccione un turno y un profesor antes de exportar.', parent=self)
			return
		profesor_id = self.profesores_dict_horario.get(profesor_nombre)
		turno_id = self.turnos_dict_horario_prof.get(turno_nombre)
		if profesor_id is None or turno_id is None:
			messagebox.showerror('Selección inválida', 'La combinación seleccionada no es válida.', parent=self)
			return
		horarios = obtener_horarios_profesor(profesor_id, turno_id)
		hoja_nombre = f"{profesor_nombre} - {turno_nombre}".strip()
		ruta = self._solicitar_ruta_exportacion(self._generar_nombre_archivo(profesor_nombre))
		if not ruta:
			return
		try:
			destino = exportar_planillas_horario([
				{'nombre': hoja_nombre, 'horarios': horarios, 'construir_texto': _texto_horario_profesor}
			], ruta)
		except Exception as exc:
			messagebox.showerror('Error al exportar', str(exc), parent=self)
			return
		messagebox.showinfo('Exportación completada', f'Archivo generado en:\n{destino}', parent=self)

	def _exportar_multiples_profesores(self):
		combinaciones = obtener_profesor_turnos()
		if not combinaciones:
			messagebox.showinfo('Sin profesores', 'No hay profesores con turnos asignados para exportar.', parent=self)
			return
		items = []
		combo_lookup = {}
		for combo in combinaciones:
			clave = (combo['profesor_id'], combo['turno_id'])
			combo_lookup[clave] = combo
			label = f"{combo['profesor']}  |  Turno: {combo['turno']}"
			items.append({'label': label, 'value': clave})

		def on_confirm(selecciones):
			hojas = []
			for clave in selecciones:
				clave_tuple = tuple(clave)
				combo = combo_lookup.get(clave_tuple)
				if not combo:
					continue
				horarios = obtener_horarios_profesor(combo['profesor_id'], combo['turno_id'])
				hoja_nombre = f"{combo['profesor']} - {combo['turno']}"
				hojas.append({'nombre': hoja_nombre, 'horarios': horarios, 'construir_texto': _texto_horario_profesor})
			if not hojas:
				messagebox.showwarning('Sin datos', 'Los profesores seleccionados no poseen horarios registrados.', parent=self)
				return False
			ruta = self._solicitar_ruta_exportacion(self._generar_nombre_archivo('profesores'))
			if not ruta:
				return False
			try:
				destino = exportar_planillas_horario(hojas, ruta)
			except Exception as exc:
				messagebox.showerror('Error al exportar', str(exc), parent=self)
				return False
			messagebox.showinfo('Exportación completada', f'Se generó el archivo:\n{destino}', parent=self)
			return True

		self._mostrar_dialogo_seleccion_multiple(
			'Exportar horarios de profesores',
			'Seleccione los profesores y turnos a exportar:',
			items,
			on_confirm
		)

	def mostrar_horarios_ciclo(self):
		self.limpiar_frame()
		ttk.Label(self.frame_principal, text='Gestión de Horarios por Curso', font=('Arial', 14)).pack(pady=10)

		# Selección paso a paso: Turno → Plan → Ciclo → División
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
		ttk.Label(frame_sel, text='Ciclo:').grid(row=0, column=4, padx=5)
		self.cb_ciclo_horario = ttk.Combobox(frame_sel, values=[], state='disabled')
		self.cb_ciclo_horario.grid(row=0, column=5, padx=5)
		ttk.Label(frame_sel, text='División:').grid(row=0, column=6, padx=5)
		self.cb_division_horario = ttk.Combobox(frame_sel, values=[], state='disabled')
		self.cb_division_horario.grid(row=0, column=7, padx=5)

		def on_turno_selected(event=None):
			turno_nombre = self.cb_turno_horario.get()
			if not turno_nombre:
				self.cb_plan_horario['values'] = []
				self.cb_plan_horario.set('')
				self.cb_plan_horario.config(state='disabled')
				self.cb_ciclo_horario['values'] = []
				self.cb_ciclo_horario.set('')
				self.cb_ciclo_horario.config(state='disabled')
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
			self.cb_ciclo_horario['values'] = []
			self.cb_ciclo_horario.set('')
			self.cb_ciclo_horario.config(state='disabled')
			self.cb_division_horario['values'] = []
			self.cb_division_horario.set('')
			self.cb_division_horario.config(state='disabled')
		def on_plan_selected(event=None):
			plan_nombre = self.cb_plan_horario.get()
			if not plan_nombre:
				self.cb_ciclo_horario['values'] = []
				self.cb_ciclo_horario.set('')
				self.cb_ciclo_horario.config(state='disabled')
				self.cb_division_horario['values'] = []
				self.cb_division_horario.set('')
				self.cb_division_horario.config(state='disabled')
				return
			plan_id = self.planes_dict_horario[plan_nombre]
			ciclos = obtener_ciclos(plan_id)
			self.ciclos_dict_horario = {a['nombre']: a['id'] for a in ciclos}
			ciclo_nombres = list(self.ciclos_dict_horario.keys())
			autocompletar_combobox(self.cb_ciclo_horario, ciclo_nombres, incluir_vacio=False)
			# Enfocar el siguiente combobox
			self.cb_ciclo_horario.focus_set()
			self.cb_division_horario['values'] = []
			self.cb_division_horario.set('')
			self.cb_division_horario.config(state='disabled')
		def on_ciclo_selected(event=None):
			ciclo_nombre = self.cb_ciclo_horario.get()
			if not ciclo_nombre:
				self.cb_division_horario['values'] = []
				self.cb_division_horario.set('')
				self.cb_division_horario.config(state='disabled')
				return
			ciclo_id = self.ciclos_dict_horario[ciclo_nombre]
			# Filtrar divisiones por turno, plan y ciclo
			turno_nombre = self.cb_turno_horario.get()
			plan_nombre = self.cb_plan_horario.get()
			if not (turno_nombre and plan_nombre):
				self.cb_division_horario['values'] = []
				self.cb_division_horario.set('')
				self.cb_division_horario.config(state='disabled')
				return
			turno_id = self.turnos_dict_horario[turno_nombre]
			plan_id = self.planes_dict_horario[plan_nombre]
			divisiones = [c for c in obtener_divisiones() if c['turno_id'] == turno_id and c['plan_id'] == plan_id and c['ciclo_id'] == ciclo_id]
			self.divisiones_dict_horario = {c['nombre']: c['id'] for c in divisiones}
			division_nombres = list(self.divisiones_dict_horario.keys())
			autocompletar_combobox(self.cb_division_horario, division_nombres, incluir_vacio=False)
			# Enfocar el siguiente combobox
			self.cb_division_horario.focus_set()
		def on_division_selected(event=None):
			self._dibujar_grilla_horario_ciclo()
		self.cb_turno_horario.bind('<<ComboboxSelected>>', on_turno_selected)
		self.cb_plan_horario.bind('<<ComboboxSelected>>', on_plan_selected)
		self.cb_ciclo_horario.bind('<<ComboboxSelected>>', on_ciclo_selected)
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

		# Botones inferiores
		frame_bottom_btns = ttk.Frame(self.frame_principal)
		frame_bottom_btns.pack(pady=6, fill='x')
		frame_left = ttk.Frame(frame_bottom_btns)
		frame_left.pack(side='left')
		frame_right = ttk.Frame(frame_bottom_btns)
		frame_right.pack(side='right')
		ttk.Button(frame_left, text='Configurar horas por turno', command=self._configurar_horas_por_turno).pack(side='left', padx=5)
		ttk.Button(frame_left, text='Limpiar horarios vacíos', command=self._limpiar_horarios_vacios_ciclo).pack(side='left', padx=5)
		ttk.Button(frame_right, text='Exportar horario visible', command=self._exportar_horario_curso_actual).pack(side='left', padx=5)
		ttk.Button(frame_right, text='Exportar múltiples cursos', command=self._exportar_multiples_cursos).pack(side='left', padx=5)
		
		# Enfocar el primer combobox al entrar
		self.cb_turno_horario.focus_set()

	def _dibujar_grilla_horario_ciclo(self):
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
								command=lambda d=dia, e=esp: self._editar_espacio_horario_ciclo(d, e))
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

	def _limpiar_horarios_vacios_ciclo(self):
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
			self._dibujar_grilla_horario_ciclo()
		except Exception as e:
			messagebox.showerror('Error', f'Error al limpiar horarios: {str(e)}')

	def _editar_espacio_horario_ciclo(self, dia, espacio):
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

		# Obligación
		ttk.Label(form, text='Obligación:', background='#f4f6fa').grid(row=2, column=0, padx=5, pady=4, sticky='e')
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
				row = cur_tmp.fetchone()
				conn_tmp.close()
				if row:
					default_h = obtener_turno_espacio_hora(row[0], espacio)
					if default_h:
						if not hora_inicio:
							hora_inicio = default_h.get('hora_inicio') or ''
						if not hora_fin:
							hora_fin = default_h.get('hora_fin') or ''
			mid = materia_ids.get(materia) if materia else None
			pid = profesor_ids.get(profesor) if profesor else None
			turno_nombre = self.cb_turno_horario.get()
			if not turno_nombre:
				messagebox.showerror('Error', 'Seleccione el turno del ciclo antes de guardar.')
				return
			turno_id = self.turnos_dict_horario[turno_nombre]
			try:
				crear_horario(division_id, dia, espacio, hora_inicio, hora_fin, mid, pid, turno_id)
				self._dibujar_grilla_horario_ciclo()
				win.destroy()
			except Exception as e:
				messagebox.showerror('Error', str(e))

		def eliminar_espacio(event=None):
			if h_existente:
				if messagebox.askyesno('Confirmar', '¿Eliminar asignación de este espacio?'):
					try:
						eliminar_horario(h_existente['id'])
						self._dibujar_grilla_horario_ciclo()
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

		# Botones inferiores
		frame_bottom_btns = ttk.Frame(self.frame_principal)
		frame_bottom_btns.pack(pady=6, fill='x')
		frame_left = ttk.Frame(frame_bottom_btns)
		frame_left.pack(side='left')
		frame_right = ttk.Frame(frame_bottom_btns)
		frame_right.pack(side='right')
		ttk.Button(frame_left, text='Configurar horas por turno', command=self._configurar_horas_por_turno).pack(side='left', padx=5)
		ttk.Button(frame_left, text='Limpiar horarios vacíos', command=self._limpiar_horarios_vacios_profesor).pack(side='left', padx=5)
		ttk.Button(frame_right, text='Exportar horario visible', command=self._exportar_horario_profesor_actual).pack(side='left', padx=5)
		ttk.Button(frame_right, text='Exportar múltiples profesores', command=self._exportar_multiples_profesores).pack(side='left', padx=5)
		
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
		# Encabezados - igual que en vista por ciclo
		# Celda vacía en esquina superior izquierda
		ttk.Label(self.frame_grilla_horario_prof, text='', font=('Segoe UI', 10, 'bold'), background='#f4f6fa').grid(row=0, column=0, padx=(0,0), pady=2, sticky='nsew')
		# Días de la semana
		for col, dia in enumerate(dias, start=1):
			ttk.Label(self.frame_grilla_horario_prof, text=dia, font=('Segoe UI', 10, 'bold'), background='#e0e7ef', foreground='#2a3a4a').grid(row=0, column=col, padx=(0,0), pady=2, sticky='nsew')

		# Configuración de columnas igual que en vista por ciclo
		self.frame_grilla_horario_prof.columnconfigure(0, weight=0, minsize=52)
		for c in range(1, 6):
			self.frame_grilla_horario_prof.columnconfigure(c, weight=1, minsize=150)

		self._grilla_botones_prof = []
		for esp in range(1, self.espacios_por_dia_prof + 1):
			# Etiqueta igual que en vista por ciclo
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
		
		# Ventana de edición - estilo similar a por ciclo
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

		# Obligación - Obtener solo las obligaciones que tiene asignadas el profesor
		ttk.Label(form, text='Obligación:', background='#f4f6fa').grid(row=2, column=0, padx=5, pady=4, sticky='e')
		banca = obtener_banca_profesor(profesor_id)
		materia_nombres = [b['materia'] for b in banca]
		
		# Necesitamos obtener los IDs de las obligaciones
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
		
		# Ciclo (se actualiza al seleccionar plan)
		ttk.Label(form, text='Ciclo:', background='#f4f6fa').grid(row=4, column=0, padx=5, pady=4, sticky='e')
		cb_ciclo = ttk.Combobox(form, values=[], state='disabled')
		cb_ciclo.grid(row=4, column=1, padx=5, pady=4, sticky='w')
		ciclos_dict = {}

		# División (se actualiza al seleccionar ciclo)
		ttk.Label(form, text='División:', background='#f4f6fa').grid(row=5, column=0, padx=5, pady=4, sticky='e')
		cb_division = ttk.Combobox(form, values=[], state='disabled')
		cb_division.grid(row=5, column=1, padx=5, pady=4, sticky='w')
		division_ids = {}
		
		def on_plan_selected(event=None):
			nonlocal ciclos_dict
			plan_nombre = cb_plan.get()
			if not plan_nombre:
				cb_ciclo['values'] = []
				cb_ciclo.set('')
				cb_ciclo.config(state='disabled')
				cb_division['values'] = []
				cb_division.set('')
				cb_division.config(state='disabled')
				return
			
			plan_id = plan_ids[plan_nombre]
			ciclos = obtener_ciclos(plan_id)
			ciclos_list = [a['nombre'] for a in ciclos]
			ciclos_dict = {a['nombre']: a['id'] for a in ciclos}
			
			# Autocompletar ciclo si solo hay uno
			if autocompletar_combobox(cb_ciclo, ciclos_list, incluir_vacio=True):
				on_ciclo_selected()  # Trigger automático si se autocompletó
		
		def on_ciclo_selected(event=None):
			nonlocal division_ids
			ciclo_nombre = cb_ciclo.get()
			if not ciclo_nombre:
				cb_division['values'] = []
				cb_division.set('')
				cb_division.config(state='disabled')
				return
			
			plan_nombre = cb_plan.get()
			if not plan_nombre:
				return
			
			ciclo_id = ciclos_dict[ciclo_nombre]
			plan_id = plan_ids[plan_nombre]
			
			# Obtener divisiones del turno, plan y ciclo seleccionados
			divisiones = obtener_divisiones()
			divisiones_filtradas = [d for d in divisiones 
								  if d['turno_id'] == turno_id 
								  and d['plan_id'] == plan_id
								  and d['ciclo_id'] == ciclo_id]
			division_nombres = [d['nombre'] for d in divisiones_filtradas]
			division_ids = {d['nombre']: d['id'] for d in divisiones_filtradas}
			
			# Autocompletar división si solo hay una
			autocompletar_combobox(cb_division, division_nombres, incluir_vacio=True)
		
		cb_plan.bind('<<ComboboxSelected>>', on_plan_selected)
		cb_ciclo.bind('<<ComboboxSelected>>', on_ciclo_selected)
		
		# Configurar plan inicial y autocompletar si solo hay uno
		if autocompletar_combobox(cb_plan, plan_nombres, incluir_vacio=True):
			on_plan_selected()  # Trigger automático si se autocompletó

		# Cargar datos existentes
		if h_existente:
			entry_inicio.insert(0, h_existente['hora_inicio'] or '')
			entry_fin.insert(0, h_existente['hora_fin'] or '')
			cb_materia.set(h_existente['materia'] or '')
			
			# Cargar plan, ciclo y división si existen
			if h_existente['division']:
				# Buscar el plan, ciclo y división
				divisiones = obtener_divisiones()
				div_encontrada = next((d for d in divisiones if d['nombre'] == h_existente['division']), None)
				if div_encontrada:
					# Encontrar el plan
					plan_encontrado = next((p for p in plan_nombres if plan_ids[p] == div_encontrada['plan_id']), None)
					if plan_encontrado:
						cb_plan.set(plan_encontrado)
						on_plan_selected()  # Actualizar ciclos
						# Encontrar el ciclo
						ciclos_disponibles = obtener_ciclos(div_encontrada['plan_id'])
						ciclo_encontrado = next((a['nombre'] for a in ciclos_disponibles if a['id'] == div_encontrada['ciclo_id']), None)
						if ciclo_encontrado:
							cb_ciclo.set(ciclo_encontrado)
							on_ciclo_selected()  # Actualizar divisiones
							cb_division.set(h_existente['division'])

		def guardar(event=None):
			hora_inicio = entry_inicio.get().strip()
			hora_fin = entry_fin.get().strip()
			division = cb_division.get().strip()
			materia = cb_materia.get().strip()
			plan_nombre_sel = cb_plan.get().strip()
			ciclo_nombre_sel = cb_ciclo.get().strip()

			if not plan_nombre_sel:
				messagebox.showerror('Error', 'Seleccione el plan de estudios para poder asignar el ciclo.')
				return
			if not ciclo_nombre_sel:
				messagebox.showerror('Error', 'Seleccione el ciclo lectivo antes de guardar.')
				return
			if not division:
				messagebox.showerror('Error', 'Seleccione la división del ciclo para sincronizar el horario con la vista por ciclo.')
				return
			if not materia:
				messagebox.showerror('Error', 'Seleccione la materia dictada por el profesor.')
				return

			try:
				div_id = division_ids.get(division)
				if div_id is None:
					messagebox.showerror('Error', 'La división seleccionada no pertenece al turno/plan elegido.')
					return
				mat_id = materia_ids.get(materia)
				if mat_id is None:
					messagebox.showerror('Error', 'La materia seleccionada no es válida.')
					return
				crear_horario_profesor(profesor_id, turno_id, dia, espacio, hora_inicio, hora_fin, div_id, mat_id)
				self._dibujar_grilla_horario_profesor()
				win.destroy()
			except Exception as e:
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
				# y NO solo cb_turno_horario (que es de vista ciclo)
				en_vista_profesor = (hasattr(self, 'cb_turno_horario_prof') and 
									hasattr(self, 'cb_profesor_horario') and 
									hasattr(self, 'profesores_dict_horario') and 
									self.cb_turno_horario_prof.winfo_exists() and
									self.cb_profesor_horario.get() and 
									self.cb_profesor_horario.get() in self.profesores_dict_horario)
				
				# Verificar si estamos en la vista de horarios por ciclo con una división seleccionada
				en_vista_ciclo = (hasattr(self, 'cb_turno_horario') and 
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
					
					elif en_vista_ciclo:
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
					elif en_vista_ciclo:
						# Aplicar a todas las divisiones del turno (vista por ciclo)
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
				self._dibujar_grilla_horario_ciclo()
			
			messagebox.showinfo('OK', 'Valores guardados.')
			win.destroy()

		btns = ttk.Frame(frame)
		btns.grid(row=11, column=0, columnspan=5, pady=15)
		ttk.Button(btns, text='Guardar', command=guardar, width=12).pack(side='left', padx=5)
		ttk.Button(btns, text='Cancelar', command=win.destroy, width=12).pack(side='left', padx=5)

	def mostrar_turnos_planes_materias(self):
		"""Ventana unificada con tabs para Turnos, Planes de Estudio y Materias"""
		self.limpiar_frame()
		ttk.Label(self.frame_principal, text='Gestión de Turnos, Planes y Materias', font=('Arial', 14)).pack(pady=10)
		
		# Crear notebook (tabs)
		notebook = ttk.Notebook(self.frame_principal)
		notebook.pack(fill='both', expand=True, padx=10, pady=5)
		
		# Tab 1: Turnos
		tab_turnos = ttk.Frame(notebook)
		notebook.add(tab_turnos, text='Turnos')
		
		# Tab 2: Planes de Estudio
		tab_planes = ttk.Frame(notebook)
		notebook.add(tab_planes, text='Planes de Estudio')
		
		# Tab 3: Materias/Obligaciones
		tab_materias = ttk.Frame(notebook)
		notebook.add(tab_materias, text='Materias/Obligaciones')
		
		# ===== CONTENIDO TAB TURNOS =====
		self._crear_tab_turnos(tab_turnos)
		
		# ===== CONTENIDO TAB PLANES =====
		self._crear_tab_planes(tab_planes)
		
		# ===== CONTENIDO TAB MATERIAS =====
		self._crear_tab_materias(tab_materias)
	
	# Alias para compatibilidad
	def mostrar_turnos_y_planes(self):
		"""Alias para mantener compatibilidad"""
		self.mostrar_turnos_planes_materias()
	
	def _crear_tab_turnos(self, parent):
		"""Crea el contenido del tab de Turnos"""
		# Frame principal con aside y tabla
		frame_principal = ttk.Frame(parent)
		frame_principal.pack(fill='both', expand=True)
		
		# Aside izquierdo para acciones
		frame_aside = ttk.Frame(frame_principal, width=250)
		frame_aside.pack(side='left', fill='y', padx=(10, 5), pady=10)
		frame_aside.pack_propagate(False)
		
		ttk.Label(frame_aside, text='Acciones', font=('Segoe UI', 11, 'bold')).pack(pady=(0, 10))
		
		# Formulario
		form = ttk.Frame(frame_aside)
		form.pack(pady=(0, 10), fill='x')
		ttk.Label(form, text='Nombre del turno:').grid(row=0, column=0, padx=5, pady=2, sticky='w')
		self.entry_nombre_turno = ttk.Entry(form, width=23)
		self.entry_nombre_turno.grid(row=1, column=0, padx=5, pady=2, sticky='ew')
		def _clear_turno_entry():
			self.entry_nombre_turno.delete(0, tk.END)
			self.entry_nombre_turno.focus_set()
		ttk.Button(form, text='🧹', width=3, command=_clear_turno_entry).grid(row=1, column=1, padx=(2, 5), pady=2)
		form.grid_columnconfigure(0, weight=1)
		
		# Botones
		btns = ttk.Frame(frame_aside)
		btns.pack(pady=(0, 10), fill='x')
		ttk.Button(btns, text='Agregar Turno', command=self._agregar_turno).pack(fill='x', pady=2)
		ttk.Button(btns, text='Eliminar Turno', command=self._eliminar_turno).pack(fill='x', pady=2)
		ttk.Button(btns, text='Ver Planes del Turno', command=self._gestionar_planes_turno).pack(fill='x', pady=2)
		
		# Tabla derecha
		frame_tabla = ttk.Frame(frame_principal)
		frame_tabla.pack(side='right', fill='both', expand=True, padx=(5, 10), pady=10)
		column_config = {'Nombre': {'width': 200, 'anchor': 'center'}}
		self.tree_turnos = crear_treeview(frame_tabla, ('Nombre',), ('Nombre',), column_config=column_config)
		self._recargar_turnos_tree()

		# Selección en tabla
		self.tree_turnos.bind('<<TreeviewSelect>>', self._on_select_turno)
		self.turno_seleccionado_id = None
	
	def _crear_tab_planes(self, parent):
		"""Crea el contenido del tab de Planes de Estudio"""
		# Frame principal con aside y tabla
		frame_principal = ttk.Frame(parent)
		frame_principal.pack(fill='both', expand=True)
		
		# Aside izquierdo para acciones
		frame_aside = ttk.Frame(frame_principal, width=250)
		frame_aside.pack(side='left', fill='y', padx=(10, 5), pady=10)
		frame_aside.pack_propagate(False)
		
		ttk.Label(frame_aside, text='Acciones', font=('Segoe UI', 11, 'bold')).pack(pady=(0, 10))
		
		# Botones
		btns = ttk.Frame(frame_aside)
		btns.pack(fill='x')
		ttk.Button(btns, text='Crear Plan', command=self._crear_plan_con_turnos).pack(fill='x', pady=2)
		ttk.Button(btns, text='Editar Plan y Turnos', command=self._editar_plan_con_turnos).pack(fill='x', pady=2)
		ttk.Button(btns, text='Eliminar Plan', command=self._eliminar_plan).pack(fill='x', pady=2)
		ttk.Button(btns, text='Ver Obligaciones del Plan', command=self._gestionar_materias_plan).pack(fill='x', pady=2)
		
		# Tabla derecha
		frame_tabla = ttk.Frame(frame_principal)
		frame_tabla.pack(side='right', fill='both', expand=True, padx=(5, 10), pady=10)
		column_config = {'Nombre': {'width': 350, 'anchor': 'w'}, 'Turnos': {'width': 150, 'anchor': 'w'}}
		self.tree_planes = crear_treeview(frame_tabla, ('Nombre', 'Turnos'), ('Nombre del Plan', 'Turnos Asignados'), column_config=column_config)
		
		self._recargar_planes_con_turnos_tree()

		# Selección en tabla
		self.tree_planes.bind('<<TreeviewSelect>>', self._on_select_plan)
		self.plan_seleccionado_id = None
	
	def _recargar_planes_con_turnos_tree(self):
		"""Recarga el árbol de planes mostrando los turnos asignados"""
		for row in self.tree_planes.get_children():
			self.tree_planes.delete(row)
		
		planes = sorted(obtener_planes(), key=lambda p: p['nombre'].lower())
		for plan in planes:
			# Obtener turnos del plan
			turnos_plan = obtener_turnos_de_plan(plan['id'])
			turnos_str = ', '.join([t['nombre'] for t in turnos_plan]) if turnos_plan else '(sin turnos)'
			
			self.tree_planes.insert('', 'end', iid=plan['id'], 
								   values=(plan['nombre'], turnos_str))
	
	def _crear_tab_materias(self, parent):
		"""Crea el contenido del tab de Materias/Obligaciones con selección múltiple"""
		# Totales
		materias = obtener_materias()
		total_materias = len(materias)
		total_horas = sum(m['horas_semanales'] for m in materias)
		frame_tot = ttk.Frame(parent)
		frame_tot.pack(pady=5)
		ttk.Label(frame_tot, text=f'Total de materias/obligaciones: {total_materias}').grid(row=0, column=0, padx=10)
		ttk.Label(frame_tot, text=f'Total de horas institucionales: {total_horas}').grid(row=0, column=1, padx=10)

		# Frame de controles (solo Filtro)
		frame_controles = ttk.Frame(parent)
		frame_controles.pack(pady=5)
		
		# Filtro
		ttk.Label(frame_controles, text='Filtro:').grid(row=0, column=0, padx=5)
		self.filtro_materia = tk.StringVar()
		entry_filtro_frame = ttk.Frame(frame_controles)
		entry_filtro_frame.grid(row=0, column=1, padx=5)
		entry_filtro = ttk.Entry(entry_filtro_frame, textvariable=self.filtro_materia, width=26)
		entry_filtro.pack(side='left')
		def _clear_filtro_materia():
			self.filtro_materia.set('')
			entry_filtro.focus_set()
		ttk.Button(entry_filtro_frame, text='🧹', width=3, command=_clear_filtro_materia).pack(side='left', padx=(5, 0))

		# Frame principal con aside y tabla
		frame_principal = ttk.Frame(parent)
		frame_principal.pack(fill='both', expand=True)
		
		# Aside izquierdo para acciones
		frame_aside = ttk.Frame(frame_principal, width=250)
		frame_aside.pack(side='left', fill='y', padx=(10, 5), pady=10)
		frame_aside.pack_propagate(False)
		
		ttk.Label(frame_aside, text='Acciones', font=('Segoe UI', 11, 'bold')).pack(pady=(0, 10))
		
		# Formulario de alta
		form = ttk.Frame(frame_aside)
		form.pack(pady=(0, 10), fill='x')
		ttk.Label(form, text='Nueva Materia:').grid(row=0, column=0, padx=5, pady=2, sticky='w')
		self.entry_nombre_materia_tab = ttk.Entry(form, width=23)
		self.entry_nombre_materia_tab.grid(row=1, column=0, padx=5, pady=2, sticky='ew')
		def _clear_materia_entry():
			self.entry_nombre_materia_tab.delete(0, tk.END)
			self.entry_nombre_materia_tab.focus_set()
		ttk.Button(form, text='🧹', width=3, command=_clear_materia_entry).grid(row=1, column=1, padx=(2, 5), pady=2)
		form.grid_columnconfigure(0, weight=1)

		# Botones
		btns = ttk.Frame(frame_aside)
		btns.pack(fill='x')
		ttk.Button(btns, text='Agregar', command=self._agregar_materia_tab).pack(fill='x', pady=2)
		ttk.Button(btns, text='Editar', command=self._editar_materia_tab).pack(fill='x', pady=2)
		ttk.Button(btns, text='Eliminar', command=self._eliminar_materias_tab).pack(fill='x', pady=2)
		ttk.Button(btns, text='Asignar a Plan de Estudio', command=self._asignar_materias_seleccionadas_a_plan).pack(fill='x', pady=2)
		
		# Tabla derecha
		frame_tabla = ttk.Frame(frame_principal)
		frame_tabla.pack(side='right', fill='both', expand=True, padx=(5, 10), pady=10)
		
		# Configurar treeview con columnas adicionales para checkboxes visuales
		self.tree_materias_tab = ttk.Treeview(frame_tabla, columns=('Sel', 'Nombre', 'Horas'), 
											  show='headings', height=3, selectmode='none')
		self.tree_materias_tab.heading('Sel', text='☐')
		self.tree_materias_tab.heading('Nombre', text='Nombre')
		self.tree_materias_tab.heading('Horas', text='Horas asignadas')
		
		# Configurar anchos de columna
		self.tree_materias_tab.column('Sel', width=5, anchor='center')
		self.tree_materias_tab.column('Nombre', width=345, anchor='center')
		self.tree_materias_tab.column('Horas', width=100, anchor='center')
		
		vsb = ttk.Scrollbar(frame_tabla, orient='vertical', command=self.tree_materias_tab.yview)
		hsb = ttk.Scrollbar(frame_tabla, orient='horizontal', command=self.tree_materias_tab.xview)
		self.tree_materias_tab.configure(yscroll=vsb.set, xscroll=hsb.set)
		
		self.tree_materias_tab.grid(row=0, column=0, sticky='nsew')
		vsb.grid(row=0, column=1, sticky='ns')
		hsb.grid(row=1, column=0, sticky='ew')
		frame_tabla.grid_rowconfigure(0, weight=1)
		frame_tabla.grid_columnconfigure(0, weight=1)
		
		# Set para rastrear materias seleccionadas
		self.materias_seleccionadas = set()
		
		# Binding para click simple (seleccionar/deseleccionar)
		self.tree_materias_tab.bind('<Button-1>', self._on_click_materias_tab)
		
		self._recargar_materias_tab()

		# Filtro en tiempo real
		def filtrar_materias(*args):
			filtro = self.filtro_materia.get().lower()
			materias_filtradas = [m for m in obtener_materias() if filtro in m['nombre'].lower()]
			self._recargar_materias_tab(materias_filtradas)
		self.filtro_materia.trace_add('write', filtrar_materias)
	
	def _recargar_materias_tab(self, materias=None):
		"""Recarga la tabla de materias manteniendo las selecciones"""
		if materias is None:
			materias = obtener_materias()
		
		# Limpiar tabla
		for row in self.tree_materias_tab.get_children():
			self.tree_materias_tab.delete(row)
		
		# Ordenar alfabéticamente
		materias_ordenadas = sorted(materias, key=lambda m: m['nombre'].lower())
		
		# Insertar materias con indicador de selección
		for materia in materias_ordenadas:
			seleccionado = '☑' if materia['id'] in self.materias_seleccionadas else '☐'
			self.tree_materias_tab.insert('', 'end', iid=materia['id'], 
										 values=(seleccionado, materia['nombre'], materia['horas_semanales']))
		
		# Actualizar heading según el estado
		self._actualizar_heading_seleccion()
	
	def _on_click_materias_tab(self, event):
		"""Maneja clicks en items o en el heading"""
		region = self.tree_materias_tab.identify('region', event.x, event.y)
		
		# Si es click en heading
		if region == 'heading':
			column = self.tree_materias_tab.identify_column(event.x)
			# Solo responder si es la primera columna (columna de checkboxes)
			if column == '#1':
				self._seleccionar_todas_materias()
			return
		
		# Si es click en item/cell
		if region != 'cell' and region != 'tree':
			return
		
		item = self.tree_materias_tab.identify_row(event.y)
		if not item:
			return
		
		materia_id = int(item)
		
		# Alternar selección
		if materia_id in self.materias_seleccionadas:
			self.materias_seleccionadas.remove(materia_id)
		else:
			self.materias_seleccionadas.add(materia_id)
		
		# Actualizar visualización
		valores = self.tree_materias_tab.item(item, 'values')
		nuevo_check = '☑' if materia_id in self.materias_seleccionadas else '☐'
		self.tree_materias_tab.item(item, values=(nuevo_check, valores[1], valores[2]))
		
		# Actualizar heading
		self._actualizar_heading_seleccion()
	
	def _actualizar_heading_seleccion(self):
		"""Actualiza el heading de la columna de selección según el estado"""
		items = self.tree_materias_tab.get_children()
		
		if not items:
			self.tree_materias_tab.heading('Sel', text='☐')
			return
		
		# Si todas están seleccionadas, mostrar ☑, sino ☐
		todas_seleccionadas = all(int(item) in self.materias_seleccionadas for item in items)
		self.tree_materias_tab.heading('Sel', text='☑' if todas_seleccionadas else '☐')
	
	def _seleccionar_todas_materias(self):
		"""Selecciona o deselecciona todas las materias visibles"""
		items = self.tree_materias_tab.get_children()
		
		if not items:
			return
		
		# Si todas están seleccionadas, deseleccionar todas
		todas_seleccionadas = all(int(item) in self.materias_seleccionadas for item in items)
		
		if todas_seleccionadas:
			# Deseleccionar todas
			for item in items:
				materia_id = int(item)
				if materia_id in self.materias_seleccionadas:
					self.materias_seleccionadas.remove(materia_id)
		else:
			# Seleccionar todas
			for item in items:
				materia_id = int(item)
				self.materias_seleccionadas.add(materia_id)
		
		# Actualizar visualización
		self._recargar_materias_tab()
	
	def _agregar_materia_tab(self):
		"""Agregar nueva materia desde el tab"""
		nombre = self.entry_nombre_materia_tab.get().strip()
		if not nombre:
			messagebox.showerror('Error', 'Ingrese un nombre válido.')
			return
		try:
			crear_materia(nombre, 0)
			self._recargar_materias_tab()
			self.entry_nombre_materia_tab.delete(0, tk.END)
		except Exception as e:
			messagebox.showerror('Error', str(e))
	
	def _editar_materia_tab(self):
		"""Editar materia - solo si hay UNA seleccionada"""
		if len(self.materias_seleccionadas) == 0:
			messagebox.showwarning('Atención', 'Seleccione una materia para editar.')
			return
		
		if len(self.materias_seleccionadas) > 1:
			messagebox.showerror('Error', 'No se puede editar más de una materia a la vez.')
			return
		
		materia_id = list(self.materias_seleccionadas)[0]
		materias = obtener_materias()
		materia = next((m for m in materias if m['id'] == materia_id), None)
		
		if not materia:
			return
		
		# Ventana de edición
		win = tk.Toplevel(self)
		win.configure(bg='#f4f6fa')
		win.title('Editar Materia')
		win.geometry('400x150')
		win.transient(self)
		win.resizable(False, False)
		win.grab_set()
		win.focus_force()
		
		ttk.Label(win, text='Editar Materia', font=('Arial', 12, 'bold')).pack(pady=10)
		
		frame = ttk.Frame(win)
		frame.pack(pady=10)
		ttk.Label(frame, text='Nombre:').grid(row=0, column=0, padx=5, pady=5)
		entry_nombre = ttk.Entry(frame, width=30)
		entry_nombre.insert(0, materia['nombre'])
		entry_nombre.grid(row=0, column=1, padx=5, pady=5)
		entry_nombre.focus_set()
		
		def guardar():
			nuevo_nombre = entry_nombre.get().strip()
			if not nuevo_nombre:
				messagebox.showerror('Error', 'Ingrese un nombre válido.', parent=win)
				return
			try:
				actualizar_materia(materia_id, nuevo_nombre, materia['horas_semanales'])
				self._recargar_materias_tab()
				win.destroy()
			except Exception as e:
				messagebox.showerror('Error', str(e), parent=win)
		
		frame_btns = ttk.Frame(win)
		frame_btns.pack(pady=10)
		ttk.Button(frame_btns, text='Guardar', command=guardar).grid(row=0, column=0, padx=5)
		ttk.Button(frame_btns, text='Cancelar', command=win.destroy).grid(row=0, column=1, padx=5)
		
		entry_nombre.bind('<Return>', lambda e: guardar())
	
	def _eliminar_materias_tab(self):
		"""Eliminar materias seleccionadas (permite múltiples)"""
		if len(self.materias_seleccionadas) == 0:
			messagebox.showwarning('Atención', 'Seleccione al menos una materia para eliminar.')
			return
		
		cantidad = len(self.materias_seleccionadas)
		mensaje = f'¿Está seguro de eliminar {cantidad} materia(s) seleccionada(s)?'
		
		if not messagebox.askyesno('Confirmar', mensaje):
			return
		
		try:
			for materia_id in list(self.materias_seleccionadas):
				eliminar_materia(materia_id)
			
			self.materias_seleccionadas.clear()
			self._recargar_materias_tab()
			messagebox.showinfo('Éxito', f'Se eliminaron {cantidad} materia(s).')
		except Exception as e:
			messagebox.showerror('Error', str(e))
	
	def _asignar_materias_seleccionadas_a_plan(self):
		"""Asignar materias seleccionadas a un plan (versión simplificada)"""
		if len(self.materias_seleccionadas) == 0:
			messagebox.showwarning('Atención', 'Seleccione al menos una materia para asignar.')
			return
		
		planes = obtener_planes()
		if not planes:
			messagebox.showinfo('Información', 'No hay planes de estudio creados.\nPor favor, cree al menos un plan primero.')
			return
		
		# Ventana simple con solo selector de plan
		win = tk.Toplevel(self)
		win.configure(bg='#f4f6fa')
		win.title('Asignar Materias a Plan')
		win.geometry('450x250')
		win.transient(self)
		win.resizable(False, False)
		win.grab_set()
		win.focus_force()
		
		ttk.Label(win, text='Asignar Materias a Plan de Estudio', font=('Arial', 12, 'bold')).pack(pady=15)
		
		# Mensaje informativo
		cantidad = len(self.materias_seleccionadas)
		ttk.Label(win, text=f'{cantidad} materia(s) seleccionada(s)', 
				 font=('Segoe UI', 10), foreground='#555').pack(pady=5)
		
		# Selector de plan
		frame_plan = ttk.Frame(win)
		frame_plan.pack(pady=15)
		ttk.Label(frame_plan, text='Plan de Estudio:').grid(row=0, column=0, padx=5)
		
		plan_nombres = [p['nombre'] for p in sorted(planes, key=lambda x: x['nombre'].lower())]
		plan_ids = {p['nombre']: p['id'] for p in planes}
		
		cb_plan = ttk.Combobox(frame_plan, values=plan_nombres, state='readonly', width=30)
		cb_plan.grid(row=0, column=1, padx=5)
		cb_plan.focus_set()
		
		def asignar():
			plan_nombre = cb_plan.get()
			if not plan_nombre:
				messagebox.showerror('Error', 'Seleccione un plan de estudio.', parent=win)
				return
			
			plan_id = plan_ids[plan_nombre]
			
			# Verificar cuáles ya están asignadas
			materias_plan = obtener_materias_de_plan(plan_id)
			materias_plan_ids = [m['id'] for m in materias_plan]
			
			asignadas = 0
			ya_asignadas = 0
			
			try:
				for materia_id in self.materias_seleccionadas:
					if materia_id in materias_plan_ids:
						ya_asignadas += 1
					else:
						agregar_materia_a_plan(plan_id, materia_id)
						asignadas += 1
				
				mensaje = f'Se asignaron {asignadas} materia(s) al plan "{plan_nombre}".'
				if ya_asignadas > 0:
					mensaje += f'\n({ya_asignadas} ya estaban asignadas)'
				
				messagebox.showinfo('Éxito', mensaje, parent=win)
				win.destroy()
				
			except Exception as e:
				messagebox.showerror('Error', str(e), parent=win)
		
		# Botones
		frame_btns = ttk.Frame(win)
		frame_btns.pack(pady=15)
		ttk.Button(frame_btns, text='Asignar', command=asignar, width=15).grid(row=0, column=0, padx=5)
		ttk.Button(frame_btns, text='Cancelar', command=win.destroy, width=15).grid(row=0, column=1, padx=5)

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
		ttk.Button(btns, text='Materias/Obligaciones del plan', command=self._gestionar_materias_plan).grid(row=0, column=2, padx=5)
		ttk.Button(btns, text='Ciclos del plan', command=self._gestionar_ciclos_plan).grid(row=0, column=3, padx=5)
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
			self._recargar_planes_tree()
			self.entry_nombre_plan.delete(0, tk.END)
		except Exception as e:
			messagebox.showerror('Error', str(e))

	def _eliminar_plan(self):
		if not self.plan_seleccionado_id:
			messagebox.showerror('Error', 'Seleccione un plan.')
			return
		try:
			eliminar_plan(self.plan_seleccionado_id)
			# Si estamos en la vista unificada, recargar con turnos
			if hasattr(self, 'tree_planes') and hasattr(self.tree_planes, 'column') and 'Turnos' in str(self.tree_planes['columns']):
				self._recargar_planes_con_turnos_tree()
			else:
				self._recargar_planes_tree()
			self.plan_seleccionado_id = None
		except Exception as e:
			messagebox.showerror('Error', str(e))

	def _on_select_plan(self, event):
		sel = self.tree_planes.selection()
		if sel:
			self.plan_seleccionado_id = int(sel[0])
		else:
			self.plan_seleccionado_id = None
	
	def _crear_plan_con_turnos(self):
		"""Ventana para crear un plan de estudio y asignarle turnos"""
		win = tk.Toplevel(self)
		win.configure(bg='#f4f6fa')
		win.title('Crear Plan de Estudio')
		win.geometry('450x400')
		win.minsize(450, 400)
		win.transient(self)
		win.resizable(False, False)
		win.grab_set()
		win.focus_force()
		
		ttk.Label(win, text='Nuevo Plan de Estudio', font=('Arial', 12, 'bold')).pack(pady=10)
		
		# Nombre del plan
		frame_nombre = ttk.Frame(win)
		frame_nombre.pack(pady=10, padx=20, fill='x')
		ttk.Label(frame_nombre, text='Nombre del Plan:', font=('Segoe UI', 10)).pack(anchor='w', pady=(0, 5))
		entry_nombre = ttk.Entry(frame_nombre, width=40)
		entry_nombre.pack(fill='x')
		entry_nombre.focus_set()
		
		# Selección de turnos
		frame_turnos = ttk.Frame(win)
		frame_turnos.pack(pady=10, padx=20, fill='both', expand=True)
		ttk.Label(frame_turnos, text='Asignar a los siguientes turnos:', font=('Segoe UI', 10)).pack(anchor='w', pady=(0, 5))
		
		# Frame con scrollbar para checkboxes
		canvas_frame = ttk.Frame(frame_turnos)
		canvas_frame.pack(fill='both', expand=True)
		
		canvas = tk.Canvas(canvas_frame, bg='#f4f6fa', highlightthickness=0, height=150)
		scrollbar = ttk.Scrollbar(canvas_frame, orient='vertical', command=canvas.yview)
		scrollable_frame = ttk.Frame(canvas)
		
		scrollable_frame.bind(
			"<Configure>",
			lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
		)
		
		canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
		canvas.configure(yscrollcommand=scrollbar.set)
		
		canvas.pack(side='left', fill='both', expand=True)
		scrollbar.pack(side='right', fill='y')
		
		# Crear checkboxes para cada turno
		turnos = obtener_turnos()
		turnos_vars = {}
		for turno in turnos:
			var = tk.IntVar(value=0)
			chk = ttk.Checkbutton(scrollable_frame, text=turno['nombre'], variable=var)
			chk.pack(anchor='w', pady=2, padx=5)
			turnos_vars[turno['id']] = var
		
		if not turnos:
			ttk.Label(scrollable_frame, text='(No hay turnos creados)', foreground='gray').pack(pady=10)
		
		# Botones
		frame_btns = ttk.Frame(win)
		frame_btns.pack(pady=15)
		
		def guardar():
			nombre = entry_nombre.get().strip()
			if not nombre:
				messagebox.showerror('Error', 'Ingrese un nombre para el plan.', parent=win)
				return
			
			# Verificar que al menos un turno esté seleccionado
			turnos_seleccionados = [tid for tid, var in turnos_vars.items() if var.get() == 1]
			if not turnos_seleccionados:
				messagebox.showerror('Error', 'Debe seleccionar al menos un turno.', parent=win)
				return
			
			try:
				# Crear el plan
				crear_plan(nombre)
				
				# Obtener el ID del plan recién creado
				planes = obtener_planes()
				plan_id = next(p['id'] for p in planes if p['nombre'] == nombre)
				
				# Asignar turnos
				for turno_id in turnos_seleccionados:
					agregar_plan_a_turno(turno_id, plan_id)
				
				# Recargar árbol
				self._recargar_planes_con_turnos_tree()
				messagebox.showinfo('Éxito', f'Plan "{nombre}" creado y asignado a {len(turnos_seleccionados)} turno(s).', parent=win)
				win.destroy()
			except Exception as e:
				messagebox.showerror('Error', str(e), parent=win)
		
		ttk.Button(frame_btns, text='Crear Plan', command=guardar, width=15).grid(row=0, column=0, padx=5)
		ttk.Button(frame_btns, text='Cancelar', command=win.destroy, width=15).grid(row=0, column=1, padx=5)
		
		entry_nombre.bind('<Return>', lambda e: guardar())
	
	def _editar_plan_con_turnos(self):
		"""Ventana para editar un plan de estudio y sus turnos asignados"""
		if not self.plan_seleccionado_id:
			messagebox.showerror('Error', 'Seleccione un plan para editar.')
			return
		
		# Obtener datos actuales
		planes = obtener_planes()
		plan_actual = next((p for p in planes if p['id'] == self.plan_seleccionado_id), None)
		if not plan_actual:
			messagebox.showerror('Error', 'Plan no encontrado.')
			return
		
		turnos_actuales = obtener_turnos_de_plan(self.plan_seleccionado_id)
		turnos_actuales_ids = [t['id'] for t in turnos_actuales]
		
		win = tk.Toplevel(self)
		win.configure(bg='#f4f6fa')
		win.title('Editar Plan de Estudio')
		win.geometry('450x400')
		win.minsize(450, 400)
		win.transient(self)
		win.resizable(False, False)
		win.grab_set()
		win.focus_force()
		
		ttk.Label(win, text='Editar Plan de Estudio', font=('Arial', 12, 'bold')).pack(pady=10)
		
		# Nombre del plan
		frame_nombre = ttk.Frame(win)
		frame_nombre.pack(pady=10, padx=20, fill='x')
		ttk.Label(frame_nombre, text='Nombre del Plan:', font=('Segoe UI', 10)).pack(anchor='w', pady=(0, 5))
		entry_nombre = ttk.Entry(frame_nombre, width=40)
		entry_nombre.insert(0, plan_actual['nombre'])
		entry_nombre.pack(fill='x')
		entry_nombre.focus_set()
		
		# Selección de turnos
		frame_turnos = ttk.Frame(win)
		frame_turnos.pack(pady=10, padx=20, fill='both', expand=True)
		ttk.Label(frame_turnos, text='Turnos asignados:', font=('Segoe UI', 10)).pack(anchor='w', pady=(0, 5))
		
		# Frame con scrollbar para checkboxes
		canvas_frame = ttk.Frame(frame_turnos)
		canvas_frame.pack(fill='both', expand=True)
		
		canvas = tk.Canvas(canvas_frame, bg='#f4f6fa', highlightthickness=0, height=150)
		scrollbar = ttk.Scrollbar(canvas_frame, orient='vertical', command=canvas.yview)
		scrollable_frame = ttk.Frame(canvas)
		
		scrollable_frame.bind(
			"<Configure>",
			lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
		)
		
		canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
		canvas.configure(yscrollcommand=scrollbar.set)
		
		canvas.pack(side='left', fill='both', expand=True)
		scrollbar.pack(side='right', fill='y')
		
		# Crear checkboxes para cada turno
		turnos = obtener_turnos()
		turnos_vars = {}
		for turno in turnos:
			var = tk.IntVar(value=1 if turno['id'] in turnos_actuales_ids else 0)
			chk = ttk.Checkbutton(scrollable_frame, text=turno['nombre'], variable=var)
			chk.pack(anchor='w', pady=2, padx=5)
			turnos_vars[turno['id']] = var
		
		if not turnos:
			ttk.Label(scrollable_frame, text='(No hay turnos creados)', foreground='gray').pack(pady=10)
		
		# Botones
		frame_btns = ttk.Frame(win)
		frame_btns.pack(pady=15)
		
		def guardar():
			nombre = entry_nombre.get().strip()
			if not nombre:
				messagebox.showerror('Error', 'Ingrese un nombre para el plan.', parent=win)
				return
			
			# Verificar que al menos un turno esté seleccionado
			turnos_seleccionados = [tid for tid, var in turnos_vars.items() if var.get() == 1]
			if not turnos_seleccionados:
				messagebox.showerror('Error', 'Debe seleccionar al menos un turno.', parent=win)
				return
			
			try:
				# Actualizar nombre del plan si cambió
				if nombre != plan_actual['nombre']:
					conn = get_connection()
					c = conn.cursor()
					c.execute('UPDATE plan_estudio SET nombre=? WHERE id=?', (nombre, self.plan_seleccionado_id))
					conn.commit()
					conn.close()
				
				# Actualizar turnos: quitar los que ya no están, agregar los nuevos
				turnos_actuales_set = set(turnos_actuales_ids)
				turnos_nuevos_set = set(turnos_seleccionados)
				
				# Quitar turnos desmarcados
				for turno_id in turnos_actuales_set - turnos_nuevos_set:
					quitar_plan_de_turno(turno_id, self.plan_seleccionado_id)
				
				# Agregar turnos nuevos
				for turno_id in turnos_nuevos_set - turnos_actuales_set:
					agregar_plan_a_turno(turno_id, self.plan_seleccionado_id)
				
				# Recargar árbol
				self._recargar_planes_con_turnos_tree()
				messagebox.showinfo('Éxito', f'Plan "{nombre}" actualizado.', parent=win)
				win.destroy()
			except Exception as e:
				messagebox.showerror('Error', str(e), parent=win)
		
		ttk.Button(frame_btns, text='Guardar Cambios', command=guardar, width=15).grid(row=0, column=0, padx=5)
		ttk.Button(frame_btns, text='Cancelar', command=win.destroy, width=15).grid(row=0, column=1, padx=5)
		
		entry_nombre.bind('<Return>', lambda e: guardar())

	def _gestionar_materias_plan(self):
		if not self.plan_seleccionado_id:
			messagebox.showerror('Error', 'Seleccione un plan.')
			return
		win = tk.Toplevel(self)
		win.configure(bg='#f4f6fa')
		win.title('Materias/Obligaciones del plan')
		win.geometry('450x480')
		win.minsize(400, 420)
		win.transient(self)
		win.grab_set()
		win.focus_force()
		materias_plan = obtener_materias_de_plan(self.plan_seleccionado_id)
		todas_materias = sorted(obtener_materias(), key=lambda m: m['nombre'].lower())
		frame = ttk.Frame(win)
		frame.pack(fill='both', expand=True, padx=10, pady=10)
		tree = ttk.Treeview(frame, columns=('Nombre',), show='headings', height=3)
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
		ttk.Button(btns, text='Agregar obligación', command=agregar).pack(side='left', padx=5)
		ttk.Button(btns, text='Quitar obligación', command=quitar).pack(side='left', padx=5)
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
			self._recargar_turnos_tree()
			self.entry_nombre_turno.delete(0, tk.END)
		except Exception as e:
			messagebox.showerror('Error', str(e))

	def _eliminar_turno(self):
		if not self.turno_seleccionado_id:
			messagebox.showerror('Error', 'Seleccione un turno.')
			return
		try:
			eliminar_turno(self.turno_seleccionado_id)
			self._recargar_turnos_tree()
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
		tree = ttk.Treeview(frame, columns=('Nombre',), show='headings', height=3)
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

	def _gestionar_ciclos_plan(self):
		if not self.plan_seleccionado_id:
			messagebox.showerror('Error', 'Seleccione un plan.')
			return
		win = tk.Toplevel(self)
		win.configure(bg='#f4f6fa')
		win.title('Ciclos del plan')
		win.geometry('450x480')
		win.minsize(400, 420)
		win.transient(self)
		win.grab_set()
		win.focus_force()
		ciclos_plan = obtener_ciclos(self.plan_seleccionado_id)
		frame = ttk.Frame(win)
		frame.pack(fill='both', expand=True, padx=10, pady=10)
		tree = ttk.Treeview(frame, columns=('Nombre',), show='headings', height=3)
		tree.heading('Nombre', text='Nombre')
		tree.pack(side='left', fill='both', expand=True)
		vsb = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
		tree.configure(yscroll=vsb.set)
		vsb.pack(side='right', fill='y')
		def cargar():
			for row in tree.get_children():
				tree.delete(row)
			for a in ciclos_plan:
				tree.insert('', 'end', iid=a['id'], values=(a['nombre'],))
		cargar()
		def agregar():
			win2 = tk.Toplevel(win)
			win2.configure(bg='#f4f6fa')
			win2.title('Agregar ciclo')
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
					crear_ciclo(nombre, [self.plan_seleccionado_id])
					ciclos_plan[:] = obtener_ciclos(self.plan_seleccionado_id)
					cargar()
					win2.destroy()
				except Exception as e:
					messagebox.showerror('Error', str(e))
			ttk.Button(win2, text='Agregar', command=aceptar).pack(pady=5)
		def quitar():
			sel = tree.selection()
			if not sel:
				return
			ciclo_id = int(sel[0])
			try:
				eliminar_ciclo(ciclo_id)
				ciclos_plan[:] = [a for a in ciclos_plan if a['id'] != ciclo_id]
				cargar()
			except Exception as e:
				messagebox.showerror('Error', str(e))
		def materias():
			sel = tree.selection()
			if not sel:
				messagebox.showerror('Error', 'Seleccione un ciclo.')
				return
			ciclo_id = int(sel[0])
			win3 = tk.Toplevel(win)
			win3.configure(bg='#f4f6fa')
			win3.title('Materias del ciclo')
			win3.geometry('450x480')
			win3.minsize(400, 420)
			win3.transient(win)
			win3.grab_set()
			win3.focus_force()
			materias_ciclo = obtener_materias_de_ciclo(ciclo_id)
			materias_plan = obtener_materias_de_plan(self.plan_seleccionado_id)
			frame3 = ttk.Frame(win3)
			frame3.pack(fill='both', expand=True, padx=10, pady=10)
			tree3 = ttk.Treeview(frame3, columns=('Nombre',), show='headings', height=3)
			tree3.heading('Nombre', text='Nombre')
			tree3.pack(side='left', fill='both', expand=True)
			vsb3 = ttk.Scrollbar(frame3, orient='vertical', command=tree3.yview)
			tree3.configure(yscroll=vsb3.set)
			vsb3.pack(side='right', fill='y')
			def cargar3():
				for row in tree3.get_children():
					tree3.delete(row)
				for m in materias_ciclo:
					tree3.insert('', 'end', iid=m['id'], values=(m['nombre'],))
			cargar3()
			def agregar3():
				opciones = [m for m in materias_plan if m not in materias_ciclo]
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
							agregar_materia_a_ciclo(ciclo_id, materia['id'])
							materias_ciclo.append(materia)
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
					quitar_materia_de_ciclo(ciclo_id, materia_id)
					materias_ciclo[:] = [m for m in materias_ciclo if m['id'] != materia_id]
					cargar3()
				except Exception as e:
					messagebox.showerror('Error', str(e))
			btns3 = ttk.Frame(win3)
			btns3.pack(pady=5)
			ttk.Button(btns3, text='Agregar obligación', command=agregar3).pack(side='left', padx=5)
			ttk.Button(btns3, text='Quitar obligación', command=quitar3).pack(side='left', padx=5)
		btns = ttk.Frame(win)
		btns.pack(pady=5)
		ttk.Button(btns, text='Agregar ciclo', command=agregar).pack(side='left', padx=5)
		ttk.Button(btns, text='Quitar ciclo', command=quitar).pack(side='left', padx=5)
		ttk.Button(btns, text='Materias del ciclo', command=materias).pack(side='left', padx=5)

	def _gestionar_turnos_profesor(self):
		if not self.profesor_seleccionado_id:
			messagebox.showwarning('Atención', 'Seleccione un profesor para gestionar sus turnos.')
			return
		
		profesor_id = self.profesor_seleccionado_id
		
		# Obtener nombre del profesor
		profesores = obtener_profesores()
		profesor = next((p for p in profesores if p['id'] == profesor_id), None)
		nombre_profesor = profesor['nombre'] if profesor else 'Agente'
		
		# Ventana principal
		win = tk.Toplevel(self)
		win.configure(bg='#f4f6fa')
		win.title(f'Turnos de {nombre_profesor}')
		win.geometry('500x450')
		win.minsize(450, 400)
		win.transient(self)
		win.grab_set()
		win.focus_force()
		
		ttk.Label(win, text='Seleccionar turnos del agente', font=('Arial', 12, 'bold')).pack(pady=10)
		
		# Frame para el Treeview
		frame_tree = ttk.Frame(win)
		frame_tree.pack(fill='both', expand=True, padx=15, pady=5)
		
		# Treeview con checkboxes
		tree = ttk.Treeview(frame_tree, columns=('Sel', 'Turno'), show='tree headings', height=8)
		tree.heading('#0', text='')
		tree.heading('Sel', text='☐')
		tree.heading('Turno', text='Turno')
		tree.column('#0', width=0, stretch=False)
		tree.column('Sel', width=40, stretch=False, anchor='center')
		tree.column('Turno', width=300)
		tree.pack(side='left', fill='both', expand=True)
		
		# Scrollbar
		vsb = ttk.Scrollbar(frame_tree, orient='vertical', command=tree.yview)
		tree.configure(yscroll=vsb.set)
		vsb.pack(side='right', fill='y')
		
		# Conjunto para trackear selección
		turnos_seleccionados = set()
		
		def cargar_turnos():
			"""Carga todos los turnos con su estado de selección"""
			tree.delete(*tree.get_children())
			turnos_seleccionados.clear()
			
			# Obtener turnos asignados al profesor
			turnos_asignados_ids = {t['id'] for t in obtener_turnos_de_profesor(profesor_id)}
			
			# Obtener todos los turnos
			todos_turnos = sorted(obtener_turnos(), key=lambda t: t['nombre'].lower())
			
			# Insertar en el tree
			for turno in todos_turnos:
				esta_asignado = turno['id'] in turnos_asignados_ids
				check = '☑' if esta_asignado else '☐'
				tree.insert('', 'end', iid=turno['id'], values=(check, turno['nombre']))
				
				if esta_asignado:
					turnos_seleccionados.add(turno['id'])
			
			actualizar_heading()
		
		def actualizar_heading():
			"""Actualiza el checkbox del heading"""
			items = tree.get_children()
			if not items:
				tree.heading('Sel', text='☐')
				return
			
			todas_seleccionadas = all(int(item) in turnos_seleccionados for item in items)
			tree.heading('Sel', text='☑' if todas_seleccionadas else '☐')
		
		def on_click(event):
			"""Maneja clicks en items o heading"""
			region = tree.identify('region', event.x, event.y)
			
			# Click en heading
			if region == 'heading':
				column = tree.identify_column(event.x)
				if column == '#1':  # Columna de checkboxes
					seleccionar_desseleccionar_todas()
				return
			
			# Click en item
			if region not in ('cell', 'tree'):
				return
			
			item = tree.identify_row(event.y)
			if not item:
				return
			
			turno_id = int(item)
			
			# Toggle selección
			if turno_id in turnos_seleccionados:
				turnos_seleccionados.remove(turno_id)
			else:
				turnos_seleccionados.add(turno_id)
			
			# Actualizar visualización
			valores = tree.item(item, 'values')
			nuevo_check = '☑' if turno_id in turnos_seleccionados else '☐'
			tree.item(item, values=(nuevo_check, valores[1]))
			
			actualizar_heading()
		
		def seleccionar_desseleccionar_todas():
			"""Selecciona o deselecciona todos los turnos"""
			items = tree.get_children()
			if not items:
				return
			
			todas_seleccionadas = all(int(item) in turnos_seleccionados for item in items)
			
			if todas_seleccionadas:
				turnos_seleccionados.clear()
			else:
				for item in items:
					turnos_seleccionados.add(int(item))
			
			# Actualizar visualización
			for item in items:
				turno_id = int(item)
				valores = tree.item(item, 'values')
				nuevo_check = '☑' if turno_id in turnos_seleccionados else '☐'
				tree.item(item, values=(nuevo_check, valores[1]))
			
			actualizar_heading()
		
		def guardar_cambios():
			"""Guarda los cambios en la base de datos"""
			try:
				# Obtener turnos actualmente asignados
				turnos_actuales = {t['id'] for t in obtener_turnos_de_profesor(profesor_id)}
				
				# Determinar qué agregar y qué quitar
				turnos_a_agregar = turnos_seleccionados - turnos_actuales
				turnos_a_quitar = turnos_actuales - turnos_seleccionados
				
				# Aplicar cambios
				for turno_id in turnos_a_agregar:
					asignar_turno_a_profesor(profesor_id, turno_id)
				
				for turno_id in turnos_a_quitar:
					quitar_turno_a_profesor(profesor_id, turno_id)
				
				messagebox.showinfo('Éxito', 'Los turnos han sido actualizados correctamente.', parent=win)
				win.destroy()
				
			except Exception as e:
				messagebox.showerror('Error', str(e), parent=win)
		
		# Bind del click
		tree.bind('<Button-1>', on_click)
		
		# Cargar datos iniciales
		cargar_turnos()
		
		# Botones
		frame_btns = ttk.Frame(win)
		frame_btns.pack(pady=15)
		ttk.Button(frame_btns, text='Guardar cambios', command=guardar_cambios).grid(row=0, column=0, padx=5)
		ttk.Button(frame_btns, text='Cancelar', command=win.destroy).grid(row=0, column=1, padx=5)

	def mostrar_gestion_usuarios(self):
		"""Ventana para gestionar usuarios (solo administradores)"""
		if not self.usuario_actual or not self.usuario_actual.get('es_admin'):
			messagebox.showerror('Error', 'No tiene permisos para acceder a esta función.')
			return
		
		self.limpiar_frame()
		ttk.Label(self.frame_principal, text='Gestión de Usuarios', font=('Arial', 14, 'bold')).pack(pady=10)
		
		# Frame principal con dos columnas
		main_frame = ttk.Frame(self.frame_principal)
		main_frame.pack(fill='both', expand=True, padx=10, pady=10)
		main_frame.columnconfigure(1, weight=1)
		main_frame.rowconfigure(0, weight=1)
		
		# Aside izquierdo
		aside = ttk.Frame(main_frame, width=250)
		aside.grid(row=0, column=0, sticky='ns', padx=(0, 10))
		aside.pack_propagate(False)
		
		ttk.Label(aside, text='Acciones', font=('Arial', 11, 'bold')).pack(pady=(0, 10))
		
		ttk.Button(aside, text='Crear Usuario', command=self._crear_nuevo_usuario, width=22).pack(pady=3)
		ttk.Button(aside, text='Eliminar Usuario', command=self._eliminar_usuario_seleccionado, width=22).pack(pady=3)
		ttk.Button(aside, text='Cambiar Contraseña', command=self._cambiar_password_usuario, width=22).pack(pady=3)
		
		# Contenido derecho
		content = ttk.Frame(main_frame)
		content.grid(row=0, column=1, sticky='nsew')
		
		# Tabla de usuarios
		frame_tabla = ttk.Frame(content)
		frame_tabla.pack(pady=10, fill='both', expand=True)
		
		column_config = {
			'Usuario': {'width': 200, 'anchor': 'w'},
			'Tipo': {'width': 120, 'anchor': 'center'},
			'Fecha Creación': {'width': 180, 'anchor': 'center'}
		}
		
		self.tree_usuarios = crear_treeview(frame_tabla, 
											('Usuario', 'Tipo', 'Fecha Creación'), 
											('Usuario', 'Tipo', 'Fecha Creación'),
											column_config=column_config)
		
		self._recargar_usuarios_tree()
		
		# Selección en tabla
		self.tree_usuarios.bind('<<TreeviewSelect>>', self._on_select_usuario)
		self.usuario_seleccionado_id = None
	
	def _recargar_usuarios_tree(self):
		"""Recarga el árbol de usuarios"""
		for row in self.tree_usuarios.get_children():
			self.tree_usuarios.delete(row)
		
		usuarios = obtener_usuarios()
		for usuario in usuarios:
			tipo = 'Administrador' if usuario['es_admin'] else 'Usuario'
			fecha = usuario['fecha_creacion'].split()[0] if usuario['fecha_creacion'] else 'N/A'
			self.tree_usuarios.insert('', 'end', iid=usuario['id'], 
									 values=(usuario['username'], tipo, fecha))
	
	def _on_select_usuario(self, event):
		"""Maneja la selección de un usuario en el árbol"""
		sel = self.tree_usuarios.selection()
		if sel:
			self.usuario_seleccionado_id = int(sel[0])
		else:
			self.usuario_seleccionado_id = None
	
	def _crear_nuevo_usuario(self):
		"""Ventana para crear un nuevo usuario"""
		win = tk.Toplevel(self)
		win.title('Crear Nuevo Usuario')
		win.geometry('450x350')
		win.resizable(False, False)
		win.configure(bg='#f4f6fa')
		win.transient(self)
		win.grab_set()
		win.focus_force()
		
		ttk.Label(win, text='Crear Nuevo Usuario', font=('Arial', 12, 'bold')).pack(pady=15)
		
		# Formulario
		form = ttk.Frame(win)
		form.pack(pady=20, padx=40)
		
		ttk.Label(form, text='Usuario:').grid(row=0, column=0, sticky='e', padx=5, pady=8)
		entry_username = ttk.Entry(form, width=25)
		entry_username.grid(row=0, column=1, padx=5, pady=8)
		entry_username.focus_set()
		
		ttk.Label(form, text='Contraseña:').grid(row=1, column=0, sticky='e', padx=5, pady=8)
		entry_password = ttk.Entry(form, show='*', width=25)
		entry_password.grid(row=1, column=1, padx=5, pady=8)
		
		ttk.Label(form, text='Confirmar:').grid(row=2, column=0, sticky='e', padx=5, pady=8)
		entry_confirm = ttk.Entry(form, show='*', width=25)
		entry_confirm.grid(row=2, column=1, padx=5, pady=8)
		
		# Checkbox para admin
		var_admin = tk.IntVar(value=0)
		chk_admin = ttk.Checkbutton(form, text='Usuario Administrador', variable=var_admin)
		chk_admin.grid(row=3, column=0, columnspan=2, pady=10)
		
		def guardar():
			username = entry_username.get().strip()
			password = entry_password.get()
			confirm = entry_confirm.get()
			
			if not username:
				messagebox.showerror('Error', 'El nombre de usuario no puede estar vacío.', parent=win)
				return
			
			if len(username) < 3:
				messagebox.showerror('Error', 'El nombre de usuario debe tener al menos 3 caracteres.', parent=win)
				return
			
			if not password:
				messagebox.showerror('Error', 'La contraseña no puede estar vacía.', parent=win)
				return
			
			if len(password) < 4:
				messagebox.showerror('Error', 'La contraseña debe tener al menos 4 caracteres.', parent=win)
				return
			
			if password != confirm:
				messagebox.showerror('Error', 'Las contraseñas no coinciden.', parent=win)
				return
			
			try:
				crear_usuario(username, password, es_admin=bool(var_admin.get()))
				messagebox.showinfo('Éxito', f'Usuario "{username}" creado correctamente.', parent=win)
				self._recargar_usuarios_tree()
				win.destroy()
			except Exception as e:
				messagebox.showerror('Error', str(e), parent=win)
		
		# Botones
		frame_btns = ttk.Frame(win)
		frame_btns.pack(pady=15)
		ttk.Button(frame_btns, text='Crear', command=guardar, width=12).grid(row=0, column=0, padx=5)
		ttk.Button(frame_btns, text='Cancelar', command=win.destroy, width=12).grid(row=0, column=1, padx=5)
		
		# Bindings
		entry_username.bind('<Return>', lambda e: entry_password.focus_set())
		entry_password.bind('<Return>', lambda e: entry_confirm.focus_set())
		entry_confirm.bind('<Return>', lambda e: guardar())
	
	def _eliminar_usuario_seleccionado(self):
		"""Elimina el usuario seleccionado"""
		if not self.usuario_seleccionado_id:
			messagebox.showwarning('Atención', 'Seleccione un usuario para eliminar.')
			return
		
		if self.usuario_seleccionado_id == self.usuario_actual['id']:
			messagebox.showerror('Error', 'No puede eliminar su propio usuario.')
			return
		
		usuarios = obtener_usuarios()
		usuario = next((u for u in usuarios if u['id'] == self.usuario_seleccionado_id), None)
		
		if not usuario:
			return
		
		if not messagebox.askyesno('Confirmar', f'¿Está seguro de eliminar el usuario "{usuario["username"]}"?'):
			return
		
		try:
			eliminar_usuario(self.usuario_seleccionado_id)
			messagebox.showinfo('Éxito', 'Usuario eliminado correctamente.')
			self._recargar_usuarios_tree()
			self.usuario_seleccionado_id = None
		except Exception as e:
			messagebox.showerror('Error', str(e))
	
	def _cambiar_password_usuario(self):
		"""Cambia la contraseña del usuario seleccionado"""
		if not self.usuario_seleccionado_id:
			messagebox.showwarning('Atención', 'Seleccione un usuario para cambiar su contraseña.')
			return
		
		usuarios = obtener_usuarios()
		usuario = next((u for u in usuarios if u['id'] == self.usuario_seleccionado_id), None)
		
		if not usuario:
			return
		
		win = tk.Toplevel(self)
		win.title('Cambiar Contraseña')
		win.geometry('420x260')
		win.resizable(False, False)
		win.configure(bg='#f4f6fa')
		win.transient(self)
		win.grab_set()
		win.focus_force()
		
		ttk.Label(win, text=f'Cambiar contraseña de: {usuario["username"]}', 
				 font=('Arial', 11, 'bold')).pack(pady=15)
		
		# Formulario
		form = ttk.Frame(win)
		form.pack(pady=15, padx=40)
		
		ttk.Label(form, text='Nueva Contraseña:').grid(row=0, column=0, sticky='e', padx=5, pady=8)
		entry_password = ttk.Entry(form, show='*', width=25)
		entry_password.grid(row=0, column=1, padx=5, pady=8)
		entry_password.focus_set()
		
		ttk.Label(form, text='Confirmar:').grid(row=1, column=0, sticky='e', padx=5, pady=8)
		entry_confirm = ttk.Entry(form, show='*', width=25)
		entry_confirm.grid(row=1, column=1, padx=5, pady=8)
		
		def guardar():
			password = entry_password.get()
			confirm = entry_confirm.get()
			
			if not password:
				messagebox.showerror('Error', 'La contraseña no puede estar vacía.', parent=win)
				return
			
			if len(password) < 4:
				messagebox.showerror('Error', 'La contraseña debe tener al menos 4 caracteres.', parent=win)
				return
			
			if password != confirm:
				messagebox.showerror('Error', 'Las contraseñas no coinciden.', parent=win)
				return
			
			try:
				cambiar_password(self.usuario_seleccionado_id, password)
				messagebox.showinfo('Éxito', 'Contraseña actualizada correctamente.', parent=win)
				win.destroy()
			except Exception as e:
				messagebox.showerror('Error', str(e), parent=win)
		
		# Botones
		frame_btns = ttk.Frame(win)
		frame_btns.pack(pady=15)
		ttk.Button(frame_btns, text='Cambiar', command=guardar, width=12).grid(row=0, column=0, padx=5)
		ttk.Button(frame_btns, text='Cancelar', command=win.destroy, width=12).grid(row=0, column=1, padx=5)
		
		# Bindings
		entry_password.bind('<Return>', lambda e: entry_confirm.focus_set())
		entry_confirm.bind('<Return>', lambda e: guardar())
	
	def cambiar_mi_password(self):
		"""Permite al usuario actual cambiar su propia contraseña"""
		win = tk.Toplevel(self)
		win.title('Cambiar Mi Contraseña')
		win.geometry('420x300')
		win.resizable(False, False)
		win.configure(bg='#f4f6fa')
		win.transient(self)
		win.grab_set()
		win.focus_force()
		
		ttk.Label(win, text='Cambiar Mi Contraseña', font=('Arial', 11, 'bold')).pack(pady=15)
		
		# Formulario
		form = ttk.Frame(win)
		form.pack(pady=15, padx=40)
		
		ttk.Label(form, text='Contraseña Actual:').grid(row=0, column=0, sticky='e', padx=5, pady=8)
		entry_actual = ttk.Entry(form, show='*', width=25)
		entry_actual.grid(row=0, column=1, padx=5, pady=8)
		entry_actual.focus_set()
		
		ttk.Label(form, text='Nueva Contraseña:').grid(row=1, column=0, sticky='e', padx=5, pady=8)
		entry_password = ttk.Entry(form, show='*', width=25)
		entry_password.grid(row=1, column=1, padx=5, pady=8)
		
		ttk.Label(form, text='Confirmar:').grid(row=2, column=0, sticky='e', padx=5, pady=8)
		entry_confirm = ttk.Entry(form, show='*', width=25)
		entry_confirm.grid(row=2, column=1, padx=5, pady=8)
		
		def guardar():
			actual = entry_actual.get()
			password = entry_password.get()
			confirm = entry_confirm.get()
			
			if not actual:
				messagebox.showerror('Error', 'Ingrese su contraseña actual.', parent=win)
				return
			
			# Verificar contraseña actual
			usuario_verificado = verificar_usuario(self.usuario_actual['username'], actual)
			if not usuario_verificado:
				messagebox.showerror('Error', 'La contraseña actual es incorrecta.', parent=win)
				return
			
			if not password:
				messagebox.showerror('Error', 'La nueva contraseña no puede estar vacía.', parent=win)
				return
			
			if len(password) < 4:
				messagebox.showerror('Error', 'La contraseña debe tener al menos 4 caracteres.', parent=win)
				return
			
			if password != confirm:
				messagebox.showerror('Error', 'Las contraseñas no coinciden.', parent=win)
				return
			
			try:
				cambiar_password(self.usuario_actual['id'], password)
				messagebox.showinfo('Éxito', 'Contraseña actualizada correctamente.', parent=win)
				win.destroy()
			except Exception as e:
				messagebox.showerror('Error', str(e), parent=win)
		
		# Botones
		frame_btns = ttk.Frame(win)
		frame_btns.pack(pady=15)
		ttk.Button(frame_btns, text='Cambiar', command=guardar, width=12).grid(row=0, column=0, padx=5)
		ttk.Button(frame_btns, text='Cancelar', command=win.destroy, width=12).grid(row=0, column=1, padx=5)
		
		# Bindings
		entry_actual.bind('<Return>', lambda e: entry_password.focus_set())
		entry_password.bind('<Return>', lambda e: entry_confirm.focus_set())
		entry_confirm.bind('<Return>', lambda e: guardar())
	
	def cerrar_sesion(self):
		"""Cierra la sesión actual y muestra el login nuevamente"""
		if messagebox.askyesno('Confirmar', '¿Está seguro de que desea cerrar sesión?'):
			self.usuario_actual = None
			self.limpiar_frame()
			# Destruir el menú actual
			self.config(menu=tk.Menu(self))
			self._mostrar_login()
	
	def crear_backup_manual(self):
		"""Crea un backup manual de la base de datos con timestamp"""
		try:
			backup_path = crear_backup_db(manual=True)
			backup_name = os.path.basename(backup_path)
			messagebox.showinfo('Éxito', 
							   f'Backup creado exitosamente:\n\n{backup_name}\n\n'
							   f'Ubicación:\n{os.path.dirname(backup_path)}')
		except Exception as e:
			messagebox.showerror('Error', f'Error al crear backup:\n{str(e)}')
	
	def mostrar_lista_backups(self):
		"""Muestra la lista de backups disponibles"""
		if not self.usuario_actual or not self.usuario_actual.get('es_admin'):
			messagebox.showerror('Error', 'No tiene permisos para acceder a esta función.')
			return
		
		self.limpiar_frame()
		ttk.Label(self.frame_principal, text='Backups de la Base de Datos', 
				 font=('Arial', 14, 'bold')).pack(pady=10)
		
		# Información sobre backup automático
		info_frame = ttk.Frame(self.frame_principal)
		info_frame.pack(pady=5, padx=20, fill='x')
		
		ttk.Label(info_frame, 
				 text='ℹ️  Se crea un backup automático (institucion.bak) cada vez que inicia el programa.',
				 font=('Segoe UI', 9), foreground='#555').pack(anchor='w')
		ttk.Label(info_frame,
				 text='    Los backups manuales incluyen fecha y hora en el nombre.',
				 font=('Segoe UI', 9), foreground='#555').pack(anchor='w')
		
		# Frame principal con dos columnas
		main_frame = ttk.Frame(self.frame_principal)
		main_frame.pack(fill='both', expand=True, padx=10, pady=10)
		main_frame.columnconfigure(1, weight=1)
		main_frame.rowconfigure(0, weight=1)
		
		# Aside izquierdo
		aside = ttk.Frame(main_frame, width=200)
		aside.grid(row=0, column=0, sticky='ns', padx=(0, 10))
		aside.pack_propagate(False)
		
		ttk.Label(aside, text='Acciones', font=('Arial', 11, 'bold')).pack(pady=(0, 10))
		
		ttk.Button(aside, text='Crear Backup', 
				  command=self.crear_backup_manual, width=18).pack(pady=3)
		ttk.Button(aside, text='Actualizar Lista', 
				  command=lambda: self._recargar_backups_tree(), width=18).pack(pady=3)
		ttk.Button(aside, text='Abrir Ubicación', 
				  command=self._abrir_ubicacion_backups, width=18).pack(pady=3)
		ttk.Button(aside, text='Eliminar Backup', 
				  command=self._eliminar_backup_seleccionado, width=18).pack(pady=3)
		
		# Contenido derecho
		content = ttk.Frame(main_frame)
		content.grid(row=0, column=1, sticky='nsew')
		
		# Tabla de backups
		frame_tabla = ttk.Frame(content)
		frame_tabla.pack(pady=10, fill='both', expand=True)
		
		column_config = {
			'Nombre': {'width': 280, 'anchor': 'w'},
			'Fecha': {'width': 140, 'anchor': 'center'},
			'Tamaño': {'width': 100, 'anchor': 'center'}
		}
		
		self.tree_backups = crear_treeview(frame_tabla,
										  ('Nombre', 'Fecha', 'Tamaño'),
										  ('Nombre del Archivo', 'Fecha de Creación', 'Tamaño'),
										  column_config=column_config)
		
		self._recargar_backups_tree()
		
		# Selección en tabla
		self.tree_backups.bind('<<TreeviewSelect>>', self._on_select_backup)
		self.backup_seleccionado = None
	
	def _recargar_backups_tree(self):
		"""Recarga el árbol de backups"""
		if not hasattr(self, 'tree_backups'):
			return
		
		for row in self.tree_backups.get_children():
			self.tree_backups.delete(row)
		
		try:
			backups = listar_backups()
			
			if not backups:
				# Insertar mensaje si no hay backups
				self.tree_backups.insert('', 'end', values=('No hay backups disponibles', '', ''))
				return
			
			for backup in backups:
				# Formatear tamaño
				tamaño_kb = backup['tamaño'] / 1024
				if tamaño_kb < 1024:
					tamaño_str = f'{tamaño_kb:.1f} KB'
				else:
					tamaño_mb = tamaño_kb / 1024
					tamaño_str = f'{tamaño_mb:.2f} MB'
				
				# Insertar en el árbol
				self.tree_backups.insert('', 'end', 
										iid=backup['ruta'],
										values=(backup['nombre'], backup['fecha'], tamaño_str))
		except Exception as e:
			messagebox.showerror('Error', f'Error al listar backups:\n{str(e)}')
	
	def _on_select_backup(self, event):
		"""Maneja la selección de un backup"""
		sel = self.tree_backups.selection()
		if sel:
			self.backup_seleccionado = sel[0]
		else:
			self.backup_seleccionado = None
	
	def _abrir_ubicacion_backups(self):
		"""Abre el explorador de archivos en la ubicación de los backups"""
		try:
			if sys.platform == 'win32':
				os.startfile(DB_DIR)
			elif sys.platform == 'darwin':  # macOS
				os.system(f'open "{DB_DIR}"')
			else:  # Linux
				os.system(f'xdg-open "{DB_DIR}"')
		except Exception as e:
			messagebox.showerror('Error', f'Error al abrir ubicación:\n{str(e)}')
	
	def _eliminar_backup_seleccionado(self):
		"""Elimina el backup seleccionado"""
		if not self.backup_seleccionado:
			messagebox.showwarning('Atención', 'Seleccione un backup para eliminar.')
			return
		
		# Verificar que no sea el backup automático
		nombre_backup = os.path.basename(self.backup_seleccionado)
		
		if nombre_backup == 'institucion.bak':
			if not messagebox.askyesno('Confirmar',
									   'Este es el backup automático.\n'
									   'Se volverá a crear en el próximo inicio.\n\n'
									   '¿Está seguro de eliminarlo?'):
				return
		else:
			if not messagebox.askyesno('Confirmar', 
									   f'¿Está seguro de eliminar el backup:\n\n{nombre_backup}?'):
				return
		
		try:
			if os.path.exists(self.backup_seleccionado):
				os.remove(self.backup_seleccionado)
				messagebox.showinfo('Éxito', 'Backup eliminado correctamente.')
				self._recargar_backups_tree()
				self.backup_seleccionado = None
			else:
				messagebox.showerror('Error', 'El archivo de backup no existe.')
		except Exception as e:
			messagebox.showerror('Error', f'Error al eliminar backup:\n{str(e)}')

if __name__ == "__main__":
	init_db()
	app = App()
	app.mainloop()
