import cv2
import numpy as np
import pandas as pd
from Evaluaciones import *

def is_image(img):
    # regresa true si la imagen se encuentra en la ruta especificada
    try:
        open_img = open(img, 'rb')
        return True
    except:
        return False

# Función que procesa la imagen
def process_image(ref, image, df, i):
    # Se convierte la imagen a escala de grises
    gray_ref = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Se calcula el histograma de la imagen
    hist_ref = cv2.calcHist([gray_ref], [0], None, [256], [0, 256])
    hist_image = cv2.calcHist([gray_image], [0], None, [256], [0, 256])

    # Se calcula la nitidez de la imagen
    sharpness = cv2.Laplacian(gray_image, cv2.CV_64F).var()

    # Se calcula la intensidad de los colores
    red_intensity = hist_image[0:64].sum()
    green_intensity = hist_image[65:128].sum()
    blue_intensity = hist_image[129:192].sum()

    # Se calcula el centrado de la imagen
    centered = centrado(image)

    # Se calcula la orientación de la imagen
    orientation = orientacion(image, ref)

    # Se agregan los resultados a la tabla
    df.loc[i] = [i, sharpness, red_intensity, green_intensity, blue_intensity, centered, orientation]

# Carga la imagen de referencia
ref = cv2.imread('Images/REF_23.PNG')

# Crear una tabla para depositar los resultados de las evaluaciones
df = pd.DataFrame(columns=['ID', 'Nitidez', 'Red Intensity', 'Green Intensity', 'Blue Intensity', 'Centrado', 'Orientacion'])

for i in range(1, 37):
    if is_image('Images/' + str(i) + '.PNG'):
        eval_image = cv2.imread('Images/' + str(i) + '.PNG')
        process_image(ref, eval_image, df, i)

# Se guarda la tabla en un archivo csv
df.to_csv('Results.csv', index=False)
