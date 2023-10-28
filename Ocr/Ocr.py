import easyocr
import cv2
import pyperclip

reader = easyocr.Reader(["es"], gpu=False)
image = cv2.imread("D:\Programas\Programas_Python\Ocr\image_0000.jpg")
result = reader.readtext(image, paragraph=False)

# Inicializa una variable para almacenar el texto completo
full_text = ""

for res in result:
     full_text += res[1] + "\n"

# Copia el texto completo al portapapeles
pyperclip.copy(full_text)
print("Texto completo copiado al portapapeles:\n", full_text)