import socket

SERVER_ADDRESS = 'localhost'
SERVER_PORT = 12001

# Create a TCP client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the server
    client_socket.connect((SERVER_ADDRESS, SERVER_PORT))
    print("Connected to the server")

    # Send the `ls` command to the server
    command = "ls"
    client_socket.send(command.encode())

    # Receive the list of files from the server
    response = client_socket.recv(4096).decode()  # Use a larger buffer if needed
    print("Files on server:\n", response)

finally:
    # Close the connection
    client_socket.close()
    print("Connection closed")