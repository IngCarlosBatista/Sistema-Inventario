import sqlite3
import hashlib
import os
import ttkbootstrap as tb
from tkinter import messagebox

ruta_actual = os.path.dirname(os.path.abspath(__file__))
ruta_db = os.path.abspath(os.path.join(ruta_actual, "..", "database", "inventario.db"))

class RegistroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📝 Registro de Usuario")
        self.root.geometry("350x300")
        
        tb.Label(self.root, text="Crear Nueva Cuenta", font=("Segoe UI", 14, "bold")).pack(pady=15)
        
        tb.Label(self.root, text="Usuario:").pack()
        self.ent_user = tb.Entry(self.root, width=30)
        self.ent_user.pack(pady=5)
        
        tb.Label(self.root, text="Contraseña:").pack()
        self.ent_pass = tb.Entry(self.root, show="*", width=30)
        self.ent_pass.pack(pady=5)
        
        btn_reg = tb.Button(self.root, text="Registrar Usuario", bootstyle="success", command=self.registrar)
        btn_reg.pack(pady=20)

    def registrar(self):
        user = self.ent_user.get()
        pwd = self.ent_pass.get()
        
        if not user or not pwd:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
            
        # Encriptación SHA-256
        pwd_hash = hashlib.sha256(pwd.encode('utf-8')).hexdigest()
        
        try:
            conn = sqlite3.connect(ruta_db)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (username, password_hash) VALUES (?, ?)", (user, pwd_hash))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Usuario registrado correctamente")
            self.root.destroy() # Cierra la ventana tras registrar
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El usuario ya existe")

if __name__ == "__main__":
    root = tb.Window(themename="flatly")
    app = RegistroApp(root)
    root.mainloop()