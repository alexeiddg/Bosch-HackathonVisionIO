from PIL import Image
import numpy as np
import os
from concurrent.futures import ThreadPoolExecutor

def check_image_illumination(image_path, min_intensity=170, max_intensity=250, region_size=50):
    try:
        with Image.open(image_path) as img:
            img_array = np.array(img)

            center_x, center_y = img_array.shape[1] // 2, img_array.shape[0] // 2
            central_region = img_array[center_y - region_size // 2:center_y + region_size // 2,
                                       center_x - region_size // 2:center_x + region_size // 2]

            avg_intensity_per_channel = np.mean(central_region.reshape(-1, 3), axis=0)
            result = all(min_intensity <= i <= max_intensity for i in avg_intensity_per_channel)

            return {
                "status": "GO" if result else "NO GO",
                "intensities": avg_intensity_per_channel.tolist(),
                "path": image_path
            }
    except IOError:
        return {
            "status": "ERROR",
            "intensities": None,
            "path": image_path
        }

def process_images(image_paths):
    results = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(check_image_illumination, path) for path in image_paths]
        for future in futures:
            results.append(future.result())

    for result in results:
        print(f"Image {result['path']}: Result: {result['status']}")
        if result['intensities']:
            print(f"Intensities - Red: {result['intensities'][0]}, Green: {result['intensities'][1]}, Blue: {result['intensities'][2]}")

# Reemplazar con las rutas reales a las imágenes
test_image_paths = [
    'Images/1.PNG',
    'Images/2.PNG',
    # ... agregar todas las rutas de imagen
]

process_images(test_image_paths)
