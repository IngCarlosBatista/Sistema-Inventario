import ttkbootstrap as tb
from tkinter import messagebox
import os
import sys

# --- DEBUG: ESTO ES CRUCIAL ---
import main
print(f"DEBUG: El archivo main.py que se está importando es: {main.__file__}")
from main import SistemaInventarioApp

from conexion import verificar_usuario
from registro import RegistroApp


class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔑 Iniciar Sesión")
        self.root.geometry("400x480")

        # --- DISEÑO ---
        container = tb.Frame(self.root, padding=30)
        container.pack(expand=True, fill="both")

        tb.Label(
            container,
            text="Bienvenido al Sistema",
            font=("Segoe UI", 20, "bold"),
            bootstyle="primary"
        ).pack(pady=(0, 30))

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

        btn_login = tb.Button(
            container,
            text="Ingresar al Sistema",
            bootstyle="success-outline",
            command=self.verificar_login
        )
        btn_login.pack(pady=10, fill="x")

        btn_reg = tb.Button(
            container,
            text="¿No tienes cuenta? Regístrate",
            bootstyle="info-link",
            command=self.abrir_registro
        )
        btn_reg.pack(pady=10)

    def abrir_registro(self):
        ventana_registro = tb.Toplevel(self.root)
        RegistroApp(ventana_registro)

    def verificar_login(self):
        username = self.ent_user.get()
        password = self.ent_pass.get()

        if verificar_usuario(username, password):

            print("=" * 80)
            print("CLASE IMPORTADA DESDE:")
            print(SistemaInventarioApp.__module__)
            print(main.__file__)
            print("=" * 80)

            # NO destruir el root principal
            self.root.withdraw()

            # Crear ventana hija
            ventana_principal = tb.Toplevel(self.root)
            ventana_principal.geometry("1200x750")

            # Cerrar todo al salir
            ventana_principal.protocol(
                "WM_DELETE_WINDOW",
                self.root.destroy
            )

            # Inicializar sistema
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