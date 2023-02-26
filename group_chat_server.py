
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
outputs = []                    # Start with no output client sockets

# Main loop - Accept client connections and read and write from/to clients
while(True):
    # Listen to socket for client connections, to all clients for incoming messages
    # Check outputs for free space to write to clients
    readable, writable, exceptional = select(inputs, outputs, [])

    # Check all input sockets
    for s in readable:
        if s is stdin:
            # Read a line form the keyboard
            line = stdin.readline()

            # If EOF ==> sever wants to close connection to all clients
            if not line:
                print('*** Server closing connection')

                # Send the line to clients
                # Close client connections
                # Close server socket
                server_sock.close()
                exit(0)

        elif s is server_sock:
            # Receive new client connection on server socket
            client_sock, client_addr = server_sock.accept()
            print(f'Connected to a client at {client_addr}')

            # Make a file stream out of client socket
            client_sock_file = client_sock.makefile()

            # Read client name
            client_name = client_sock_file.readline()
            print(f'Connected to Client {client_name}')

            # Add client socket to dictionary
            clients[client_sock_file] = (client_name, client_sock)

            # Add client to inputs list
            inputs.append(client_sock_file)

        else:
            print(s)
            # Input is from a client - write message to all clients
            if(s.readline()):
                print('yes')



# Keep sending and receiving messages from the client
while True:

    # Wait for a message from keyboard or socket
    readable_set, x, x = select(input_set,[],[])

    # Check if there is a message from the keyboard
    if stdin in readable_set:
        # Read a line form the keyboard
        line = stdin.readline()

        # If EOF ==> sever wants to close connection
        if not line:
            print('*** Server closing connection')
            break

        # Send the line to client
        client_sock.send(line.encode())

    # Check if there is a message from the client
    if client_sock_file in readable_set:
        # Read a message from the client
        line = client_sock_file.readline()

        # If EOF ==> client closed the connection
        if not line:
            print('*** Client closed connection')
            break

        # Display the line
        print('Client:', line, end='')

# Close the connection
client_sock_file.close()
client_sock.close()

# End of program, close server socket
server_sock.close()


