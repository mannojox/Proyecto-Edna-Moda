import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

# Paleta de colores
colores = {
    "fondo": "#02c39a",
    "boton": "#fb8500",
    "texto_boton": "#03045e",
}

# Ventana principal
ventana = tk.Tk()
ventana.title("FashionHolic")  


ancho_ventana = 800
alto_ventana = 600
ventana.geometry(f"{ancho_ventana}x{alto_ventana}")

# Color de fondo de la ventana
ventana.config(bg=colores["fondo"])


marco_principal = ttk.Frame(ventana, style="fondo.TFrame") 
marco_principal.pack(padx=10, pady=10)


estilo_fondo = ttk.Style()
estilo_fondo.configure("fondo.TFrame", background=colores["fondo"])


etiqueta_titulo = ttk.Label(marco_principal,
                         text="FashionHolic",
                         font=("Arial", 30, "bold"),  # Set font using tuple
                         background=colores["fondo"])  # Set background color
etiqueta_titulo.pack(pady=20)


def seleccionar_archivo():
    ruta_archivo = filedialog.askopenfilename(
        initialdir="C:/",
        title="Seleccionar archivo",
        filetypes=(("Archivos de imagen", "*.jpg *.png *.gif"), ("Todos los archivos", "*.*"))
    )
    if ruta_archivo:
        # Crea una nueva ventana donde se muestra el resultado
        nueva_ventana = tk.Toplevel(ventana)
        nueva_ventana.title("Resultado")
        nueva_ventana.geometry("300x150")
        nueva_ventana.config(bg=colores["fondo"])

        # Crea un label en la nueva ventana donde se imprime el resultado
        etiqueta_mensaje = ttk.Label(nueva_ventana,
                                     text="Imagen seleccionada",
                                     font=("Arial", 20, "bold"),
                                     background=colores["fondo"])
        etiqueta_mensaje.pack(pady=20)


boton_seleccionar = ttk.Button(marco_principal,
                               text="Seleccionar archivo",
                               command=seleccionar_archivo,
                               style="boton.TButton",
                               padding=10,
                               )
boton_seleccionar.pack(pady=20)

# Estilo del boton
estilo_boton = ttk.Style()
estilo_boton.configure("boton.TButton",
                      background=colores["boton"],
                      foreground=colores["texto_boton"])

# Corre la GUI
ventana.mainloop()
