## [![Stack](https://skillicons.dev/icons?i=py)](https://skillicons.dev) Welcome to Bosch-HackathonVisionIO! 

Project Overview:
Bosch-HackathonVisionIO was conceived and executed during the intense and innovative environment of the Bosch Hackathon. This project aims to evaluate the quality of images previously captured by a video camera system. By applying a variety of digital image processing techniques, including signal analysis and customized filtering, our system measures the clarity, focus, and color intensity of the images, delivering a comprehensive assessment of each.

Technology Stack: 

Programming Language: Python
Image Processing Libraries: OpenCV, PIL, and custom-built tools for specialized analyses
Testing and Evaluation: Automated scripts to validate image quality against ISO standards
Achievements:
Our team successfully developed an algorithm capable of distinguishing between high and low-quality images based on pre-set standards, achieving remarkable accuracy. The solution not only met the hackathon's criteria but also showcased our ability to innovate under pressure and deliver technically sound and reliable software.

Evaluation Instructions:

Setup Environment: Ensure Python and necessary libraries are installed. Clone this repository and navigate into the project directory.
Running Tests: Execute main.py to start the evaluation process. The script automatically processes images stored in the Images directory.
Review Results: After running the tests, the system will output a detailed report on the image quality, highlighting areas that meet or fail the specified criteria.

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Se debe crear un sistema de procesamiento de imágenes para evaluar la calidad de imágenes capturadas previamente por una cámara de video.
Aplicar análisis de señales, filtros y parametrizaciones, para obtener una medición de la calidad de enfoque de las imágenes, entre otras pruebas.

Datos de entrada:
    Imágenes digitales basadas en el estándar ISO12233, incluyendo:
    Imágenes de referencia
    Imágenes con distintas calidades de enfoque
    Imágenes con enfoque incorrecto

Parametros de salida:
    El sistema evaluará la calidad de las imágenes en cuanto a:
    Nitidez
    Iluminación (intensidad de los pixeles: R, G, B)
    Centrado contra la imagen de referencia
    Orientación

Evaluación de Nitidez:
    Se debe de medir la nitidez de la imagen con respecto a la imagen de referencia, con el propósito de determinar si el lente esta correctamente alineado respecto al sensor de imagen de la cámara.
    Límites de prueba: minimo 0.15 ciclos/pixel al 50% de modulación (MTF50).
    La prueba debe de ser capaz de determinar si la nitidez de las 20 imagenes proveídas estan dentro (pasa la prueba) o fuera (falla la prueba) de los límites de prueba establecidos.
    Module Transfer Function (MTF) se puede definir como la evaluación  de la intensidad de los pixeles a lo largo de un borde el cual es la frontera entre el color blanco y el color negro.
    Con este método, se evalua la nitidez de la cámara. Idealmente, la frontera entre el blanco y el negro debe de ser bien definida pero debido a la naturaleza de los sistemas de visión, la imagen mezcla parte de los dos colores en la frontera causando pixeles en color gris.

Evaluación de Iluminación:
    Se debe de medir la intensidad de los pixeles cerca del centro de la imagen, para determinar que tan Iluminada está la imagen tomada por la cámara. La intensidad se mide en un rango de 0 a 255 (una mezcla de los tres canales de color: Rojo, Verde y Azul (RGB de 8 bits).
    Límites de prueba: mínimo 170, máximo 250
    La prueba debe de ser capaz de determinar si la iluminación de las 20 imágenes proveídas estan dentro de los límites de prueba (pasa la prueba) o fuera (falla la prueba).
    Debe de identificar la intensidad de los rojos, verdes y azules

Evaluación de Centrado:
    Se debe de medir el centrado de la imagen con respecto a la imagen de referencia, con el propósito de determinar si el lente esta correctamente centrado respecto al sensor de imagen de la cámara.
    Límites de prueba: +/-10 pixeles respecto a imagen de referencia.
    La prueba debe de ser capaz de determinar si el centrado de las 20 imagenes proveídas estan dentro (pasa la prueba) o fuera (falla la prueba) de los límites de prueba establecidos.

Evaluación de Orientación:
    Se debe de determinar si la orientación de la imagen es la correcta respecto a la imagen de referencia. Para ello se tiene un cuadro negro en la esquina superior derecha, por lo que si esta no se encuentra entonces no tiene una orientacion correcta.
    Límites de prueba: GO / NO GO
    La prueba debe de ser capaz de determinar si la orientación de las 20 imágenes proveídas estan dentro de los límites de prueba (pasa la prueba) o fuera (falla la prueba).

Pasos para prueba de MTF50:
    Elegir una región de interes donde se muestre el borde del cuadro negro central en el centro. (por ejemplo, 50x50 pixels)
    Detectar el borde dentro de la región de interés
    Medir la intensidad de los pixeles en líneas perpendiculares al borde detectado, atravesando la frontera entre blanco y negro, normalizar y graficar los datos (esta gráfica de datos se llama ESF, Edge Spread Function).
    Adecuar una función matematica que represente a la gráfica ESF.
    Derivar la función matematica que representa ESF, esta nueva función se llamaria LSF (Line Spread function)
    Hacer Transformada de Fourier de LSF, y calcular magnitud para cada frecuencia espacial.
    Graficar curva de MTF, normalizando los datos a MTF=1 cuando la frecuencia espacial es 0.
