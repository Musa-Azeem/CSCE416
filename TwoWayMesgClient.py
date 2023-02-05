"""
    Two Way Message Client
    Author: Musa Azeem
    Date: 2/5/23

    Uses a domain socket to send and recieve messages to/from a server
"""

from socket import *
from sys import *


# Take server name and port number its listening on as cmd line arguments
if len(argv) != 3:
    print("usage:", argv[0], "[server name] [server port]")
    exit()

# Get server's whereabouts
serverName = argv[1]
serverPort = int(argv[2])

# Create a socket
sock = socket(AF_INET, SOCK_STREAM)

# Connect to the server
sock.connect((serverName, serverPort))
print(f"Connected to server at ('{serverName}', '{serverPort}')");

# Make a file stream out of socket
sockFile = sock.makefile(mode='rw')

# Keep reading lines and send to server
for line in stdin:
    # Send the line to server
    sock.send(line.encode())

    # Get response from server
    response = sockFile.readline()
    print('Server:', response, end='')

# done
print("Closing connection")
sock.close()