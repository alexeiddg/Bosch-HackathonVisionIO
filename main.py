import cv2
import numpy as np
from PIL import Image, ImageDraw
import math
import os
import matplotlib.pyplot as plt
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})

def sum_channels(channels):
    red = channels[0]
    green = channels[1]
    blue = channels[2]
    sum = 0.2989 * red + 0.5870 * green + 0.1140 * blue
    return round(sum, 2)


ref = Image.open('REF_23.png')
image_array = np.array(ref)
height = image_array.shape[0]
width = image_array.shape[1]

tercerCuadranteY = height - height // 4
tercerCuadranteX = width - width // 4

segundoCuadranteY = height // 2
segundoCuadranteX = width // 2


def obtener_esquina_C(image_array):
    height = image_array.shape[0]
    width = image_array.shape[1]

    tercerCuadranteY = height - height // 4
    tercerCuadranteX = width - width // 4

    segundoCuadranteY = height // 2
    segundoCuadranteX = width // 2
    x = width // 4
    negro = False
    while not negro:
        for i in range(tercerCuadranteY, segundoCuadranteY, -1):
            if sum_channels(image_array[i][x]) < 20:
                negro = True;
                cX = x
                cY = i
                break
        x = x + 1
    return [cX, cY]


def obtener_esquina_B(image_array):
    height = image_array.shape[0]
    width = image_array.shape[1]

    tercerCuadranteY = height - height // 4
    tercerCuadranteX = width - width // 4

    segundoCuadranteY = height // 2
    segundoCuadranteX = width // 2
    x = tercerCuadranteX
    negro = False
    while not negro:
        for i in range(height // 4, segundoCuadranteY, +1):
            if sum_channels(image_array[i][x]) < 20:
                negro = True;
                cX = x
                cY = i
                break
        x = x - 1
    return [cX, cY]


def obtener_esquina_A(image_array):
    height = image_array.shape[0]
    width = image_array.shape[1]

    tercerCuadranteY = height - height // 4
    tercerCuadranteX = width - width // 4

    segundoCuadranteY = height // 2
    segundoCuadranteX = width // 2
    y = height // 4
    negro = False
    while not negro:
        for i in range(width // 4, segundoCuadranteX, +1):
            if sum_channels(image_array[y][i]) < 20:
                negro = True;
                cX = i
                cY = y
                break
        y = y + 1
    return [cX, cY]


def obtener_esquina_D(image_array):
    height = image_array.shape[0]
    width = image_array.shape[1]

    tercerCuadranteY = height - height // 4
    tercerCuadranteX = width - width // 4

    segundoCuadranteY = height // 2
    segundoCuadranteX = width // 2
    y = tercerCuadranteY
    negro = False
    while not negro:
        for i in range(tercerCuadranteX, segundoCuadranteX, -1):
            if sum_channels(image_array[y][i]) < 20:
                negro = True;
                cX = i
                cY = y
                break
        y = y - 1
    return [cX, cY]


def obtenerCoordenadas(image_array):
    coordenadas = []
    coordenadas.append(obtener_esquina_A(image_array))
    coordenadas.append(obtener_esquina_B(image_array))
    coordenadas.append(obtener_esquina_C(image_array))
    coordenadas.append(obtener_esquina_D(image_array))
    return coordenadas


def distanciaEntrePuntos(coordsA, coordsB):
    distancia = math.sqrt((coordsB[0] - coordsA[0]) ** 2 + (coordsB[1] - coordsA[1]) ** 2)
    return distancia
    distancia = distanciaEntrePuntos(coordsA[0], coordsA[1])
    return distancia


def compararCoordenadas(coordsREF, arrayB):
    diferenciaMax = 10
    coordsB = obtenerCoordenadas(arrayB)
    for i in range(4):
        if (distanciaEntrePuntos(coordsREF[i], coordsB[
            i]) > diferenciaMax):  # Aqui decidimos la distancia entre todas las esquinas del cuadrado y si esta es mayor que el valor decidido entonces regresaremos que no esta centrado correctamente
            return False
    return True


def revisarCentrado(nomCarpeta, nomImgREF):
    ref = Image.open(nomImgREF)
    ref_array = np.array(ref)
    coords_ref = obtenerCoordenadas(ref_array)

    # Obtener la lista de archivos en el directorio
    files = os.listdir(nomCarpeta)

    # Filtrar solo los archivos de imagen
    image_files = [f for f in files]

    centrado = []
    # Iterar sobre la lista de archivos de imagen y procesar cada imagen
    for image_file in image_files:
        condicion = []
        condicion.append(image_file)
        # Cargar la imagen y procesarla
        image_path = os.path.join(nomCarpeta, image_file)
        image = Image.open(image_path)
        image_array = np.array(image)
        condicion.append(compararCoordenadas(coords_ref, image_array))
        # Hacer algo con las coordenadas obtenidas
        centrado.append(condicion)
    return centrado


# print(revisarCentrado('./Hackaton','REF_23.png'))
# Guardar la imagen procesada

def revisarOrientacion(nomCarpeta, nomImgREF):
    ref = cv2.imread(nomImgREF)

    # Obtener la lista de archivos en el directorio
    files = os.listdir(nomCarpeta)

    # Filtrar solo los archivos de imagen
    image_files = [f for f in files]

    resultados = []
    # Iterar sobre la lista de archivos de imagen y procesar cada imagen
    for image_file in image_files:
        condicion = []
        condicion.append(image_file)
        # Cargar la imagen y procesarla
        image_path = os.path.join(nomCarpeta, image_file)
        image = cv2.imread(image_path)
        condicion.append(orientacion(image, ref))
        # Hacer algo con las coordenadas obtenidas
        resultados.append(condicion)
    return resultados


# print(revisarCentrado('./Hackaton','REF_23.png'))
# Guardar la imagen procesada


def orientacion(image, ref_image):
    # Se convierte la imagen a escala de grises
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_ref = cv2.cvtColor(ref_image, cv2.COLOR_BGR2GRAY)

    # Se obtiene el tamaño de la imagen
    height, width = gray_image.shape

    # Se obtiene la esquina superior derecha de la imagen
    corner = gray_image[0:height // 4, width - width // 4:width]

    # Se obtiene el histograma de la esquina superior derecha de la imagen
    hist_corner = cv2.calcHist([corner], [0], None, [256], [0, 256])

    # Se obtiene el valor máximo del histograma
    max_value = hist_corner.max()

    # Se obtiene el valor mínimo del histograma
    min_value = hist_corner.min()

    # Se obtiene el valor de la esquina superior derecha de la imagen de referencia
    corner_ref = gray_ref[0:height // 10, width - width // 10:width]

    # Se obtiene el histograma de la esquina superior derecha de la imagen de referencia
    hist_corner_ref = cv2.calcHist([corner_ref], [0], None, [256], [0, 256])

    # Se obtiene el valor máximo del histograma de la imagen de referencia
    max_value_ref = hist_corner_ref.max()

    # Se obtiene el valor mínimo del histograma de la imagen de referencia
    min_value_ref = hist_corner_ref.min()

    # Se calcula el rango de valores del histograma de la imagen de referencia
    range_ref = max_value_ref - min_value_ref

    # Se calcula el rango de valores del histograma de la imagen
    range_image = max_value - min_value

    # Se calcula el porcentaje de valores del histograma
    percentage = range_image / range_ref

    # Se determina si la imagen se encuentra en el rango de la imagen de referencia
    if percentage >= 1:
        return True
    else:
        return False


def obtener_roi(coord):
    x1 = coord[1][0]
    x2 = coord[3][0]
    y1 = coord[1][1]
    y2 = coord[3][1]
    pm_x = int((x1 + x2) / 2)
    pm_y = int((y1 + y2) / 2)
    coord_cuadrado = [[pm_y + 25, pm_x - 25], [pm_y + 25, pm_x + 25], [pm_y - 25, pm_x - 25], [pm_y - 25, pm_x + 25]]
    return [pm_x, pm_y]


def obtener_esf(pm_x, pm_y, matriz_imagen):
    x = pm_x
    y = pm_y + 25
    intensidades = []
    for j in range(50):
        x = x - 1
        y = y - 1
        yI = y
        xI = x
        for i in range(50):
            yI = yI - 1
            xI = xI + 1
            intensidades.append([i, sum_channels(matriz_imagen[yI][xI]) / 255])
    return intensidades


app = Flask(__name__)


@app.route("/get-centrado/")
def get_centrado():
    result = revisarCentrado('./Hackaton', 'REF_23.png')
    result_json = {}
    for item in result:
        result_json[item[0]] = item[1]
    json_result = json.dumps(result_json)
    return json_result

# Parámetros
MIN_INTENSITY = 170
MAX_INTENSITY = 250
IMAGE_FOLDER = 'Images'  # Asegúrate de actualizar esto a la ubicación de tus imágenes
IMAGE_EXTENSIONS = ['.png']  # Las extensiones de archivos que quieres procesar

# Nuevas coordenadas para analizar la iluminación (180 a 220 en x y y)
X1, Y1 = 180, 180
X2, Y2 = 220, 220

def check_illumination_focus_area(img_path, x1, y1, x2, y2):
    img = Image.open(img_path).convert('RGB')
    img_array = np.array(img)

    focus_array = img_array[y1:y2, x1:x2]  # Utiliza las coordenadas personalizadas
    red = focus_array[:, :, 0].mean()
    green = focus_array[:, :, 1].mean()
    blue = focus_array[:, :, 2].mean()
    intensity = sum_channels([red, green, blue])

    return {
        "status": "GO" if MIN_INTENSITY <= intensity <= MAX_INTENSITY else "NO GO",
        "intensity": intensity,
        "red": red,
        "green": green,
        "blue": blue
    }


# Obtener la lista de nombres de archivos en el directorio
image_files = [f for f in os.listdir(IMAGE_FOLDER) if any(f.lower().endswith(ext) for ext in IMAGE_EXTENSIONS)]

image_matrix = [[filename, False] for filename in image_files]


def process_images(image_folder):
    for file_name in os.listdir(image_folder):
        if any(file_name.lower().endswith(ext) for ext in IMAGE_EXTENSIONS):
            img_path = os.path.join(image_folder, file_name)
            result = check_illumination_focus_area(img_path, X1, Y1, X2,
                                                   Y2)  # Llama a la función con las coordenadas personalizadas
            print(f"Image: {file_name}")
            print(f"Status: {result['status']}")
            print(f"Intensity: {result['intensity']:.2f}")
            print(f"Red: {result['red']:.2f}")
            print(f"Green: {result['green']:.2f}")
            print(f"Blue: {result['blue']:.2f}")
            print("-" * 30)

            # Actualiza el atributo de la foto en la matriz según el resultado
            for image_info in image_matrix:
                if image_info[0] == file_name:
                    image_info[1] = result['status'] == "GO"
            return image_matrix



# Convert the result_json to JSON using json.dumps or jsonify
# json.dumps is used if you want to return a JSON string, jsonify for a JSON response
# OR
# json_result = jsonify(result_json)

@app.route("/get-orientacion/")
def get_orientacion():
    result = revisarOrientacion('./Hackaton', 'REF_23.png')
    result_json = {}
    for item in result:
        result_json[item[0]] = item[1]
    json_result = json.dumps(result_json)
    return json_result

@app.route("/get-luminosidad/")
def get_luminosidad():
    # Crear la matriz con valores predeterminados

    # Procesar las imágenes
    process_images(IMAGE_FOLDER)

    # Imprimir la matriz actualizada
    result = process_images('Images')
    result_json = {}
    for item in result:
        result_json[item[0]] = item[1]
    json_result = json.dumps(result_json)
    return json_result

# Convert the result_json to JSON using json.dumps or jsonify
# json.dumps is used if you want to return a JSON string, jsonify for a JSON response
# OR
# json_result = jsonify(result_json)


if __name__ == "__main__":
    app.run(debug=True)
