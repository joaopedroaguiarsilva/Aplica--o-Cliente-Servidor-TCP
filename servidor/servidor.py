# servidor.py
import socket
import threading
from collections import defaultdict
import csv

sensor_dados = defaultdict(list)  # {'Sensor-001': [(temp, timestamp), ...]}
ALERTA_BAIXA = 15
ALERTA_ALTA = 35

def tratar_cliente(conexao, endereco):
    try:
        mensagem = conexao.recv(1024).decode()
        sensor_id, temperatura, timestamp = mensagem.split('|')
        temperatura = float(temperatura)

        # Armazena
        sensor_dados[sensor_id].append((temperatura, timestamp))

        # Salva em CSV
        with open('log_temperaturas.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([sensor_id, temperatura, timestamp])

        # Verifica alerta
        if temperatura < ALERTA_BAIXA or temperatura > ALERTA_ALTA:
            resposta = f"[ALERTA] Temperatura fora do padrão: {temperatura}°C"
        else:
            resposta = f"Temperatura normal: {temperatura}°C"

        print(f"{sensor_id} - {temperatura}°C às {timestamp} → {resposta}")
        conexao.send(resposta.encode())
    except Exception as e:
        print("Erro no tratamento do cliente:", e)
    finally:
        conexao.close()

def iniciar_servidor():
    host = ''
    porta = 12000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, porta))
    server_socket.listen(5)
    print("Servidor iniciado. Aguardando sensores...")

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=tratar_cliente, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    iniciar_servidor()
