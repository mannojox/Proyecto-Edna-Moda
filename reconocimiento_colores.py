import cv2
from collections import Counter
import webcolors
from PIL import Image

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
    # carga imagen
    imagen = cv2.imread(ruta_imagen)
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

# VERIFICA SI ES BUENA COMBINACION (0 = mala, 1 = buena)
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
        {'pink','purple'},
        {''}
    ]

    set_colores = set(nombres_colores)
    for combinacion in combinaciones_aprobatorias:
        if combinacion.issubset(set_colores):
            return 1
    return 0

# IMPRIME LOS COLORES DE LA IMAGEN EN CONSOLA
def mostrar_colores(nombres_colores):
    for i, nombre_color in enumerate(nombres_colores):
        print(f"Color {i+1}: {nombre_color}")

# ---------------- MAIN

if __name__ == "__main__":
    ruta_imagen = 'R0.png' # URL IMAGEN
    nombres_colores = obtener_colores(ruta_imagen)
    mostrar_colores(nombres_colores)
    resultado = verificar_combinacion(nombres_colores)
    print("Buena combinacion? ", resultado) #(0 = mala, 1 = buena)
