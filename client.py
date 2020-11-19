import socket
import select
import errno
import sys



HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234
my_username = input("Username: ")

# Create a socket
# socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
# socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to a given ip and port
client_socket.connect((IP, PORT))

# Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
client_socket.setblocking(False)

# Prepare username and header and send them
# We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

def receive_message(client_socket):
    message_header = client_socket.recv(HEADER_LENGTH)
    message_length = int(message_header.decode('utf-8').strip())
    message = client_socket.recv(message_length).decode('utf-8')
    print(message)
    return message

def send_message(client_socket,message):
    try:
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        server_header = f"{len('SERVER'.encode('utf-8')):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(server_header + "SERVER".encode('utf-8') +message_header + message)
        print(message_header.decode('utf-8')+message.decode('utf-8'))
        return True
    except:
        return False

while True:

    try:
        # Now we want to loop over received messages (there might be more than one) and print them
        while True:


            # Receive our "header" containing username length, it's size is defined and constant
            username_header = client_socket.recv(HEADER_LENGTH)
            # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            # Convert header to int value
            username_length = int(username_header.decode('utf-8').strip())

            # Receive and decode username
            username = client_socket.recv(username_length).decode('utf-8')

            # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
            message=receive_message(client_socket)
           
            if message == "NUMERO DE CLIENTES EXCEDIDO":
                print(f'{username} > {message}')
                sys.exit()
            if message == my_username+">" and username==my_username:
                message = input(f'{my_username} > ').upper()

                while len(message)<2 or len(message)>2:
                    message = input(f'{my_username} > ').upper()



                # Wait for user to input a message

                # If message is not empty - send it
                if message:

                    # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
                    send_message(client_socket,message)
         
            if  my_username in str(username) :

                # Print message
                print(f'{username} > {message}')


    except IOError as e:
        # This is normal on non blocking connections - when there are no incoming data error is going to be raised
        # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
        # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
        # If we got different error code - something happened
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()
        # We just did not receive anything
        continue

    except Exception as e:
        # Any other exception - something happened, exit
        print('Reading error: '.format(str(e)))
        print(e)
        sys.exit()

