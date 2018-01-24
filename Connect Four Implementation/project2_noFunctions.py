import connectfour

def colorPrint(color: int) -> str:
    if (color == connectfour.RED):
        return "R"
    if (color == connectfour.YELLOW):
        return "Y"
    if (color == connectfour.NONE):
        return "."

def printBoard(currentBoard: connectfour.GameState):
    print ("1  2  3  4  5  6  7")
    for row in range(connectfour.BOARD_ROWS):
        for col in range(connectfour.BOARD_COLUMNS):
            print(colorPrint(currentBoard.board[col][row]) + "  ", end="")
        print()

def turn(currentBoard: connectfour.GameState) -> connectfour.GameState:
    while True:
        printBoard(currentBoard)
        if (currentBoard.turn == connectfour.RED):
            print ("Red Turn")
        if (currentBoard.turn == connectfour.YELLOW):
            print ("Yellow Turn")
            
        nextIn = input("\n\"POP *column number*\" to pop out piece  |  \"DROP *column number*\" to drop piece\n")

        if nextIn.upper().startswith("POP "):
            try:
                return connectfour.pop(currentBoard, int(nextIn[4::]) - 1)
            except:
                print("Please Enter Proper Input")
##                return turn(currentBoard)
                continue
        elif nextIn.upper().startswith("DROP "):
            try:
                return connectfour.drop(currentBoard, int(nextIn[5::]) - 1)
            except:
                print("Please Enter Proper Input")
##                return turn(currentBoard)
                continue
        print("Please Enter Proper Input:")
##        return turn(currentBoard)
        
            

currentBoard = connectfour.new_game()


while(connectfour.winner(currentBoard) == connectfour.NONE):
    currentBoard = turn(currentBoard)
    
printBoard(currentBoard)
print("WINNER: ", end = "")
if (connectfour.winner(currentBoard) == connectfour.RED):
    print ("Red")
if (connectfour.winner(currentBoard) == connectfour.YELLOW):
    print ("Yellow")

##printBoard(currentBoard)

##nextIn = input("\n\"P *column number*\" to pop out piece  |  \"D *column number*\" to drop piece\n")



