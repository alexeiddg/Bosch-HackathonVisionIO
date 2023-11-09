import cv2

def orientacion(image, ref_image):
    # Se convierte la imagen a escala de grises
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_ref = cv2.cvtColor(ref_image, cv2.COLOR_BGR2GRAY)

    # Se obtiene el tamaño de la imagen
    height, width = gray_image.shape

    # Se obtiene la esquina superior derecha de la imagen
    corner = gray_image[0:height//10, width - width//10:width]

    # Se obtiene el histograma de la esquina superior derecha de la imagen
    hist_corner = cv2.calcHist([corner], [0], None, [256], [0, 256])

    # Se obtiene el valor máximo del histograma
    max_value = hist_corner.max()

    # Se obtiene el valor mínimo del histograma
    min_value = hist_corner.min()

    # Se obtiene el valor de la esquina superior derecha de la imagen de referencia
    corner_ref = gray_ref[0:height//10, width - width//10:width]

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

    # Se calcula el porcentaje de valores del histograma de la
    # imagen de referencia que se encuentran en el rango de la imagen
    percentage = range_image / range_ref

    # Se determina si la imagen se encuentra en el rango de la imagen de referencia
    if percentage >= 0.8:
        return 'GO'
    else:
        return 'NO GO'

def centrado(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    moments = cv2.moments(gray_image)
    cx = int(moments['m10'] / moments['m00'])
    return cx
