from PIL import Image
import numpy as np

# Parámetros
MIN_INTENSITY = 170
MAX_INTENSITY = 250
REGION_SIZE = 50


def sum_channels(channels):
    red = channels[0]
    green = channels[1]
    blue = channels[2]

    sum = 0.2989 * red + 0.5870 * green + 0.1140 * blue

    return round(sum, 2)


def check_illumination(img_path):
    # Leer imagen
    img = Image.open(img_path).convert('RGB')

    # Convertir a array
    img_array = np.array(img)

    # Obtener region central
    x_center = img_array.shape[1] // 2
    y_center = img_array.shape[0] // 2

    region = img_array[y_center - REGION_SIZE // 2: y_center + REGION_SIZE // 2,
             x_center - REGION_SIZE // 2: x_center + REGION_SIZE // 2]

    # Promediar canales
    red = region[:, :, 0].mean()
    green = region[:, :, 1].mean()
    blue = region[:, :, 2].mean()

    # Sumar canales
    intensity = sum_channels([red, green, blue])

    # Verificar límites
    is_valid = (intensity >= MIN_INTENSITY) and (intensity <= MAX_INTENSITY)

    if is_valid:
        status = "GO"
    else:
        status = "NO GO"

    return {
        "status": status,
        "intensity": intensity
    }


# Probar con imágenes
test_images = [
    'Images/1.PNG',
    'Images/2.PNG',
    'Images/8.PNG',
    'Images/9.PNG',
    'Images/11.PNG',
    'Images/12.PNG',
    'Images/14.PNG',
    'Images/18.PNG',
    'Images/19.PNG',
    'Images/20.PNG',
    'Images/21.PNG',
    'Images/22.PNG',
    'Images/24.PNG',
    'Images/26.PNG',
    'Images/27.PNG',
    'Images/28.PNG',
    'Images/29.PNG',
    'Images/32.PNG',
    'Images/36.PNG',
]

for img in test_images:
    result = check_illumination(img)
    print(f"Image {img}: {result['status']}, Intensity: {result['intensity']}")

    '''
    
    '''