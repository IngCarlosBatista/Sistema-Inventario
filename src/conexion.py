import sqlite3
import os
import hashlib

def conectar():
    """Establece una conexión con la base de datos SQLite dentro de la carpeta database."""
    # Obtener la ruta del directorio raíz del proyecto de forma dinámica (sube un nivel desde src)
    ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    ruta_db_folder = os.path.join(ruta_raiz, "database")
    
    # Asegurar que la carpeta 'database' exista físicamente en el disco
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
    """Crea las tablas obligatorias del sistema si no existen."""
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        
        # 1. Tabla de Productos (la que ya tenías)
        sql_productos = """
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            cantidad INTEGER NOT NULL DEFAULT 0,
            precio REAL NOT NULL DEFAULT 0.0,
            stock_minimo INTEGER NOT NULL DEFAULT 5
        )
        """
        
        # 2. NUEVA Tabla de Usuarios
        sql_usuarios = """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            rol TEXT DEFAULT 'empleado'
        )
        """
        
        try:
            # Ejecutamos ambos comandos
            cursor.execute(sql_productos)
            cursor.execute(sql_usuarios)
            conexion.commit()
            print("Base de datos y tablas verificadas correctamente.")
        except sqlite3.Error as e:
            print(f"Error al crear las tablas: {e}")
        finally:
            conexion.close()

def registrar_usuario(username, password, rol="empleado"):
    """Encripta la contraseña y guarda el usuario en la base de datos."""
    # Convertimos la contraseña a bytes y la encriptamos (SHA-256)
    password_bytes = password.encode('utf-8')
    password_hash = hashlib.sha256(password_bytes).hexdigest()
    
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute('''
                INSERT INTO usuarios (username, password_hash, rol)
                VALUES (?, ?, ?)
            ''', (username, password_hash, rol))
            conexion.commit()
            print(f"Usuario '{username}' registrado con éxito.")
            return True
        except sqlite3.IntegrityError:
            print(f"Error: El usuario '{username}' ya existe.")
            return False
        finally:
            conexion.close()
    return False