#Este programa no corre porque necesita de las funciones del backend, solo es demostrativo de la parte
#del frontend. Para encontrar el programa completo, dirigirse al archivo "version_final.py"

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from tkinter import Label
from PIL import Image, ImageTk


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

#Imagen del logo
imagen1 = Image.open("logo.jpeg")
imagen1 = imagen1.resize((400, 400))
# Convertir la imagen en un objeto PhotoImage
imagen_tk = ImageTk.PhotoImage(imagen1)

# Crear un widget de Label para mostrar la imagen
label_imagen = Label(ventana, image=imagen_tk)
label_imagen.pack()

def seleccionar_archivo():
    ruta_archivo = filedialog.askopenfilename(
        initialdir="C:/",
        title="Seleccionar archivo",
        filetypes=(("Archivos de imagen", "*.jpg *.png *.gif"), ("Todos los archivos", "*.*"))
    )
    if ruta_archivo:
        try:
            # Crear la nueva ventana
            nueva_ventana = tk.Toplevel(ventana)
            nueva_ventana.title("Resultado")
            nueva_ventana.geometry("800x600")
            nueva_ventana.config(bg=colores["fondo"])
            # Abrir la ventana en pantalla completa
            nueva_ventana.attributes('-fullscreen', True)

            #Funcion para salir de fullscreen
            def salir_pantalla_completa(event):
                nueva_ventana.attributes('-fullscreen', False)

            #Asocia la funcion al evento de presionar Escape en el teclado
            nueva_ventana.bind("<Escape>", salir_pantalla_completa)

            # Obtener los colores dominantes usando el backend
            colores_dominantes = obtener_colores(ruta_archivo)

            if not colores_dominantes:
                raise ValueError("No se pudieron obtener colores dominantes de la imagen.")

            # Mostrar los resultados en la nueva ventana
            etiqueta_mensaje = ttk.Label(nueva_ventana,
                                         text=f"Colores dominantes: {colores_dominantes}",
                                         font=("Arial", 12, "bold"),
                                         background=colores["fondo"])
            etiqueta_mensaje.pack(pady=20)

            # Verificar si la combinacion es buena
            resultado_combinacion = verificar_combinacion(colores_dominantes)
            etiqueta_combinacion = ttk.Label(nueva_ventana,
                                             text=f"{resultado_combinacion}",
                                             font=("Arial", 12, "bold"),
                                             background=colores["fondo"])
            etiqueta_combinacion.pack(pady=10)

            # Mostrar la imagen seleccionada
            imagen = Image.open(ruta_archivo)
            imagen = imagen.resize((400, 200), Image.Resampling.LANCZOS)
            imagen_tk = ImageTk.PhotoImage(imagen)
            etiqueta_imagen = tk.Label(nueva_ventana, image=imagen_tk)
            etiqueta_imagen.image = imagen_tk  # Guardar una referencia a la imagen
            etiqueta_imagen.pack(pady=10)

            if resultado_combinacion=="Buena combinación":
                # Mostrar la imagen SI
                imagenSI = Image.open("ednaSI.webp")
                imagenSI = imagenSI.resize((250, 300), Image.Resampling.LANCZOS)
                imagenSI_tk = ImageTk.PhotoImage(imagenSI)
                etiqueta_imagenSI = tk.Label(nueva_ventana, image=imagenSI_tk)
                etiqueta_imagenSI.image = imagenSI_tk  # Guardar una referencia a la imagen
                etiqueta_imagenSI.pack(pady=10)

            else:
                # Mostrar la imagen NO
                imagenNO = Image.open("ednaNO.webp")
                imagenNO = imagenNO.resize((400, 300), Image.Resampling.LANCZOS)
                imagenNO_tk = ImageTk.PhotoImage(imagenNO)
                etiqueta_imagenNO = tk.Label(nueva_ventana, image=imagenNO_tk)
                etiqueta_imagenNO.image = imagenNO_tk  # Guardar una referencia a la imagen
                etiqueta_imagenNO.pack(pady=10)

                


        except Exception as e:
            messagebox.showerror("Error", f"No se pudo procesar la imagen: {e}")

boton_seleccionar = ttk.Button(marco_principal,
                               text="Seleccionar archivo",
                               command=seleccionar_archivo,
                               style="boton.TButton",
                               padding=10)
boton_seleccionar.pack(pady=20)

# Estilo del boton
estilo_boton = ttk.Style()
estilo_boton.configure("boton.TButton",
                      background=colores["boton"],
                      foreground=colores["texto_boton"])

# Corre la GUI
ventana.mainloop()
