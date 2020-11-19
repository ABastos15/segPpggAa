import socket
import select
import serverGameLogic as gl

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234
contestCount=0

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()
validPlay=True

sockets_list = [server_socket]
clients = {}
rounds=0
hand = {}
handPlayer = {}
cardsWin=[[],[],[],[],[]]
handPlayers = 0
handWinner=5
countHandPlayers=0

print(f'Listening for connections on {IP}:{PORT}...')


# manipulação de mensagens recebidas
def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False

        message_length = int(message_header.decode('utf-8').strip())

        return {"header": message_header, "data": client_socket.recv(message_length)}

    except:
        return False

def receive_user(client_socket, client_address):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False

        message_length = int(message_header.decode('utf-8').strip())

        return {"header": message_header, "data": client_socket.recv(message_length), "address": client_address}

    except:
        return False    


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

    read_sockets, write_sockets, exception_sockets = select.select(sockets_list, [], sockets_list)
    if clients.__len__()<4 and rounds ==1:
        rounds=0
        handWinner=0
        gameWinner=0
        handPlayers=0
        hand = {}
        countHandPlayers=0


    for notified_socket in read_sockets:


        if notified_socket == server_socket:

            client_socket, client_address = server_socket.accept()
            user = receive_user(client_socket, client_address)

            if user is False:
                continue

            sockets_list.append(client_socket)
            clients[client_socket] = user
            print('Accepted new connection from {}:{}, username: {}'.format(*client_address,
                                                                            user['data'].decode('utf-8')))
            if clients.__len__()>4:
                print('Closed connection from: {}'.format(*client_address,user['data'].decode('utf-8')))
                message = "NUMERO DE CLIENTES EXCEDIDO".encode('utf-8')
                send_message(client_socket,message)
                sockets_list.remove(client_socket)
                del clients[client_socket]
                continue

        else:
            message = receive_message(notified_socket)


            if message is False:
                print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]
            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')




    for notified_socket in exception_sockets:
        # Remove from list for socket.socket()
        sockets_list.remove(notified_socket)

        # Remove from our list of users
        del clients[notified_socket]
