
"""
    Group Chat Message Server
    Author: Musa Azeem
    Date: 2/27/23
    Implementation of a group chat message server in python
"""

from sys import argv, stdin
from select import select
from socket import socket, AF_INET, SOCK_STREAM

# Check for port number in command line arguments
if len(argv) != 2:
    print('usage:', argv[0], '[port]')
    exit()

server_port = int(argv[1])

# Create the server socket
server_sock = socket(AF_INET, SOCK_STREAM)

# Bind the socket to the given port
server_sock.bind(('', server_port))

# Set the server for listening */
server_sock.listen()
print('Waiting for a client ...')


clients = {}                    # Dictionary of clients
inputs = [stdin, server_sock]   # start by only listening on server socket and stdin

# Main loop - Accept client connections and read and write from/to clients
while(True):
    # Listen to socket for client connections, to all clients for incoming messages
    # Check outputs for free space to write to clients
    readable, _,_ = select(inputs, outputs, [])

    # Check all input sockets
    for s in readable:
        print("ACTIVE CLIENTS: ", [name for _, (name,_) in clients.items()])

        # Handle stdin Input
        if s is stdin:
            print("Input Received From: stdin")
            # Read a line form the keyboard
            line = stdin.readline()

            # If EOF ==> sever wants to close connection to all clients
            if not line:
                print('*** Server closing connection ...')

                # Send the line to clients
                # Close client connections
                for client_sock_file, (client_name, client_sock) in clients.items():
                    print(f'*** Closing Connection to "{client_name}"')
                    client_sock.send(line.encode())
                    client_sock_file.close()
                    client_sock.close()

                # Close server socket
                server_sock.close()
                exit(0)

        # Handle Server Socket Input
        elif s is server_sock:
            print("Input Reveived From: server_sock")
            # Receive new client connection on server socket
            client_sock, client_addr = server_sock.accept()
            print(f'*** Connected to a client at {client_addr}')

            # Make a file stream out of client socket
            client_sock_file = client_sock.makefile()

            # Read client name
            client_name = client_sock_file.readline().strip()
            print(f'*** Connected to Client {client_name}')

            # Add client socket to dictionary and input list
            clients[client_sock_file] = (client_name, client_sock)
            inputs.append(client_sock_file)

        # Handle Client Socket Inputs
        else:
            # Input is from a client - write message to all clients
            print(f'Input Received From: {clients[s][0]}')
            client_name = clients[s][0]
            client_sock = clients[s][1]

            line = s.readline()
            if not line:
                # Remove Client
                print(f'*** Client {clients[s][0]} closed connection')
                s.close()               # Close socket file
                client_sock.close()     # Close socket

                # Remove from clients and inputs list
                del clients[s]
                inputs.remove(s)

                continue

            print(f'\tMSG: {line}')

            # Send Message to all clients
            for other_client_sock_file, (other_client_name, other_client_sock) in clients.items():
                # Skip if its the client sending the message
                if other_client_sock_file is s:
                    continue
                other_client_sock.send(f'[MSG from {client_name}]: {line}'.encode())