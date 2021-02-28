# Only Allow Imports
if __name__ == "__main__":
    exit()
else:
    # Imports
    import socket
    # Client
    class Client():
        # Init
        def __init__(self, ip_address, port):
            self.HEADER = 2048
            self.SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.SOCKET.connect((ip_address, port))
        # Send
        def send_string(self, message):
            message = message.encode("utf-8")
            message_length = len(message)
            message_length = str(message_length).encode("utf-8")
            message_length += b" " * (self.HEADER - len(message_length))
            self.SOCKET.send(message_length)
            self.SOCKET.send(message)
            if message == "!DISSCONNECT":
                self.SOCKET.close()
        # Send
        def send_byte(self, message):
            message_length = len(message)
            message_length = str(message_length).encode("utf-8")
            message_length += b" " * (self.HEADER - len(message_length))
            self.SOCKET.send(message_length)
            self.SOCKET.send(message)
            if message == "!DISSCONNECT":
                self.SOCKET.close()
        # Receive
        def receive_string(self):
            message_length = self.SOCKET.recv(self.HEADER).decode("utf-8")
            if message_length:
                message_length = int(message_length)
                message = self.SOCKET.recv(message_length).decode("utf-8")
                return message
        # Receive
        def receive_byte(self):
            message_length = self.SOCKET.recv(self.HEADER).decode("utf-8")
            if message_length:
                message_length = int(message_length)
                message = self.SOCKET.recv(message_length)
                return message
    # Server
    class Server():
        # Init
        def __init__(self, ip_address, port):
            self.HEADER = 2048
            self.SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.SOCKET.bind((ip_address, port))
            self.SOCKET.listen()
        # Connection
        def receive_connection(self):
            connection, address = self.SOCKET.accept()
            return connection, address
        # Send
        def send_string(self, connection, message):
            message = message.encode("utf-8")
            message_length = len(message)
            message_length = str(message_length).encode("utf-8")
            message_length += b" " * (self.HEADER - len(message_length))
            connection.send(message_length)
            connection.send(message)
        # Send
        def send_byte(self, connection, message):
            message = message
            message_length = len(message)
            message_length = str(message_length).encode("utf-8")
            message_length += b" " * (self.HEADER - len(message_length))
            connection.send(message_length)
            connection.send(message)
        # Receive
        def receive_string(self, connection):
            message_length = connection.recv(self.HEADER).decode("utf-8")
            if message_length:
                message_length = int(message_length)
                message = connection.recv(message_length).decode("utf-8")
                return message
        # Receive
        def receive_byte(self, connection):
            message_length = connection.recv(self.HEADER).decode("utf-8")
            if message_length:
                message_length = int(message_length)
                message = connection.recv(message_length)
                return message