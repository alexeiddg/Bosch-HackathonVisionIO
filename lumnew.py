from PIL import Image
import numpy as np
import os

# Parámetros
MIN_INTENSITY = 170
MAX_INTENSITY = 250
IMAGE_FOLDER = 'Images'  # Asegúrate de actualizar esto a la ubicación de tus imágenes
IMAGE_EXTENSIONS = ['.png']  # Las extensiones de archivos que quieres procesar


def sum_channels(channels):
    red = channels[0]
    green = channels[1]
    blue = channels[2]
    return 0.2989 * red + 0.5870 * green + 0.1140 * blue


def check_illumination_focus_area(img_path):
    img = Image.open(img_path).convert('RGB')
    img_array = np.array(img)
    w, h = img.size

    # Definir los límites de los cuadrantes a analizar
    quad_width = w // 6
    quad_height = h // 4
    left = quad_width * 1
    upper = quad_height * 1
    right = quad_width * 3
    lower = quad_height * 3

    focus_array = img_array[upper:lower, left:right]
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


def process_images(image_folder):
    for file_name in os.listdir(image_folder):
        if any(file_name.lower().endswith(ext) for ext in IMAGE_EXTENSIONS):
            img_path = os.path.join(image_folder, file_name)
            result = check_illumination_focus_area(img_path)
            print(f"Image: {file_name}")
            print(f"Status: {result['status']}")
            print(f"Intensity: {result['intensity']:.2f}")
            print(f"Red: {result['red']:.2f}")
            print(f"Green: {result['green']:.2f}")
            print(f"Blue: {result['blue']:.2f}")
            print("-" * 30)


# Ejemplo de uso
process_images(IMAGE_FOLDER)
