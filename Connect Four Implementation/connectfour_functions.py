import connectfour as cf

#Returns Color Symbol based on Int
def colorPrint(color: int) -> str:
    if (color == cf.RED):
        return "R"
    if (color == cf.YELLOW):
        return "Y"
    if (color == cf.NONE):
        return "."

#Prints Board
def printBoard(currentBoard: cf.GameState) -> 'None':
    print ("1  2  3  4  5  6  7")
    for row in range(cf.BOARD_ROWS):
        for col in range(cf.BOARD_COLUMNS):
            print(colorPrint(currentBoard.board[col][row]) + "  ", end="")
        print()

#Prints Turn Info
def printInfo(currentBoard: cf.GameState) -> 'None':
        printBoard(currentBoard)
        if (currentBoard.turn == cf.RED):
            print ("Red Turn")
        if (currentBoard.turn == cf.YELLOW):
            print ("Yellow Turn")

#Processes Action based on input
def processTurn(currentBoard: cf.GameState, action: str, col: int) -> (cf.GameState, str, int):
        if action == "P":
            newBoard, action, col = popBoard(currentBoard, col)
            return newBoard, action, col
        elif action == "D":
            newBoard, action, col = dropBoard(currentBoard,col)
            return newBoard, action, col
        else:
            print("Please Enter Proper Input:")

#Takes User Input
def userInput(currentBoard: cf.GameState) -> (cf.GameState, str, int):
        nextIn = input("\n\"DROP *column number*\" to drop piece  |  \"POP *column number*\" to pop out piece\n")
        if nextIn.upper().startswith("POP "):
            try:
                newBoard, action, col = processTurn(currentBoard, "P", int(nextIn[3::])-1)
                return newBoard, action, col
            except ValueError: #If no column number is input
                print("Please Enter a Column")
                return currentBoard, "NO_COLUMN", 0
        elif nextIn.upper().startswith("DROP "):
            try:
                newBoard, action, col = processTurn(currentBoard, "D", int(nextIn[4::])-1)
                return newBoard, action, col
            except ValueError: #If no column number is input
                print("Please Enter a Column")
                return currentBoard, "NO_COLUMN", 0
        else:
            print("Please Enter Proper Input:")
            return currentBoard, "INVALID_INPUT", 0


#Pop
def popBoard(currentBoard: cf.GameState, col: int) -> (cf.GameState, str, int):
    try:
        return cf.pop(currentBoard, col), "POP ", col
    except ValueError:
        print("Please Enter Valid Column")
        return currentBoard, "INVALID_COLUMN", 0
        pass
    except cf.InvalidMoveError:
        print("Please Enter Valid Pop")
        return currentBoard, "INVALID_MOVE", 0
        pass

#Drop
def dropBoard(currentBoard: cf.GameState, col: int) -> (cf.GameState, str, int):
    try:
        return cf.drop(currentBoard, col), "DROP ", col
    except ValueError:
        print("Please Enter Valid Column")
        return currentBoard, "INVALID_COLUMN", 0
        pass
    except cf.InvalidMoveError:
        print("Please Enter Valid Drop")
        return currentBoard, "INVALID_MOVE", 0
        pass

#Prints Winner
def winMessage(currentBoard: cf.GameState) -> 'None':
    print("WINNER: ", end = "")
    if (cf.winner(currentBoard) == cf.RED):
        print ("Red")
    if (cf.winner(currentBoard) == cf.YELLOW):
        print ("Yellow")





        
