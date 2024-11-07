import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))  # Connect to the server

    while True:
        command = input("ftp> ")
        client_socket.send(command.encode())
        if command == "quit":
            print("Disconnected from server.")
            client_socket.close()
            break
        response = client_socket.recv(1024).decode()
        print(response)

if __name__ == "__main__":
    start_client()
