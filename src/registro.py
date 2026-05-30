import ttkbootstrap as tb
from tkinter import messagebox, filedialog
import os
import shutil
from PIL import Image, ImageTk

# Importación específica
from conexion import registrar_usuario as registrar_en_bd

class RegistroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Registrar Usuario")
        self.root.geometry("400x750")
        self.path_foto = ""

        # --- DISEÑO ---
        container = tb.Frame(self.root, padding=30)
        container.pack(expand=True, fill="both")

        # --- LOGO ---
        ruta_logo = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "logo.png"))
        if os.path.exists(ruta_logo):
            try:
                img = Image.open(ruta_logo)
                img = img.resize((200, 80), Image.Resampling.LANCZOS)
                self.logo_tk = ImageTk.PhotoImage(img, master=self.root)
                tb.Label(container, image=self.logo_tk).pack(pady=(0, 20))
            except Exception as e:
                print(f"Error cargando logo: {e}")

        # --- TÍTULO ---
        tb.Label(container, text="Registrar Usuario", font=("Segoe UI", 18, "bold"), bootstyle="primary").pack(pady=(0, 20))

        # --- CAMPOS ---
        self.ent_nombre = self._crear_campo(container, "Nombre:")
        self.ent_apellido = self._crear_campo(container, "Apellido:")
        self.ent_user = self._crear_campo(container, "Usuario:")
        self.ent_pass = self._crear_campo(container, "Contraseña:", is_password=True)
        self.ent_conf_pass = self._crear_campo(container, "Confirmar Contraseña:", is_password=True)

        # --- BOTÓN FOTO ---
        tb.Button(container, text="Seleccionar Foto de Perfil", bootstyle="info-outline", command=self.subir_foto).pack(pady=10, fill="x")
        self.lbl_status_foto = tb.Label(container, text="Sin foto seleccionada", font=("Segoe UI", 8), foreground="gray")
        self.lbl_status_foto.pack()

        # --- BOTÓN REGISTRAR ---
        tb.Button(container, text="Registrar", bootstyle="success-outline", command=self.registrar_usuario).pack(pady=20, fill="x")

    def _crear_campo(self, parent, label_text, is_password=False):
        tb.Label(parent, text=label_text, font=("Segoe UI", 10, "bold")).pack(anchor="w")
        entry = tb.Entry(parent, show="*" if is_password else "", width=30, font=("Segoe UI", 11))
        entry.pack(pady=(5, 10), fill="x")
        return entry

    def subir_foto(self):
        archivo = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")])
        if archivo:
            dir_profiles = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "profiles"))
            os.makedirs(dir_profiles, exist_ok=True)
            
            username = self.ent_user.get() or "usuario_temp"
            ext = os.path.splitext(archivo)[1]
            nuevo_path = os.path.join(dir_profiles, f"{username}{ext}")
            
            shutil.copy(archivo, nuevo_path)
            self.path_foto = nuevo_path
            self.lbl_status_foto.config(text=f"Foto cargada correctamente", foreground="green")

    def registrar_usuario(self):
        usuario = self.ent_user.get()
        password = self.ent_pass.get()
        conf_password = self.ent_conf_pass.get()
        nombre = self.ent_nombre.get()
        apellido = self.ent_apellido.get()

        if not (nombre and apellido and usuario and password and conf_password):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        if password != conf_password:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return

        # AQUÍ ESTÁ EL CAMBIO: Pasamos nombre y apellido a la función
        if registrar_en_bd(usuario, password, self.path_foto, nombre, apellido):
            messagebox.showinfo("Éxito", f"Usuario {usuario} registrado correctamente")
            self.root.destroy()
        else:
            messagebox.showerror("Error", "No se pudo registrar. El usuario ya existe.")

if __name__ == "__main__":
    root = tb.Window(themename="flatly")
    app = RegistroApp(root)
    root.mainloop()