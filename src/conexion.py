import sqlite3
import os

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
        sql = """
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            cantidad INTEGER NOT NULL DEFAULT 0,
            precio REAL NOT NULL DEFAULT 0.0,
            stock_minimo INTEGER NOT NULL DEFAULT 5
        )
        """
        try:
            cursor.execute(sql)
            conexion.commit()
        except sqlite3.Error as e:
            print(f"Error al crear las tablas: {e}")
        finally:
            conexion.close()