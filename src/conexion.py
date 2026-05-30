import sqlite3
import os
import hashlib

def conectar():
    """Establece una conexión con la base de datos SQLite."""
    ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    ruta_db_folder = os.path.join(ruta_raiz, "database")
    
    if not os.path.exists(ruta_db_folder):
        os.makedirs(ruta_db_folder)
        
    ruta_final_db = os.path.join(ruta_db_folder, "inventario.db")
    
    try:
        conexion = sqlite3.connect(ruta_final_db)
        return conexion
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def crear_tablas():
    """Crea las tablas obligatorias del sistema."""
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        
        # 1. Tabla de Productos
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            cantidad INTEGER NOT NULL DEFAULT 0,
            precio REAL NOT NULL DEFAULT 0.0,
            stock_minimo INTEGER NOT NULL DEFAULT 5
        )
        """)
        
        # 2. Tabla de Usuarios (Actualizada con nombre, apellido y foto_path)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            rol TEXT DEFAULT 'empleado',
            nombre TEXT,
            apellido TEXT,
            foto_path TEXT
        )
        """)
        
        conexion.commit()
        conexion.close()
        print("Base de datos y tablas verificadas correctamente.")

def registrar_usuario(username, password, path_foto, nombre="", apellido="", rol="empleado"):
    """Encripta la contraseña y guarda el usuario incluyendo los nuevos datos."""
    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute('''
                INSERT INTO usuarios (username, password_hash, rol, nombre, apellido, foto_path)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, password_hash, rol, nombre, apellido, path_foto))
            conexion.commit()
            print(f"Usuario '{username}' registrado con éxito.")
            return True
        except sqlite3.IntegrityError:
            print(f"Error: El usuario '{username}' ya existe.")
            return False
        finally:
            conexion.close()
    return False

def verificar_usuario(username, password):
    """
    Verifica credenciales.
    Si es correcto, retorna un diccionario con los datos del usuario (útil para la sesión).
    Si es incorrecto, retorna None.
    """
    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        # Buscamos el usuario y traemos los datos adicionales
        cursor.execute("SELECT password_hash, nombre, apellido, foto_path FROM usuarios WHERE username = ?", (username,))
        resultado = cursor.fetchone()
        conexion.close()
        
        if resultado and resultado[0] == password_hash:
            # Retornamos los datos para poder usarlos en el sistema
            return {
                "nombre": resultado[1],
                "apellido": resultado[2],
                "foto": resultado[3]
            }
    return None