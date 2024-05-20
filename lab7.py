import socket
import threading


class P2PChat:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.nicknames = []

    def start(self):
        self.server.bind((self.host, self.port))
        self.server.listen()
        print(f"Server started on {self.host}:{self.port}")

        while True:
            client_socket, client_address = self.server.accept()
            print(f"New connection from {client_address}")

            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def handle_client(self, client_socket):
        nickname = client_socket.recv(1024).decode()
        self.nicknames.append(nickname)
        self.clients.append(client_socket)

        print(f"Nickname of the client is {nickname}")
        self.broadcast(f"{nickname} joined the chat!\n".encode())
        client_socket.send("Connected to the server!\n".encode())

        while True:
            try:
                message = client_socket.recv(1024)
                self.broadcast(message)
            except:
                index = self.clients.index(client_socket)
                self.clients.remove(client_socket)
                client_socket.close()
                nickname = self.nicknames[index]
                self.nicknames.remove(nickname)
                self.broadcast(f"{nickname} left the chat!\n".encode())
                break

    def chat_with_all(self):
        nickname = input("Enter your nickname: ")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.host, self.port))
        client_socket.send(nickname.encode())

        receive_thread = threading.Thread(target=self.receive_messages, args=(client_socket,))
        receive_thread.start()

        while True:
            message = input()
            if message == 'exit':
                break
            client_socket.send(message.encode())

    def chat_with_user(self, user_host, user_port):
        nickname = input("Enter your nickname: ")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((user_host, user_port))
        client_socket.send(nickname.encode())

        receive_thread = threading.Thread(target=self.receive_messages, args=(client_socket,))
        receive_thread.start()

        while True:
            message = input()
            if message == 'exit':
                break
            client_socket.send(message.encode())

    def receive_messages(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode()
                print(message)
            except:
                break


if __name__ == '__main__':
    chat = P2PChat()
    chat.start()
