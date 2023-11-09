from PIL import Image
import numpy as np


# Function to detect the black square in an image
def detect_black_square(image_path):
    with Image.open(image_path) as img:
        img_array = np.array(img)

        # Assuming the black square is distinctly darker than the rest of the image
        threshold = 50  # pixel values below this are considered black
        black_pixels = np.where(np.all(img_array < threshold, axis=-1))

        # Find the corner where the black square is located
        height, width = img_array.shape[:2]
        top, left = np.min(black_pixels, axis=1)
        bottom, right = np.max(black_pixels, axis=1)

        # Determine the corner
        # Tolerance is a small number of pixels that the black square can be away from the actual corner
        tolerance = 10
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
def check_orientation(test_image_path, ref_corner):
    test_corner = detect_black_square(test_image_path)
    return 'GO' if test_corner == ref_corner else 'NO GO'


# Replace these paths with the actual paths to your images
ref_image_path = 'Images/REF_23.PNG'  # Path to the reference image
test_image_paths = [
    'Images/1.PNG',
    'Images/2.PNG',
]

# Detecting the black square in the reference image
ref_corner = detect_black_square(ref_image_path)

# Dictionary to hold the test results
test_results = {}

# Apply the check_orientation function to each test image
for test_image_path in test_image_paths:
    test_results[test_image_path] = check_orientation(test_image_path, ref_corner)

# Output the results
for path, result in test_results.items():
    print(f"Image {path} - Result: {result}")
