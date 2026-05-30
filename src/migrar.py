import sqlite3
import os

# Ruta a tu base de datos (asegúrate de que coincida con la de conexion.py)
ruta_db = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "database", "inventario.db"))

def aplicar_migracion():
    try:
        conn = sqlite3.connect(ruta_db)
        cursor = conn.cursor()
        
        # Ejecutar el cambio
        cursor.execute("ALTER TABLE usuarios ADD COLUMN foto_path TEXT")
        conn.commit()
        print("✅ Columna 'foto_path' agregada con éxito.")
        
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print("⚠️ La columna ya existía, no es necesario hacer nada.")
        else:
            print(f"❌ Error inesperado: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    aplicar_migracion()