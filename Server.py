#!/usr/bin/python3

import socket

# Create a socket object using IPv4 and TCP protocol
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Allow the server socket to reuse the address
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the server socket to a specific address and port
server.bind(("192.168.87.81", 12345))

print("-" * 60)

# Listen for incoming connections
server.listen()
print("Server is online...\nListening to connections...")

# Accept a client connection
client, address = server.accept()
print(f"Connected to: {address}")

# Receive the operating system information from the client
os = client.recv(1024)
print(f"Getting shell of {os.decode()}...")
print("-" * 60)

try:
    while True:
        # Receive the current working directory from the client
        pwd = client.recv(1024)

        # Prompt the user for a command input
        cmd = input(f"{pwd.decode()} $ ")

        # Send the command input to the client
        client.send(cmd.encode())

        # Check if the user wants to exit the shell
        if cmd == "exit":
            print("-" * 60)
            print("Exitting...")
            break

        received_data = b""
        while True:
            # Receive data from the client in chunks
            data = client.recv(1024)
            if not data:
                break
            received_data += data

            # Check if the end of output marker is received
            if b"END_OF_OUTPUT" in received_data:
                # Extract the output from the received data
                output, _ = received_data.split(b"END_OF_OUTPUT", 1)
                print(output.decode())
                break
except KeyboardInterrupt:
    # Handle KeyboardInterrupt gracefully
    print("\nExiting due to KeyboardInterrupt.")
except BrokenPipeError:
    # Handle BrokenPipeError when the server closes the connection
    print("\nServer closed the connection.")
finally:
    # Close the client and server sockets
    client.close()
    server.close()
