from PIL import Image
import numpy as np

# Parámetros
MIN_INTENSITY = 170
MAX_INTENSITY = 250


def get_quadrants(img, x_quad=2, y_quad=4):
    # Dividir imagen en cuadrantes
    y_sections = np.array_split(img, y_quad, axis=0)

    quadrants = []
    for section in y_sections:
        x_sections = np.array_split(section, x_quad, axis=1)
        quadrants.extend(x_sections)

    return quadrants


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

    # Dividir en cuadrantes
    quadrants = get_quadrants(img_array)

    status = "GO"

    for q in quadrants:

        # Promediar canales
        red = q[:, :, 0].mean()
        green = q[:, :, 1].mean()
        blue = q[:, :, 2].mean()

        # Sumar canales
        intensity = sum_channels([red, green, blue])

        # Verificar límites
        if not (MIN_INTENSITY <= intensity <= MAX_INTENSITY):
            status = "NO GO"
            break

    return {
        "status": status
    }


# Ejemplo
test_img = 'Images/REF_23.PNG'
result = check_illumination(test_img)

print(result["status"])