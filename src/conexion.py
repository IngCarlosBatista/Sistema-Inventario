import sqlite3
import os

# Ruta donde se guardará la base de datos
DB_PATH = os.path.join("database", "inventario.db")

def conectar():
    """Establece conexión con la base de datos SQLite."""
    try:
        conexion = sqlite3.connect(DB_PATH)
        return conexion
    except sqlite3.Error as e:
        print(f"❌ Error al conectar a la base de datos: {e}")
        return None

def crear_tablas():
    """Crea la tabla de productos si no existe en el sistema."""
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        
        # Sentencia SQL para crear la tabla con control de stock mínimo
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
            print(f"❌ Error al crear la tabla: {e}")
        finally:
            conexion.close()