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
dominosF = {}
rounds=0
handPlayers = 0
firstPlayer=0

print(f'Listening for connections on {IP}:{PORT}...')

class Player:
    hand = []
    client_socket=""
    user=""
    def __init__(self, client_socket, hand,user):
        self.client_socket = client_socket
        self.hand = hand
        self.user = user

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
        client_socket.send(server_header + "SERVER ".encode('utf-8') +message_header + message)
        print(message_header.decode('utf-8')+message.decode('utf-8'))
        return True
    except:
        return False

def deletePlayer(client_socket):
    try:
        message = "NUMERO DE CLIENTES EXCEDIDO".encode('utf-8')
        send_message(client_socket, message)
        sockets_list.remove(client_socket)
        del clients[client_socket]
        return True
    except:
        return False
def addPlayer(client_socket,user):
    try:
        player=Player(client_socket,[],user)
        sockets_list.append(client_socket)
        clients[client_socket] = player
        print('Accepted new connection from {}:{}, username: {}'.format(*client_address,clients[client_socket].user['data'].decode('utf-8')))
        return True
    except:
        return False
def closedConnection(notified_socket):
    print('Closed connection from: {} {}'.format(*client_address,clients[notified_socket].user['data'].decode('utf-8')))
    sockets_list.remove(notified_socket)
    del clients[notified_socket]

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

            addPlayer(client_socket,user)

            if clients.__len__()>4:
                print('Closed connection from: {}'.format(*client_address,clients[client_socket].user['data'].decode('utf-8')))
                deletePlayer(client_socket)
                continue

            if clients.__len__() <= 4 and rounds == 0:
                count = 0
                players = {}
                for player in clients:
                    players[count] = player
                    count += 1
                print(user)

            if clients.__len__() >= 2 :
                for p in clients:
                    print("send message _ start game")
                    send_message(p,"Do you want to start the game ?")

            if clients.__len__() >= 2 and rounds == 1:
                #generate dominos, find who is first to play
                dominosF = gl.generateDominos(dominosF)
                firstPlayer=gl.firstPlayer(dominosF, clients)
                dominosF = gl.generateDominos(dominosF)
                #send message to activate first player
                for user in clients:
                    print(149)
                    print(firstPlayer)
                    print(clients[firstPlayer].user)
                    send_message(firstPlayer, clients[firstPlayer].user)

        else:
            message = receive_message(notified_socket)


            if message is False:
                closedConnection(notified_socket)
                continue

            user = clients[notified_socket]
            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

            if rounds==0:
                if(message["data"].decode("utf-8")=="start"):
                    rounds=1
                    continue
            #if there's dominos
            if len(dominosF) != 0 & players[0].hand<5 & players[1].hand<5 & players[2].hand<5 & players[3].hand<5 :
                #pick domino notify next player
                clients[notified_socket].hand.append(dominosF.pop(message["data"].decode("utf-8")))
                boola = False
                for nextUser in players:
                    if(boola):
                        break
                    if(nextUser==clients[notified_socket]):
                        boola=True

                for user in clients:
                    send_message(user.client_socket, nextUser)





    for notified_socket in exception_sockets:
        # Remove from list for socket.socket()
        closedConnection(notified_socket)
