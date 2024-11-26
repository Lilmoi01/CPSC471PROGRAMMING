import socket
import os

serv_host = '127.0.0.1' #local host
serv_port = 65432
buffer_size = 1024

def send_request(cmd, args=""):
    cli_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cli_socket.connect((serv_host, serv_port))
    cli_socket.send(f"{cmd}|{args}".encode('utf-8'))
    return cli_socket

def list_files():
    cli_socket = send_request("ls")
    response = cli_socket.recv(buffer_size).decode('utf-8')
    cmd, files = response.split('|', 1)
    if cmd == "LS":
        print("Files on server:")
        for file in files.split('|'):
            print(file)
    cli_socket.close()

def get_file(file_name):
    cli_socket = send_request("get", file_name)
    response = cli_socket.recv(buffer_size).decode('utf-8')
    cmd, payload = response.split('|', 1)

    if cmd == "SendFile":
        file_size = int(payload)
        cli_socket.send("Ready".encode('utf-8'))

        with open(f"downloaded_{file_name}", 'wb') as file:
            received_size = 0
            while received_size < file_size:
                chunk = cli_socket.recv(buffer_size)
                file.write(chunk)
                received_size += len(chunk)
                cli_socket.send("Acknowledge".encode('utf-8'))
        print(f"File '{file_name}' downloaded successfully.")
    elif cmd == "FileNotFound":
        print(f"Error: File '{file_name}' not found on the server.")
    cli_socket.close()

def put_file(file_name):
    try:
        file_size = os.path.getsize(file_name)
        cli_socket = send_request("put", f"{file_name}|{file_size}")
        response = cli_socket.recv(buffer_size).decode('utf-8')

        if response == "Ready":
            with open(file_name, 'rb') as file:
                while chunk := file.read(buffer_size):
                    cli_socket.send(chunk)
                    # Waiting for ACK
                    cli_socket.recv(buffer_size)  
            print(f"File '{file_name}' uploaded successfully.")
        cli_socket.close()
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found on the client.")

if __name__ == "__main__":
    while True:
        cmd = input("Enter command (ls, get <file>, put <file>, quit): ").strip()
        if cmd == "ls":
            list_files()
        elif cmd.startswith("get "):
            file_name = cmd.split(" ", 1)[1]
            get_file(file_name)
        elif cmd.startswith("put "):
            file_name = cmd.split(" ", 1)[1]
            put_file(file_name)
        elif cmd == "quit":
            print("Client is exiting.")
            break
        else:
            print("Unknown command.")
