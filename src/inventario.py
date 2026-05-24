import sqlite3
from conexion import conectar

def registrar_producto(nombre, descripcion, cantidad, precio, stock_minimo):
    """Inserta un nuevo producto en la base de datos."""
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        sql = """
        INSERT INTO productos (nombre, descripcion, cantidad, precio, stock_minimo)
        VALUES (?, ?, ?, ?, ?)
        """
        try:
            cursor.execute(sql, (nombre, descripcion, cantidad, precio, stock_minimo))
            conexion.commit()
            print("\n✅ ¡Producto registrado exitosamente!")
        except sqlite3.Error as e:
            print(f"\n❌ Error al registrar el producto: {e}")
        finally:
            conexion.close()

def mostrar_stock():
    """Recupera y muestra todos los productos en el almacén con formato de tabla."""
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        sql = "SELECT id, nombre, cantidad, precio, stock_minimo FROM productos"
        
        try:
            cursor.execute(sql)
            productos = cursor.fetchall()
            
            if not productos:
                print("\n📦 El almacén está vacío actualmente.")
                return False
            else:
                print("\n" + "="*75)
                print(f"{'ID':<5} | {'PRODUCTO':<25} | {'CANTIDAD':<10} | {'PRECIO':<12} | {'ESTADO':<15}")
                print("="*75)
                
                for prod in productos:
                    id_p, nombre, cant, precio, min_s = prod
                    estado = "⚠️ Stock Bajo" if cant <= min_s else "✅ OK"
                    print(f"{id_p:<5} | {nombre:<25} | {cant:<10} | ${precio:<11.2f} | {estado:<15}")
                print("="*75)
                return True
                
        except sqlite3.Error as e:
            print(f"\n❌ Error al consultar el inventario: {e}")
            return False
        finally:
            conexion.close()

def actualizar_stock(id_producto, cantidad_cambio, tipo_movimiento):
    """Modifica la cantidad de un producto existente (Suma o Resta)."""
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        
        # Primero verificamos si el producto existe y su cantidad actual
        cursor.execute("SELECT nombre, cantidad FROM productos WHERE id = ?", (id_producto,))
        producto = cursor.fetchone()
        
        if not producto:
            print("\n❌ Error: No se encontró ningún producto con el ID especificado.")
            conexion.close()
            return
        
        nombre_prod, cantidad_actual = producto
        
        # Calculamos el nuevo inventario según la transacción comercial
        if tipo_movimiento == "entrada":
            nueva_cantidad = cantidad_actual + cantidad_cambio
        elif tipo_movimiento == "salida":
            if cantidad_cambio > cantidad_actual:
                print(f"\n❌ Error: Stock insuficiente. Solo quedan {cantidad_actual} unidades de '{nombre_prod}'.")
                conexion.close()
                return
            nueva_cantidad = cantidad_actual - cantidad_cambio
            
        # Ejecutamos la actualización
        sql = "UPDATE productos SET cantidad = ? WHERE id = ?"
        try:
            cursor.execute(sql, (nueva_cantidad, id_producto))
            conexion.commit()
            print(f"\n✅ ¡Inventario actualizado! '{nombre_prod}' ahora tiene {nueva_cantidad} unidades.")
        except sqlite3.Error as e:
            print(f"\n❌ Error al actualizar el stock: {e}")
        finally:
            conexion.close()

def eliminar_producto(id_producto):
    """Elimina definitivamente un producto de la base de datos por su ID."""
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        
        # Verificamos si existe antes de borrar
        cursor.execute("SELECT nombre FROM productos WHERE id = ?", (id_producto,))
        producto = cursor.fetchone()
        
        if not producto:
            print("\n❌ Error: No se encontró ningún producto con el ID especificado.")
            conexion.close()
            return
            
        sql = "DELETE FROM productos WHERE id = ?"
        try:
            cursor.execute(sql, (id_producto,))
            conexion.commit()
            print(f"\n🗑️ ¡Producto '{producto}' eliminado correctamente del sistema!")
        except sqlite3.Error as e:
            print(f"\n❌ Error al eliminar el producto: {e}")
        finally:
            conexion.close()