from PIL import Image
import numpy as np
from concurrent.futures import ThreadPoolExecutor

# Function to detect the black square in an image
def detect_black_square(img_array, width, height, threshold=50, tolerance=10):
    black_pixels = np.where(np.all(img_array < threshold, axis=-1))

    top, left = np.min(black_pixels, axis=1)
    bottom, right = np.max(black_pixels, axis=1)

    if top <= tolerance and left <= tolerance:
        return 'top_left'
    elif top <= tolerance and right >= width - tolerance:
        return 'top_right'
    elif bottom >= height - tolerance and left <= tolerance:
        return 'bottom_left'
    elif bottom >= height - tolerance and right >= width - tolerance:
        return 'bottom_right'
    else:
        return 'unknown'

# Function to check the orientation of a test image against the reference corner
def check_orientation(img_array, width, height, ref_corner):
    test_corner = detect_black_square(img_array, width, height)
    return 'GO' if test_corner == ref_corner else 'NO GO'

# Replace these paths with the actual paths to your images
ref_image_path = 'Images/REF_23.PNG'  # Path to the reference image

# Load the reference image once and cache the result
with Image.open(ref_image_path) as ref_img:
    ref_img_array = np.array(ref_img)
    ref_height, ref_width = ref_img_array.shape[:2]
    ref_corner = detect_black_square(ref_img_array, ref_width, ref_height)

def process_image(test_image_path):
    with Image.open(test_image_path) as test_img:
        test_img_array = np.array(test_img)
        test_height, test_width = test_img_array.shape[:2]
        return test_image_path, check_orientation(test_img_array, test_width, test_height, ref_corner)

# Function to process images in parallel
def process_images_in_parallel(image_paths):
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(process_image, image_paths))

    for path, result in results:
        print(f"Image {path} - Result: {result}")

# List of paths to test images
test_image_paths = [
    'Images/1.PNG',
    'Images/2.PNG',
    # ... add all image paths
]

process_images_in_parallel(test_image_paths)
