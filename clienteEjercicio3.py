# Cliente
import socket
import threading

class ChatClient:
    def __init__(self):
        self.server_host = '127.0.0.1'
        self.server_port = 55555
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_host, self.server_port))
        print("Conectado al servidor.")
        threading.Thread(target=self.receive_messages).start()

    def send_message(self):
        while True:
            message = input()
            self.client_socket.sendall(message.encode('utf-8'))

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024).decode('utf-8')
                print(data)
            except ConnectionResetError:
                print("Conexión perdida con el servidor.")
                break

    def start(self):
        threading.Thread(target=self.send_message).start()

if __name__ == "__main__":
    client = ChatClient()
    client.start()