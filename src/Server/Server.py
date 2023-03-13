import datetime
import socket
import threading
import ssl


class Server:
    def __init__(self, host="localhost", port=7000):
        self.clients = {}
        self.serverSocket = socket.socket()
        self.serverSocket.bind((host, port))
        self.serverSocket.listen(5)
        print(f"Server started at {datetime.datetime.now()}.")

        # Wrap the socket with TLS
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.load_cert_chain(certfile='crt/server.crt', keyfile='crt/server.key')
        self.securedServerSocket = self.context.wrap_socket(self.serverSocket, server_side=True)

    def start(self):
        while True:
            clientSocket, addr = self.securedServerSocket.accept()
            threading.Thread(target=self.handle_client, args=(clientSocket, addr)).start()

    def handle_client(self, socket, address):
        # Receive the username from the client and append the client socket with its username that was received by user
        self.clients[socket] = socket.recv(1024).decode()

        cipher = socket.cipher()
        if cipher is not None:
            print(f"TLS handshake successful, User {address} connected at {datetime.datetime.now()}")
        else:
            print(f"TLS handshake failed with {address}")

        while True:
            self.broadcast(f"CLIENTS_LIST{list(self.clients.values())}")

            try:
                message = socket.recv(1024).decode()

                if message:
                    print(f"received message from {address}: {message}.")
                    self.broadcast(f"{message} ")
                else:
                    socket.close()
                    print(f"Client disconnected: {address}")
                    break
            except:
                disClient = f"System: {self.clients[socket]} Disconnected."
                del self.clients[socket]
                self.broadcast(disClient)
                self.broadcast(f"CLIENTS_LIST{list(self.clients.values())}")
                socket.close()
                print(f"Client: {address} Disconnected.")
                break

    def broadcast(self, message):
        template = "{:<46} {:>0}"
        for client in self.clients:
            if message.startswith("CLIENTS_LIST"):
                client.send(message.encode())
            else:
                client.send(template.format(message, datetime.datetime.now().strftime('%d %b %I:%M %p')).encode())


if __name__ == "__main__":
    Server().start()
