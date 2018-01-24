import connectfour as cf
import connectfour_functions as cff
import connectfour_socket as cfs

##Test Drop3 Drop7 Drop 4 Drop 7
host = "woodhouse.ics.uci.edu"
port = 4444
username = 'myUser'

def playerTurn(connection: 'connection', currentBoard: cf.GameState) -> cf.GameState:
    while True:
        cff.printInfo(currentBoard)

        while True:
            newBoard, action, col = cff.userInput(currentBoard)
            if (action == "INVALID_INPUT"):
##                print("Please Enter Valid Input")
                cff.printBoard(currentBoard)
                continue
            elif (action == "NO_COLUMN"):
##                print("Please Enter Valid Column")
                cff.printBoard(currentBoard)
                continue
            elif (action == "INVALID_COLUMN"):
##                print("Please Enter Valid Column")
                cff.printBoard(currentBoard)
                continue
            elif (action == "INVALID_MOVE"):
##                print("PLease Enter Valid Move")
                cff.printBoard(currentBoard)
                continue
            else:
                break

        response = cfs.send_receive(connection, action + str(col+1))
        if(response.startswith('WINNER_')):#Since player turn, received WINNER_RED
##           AI_Winner = response[6::]#Not Used
##           print('GameOverPlayer')
##           cfs.close(connection)#Cut, Game Over
           return newBoard
        elif (response == 'ERROR'):
            print("Invalid Input")
            continue
        elif (response != 'OKAY'):
            print('Response1:' + response + '\nCut')
            cfs.close(connection)##CUT
        return newBoard

def AITurn(connection: 'connection', currentBoard: cf.GameState) -> cf.GameState:
    while True:
        cff.printInfo(currentBoard)

        response = cfs.receive_response(connection)
        print(response)
        if response.upper().startswith("POP "):
            newBoard, action, col = cff.processTurn(currentBoard, "P", int(response[3::])-1)
            return newBoard
        elif response.upper().startswith("DROP "):
            newBoard, action, col = cff.processTurn(currentBoard, "D", int(response[4::])-1)        
            return newBoard
        else:
            print('Response:' + response + '\nCut')
            cfs.close(connection)##CUT

def checkServerReady(connection: 'connection'):
        response = cfs.receive_response(connection)
        if (response.startswith('WINNER_')):
##            AI_Winner = response[6::]#Not Used
            cfs.close(connection)##Connection Cut: Game Over
            return 'GameOver'
        elif (response != 'READY'):
            print('Server Response: ' + response + '\nConnection Cut')
            cfs.close(connection)##Connection Cut: Bad Response
            return 'BadConnection'
        else:
            return 'Continue'

        

connection = cfs.connect(host, port)

#Connect to Server
response = cfs.send_receive(connection, 'I32CFSP_HELLO ' + username)

if(response != 'WELCOME ' + username):
    print('Response:' + response + '\nCut')
    cfs.close(connection)##CUT

#Reqeust AI Game
response = cfs.send_receive(connection, 'AI_GAME')
if(response != 'READY'):
    print('Response:' + response + '\nCut')
    cfs.close(connection)##CUT

currentBoard = cf.new_game()
#Begin Turns
while True:
    
    try:
        if cf.winner(currentBoard) != cf.NONE:
            print(cff.colorPrint(cf.winner(currentBoard)))
##            break
##            resp = cfs.receive_response(connection)
##            print('resp0' + resp)
    except AttributeError:
        continue
    
    currentBoard = playerTurn(connection, currentBoard)
    
    try:
        if cf.winner(currentBoard) != cf.NONE:
            cff.printBoard(currentBoard)
            cff.winMessage(currentBoard)
            break
##            break
##            resp = cfs.receive_response(connection)
##            print('resp' + resp)
    except AttributeError:
        continue
    
    currentBoard = AITurn(connection, currentBoard)
    
    serverCheck = checkServerReady(connection)
    if serverCheck =='GameOver':
        cff.printBoard(currentBoard)
        cff.winMessage(currentBoard)
        break
    elif serverCheck == 'BadConnection':
        print("Bad Connection: Server Cut")
        break


    
