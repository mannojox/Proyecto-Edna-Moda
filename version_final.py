import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from tkinter import Label
from PIL import Image, ImageTk


import cv2
from collections import Counter
import webcolors

# ENCUENTRA NOMBRE COLOR
def encontrar_color(color):
    min_colores = {}
    for llave, nombre in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(llave)
        rd = (r_c - color[0]) ** 2
        gd = (g_c - color[1]) ** 2
        bd = (b_c - color[2]) ** 2
        min_colores[(rd + gd + bd)] = nombre
    return min_colores[min(min_colores.keys())]

# OBTIENE COLORES IMAGEN
def obtener_colores(ruta_imagen, num_colores=10):
    try:
        # carga imagen
        imagen = cv2.imread(ruta_imagen)
        if imagen is None:
            raise ValueError("No se puede cargar la imagen. Verifica la ruta del archivo y su integridad.")
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

        # cambia tamaño imagen
        nueva_imagen = cv2.resize(imagen, (600, 400), interpolation=cv2.INTER_AREA)
        
        # convierte el array de la imagen en lista de tuplas
        pixeles = nueva_imagen.reshape(-1, 3).tolist()

        # cuenta los colores mas comunes
        counter = Counter(tuple(pixel) for pixel in pixeles)
        colores_principales = counter.most_common(num_colores)

        # convierte colores de tuplas a nombres
        nombres_colores = [encontrar_color(color) for color, count in colores_principales]

        # Standardize color names
        colores_estandarizados = estandarizar_colores(nombres_colores)
        return colores_estandarizados
    except Exception as e:
        print(f"Error al obtener los colores de la imagen: {e}")
        return []

# ESTANDARIZA LOS NOMBRES DE LOS COLORES
def estandarizar_colores(nombres_colores):
    # estandarizaciones
    mapa_colores = {
        'blue': ['skyblue', 'navy', 'mediumblue', 'darkblue', 'dodgerblue', 'deepskyblue','darkslateblue', 'midnightblue', 'darkcyan','steelblue'],
        'red': ['darkred', 'firebrick', 'crimson', 'salmon'],
        'green': ['lime', 'forestgreen', 'darkgreen', 'seagreen'],
        'purple': ['indigo', 'violet', 'darkviolet', 'blueviolet'],
        'orange': ['darkorange', 'coral', 'tomato', 'orangered'],
        'yellow': ['gold', 'khaki', 'lightyellow'],
        'pink': ['lightpink', 'hotpink', 'deeppink', 'thistle'],
        'black': ['chocolate'],
        'gray': ['darkslategray'],
        'white': ['whitesmoke'],
        'brown': ['saddlebrown', 'sandybrown']
    }

    # reversa el mapa de colores
    colores_estandar = {}
    for estandar, variantes in mapa_colores.items():
        for variante in variantes:
            colores_estandar[variante] = estandar
    # salva los colores
    for estandar in mapa_colores.keys():
        colores_estandar[estandar] = estandar

    # estandariza nombres
    nombres_estandarizados = [colores_estandar.get(color, color) for color in nombres_colores]
    return nombres_estandarizados

# VERIFICA SI ES BUENA COMBINACION
def verificar_combinacion(nombres_colores):
    combinaciones_aprobatorias = [
        {'orange', 'blue'},
        {'red', 'blue'},
        {'red', 'green'},
        {'purple', 'green'},
        {'purple', 'yellow'},
        {'blue', 'orange'},
        {'pink', 'blue'},
        {'black', 'pink'},
        {'pink', 'green'},
        {'gray', 'blue'},
        {'black', 'white'},
        {'black','red'},
        {'pink', 'pink'},
        {'black','brown'},
        {'white','gray'},
        {'green','black'},
        {'pink','purple'}
    ]

    set_colores = set(nombres_colores)
    for combinacion in combinaciones_aprobatorias:
        if combinacion.issubset(set_colores):
            return "Buena combinación"
    return "Mala combinación"

# IMPRIME LOS COLORES DE LA IMAGEN EN CONSOLA
def mostrar_colores(nombres_colores):
    for i, nombre_color in enumerate(nombres_colores):
        print(f"Color {i+1}: {nombre_color}")



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
