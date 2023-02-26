"""
    Group Chat Message Client
    Author: Musa Azeem
    Date: 2/27/23
    Implementation of a group chat message client in python
"""

from sys import argv, stdin
from select import select
from socket import socket, AF_INET, SOCK_STREAM

# Client needs server's contact information and a name
if len(argv) != 4:
    print("usage:", argv[0], "[server name] [server port] [client name]")
    exit()

# Get command line inputs
server_name = argv[1]
server_port = int(argv[2])
client_name = argv[3]


# Create a socket
sock = socket(AF_INET, SOCK_STREAM)

# Connect to the server
sock.connect((server_name, server_port))
print(f"Connected to server at ('{server_name}', '{server_port}')");

# Make a file stream out of socket
sock_file = sock.makefile(mode='r')

# Make a list of inputs to watch for
input_set = [stdin, sock_file]

# Send name to server
sock.send(f"{client_name}\r\n".encode())

# Keep sending and receiving messages from the server
while True:

    # Wait for a message from keyboard or socket
    readable_set, x, x = select(input_set,[],[])

    # Check if there is a message from the keyboard
    if stdin in readable_set:
        # Read a line form the keyboard
        line = stdin.readline()

        # If EOF ==> client wants to close connection
        if not line:
            print('*** Client closing connection')
            break

        # Send the line to server
        sock.send(line.encode())

    # Check if there is a message from the socket
    if sock_file in readable_set:
        # Read a message from the client
        line = sock_file.readline()

        # If EOF ==> client closed the connection
        if not line:
            print('*** Server closed connection')
            break

        # Display the line
        print('Server:', line, end='')

# Close the connection
sock_file.close()
sock.close()

