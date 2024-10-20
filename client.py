import socket
import os
import threading

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000
BUFFER_SIZE = 1024

messages = []

def send_file(client_socket, filename):
    if os.path.isfile(filename):
        messages.append(f"[Sending file: {filename}]")
        print_conversation()
        
        with open(filename, "rb") as f:
            while True:
                file_chunk = f.read(BUFFER_SIZE)
                if not file_chunk:
                    break
                client_socket.send(file_chunk)

        messages.append(f"[File sent: {filename}]")
        print_conversation()

def receive_file(client_socket):
    print_conversation()

    while True:
        file_chunk = client_socket.recv(BUFFER_SIZE)
        if not file_chunk:
            break
        print(file_chunk.decode('utf-8'), end="") 
    print_conversation()

def handle_server(client_socket):
    while True:
        try:
            response = client_socket.recv(BUFFER_SIZE).decode('utf-8')
            if not response:
                break
            if response.startswith("/file "):
                filename = response.split(":")[1]
                receive_file(client_socket, filename)
            else:
                messages.append(f"Server: {response}")
                print_conversation()
        except:
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    print(f"Connected to server at {SERVER_HOST}:{SERVER_PORT}")

    threading.Thread(target=handle_server, args=(client_socket,)).start()

    while True:
        message = input()
        if message.startswith("/file "):
            filename = message.split(" ", 1)[1]
            send_file(client_socket, filename)
        elif message == "/quit":
            client_socket.close()
            break
        elif message:
            client_socket.send(message.encode('utf-8'))
            messages.append(f"Client: {message}")
            print_conversation()

def print_conversation():
    os.system('cls')
    print("\n".join(messages))

if __name__ == "__main__":
    start_client()
