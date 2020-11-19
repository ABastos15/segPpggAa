import random
from collections import deque


#args p1 p2 p3 e p4 sºao as portas!!!

def generateCards(p1,p2,p3,p4,clients):
    #O = ouros
    #C = copas
    #E = espadas
    #P = paus
    # 2 3 4 5 6 7
    # v = Valete Q = Dama K = King  A = Ace
    cartas = ["2O", "3O", "4O", "5O", "6O", "7O", "VO", "QO", "KO", "AO", "2C", "3C", "4C", "5C", "6C", "7C", "VC", "QC", "KC", "AC", "2E", "3E", "4E", "5E", "6E", "7E", "VE", "QE", "KE", "AE", "2P", "3P", "4P", "5P", "6P", "7P", "VP", "QP", "KP", "AP"]
    #p1 = player 1
    #p2 = player 2
    #p3 = player 3
    #p4 = player 4
    #Escolher 10 cartas diferentes para jogador
    p1r=clients[p1]['address'][1]
    p2r=clients[p2]['address'][1]
    p3r=clients[p3]['address'][1]
    items = deque(cartas)
    items.rotate(p1r)
    cartas = list(items)
    p1 = random.sample(cartas, k=10)
        #remover cartas da lista cartas
    cartas = [x for x in cartas if (x not in p1)]
    #Escolher 10 cartas diferentes para jogador
    items = deque(cartas)
    items.rotate(p2r)
    cartas=list(items)
    p2 = random.sample(cartas, k=10)
        #remover cartas da lista cartas
    cartas = [x for x in cartas if (x not in p2)]
    #Escolher 10 cartas diferentes para jogador
    items = deque(cartas)
    items.rotate(p3r)
    cartas=list(items)
    p3 = random.sample(cartas, k=10)
        #remover cartas da lista cartas
    cartas = [x for x in cartas if (x not in p3)]
    #Escolher 10 cartas diferentes para jogador
    p4 = random.sample(cartas, k=10)
        #remover cartas da lista cartas
    cartas = [x for x in cartas if (x not in p4)]


    hands = [p1,p2,p3,p4]
    return hands


def gameWinner(p1,p2,p3,p4):
    #lista de cartas que player recebeu nas rondas que ganhou
    #p1 player1
    #p2 player2
    #p3 player3
    #p4 player4
    #por ordem de jogada
    #Dama de espadas vale 10 pontos
    #copa vale 1 ponto cada
    copas = ["2C", "3C", "4C", "5C", "6C", "7C", "VC", "QC", "KC", "AC"]
    dama = "QE";
    print(p1)
    print(p2)
    print(p3)
    print(p4)
    #copas que cada jogador recebeu
    copasp1 =  [x for x in p1 if x in copas]
    copasp2 =  [x for x in p2 if x in copas]
    copasp3 =  [x for x in p3 if x in copas]
    copasp4 =  [x for x in p4 if x in copas]

    #pontos que o jogador ganha so das copas
    pontosp1 = copasp1.__len__()
    pontosp2 = copasp2.__len__()
    pontosp3 = copasp3.__len__()
    pontosp4 = copasp4.__len__()

    #pontos que o jogador ganha da dama de espadas
    if p1.__contains__(dama):
        pontosp1+=10
    if p2.__contains__(dama):
        pontosp2+=10
    if p3.__contains__(dama):
        pontosp3+=10
    if p4.__contains__(dama):
        pontosp4+=10
    print(pontosp1)
    print(pontosp2)
    print(pontosp3)
    print(pontosp4)

    if pontosp1<pontosp2 and pontosp1<pontosp3 and pontosp1<pontosp4:
        return 0
    if pontosp2<pontosp1 and pontosp2<pontosp3 and pontosp2<pontosp4:
        return 1
    if pontosp3<pontosp1 and pontosp3<pontosp2 and pontosp3<pontosp4:
        return 2
    if pontosp4<pontosp1 and pontosp4<pontosp2 and pontosp4<pontosp3:
        return 3
    return 5


def handWinner(p1,p2,p3,p4):
    #p1 player1
    #p2 player2
    #p3 player3
    #p4 player4
    #por ordem de jogada
    #p1="7E"
    #p2="2E"
    #p3="3O"
    #p4="5E"
    #mão actual
    hand=[p1,p2,p3,p4]
    #naipe da jogada actual
    handNaipe = p1[1]
    #jogadores que jogaram outro naipe
    losers = [x for x in hand if x[1]!=handNaipe]
    #mão actual sem jogadores que ja perderam
    handWinners = [x for x in hand if (x not in losers)]
    #jogadores com figuras
    letras =  [x for x in handWinners if x[0].isalpha()]
    #se houver jogador com figura
    if len(letras)>0:
        winner = 0
        for x in letras:
            #A vale mais ganha
            if x[0] ==  'A' :
                winner = 4
                pWinner = x
            #K perde com A ganha aos outros
            if x[0] == 'K' and winner != 4:
                winner = 3
                pWinner = x
            #Q perde com K,A ganha aos outros
            if x[0] == 'Q' and winner != 3 and winner != 4:
                winner = 2
                pWinner = x
            #J perde com Q,K,A ganha aos outros
            if x[0] == 'J'  and winner != 2 and winner != 3 and winner != 4:
                winner = 1
                pWinner = x
        count=0
        for hWinner in hand:
            if hWinner==pWinner:
                break
            count+=1
        print("WINNER"+str(count))
        return count
    #se so houver jogadores com numeros
    else:
        #sort players por carta mais alta
        numeros = [x for x in handWinners if x[0].isdigit()]
        numeros.sort()
        count=0
        for hWinner in hand:
            if hWinner==numeros[numeros.__len__()-1]:
                break
            count+=1
        print("WINNER"+str(count))
        return count