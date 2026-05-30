import ttkbootstrap as tb
from tkinter import messagebox
import os
import sys
from PIL import Image, ImageTk

# --- DEBUG ---
import main
from main import SistemaInventarioApp
from conexion import verificar_usuario
from registro import RegistroApp

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔑 Iniciar Sesión")
        self.root.geometry("400x580")

        # --- DISEÑO ---
        container = tb.Frame(self.root, padding=30)
        container.pack(expand=True, fill="both")

        # --- LOGO ---
        # Asegura que la ruta busque en la carpeta correcta
        ruta_logo = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "assets", "logo.png")
        )

        if os.path.exists(ruta_logo):
            img = Image.open(ruta_logo)
            img = img.resize((200, 80), Image.Resampling.LANCZOS)
            self.logo_tk = ImageTk.PhotoImage(img, master=self.root)
            tb.Label(container, image=self.logo_tk).pack(pady=(0, 20))

        # --- TÍTULO ---
        tb.Label(
            container,
            text="Iniciar Sesión",
            font=("Segoe UI", 18, "bold"),
            bootstyle="primary"
        ).pack(pady=(0, 20))

        # --- CAMPOS ---
        tb.Label(
            container,
            text="Usuario:",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")

        self.ent_user = tb.Entry(
            container,
            width=30,
            font=("Segoe UI", 11)
        )
        self.ent_user.pack(pady=(5, 15), fill="x")

        tb.Label(
            container,
            text="Contraseña:",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")

        self.ent_pass = tb.Entry(
            container,
            show="*",
            width=30,
            font=("Segoe UI", 11)
        )
        self.ent_pass.pack(pady=(5, 20), fill="x")

        # --- BOTONES ---
        btn_login = tb.Button(
            container,
            text="Ingresar al Sistema",
            bootstyle="success-outline",
            command=self.verificar_login
        )
        btn_login.pack(pady=10, fill="x")

        btn_reg = tb.Button(
            container,
            text="¿No tienes una cuenta? Regístrate aquí",
            bootstyle="link-success",
            command=self.abrir_registro
        )
        btn_reg.pack(pady=10, fill="x")

    def abrir_registro(self):
        ventana_registro = tb.Toplevel(self.root)
        # Aseguramos que la ventana llame a la clase del archivo registro.py
        RegistroApp(ventana_registro)

    def verificar_login(self):
        username = self.ent_user.get()
        password = self.ent_pass.get()

        if verificar_usuario(username, password):
            self.root.withdraw()

            ventana_principal = tb.Toplevel(self.root)
            ventana_principal.geometry("1200x750")
            ventana_principal.protocol(
                "WM_DELETE_WINDOW",
                self.root.destroy
            )

            SistemaInventarioApp(ventana_principal)

        else:
            messagebox.showerror(
                "Error",
                "Usuario o contraseña incorrectos"
            )


if __name__ == "__main__":
    root = tb.Window(themename="flatly")
    app = LoginApp(root)
    root.mainloop()