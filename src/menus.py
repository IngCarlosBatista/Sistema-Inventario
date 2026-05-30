import ttkbootstrap as tb
from tkinter import Toplevel, messagebox, END

# --- FUNCIÓN PERFIL ---
def abrir_perfil(root, datos_usuario):
    ventana = Toplevel(root)
    ventana.title("Mi Perfil")
    ventana.geometry("450x550")
    ventana.resizable(False, False)
    
    frame = tb.Frame(ventana, padding=20)
    frame.pack(fill="both", expand=True)
    
    lbl_icono = tb.Label(frame, text="👤", font=("Segoe UI", 48))
    lbl_icono.pack(pady=10)
    
    tb.Label(frame, text=datos_usuario.get("nombre", "Usuario"), font=("Segoe UI", 16, "bold")).pack()
    tb.Label(frame, text=f"Rol: {datos_usuario.get('rol', 'Usuario')}", font=("Segoe UI", 10), foreground="#7f8c8d").pack(pady=5)
    
    tb.Separator(frame).pack(fill="x", pady=15)
    
    info_frame = tb.LabelFrame(frame, text="Información Detallada", padding=15)
    info_frame.pack(fill="x", pady=10)
    
    campos = [
        ("Nombre Completo:", datos_usuario.get("nombre", "N/A")),
        ("Correo Electrónico:", datos_usuario.get("email", "N/A")),
        ("Teléfono:", datos_usuario.get("telefono", "N/A")),
        ("Departamento:", datos_usuario.get("depto", "N/A")),
        ("Fecha Ingreso:", datos_usuario.get("fecha", "N/A")),
    ]
    
    for i, (label, valor) in enumerate(campos):
        tb.Label(info_frame, text=label, font=("Segoe UI", 9, "bold")).grid(row=i, column=0, sticky="w", pady=5, padx=5)
        tb.Label(info_frame, text=valor, font=("Segoe UI", 9)).grid(row=i, column=1, sticky="w", pady=5, padx=5)
    
    if datos_usuario.get("rol") == "Administrador":
        tb.Button(frame, text="Editar Perfil", bootstyle="primary", width=25).pack(pady=20)
    else:
        tb.Label(frame, text="Acceso limitado: Contacte al administrador", 
                 font=("Segoe UI", 8, "italic"), foreground="red").pack(pady=10)

    tb.Button(frame, text="Cerrar", command=ventana.destroy, bootstyle="secondary").pack()

# --- FUNCIÓN CONFIGURACIÓN ---
def abrir_configuracion(root):
    ventana = Toplevel(root)
    ventana.title("Configuración")
    ventana.geometry("400x350")
    
    notebook = tb.Notebook(ventana)
    notebook.pack(pady=10, padx=10, fill="both", expand=True)
    
    # Pestaña General
    frame_gen = tb.Frame(notebook, padding=15)
    notebook.add(frame_gen, text="General")
    tb.Label(frame_gen, text="Empresa:").pack(anchor="w")
    tb.Entry(frame_gen).pack(fill="x", pady=5)
    
    # Pestaña Backup
    frame_back = tb.Frame(notebook, padding=15)
    notebook.add(frame_back, text="Respaldo")
    tb.Label(frame_back, text="Ruta de guardado:").pack(anchor="w")
    tb.Entry(frame_back).pack(fill="x", pady=5)
    
    tb.Button(ventana, text="Guardar", bootstyle="success", command=ventana.destroy).pack(pady=10)

# --- FUNCIÓN CAMBIAR CONTRASEÑA ---
def abrir_cambiar_contrasena(root):
    ventana = Toplevel(root)
    ventana.title("Seguridad")
    ventana.geometry("350x300")
    
    frame = tb.Frame(ventana, padding=20)
    frame.pack(fill="both", expand=True)
    
    tb.Label(frame, text="Contraseña Actual:").pack(anchor="w")
    tb.Entry(frame, show="*").pack(fill="x", pady=5)
    
    tb.Label(frame, text="Nueva Contraseña:").pack(anchor="w", pady=(10, 0))
    tb.Entry(frame, show="*").pack(fill="x", pady=5)
    
    tb.Label(frame, text="Confirmar Contraseña:").pack(anchor="w", pady=(10, 0))
    tb.Entry(frame, show="*").pack(fill="x", pady=5)
    
    tb.Button(frame, text="Actualizar", bootstyle="warning", command=ventana.destroy).pack(pady=20)

# --- FUNCIÓN TEMA VISUAL ---
def abrir_tema_visual(root):
    ventana = Toplevel(root)
    ventana.title("Cambiar Tema")
    ventana.geometry("300x250")
    
    frame = tb.Frame(ventana, padding=20)
    frame.pack(fill="both", expand=True)
    
    # Lista ampliada de temas disponibles en ttkbootstrap
    temas = [
        "flatly", "cosmo", "darkly", "superhero", "cyborg", 
        "litera", "minty", "pulse", "sandstone", "united", 
        "yeti", "vapor", "solar", "lux", "sketchy"
    ]
    
    tb.Label(frame, text="Selecciona un tema:").pack(pady=5)
    combo = tb.Combobox(frame, values=temas, state="readonly")
    combo.pack(pady=10)
    
    def aplicar_tema():
        nuevo_tema = combo.get()
        if nuevo_tema:
            root.style.theme_use(nuevo_tema)
            messagebox.showinfo("Tema", f"Tema cambiado a {nuevo_tema}")
            ventana.destroy()
            
    tb.Button(frame, text="Aplicar", bootstyle="info", command=aplicar_tema).pack(pady=10)