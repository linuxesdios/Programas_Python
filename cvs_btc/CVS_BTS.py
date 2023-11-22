import matplotlib.pyplot as plt
import csv
from datetime import datetime

entrada = open("BTC-USD.csv")
tabla = []
for fila in csv.reader(entrada):
    tabla.append(fila)
entrada.close()

x = []
y1 = []  # Primera serie de datos
y2 = []  # Segunda serie de datos

for fila in range(1, len(tabla)):
    fecha = datetime.strptime(tabla[fila][0], '%Y-%m-%d')
    x.append(fecha)
    y1.append(float(tabla[fila][1]))  # Primera serie de datos
    y2.append(float(tabla[fila][6]))  # Segunda serie de datos

# Normaliza las series dividiendo cada valor por el máximo valor de la serie
max_y1 = max(y1)
max_y2 = max(y2)
y1_normalized = [val / max_y1 for val in y1]
y2_normalized = [val / max_y2 for val in y2]

plt.plot(x, y1_normalized, label='open', color='blue')
plt.xlabel('Fecha')
plt.ylabel('open')
plt.twinx()  # Crea un segundo eje y en el lado derecho
plt.plot(x, y2_normalized, label='volumeeçn', color='red')
plt.ylabel('volumen')

plt.title('Ejemplo de gráfica de dos series normalizadas')
plt.legend(loc='upper left')  # Ubica la leyenda de la serie 1 en la parte superior izquierda
plt.legend(loc='upper right')  # Ubica la leyenda de la serie 2 en la parte superior derecha
plt.show()