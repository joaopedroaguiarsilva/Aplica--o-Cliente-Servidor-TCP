# grafico.py
import matplotlib.pyplot as plt
import csv
from collections import defaultdict

dados = defaultdict(list)

with open('log_temperaturas.csv', 'r') as f:
    leitor = csv.reader(f)
    for sensor_id, temperatura, timestamp in leitor:
        dados[sensor_id].append((timestamp, float(temperatura)))

for sensor_id, valores in dados.items():
    tempos = [t for t, _ in valores]
    temperaturas = [temp for _, temp in valores]
    plt.plot(tempos, temperaturas, label=sensor_id)

plt.xlabel("Horário")
plt.ylabel("Temperatura (°C)")
plt.title("Temperaturas por Sensor")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()
