import sqlite3
import os

# Ruta a tu base de datos (asegúrate de que coincida con la de conexion.py)
ruta_db = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "database", "inventario.db"))

# Lista de migraciones a aplicar
# Puedes agregar nuevas consultas SQL en esta lista cuando necesites actualizar la estructura
migraciones = [
    "ALTER TABLE usuarios ADD COLUMN foto_path TEXT"
]

def aplicar_migraciones():
    try:
        conn = sqlite3.connect(ruta_db)
        cursor = conn.cursor()
        print(f"--- Iniciando migración en: {ruta_db} ---")
        
        for sql in migraciones:
            try:
                cursor.execute(sql)
                conn.commit()
                print(f"✅ Ejecutado con éxito: {sql[:50]}...")
            except sqlite3.OperationalError as e:
                # Manejo específico si la columna ya existe
                if "duplicate column name" in str(e).lower():
                    print(f"⚠️ Ya existía (omitido): {sql[:50]}...")
                else:
                    print(f"❌ Error al ejecutar: {sql[:50]}... -> {e}")
        
        print("--- Proceso de migración finalizado ---")
        
    except Exception as e:
        print(f"❌ Error crítico de conexión: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    aplicar_migraciones()