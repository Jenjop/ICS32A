import connectfour as cf
import connectfour_functions as cff

#Turn
def turn(currentBoard: cf.GameState) -> cf.GameState:
    while True:
        cff.printInfo(currentBoard)

        newBoard, action, col = cff.userInput(currentBoard)
        return newBoard
        


if __name__ == '__main__':
    currentBoard = cf.new_game()


    while True:
        try:
            if cf.winner(currentBoard) != cf.NONE:
                print (cf.winner(currentBoard))
                break
        except AttributeError:
            continue
        currentBoard = turn(currentBoard)
        
    cff.printBoard(currentBoard)
    cff.winMessage(currentBoard)





