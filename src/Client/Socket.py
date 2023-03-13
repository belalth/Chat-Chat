import socket
import ssl


class Socket:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        # TLS AUTH AND CONNECTING TO SERVER
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.load_verify_locations('crt/server.crt')
        self.securedClientSocket = context.wrap_socket(self.clientSocket, server_hostname=self.host)

    def connect(self):
        # Connect to the server
        self.securedClientSocket.connect((self.host, self.port))

    def send(self, data):
        # Send data to the server
        if ":" in data and len(data.split(":")[1].strip()) > 0 :
            self.securedClientSocket.sendall(data.encode())
        if ":" not in data :
            self.securedClientSocket.sendall(data.encode())

    def receive(self, buffer_size=1024):
        # Receive data from the server
        return self.securedClientSocket.recv(buffer_size).decode()

    def close(self):
        # Close the socket
        self.securedClientSocket.close()
