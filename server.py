import socket
import os

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))  # Bind to localhost on port 12345
    server_socket.listen(5)  # Listen for connections
    print("Server is listening on port 12345...")

    while True:
        client_socket, address = server_socket.accept()
        print(f"Connection from {address} has been established.")
        handle_client(client_socket)

def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024).decode()
        if data == "quit":
            print("Client disconnected.")
            client_socket.close()
            break
        elif data == "ls":
            files = os.listdir(".")
            client_socket.send("\n".join(files).encode())
        else:
            client_socket.send("Unknown command".encode())

if __name__ == "__main__":
    start_server()
