# Servidor
import socket
import threading

class ChatServer:
    def __init__(self):
        self.server_host = '127.0.0.1'
        self.server_port = 55555
        self.client_connections = {}
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.server_host, self.server_port))
        self.server_socket.listen(5)
        print("Servidor iniciado en {}:{}".format(self.server_host, self.server_port))

    def handle_client(self, client_conn, client_addr):
        print(f"Nueva conexión establecida: {client_addr}")
        with client_conn:
            while True:
                try:
                    data = client_conn.recv(1024).decode('utf-8')
                    if not data:
                        break
                    print(f"Mensaje recibido de {client_addr}: {data}")
                    self.broadcast_message(data, client_conn)
                except ConnectionResetError:
                    break
        print(f"Cliente {client_addr} desconectado.")
        del self.client_connections[client_addr]
        self.broadcast_message(f"Cliente {client_addr} se ha desconectado.", client_conn)

    def broadcast_message(self, message, sender_conn):
        for addr, conn in self.client_connections.items():
            if conn != sender_conn:
                try:
                    conn.sendall(message.encode('utf-8'))
                except ConnectionResetError:
                    del self.client_connections[addr]
                    print(f"Error al enviar mensaje a {addr}. Cliente desconectado.")
                    self.broadcast_message(f"Cliente {addr} se ha desconectado.", sender_conn)

    def start(self):
        try:
            while True:
                client_conn, client_addr = self.server_socket.accept()
                self.client_connections[client_addr] = client_conn
                threading.Thread(target=self.handle_client, args=(client_conn, client_addr)).start()
        except KeyboardInterrupt:
            print("Deteniendo el servidor...")
        finally:
            self.server_socket.close()

if __name__ == "__main__":
    server = ChatServer()
    server.start()


