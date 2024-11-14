import socket
import os

SERVER_PORT = 12001
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('', SERVER_PORT))
server_socket.listen(1)

print("The server is ready to receive on port", SERVER_PORT)

while True:
    connection_socket, client_address = server_socket.accept()
    print("Connected to client at", client_address)

    # Receive the command from the client
    command = connection_socket.recv(1024).decode()
    print("Received command:", command)

    # Handle the `ls` command
    if command == "ls":
        # List files in the current directory
        files = os.listdir('.')  # Get list of files
        files_list = "\n".join(files)  # Join files with newline for readability
        connection_socket.send(files_list.encode())  # Send list back to client
    else:
        # Send a message for unsupported commands
        connection_socket.send("Unsupported command".encode())

    # Close the connection after each command for simplicity
    connection_socket.close()