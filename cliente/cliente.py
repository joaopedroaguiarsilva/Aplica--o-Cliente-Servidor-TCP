# cliente_sensor.py
import socket
import time
import random
import uuid
from datetime import datetime

class Sensor:
    def __init__(self, sensor_id=None):
        # Gera um ID único automaticamente se nenhum for fornecido
        self.sensor_id = sensor_id or f"Sensor-{uuid.uuid4().hex[:8]}"

    def get_temperature_data(self):
        temperature = round(random.uniform(5, 45), 2)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return {
            'id': self.sensor_id,
            'temperature': temperature,
            'timestamp': timestamp
        }

def enviar_dados(sensor):
    server_host = 'localhost'
    server_port = 12000

    while True:
        data = sensor.get_temperature_data()
        message = f"{data['id']}|{data['temperature']}|{data['timestamp']}"
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((server_host, server_port))
                client_socket.send(message.encode())
                resposta = client_socket.recv(1024).decode()
                print(f"[{data['timestamp']}] {sensor.sensor_id} → Servidor respondeu: {resposta}")
        except Exception as e:
            print("Erro de conexão:", e)

        time.sleep(60)  # Espera 1 minuto

if __name__ == "__main__":
    sensor = Sensor()  # ID será gerado automaticamente
    print(f"Iniciando sensor com ID: {sensor.sensor_id}")
    enviar_dados(sensor)
