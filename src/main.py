import sys
import os
import sqlite3
import pandas as pd
from tkinter import filedialog, messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from conexion import crear_tablas
from PIL import Image, ImageTk # Importación necesaria para imágenes

# Forzar el directorio de trabajo a la ubicación de este script
ruta_actual = os.path.dirname(os.path.abspath(__file__))
os.chdir(ruta_actual)

# =====================================================================
# 📊 LÓGICA DE NEGOCIO E INTERACCIÓN CON LA BASE DE DATOS
# =====================================================================

def obtener_conexion():
    ruta_db = os.path.abspath(os.path.join(ruta_actual, "..", "database", "inventario.db"))
    return sqlite3.connect(ruta_db)

def obtener_productos():
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
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
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
        return True, f"Stock de '{nombre}' actualizado."
    except Exception as e:
        return False, f"Error al actualizar: {str(e)}"

def eliminar_producto(id_p):
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
        return True, f"Producto '{resultado}' eliminado."
    except Exception as e:
        return False, f"Error al eliminar: {str(e)}"

# =====================================================================
# 📦 INTERFAZ GRÁ GRÁFICA DE USUARIO
# =====================================================================

class SistemaInventarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📦 Sistema de Control de Inventario Premium")
        self.root.geometry("1200x720")
        self.root.resizable(True, True)
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        crear_tablas()
        self.fuente_labels = ("Segoe UI", 10, "bold")
        
        style = tb.Style()
        style.configure("Treeview.Heading", background="#2c3e50", foreground="#ffffff", font=("Segoe UI", 10, "bold"))
        
        main_frame = tb.Frame(self.root, padding=20)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # --- ENCABEZADO ---
        header_frame = tb.Frame(main_frame, padding=15)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        
        # --- LOGO (Izquierda) ---
        self.logo_w, self.logo_h = 200, 80
        ruta_logo = os.path.join(ruta_actual, "..", "assets", "logo.png")
        if os.path.exists(ruta_logo):
            img = Image.open(ruta_logo)
            img = img.resize((self.logo_w, self.logo_h), Image.Resampling.LANCZOS)
            self.logo_tk = ImageTk.PhotoImage(img)
            tb.Label(header_frame, image=self.logo_tk).pack(side=LEFT, padx=(0, 15))

        # --- TÍTULO (Centro) ---
        header_label = tb.Label(header_frame, text="PANEL DE CONTROL", 
                                font=("Segoe UI", 18, "bold"), foreground="#2980b9")
        header_label.pack(side=LEFT, expand=True)
        
        # --- PANEL IZQUIERDO ---
        left_panel = tb.Frame(main_frame, padding=10)
        left_panel.grid(row=1, column=0, sticky="nw")
        
        lbl_titulo_left = tb.Label(left_panel, text="GESTIÓN DE ALMACÉN", font=("Segoe UI", 13, "bold"), foreground="#27ae60")
        lbl_titulo_left.pack(anchor=W, pady=(0, 15))
        
        tb.Label(left_panel, text="Nombre del Producto:", font=self.fuente_labels).pack(anchor=W, pady=(0, 2))
        self.ent_nombre = tb.Entry(left_panel, width=32, font=("Segoe UI", 10))
        self.ent_nombre.pack(anchor=W, pady=(0, 12))
        
        tb.Label(left_panel, text="Descripción:", font=self.fuente_labels).pack(anchor=W, pady=(0, 2))
        self.ent_desc = tb.Entry(left_panel, width=32, font=("Segoe UI", 10))
        self.ent_desc.pack(anchor=W, pady=(0, 12))
        
        tb.Label(left_panel, text="Cantidad Inicial:", font=self.fuente_labels).pack(anchor=W, pady=(0, 2))
        self.ent_cant = tb.Entry(left_panel, width=32, font=("Segoe UI", 10))
        self.ent_cant.pack(anchor=W, pady=(0, 12))
        
        tb.Label(left_panel, text="Precio Unitario ($):", font=self.fuente_labels).pack(anchor=W, pady=(0, 2))
        self.ent_precio = tb.Entry(left_panel, width=32, font=("Segoe UI", 10))
        self.ent_precio.pack(anchor=W, pady=(0, 12))
        
        tb.Label(left_panel, text="Stock Mínimo Alerta:", font=self.fuente_labels).pack(anchor=W, pady=(0, 2))
        self.ent_min = tb.Entry(left_panel, width=32, font=("Segoe UI", 10))
        self.ent_min.pack(anchor=W, pady=(0, 18))
        
        btn_registrar = tb.Button(left_panel, text="📥 Registrar Producto", bootstyle="success-outline", width=30, command=self.ejecutar_registro)
        btn_registrar.pack(anchor=W, pady=(0, 15))
        
        tb.Separator(left_panel).pack(fill=X, pady=10)
        
        tb.Label(left_panel, text="Modificar Stock por ID:", font=self.fuente_labels).pack(anchor=W, pady=(0, 5))
        action_frame = tb.Frame(left_panel)
        action_frame.pack(anchor=W, pady=(0, 12))
        
        tb.Label(action_frame, text="ID:", font=self.fuente_labels).grid(row=0, column=0, padx=(0, 5))
        self.ent_id_act = tb.Entry(action_frame, width=6, font=("Segoe UI", 10))
        self.ent_id_act.grid(row=0, column=1, padx=(0, 12))
        
        tb.Label(action_frame, text="Cant:", font=self.fuente_labels).grid(row=0, column=2, padx=(0, 5))
        self.ent_cant_act = tb.Entry(action_frame, width=8, font=("Segoe UI", 10))
        self.ent_cant_act.grid(row=0, column=3)
        
        btn_frame = tb.Frame(left_panel)
        btn_frame.pack(fill=X, pady=(0, 15))
        
        tb.Button(btn_frame, text="➕ Entrada", bootstyle="info-outline", width=13, command=lambda: self.ejecutar_cambio_stock("entrada")).pack(side=LEFT, padx=(0, 8))
        tb.Button(btn_frame, text="➖ Salida", bootstyle="warning-outline", width=13, command=lambda: self.ejecutar_cambio_stock("salida")).pack(side=LEFT)
        
        tb.Button(left_panel, text="🗑️ Eliminar Producto por ID", bootstyle="danger-outline", width=30, command=self.ejecutar_eliminacion).pack(anchor=W)
        
        # --- PANEL DERECHO ---
        right_panel = tb.Frame(main_frame, padding=10)
        right_panel.grid(row=1, column=1, sticky="nsew")
        right_panel.columnconfigure(0, weight=1)
        right_panel.rowconfigure(1, weight=1)
        
        # --- CABECERA PANEL DERECHO (Título + Buscador) ---
        header_right_frame = tb.Frame(right_panel)
        header_right_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        
        tb.Label(header_right_frame, text="Stock en Tiempo Real", font=("Segoe UI", 14, "bold"), foreground="#2980b9").pack(side=LEFT)
        
        self.ent_busqueda = tb.Entry(header_right_frame, width=25)
        self.ent_busqueda.pack(side=RIGHT)
        self.ent_busqueda.insert(0, "Buscar producto...")
        self.ent_busqueda.bind("<FocusIn>", lambda e: self.ent_busqueda.delete(0, END) if self.ent_busqueda.get() == "Buscar producto..." else None)
        self.ent_busqueda.bind("<KeyRelease>", self.filtrar_tabla)
        
        table_container = tb.Frame(right_panel)
        table_container.grid(row=1, column=0, sticky="nsew", pady=(0, 20))
        table_container.columnconfigure(0, weight=1)
        table_container.rowconfigure(0, weight=1)
        
        columnas = ("id", "nombre", "cantidad", "precio", "estado")
        self.tabla = tb.Treeview(table_container, columns=columnas, show="headings")
        self.tabla.grid(row=0, column=0, sticky="nsew")
        
        scrollbar = tb.Scrollbar(table_container, orient=VERTICAL, command=self.tabla.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tabla.configure(yscrollcommand=scrollbar.set)
        
        self.tabla.heading("id", text="ID")
        self.tabla.heading("nombre", text="Producto")
        self.tabla.heading("cantidad", text="Existencias")
        self.tabla.heading("precio", text="Precio Unitario")
        self.tabla.heading("estado", text="Estado de Alerta")
        
        self.tabla.column("id", width=60, anchor=CENTER)
        self.tabla.column("nombre", width=280, anchor=W)
        self.tabla.column("cantidad", width=110, anchor=CENTER)
        self.tabla.column("precio", width=140, anchor=E)
        self.tabla.column("estado", width=160, anchor=CENTER)
        
        self.dash_frame = tb.Labelframe(right_panel, text="RESUMEN EJECUTIVO DEL ALMACÉN")
        self.dash_frame.grid(row=2, column=0, sticky="ew")
        self.dash_frame.configure(padding=15)
        
        self.dash_frame.columnconfigure((0, 1, 2), weight=1)
        
        self.card_productos_val = tb.Label(self.dash_frame, text="0", font=("Segoe UI", 18, "bold"), foreground="#2980b9")
        self.card_productos_val.grid(row=0, column=0, sticky=S)
        tb.Label(self.dash_frame, text="Ítems Registrados", font=("Segoe UI", 9, "bold")).grid(row=1, column=0, sticky=N)
        
        self.card_valor_val = tb.Label(self.dash_frame, text="$0.00", font=("Segoe UI", 18, "bold"), foreground="#27ae60")
        self.card_valor_val.grid(row=0, column=1, sticky=S)
        tb.Label(self.dash_frame, text="Capital en Stock", font=("Segoe UI", 9, "bold")).grid(row=1, column=1, sticky=N)
        
        self.card_alertas_val = tb.Label(self.dash_frame, text="0", font=("Segoe UI", 18, "bold"), foreground="#c0392b")
        self.card_alertas_val.grid(row=0, column=2, sticky=S)
        tb.Label(self.dash_frame, text="Alertas de Stock Bajo", font=("Segoe UI", 9, "bold")).grid(row=1, column=2, sticky=N)
        
        btn_excel = tb.Button(right_panel, text="📊 Exportar Reporte a Excel", bootstyle="success-outline", command=self.exportar_excel)
        btn_excel.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        
        self.cargar_tabla_datos()
    
    def filtrar_tabla(self, event=None):
        """Filtra la tabla según el texto en el buscador"""
        query = self.ent_busqueda.get().lower()
        if query == "buscar producto...": query = ""
        
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        productos = obtener_productos()
        for prod in productos:
            id_p, nombre, cant, precio, min_s = prod
            if query in nombre.lower():
                estado = "⚠️ Stock Bajo" if cant <= min_s else "✅ OK"
                self.tabla.insert("", END, values=(id_p, nombre, cant, f"${precio:,.2f}", estado))

    def exportar_excel(self):
        try:
            productos = obtener_productos()
            if not productos:
                messagebox.showwarning("Aviso", "No hay datos para exportar.")
                return
            archivo_guardado = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], title="Guardar reporte", initialfile="Reporte_Inventario.xlsx")
            if not archivo_guardado: return
            df = pd.DataFrame(productos, columns=["ID", "Nombre", "Cantidad", "Precio", "Stock Mínimo"])
            df.to_excel(archivo_guardado, index=False)
            messagebox.showinfo("Éxito", f"Reporte guardado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el archivo: {e}")
    
    def cargar_tabla_datos(self):
        for item in self.tabla.get_children(): self.tabla.delete(item)
        productos = obtener_productos()
        total_items = len(productos)
        capital_total = 0.0
        alertas_activas = 0
        for prod in productos:
            id_p, nombre, cant, precio, min_s = prod
            capital_total += (cant * precio)
            estado = "⚠️ Stock Bajo" if cant <= min_s else "✅ OK"
            if cant <= min_s: alertas_activas += 1
            self.tabla.insert("", END, values=(id_p, nombre, cant, f"${precio:,.2f}", estado))
        
        self.card_productos_val.config(text=str(total_items))
        self.card_valor_val.config(text=f"${capital_total:,.2f}")
        self.card_alertas_val.config(text=str(alertas_activas))
    
    def limpiar_formulario(self):
        self.ent_nombre.delete(0, END)
        self.ent_desc.delete(0, END)
        self.ent_cant.delete(0, END)
        self.ent_precio.delete(0, END)
        self.ent_min.delete(0, END)
    
    def ejecutar_registro(self):
        nombre = self.ent_nombre.get().strip()
        descripcion = self.ent_desc.get().strip()
        if not nombre:
            messagebox.showerror("Error", "El nombre es obligatorio")
            return
        try:
            valor_min = int(self.ent_min.get()) if self.ent_min.get().strip() else 0
            exito, msg = registrar_producto(nombre, descripcion, int(self.ent_cant.get()), float(self.ent_precio.get()), valor_min)
            if exito:
                messagebox.showinfo("Éxito", msg)
                self.limpiar_formulario()
                self.cargar_tabla_datos()
            else:
                messagebox.showerror("Error", msg)
        except ValueError:
            messagebox.showerror("Error", "Datos numéricos inválidos")
    
    def ejecutar_cambio_stock(self, accion):
        try:
            exito, msg = actualizar_stock(int(self.ent_id_act.get()), int(self.ent_cant_act.get()), accion)
            if exito:
                self.cargar_tabla_datos()
            else:
                messagebox.showerror("Error", msg)
        except ValueError:
            messagebox.showerror("Error", "IDs o cantidades inválidas")
    
    def ejecutar_eliminacion(self):
        try:
            if messagebox.askyesno("Confirmar", "¿Eliminar?"):
                exito, msg = eliminar_producto(int(self.ent_id_act.get()))
                if exito:
                    self.cargar_tabla_datos()
                else:
                    messagebox.showerror("Error", msg)
        except ValueError:
            messagebox.showerror("Error", "ID inválido")

if __name__ == "__main__":
    app_root = tb.Window(themename="flatly")
    app = SistemaInventarioApp(app_root)
    app_root.mainloop()