import connectfour as cf
import connectfour_functions as cff
import connectfour_socket as cfs

#Player Turn
def playerTurn(connection: 'connection', currentBoard: cf.GameState) -> cf.GameState:
    while True:
        cff.printInfo(currentBoard)

        while True:
            newBoard, action, col = cff.userInput(currentBoard)#Run/Process User Input
            #Check For Errors
            if (action == "INVALID_INPUT"):
                cff.printBoard(currentBoard)
                continue
            elif (action == "NO_COLUMN"):
                cff.printBoard(currentBoard)
                continue
            elif (action == "INVALID_COLUMN"):
                cff.printBoard(currentBoard)
                continue
            elif (action == "INVALID_MOVE"):
                cff.printBoard(currentBoard)
                continue
            else:
                break

        response = cfs.send_receive(connection, action + str(col+1))#Send Move to Server
        
        if(response.startswith('WINNER_')):#Since player turn, received WINNER_RED
           return newBoard
        elif (response == 'ERROR'):#Should Never Run
            print("Invalid Input")
            continue
        elif (response == "INVALID"):#Should Never Run
              print("Invalid Input")
        elif (response != 'OKAY'):#Bad Response
            cfs.close(connection)#Cut Connection
        return newBoard

#AI Turn
def AITurn(connection: 'connection', currentBoard: cf.GameState) -> cf.GameState:
    while True:
        cff.printInfo(currentBoard)

        response = cfs.receive_response(connection)#Listen for Server
        print(response)#Print Server Move

        #Run/Process Server Input
        if response.upper().startswith("POP "):
            newBoard, action, col = cff.processTurn(currentBoard, "P", int(response[3::])-1)
            return newBoard
        elif response.upper().startswith("DROP "):
            newBoard, action, col = cff.processTurn(currentBoard, "D", int(response[4::])-1)        
            return newBoard
        else:#Bad Response
            cfs.close(connection)#Cut Connection

#Check if Server is Ready
def checkServerReady(connection: 'connection'):
        response = cfs.receive_response(connection)
        if (response.startswith('WINNER_')):#Should only receive WINNER_YELLOW
            cfs.close(connection)#Connection Cut: Game Over
            return 'GameOver'
        elif (response != 'READY'):#Bad Response
            cfs.close(connection)#Connection Cut
            return 'BadConnection'
        else:
            return 'Continue'
if __name__ == '__main__':
    #Ask For Username
    #host = "woodhouse.ics.uci.edu"
    #port = 4444
    #username = Boo

    #Connect to Server
    try:
        host = input('Input Host: ')
        while True:
            try:
                port = int(input('Input Port: '))
                break
            except ValueError:
                print('Invalid Port')
                continue
        connection = cfs.connect(host, port)
        #Caught by cfs.socket.gaierror if unable to connect            

        #Send/Receive Username
        while True:
            username = input('Input Username: ')
            if ((' ' in username) != True):#Repeat until username has no whitespaces
                break
            else:
                print("Username cannot contain whitespace")
            
        response = cfs.send_receive(connection, 'I32CFSP_HELLO ' + username)
        if(response != 'WELCOME ' + username):#Bad Response
            cfs.close(connection)#Cut Connection

        #Reqeust AI Game
        response = cfs.send_receive(connection, 'AI_GAME')
        if(response != 'READY'):#Bad Response
            cfs.close(connection)#Cut Connection

        #Create Blank Game
        currentBoard = cf.new_game()

        #Begin Turns
        while True:
            
            try:#Test for Winner following AI turn(Should Not Run)
                if cf.winner(currentBoard) != cf.NONE:
                    cff.printBoard(currentBoard)
                    cff.winMessage(currentBoard)
                    break
            except AttributeError:
                continue
            
            currentBoard = playerTurn(connection, currentBoard)#Run Player Turn
            
            try:#Test for Winner following Player turn
                if cf.winner(currentBoard) != cf.NONE:
                    cff.printBoard(currentBoard)
                    cff.winMessage(currentBoard)
                    break

            except AttributeError:
                continue
            
            currentBoard = AITurn(connection, currentBoard)#Run AI Turn

            serverCheck = checkServerReady(connection)#Check if Server is ready or game is over
            if serverCheck =='GameOver':#Winner has been declared
                cff.printBoard(currentBoard)
                cff.winMessage(currentBoard)
                break
            elif serverCheck == 'BadConnection':#Bad Response
                print("Bad Connection: Server Cut")
                break
    except ConnectionRefusedError:#Connection was Refused
        print('Connection Refused: Cannot Connect to Server')
    except cfs.socket.gaierror:#Unable to connect
        print('Unable to connect with given host and port')
    except ValueError:#Unable to send bytes
        print('Connection Closed: Cannot access server')

        
