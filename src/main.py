import sys
import os
import sqlite3

# Forzar el directorio de trabajo a la ubicación de este script para evitar pérdidas con la BD
ruta_actual = os.path.dirname(os.path.abspath(__file__))
os.chdir(ruta_actual)

import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox

# Importamos la creación de tablas desde tu archivo existente conexion.py
from conexion import crear_tablas

# =====================================================================
# 📊 LÓGICA DE NEGOCIO E INTERACCIÓN CON LA BASE DE DATOS (Antes en inventario.py)
# =====================================================================

def obtener_conexion():
    """Establece conexión con la base de datos central en la carpeta superior."""
    # Sube un nivel para encontrar la carpeta 'database' tal como lo tienes estructurado
    ruta_db = os.path.abspath(os.path.join(ruta_actual, "..", "database", "inventario.db"))
    return sqlite3.connect(ruta_db)

def obtener_productos():
    """Trae todos los registros de la tabla productos."""
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, cantidad, precio, stock_minimo FROM productos")
        productos = cursor.fetchall()
        conn.close()
        return productos
    except Exception as e:
        print(f"Error al obtener productos: {e}")
        return []

def registrar_producto(nombre, descripcion, cantidad, precio, stock_minimo):
    """Inserta un nuevo producto en el almacén."""
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO productos (nombre, descripcion, cantidad, precio, stock_minimo)
            VALUES (?, ?, ?, ?, ?)
        """, (nombre, descripcion, cantidad, precio, stock_minimo))
        conn.commit()
        conn.close()
        return True, f"Producto '{nombre}' registrado correctamente."
    except Exception as e:
        return False, f"Error en la base de datos: {str(e)}"

def actualizar_stock(id_p, cantidad, accion):
    """Incrementa (entrada) o decrementa (salida) el stock de un ID."""
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        # Verificar si el producto existe y su cantidad actual
        cursor.execute("SELECT cantidad, nombre FROM productos WHERE id = ?", (id_p,))
        resultado = cursor.fetchone()
        
        if not resultado:
            conn.close()
            return False, f"El ID {id_p} no corresponde a ningún producto."
            
        cantidad_actual, nombre = resultado
        
        if accion == "entrada":
            nueva_cantidad = cantidad_actual + cantidad
        elif accion == "salida":
            if cantidad_actual < cantidad:
                conn.close()
                return False, f"Stock insuficiente. Solo quedan {cantidad_actual} unidades de {nombre}."
            nueva_cantidad = cantidad_actual - cantidad
            
        cursor.execute("UPDATE productos SET cantidad = ? WHERE id = ?", (nueva_cantidad, id_p))
        conn.commit()
        conn.close()
        return True, f"Stock de '{nombre}' actualizado a {nueva_cantidad} unidades."
    except Exception as e:
        return False, f"Error al actualizar: {str(e)}"

def eliminar_producto(id_p):
    """Elimina permanentemente un producto por su ID."""
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        cursor.execute("SELECT nombre FROM productos WHERE id = ?", (id_p,))
        resultado = cursor.fetchone()
        
        if not resultado:
            conn.close()
            return False, f"El ID {id_p} no existe."
            
        cursor.execute("DELETE FROM productos WHERE id = ?", (id_p,))
        conn.commit()
        conn.close()
        return True, f"Producto '{resultado}' eliminado del sistema."
    except Exception as e:
        return False, f"Error al eliminar: {str(e)}"


# =====================================================================
# 📦 INTERFAZ GRÁFICA DE USUARIO (GUI)
# =====================================================================

class SistemaInventarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📦 Sistema de Control de Inventario")
        self.root.geometry("1150x680")
        self.root.resizable(True, True)
        
        # Inicialización de la base de datos local usando tu conexion.py
        crear_tablas()
        
        # --- CONTENEDOR PRINCIPAL ---
        main_frame = tb.Frame(self.root, padding=20)
        main_frame.pack(fill=BOTH, expand=YES)
        
        # --- ENCABEZADO ESTILO BANNER PRO ---
        header_frame = tb.Frame(main_frame, bootstyle=PRIMARY, padding=12)
        header_frame.pack(fill=X, pady=(0, 20))
        
        header_label = tb.Label(
            header_frame, 
            text="📦 PANEL DE CONTROL DE INVENTARIO COMMERCIAL v1.0", 
            font=("Helvetica", 14, "bold"), 
            foreground="white",
            bootstyle=INVERSE
        )
        header_label.pack(anchor=CENTER)
        
        # --- ESTRUCTURA DEL CUERPO ---
        body_frame = tb.Frame(main_frame)
        body_frame.pack(fill=BOTH, expand=YES)
        
        # Panel Izquierdo (Módulos de Entrada de Datos)
        left_panel = tb.Frame(body_frame, padding=10)
        left_panel.pack(side=LEFT, fill=Y, padx=(0, 20))
        
        # Título del Panel Izquierdo
        lbl_titulo_left = tb.Label(left_panel, text="🛠️ GESTIÓN DE ALMACÉN", font=("Helvetica", 11, "bold"), bootstyle=PRIMARY)
        lbl_titulo_left.pack(anchor=W, pady=(0, 15))
        
        # Panel Derecho (Visualización del Stock)
        right_panel = tb.Frame(body_frame, padding=10)
        right_panel.pack(side=RIGHT, fill=BOTH, expand=YES)
        
        # Título del Panel Derecho
        lbl_titulo_right = tb.Label(right_panel, text="📊 STOCK ACTUAL EN TIEMPO REAL", font=("Helvetica", 11, "bold"), bootstyle=INFO)
        lbl_titulo_right.pack(anchor=W, pady=(0, 15))
        
        # --- FORMULARIO DE REGISTRO ---
        tb.Label(left_panel, text="Nombre del Producto:", font=("Helvetica", 10, "bold")).pack(anchor=W, pady=(0, 2))
        self.ent_nombre = tb.Entry(left_panel, width=30)
        self.ent_nombre.pack(anchor=W, pady=(0, 12))
        
        tb.Label(left_panel, text="Descripción:", font=("Helvetica", 10, "bold")).pack(anchor=W, pady=(0, 2))
        self.ent_desc = tb.Entry(left_panel, width=30)
        self.ent_desc.pack(anchor=W, pady=(0, 12))
        
        tb.Label(left_panel, text="Cantidad Inicial:", font=("Helvetica", 10, "bold")).pack(anchor=W, pady=(0, 2))
        self.ent_cant = tb.Entry(left_panel, width=30)
        self.ent_cant.pack(anchor=W, pady=(0, 12))
        
        tb.Label(left_panel, text="Precio Unitario ($):", font=("Helvetica", 10, "bold")).pack(anchor=W, pady=(0, 2))
        self.ent_precio = tb.Entry(left_panel, width=30)
        self.ent_precio.pack(anchor=W, pady=(0, 12))
        
        tb.Label(left_panel, text="Stock Mínimo Alerta:", font=("Helvetica", 10, "bold")).pack(anchor=W, pady=(0, 2))
        self.ent_min = tb.Entry(left_panel, width=30)
        self.ent_min.insert(0, "5")
        self.ent_min.pack(anchor=W, pady=(0, 18))
        
        btn_registrar = tb.Button(left_panel, text="📥 Registrar Producto", bootstyle=SUCCESS, width=28, command=self.ejecutar_registro)
        btn_registrar.pack(anchor=W, pady=(0, 15))
        
        # Divisor estético
        tb.Separator(left_panel, bootstyle=SECONDARY).pack(fill=X, pady=10)
        
        # --- PANEL DE TRANSACCIONES RÁPIDAS ---
        tb.Label(left_panel, text="Modificar Stock por ID:", font=("Helvetica", 10, "bold")).pack(anchor=W, pady=(0, 5))
        
        action_frame = tb.Frame(left_panel)
        action_frame.pack(anchor=W, pady=(0, 12))
        
        tb.Label(action_frame, text="ID:").grid(row=0, column=0, padx=(0, 5))
        self.ent_id_act = tb.Entry(action_frame, width=6)
        self.ent_id_act.grid(row=0, column=1, padx=(0, 12))
        
        tb.Label(action_frame, text="Cant:").grid(row=0, column=2, padx=(0, 5))
        self.ent_cant_act = tb.Entry(action_frame, width=8)
        self.ent_cant_act.grid(row=0, column=3)
        
        btn_frame = tb.Frame(left_panel)
        btn_frame.pack(fill=X, pady=(0, 15))
        
        tb.Button(btn_frame, text="➕ Entrada", bootstyle=INFO, width=12, command=lambda: self.ejecutar_cambio_stock("entrada")).pack(side=LEFT, padx=(0, 6))
        tb.Button(btn_frame, text="➖ Salida", bootstyle=WARNING, width=12, command=lambda: self.ejecutar_cambio_stock("salida")).pack(side=LEFT)
        
        # Botón de Eliminación Crítica
        tb.Button(left_panel, text="🗑️ Eliminar Producto por ID", bootstyle=DANGER, width=28, command=self.ejecutar_eliminacion).pack(anchor=W)
        
        # --- TABLA TREEVIEW ---
        columnas = ("id", "nombre", "cantidad", "precio", "estado")
        self.tabla = tb.Treeview(right_panel, columns=columnas, show="headings", bootstyle=INFO)
        self.tabla.pack(fill=BOTH, expand=YES, side=LEFT)
        
        # Barra de desplazamiento vertical
        scrollbar = tb.Scrollbar(right_panel, orient=VERTICAL, command=self.tabla.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        
        # Configuración de Cabeceras
        self.tabla.heading("id", text="ID", anchor=CENTER)
        self.tabla.heading("nombre", text="Producto", anchor=W)
        self.tabla.heading("cantidad", text="Existencias", anchor=CENTER)
        self.tabla.heading("precio", text="Precio Unitario", anchor=E)
        self.tabla.heading("estado", text="Estado de Alerta", anchor=CENTER)
        
        # Ajuste de Columnas
        self.tabla.column("id", width=60, anchor=CENTER)
        self.tabla.column("nombre", width=280, anchor=W)
        self.tabla.column("cantidad", width=110, anchor=CENTER)
        self.tabla.column("precio", width=140, anchor=E)
        self.tabla.column("estado", width=160, anchor=CENTER)
        
        # Sincronización de base de datos en el arranque
        self.cargar_tabla_datos()

    def cargar_tabla_datos(self):
        """Limpia y repobla la tabla con la información en tiempo real."""
        for item in self.tabla.get_children():
            self.tabla.delete(item)
            
        productos = obtener_productos()
        for prod in productos:
            id_p, nombre, cant, precio, min_s = prod
            estado = "⚠️ Stock Bajo" if cant <= min_s else "✅ OK"
            self.tabla.insert("", END, values=(id_p, nombre, cant, f"${precio:,.2f}", estado))

    def limpiar_formulario(self):
        self.ent_nombre.delete(0, END)
        self.ent_desc.delete(0, END)
        self.ent_cant.delete(0, END)
        self.ent_precio.delete(0, END)
        self.ent_min.delete(0, END)
        self.ent_min.insert(0, "5")

    def ejecutar_registro(self):
        nombre = self.ent_nombre.get().strip()
        descripcion = self.ent_desc.get().strip()
        
        if not nombre:
            messagebox.showerror("Error de Validacion", "El nombre del producto es obligatorio.")
            return
            
        try:
            get_cant_val = self.ent_cant.get().strip()
            get_precio_val = self.ent_precio.get().strip()
            get_min_val = self.ent_min.get().strip()
            
            if not get_cant_val or not get_precio_val:
                messagebox.showerror("Error de Validacion", "Cantidad e Inicial son obligatorios.")
                return

            cantidad = int(get_cant_val)
            precio = float(get_precio_val)
            stock_minimo = int(get_min_val or 5)
            
            exito, msg = registrar_producto(nombre, descripcion, cantidad, precio, stock_minimo)
            if exito:
                messagebox.showinfo("Operacion Exitosa", msg)
                self.limpiar_formulario()
                self.cargar_tabla_datos()
            else:
                messagebox.showerror("Error del Sistema", msg)
        except ValueError:
            messagebox.showerror("Error de Validacion", "Cantidad, Precio y Stock Mínimo deben ser numéricos.")

    def ejecutar_cambio_stock(self, accion):
        try:
            id_p = int(self.ent_id_act.get().strip())
            cant_cambio = int(self.ent_cant_act.get().strip())
            
            if cant_cambio <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor a cero.")
                return
                
            exito, msg = actualizar_stock(id_p, cant_cambio, accion)
            if exito:
                messagebox.showinfo("Sincronizado", msg)
                self.ent_id_act.delete(0, END)
                self.ent_cant_act.delete(0, END)
                self.cargar_tabla_datos()
            else:
                messagebox.showerror("Regla de Almacen", msg)
        except ValueError:
            messagebox.showerror("Error de Entrada", "Complete ID y Cantidad con valores numéricos enteros.")

    def ejecutar_eliminacion(self):
        try:
            id_p = int(self.ent_id_act.get().strip())
            
            confirmacion = messagebox.askyesno("Confirmacion de Seguridad", f"¿Desea borrar permanentemente el ID {id_p}?")
            if confirmacion:
                exito, msg = eliminar_producto(id_p)
                if exito:
                    messagebox.showinfo("Eliminado", msg)
                    self.ent_id_act.delete(0, END)
                    self.cargar_tabla_datos()
                else:
                    messagebox.showerror("Error", msg)
        except ValueError:
            messagebox.showerror("Error de Entrada", "Escriba un ID numérico en el recuadro para ejecutar la eliminación.")

if __name__ == "__main__":
    app_root = tb.Window(themename="flatly")
    app = SistemaInventarioApp(app_root)
    app_root.mainloop()