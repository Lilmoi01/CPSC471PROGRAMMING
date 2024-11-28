import socket
import os

serv_host = '127.0.0.1'
serv_port = 65432
buffer_size = 1024

def list_files():
    """List files in the current directory."""
    return '|'.join(os.listdir('.'))

def handle_ls(cli_socket):
    """Process the `ls` command."""
    files = list_files()
    cli_socket.send(f"LS|{files}".encode('utf-8'))

def handle_get(cli_socket, file_name):
    """Process the `get` command."""
    try:
        with open(file_name, 'rb') as file:
            file_size = os.path.getsize(file_name)
            cli_socket.send(f"SendFile|{file_size}".encode('utf-8'))
            ack = cli_socket.recv(buffer_size).decode('utf-8')

            if ack == "Ready":
                while chunk := file.read(buffer_size):
                    cli_socket.send(chunk)
                    # Waiting for ACK
                    cli_socket.recv(buffer_size)  
                print(f"File '{file_name}' sent successfully.")
    except FileNotFoundError:
        cli_socket.send("FileNotFound|0".encode('utf-8'))

def handle_put(cli_socket, file_name, file_size):
    """Process the `put` command."""
    cli_socket.send("Ready".encode('utf-8'))
    with open(file_name, 'wb') as file:
        received_size = 0
        while received_size < file_size:
            chunk = cli_socket.recv(buffer_size)
            file.write(chunk)
            received_size += len(chunk)
            cli_socket.send("Acknowledge".encode('utf-8'))
    print(f"File '{file_name}' received successfully.")

def process_cmd(cli_socket, cmd, args):
    """Process a client command."""
    if cmd == "ls":
        handle_ls(cli_socket)
    elif cmd == "get":
        file_name = args[0]
        handle_get(cli_socket, file_name)
    elif cmd == "put":
        file_name = args[0]
        file_size = int(args[1])
        handle_put(cli_socket, file_name, file_size)
    else:
        print(f"Unknown command: {cmd}")

def handle_client(cli_socket):
    """Handle client connections and process requests."""
    request = cli_socket.recv(buffer_size).decode('utf-8')
    print(f"Received request: {request}")
    
    # Checks if the request is formatted correctly
    if '|' in request:
        cmd, *args = request.split('|')
        process_cmd(cli_socket, cmd, args)
    else:
        print(f"Malformed request: {request}")
        cli_socket.send("Error|Malformed request".encode('utf-8'))
    
    cli_socket.close()

def start_server():
    """Start the FTP server."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((serv_host, serv_port))
    server_socket.listen(5)
    print(f"Server listening on {serv_host}:{serv_port}")

    while True:
        cli_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        handle_client(cli_socket)

if __name__ == "__main__":
    start_server()
