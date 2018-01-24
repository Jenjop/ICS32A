#Longinus Pun: 90955222
EMPTY = " "

#States
FROZEN = 0
FALLER = 1
LANDED = 2
MATCH = 3

class game_state():

    def __init__(self, rows: int, columns: int):
        '''initialization'''
        self.board = []
        self.rows = rows
        self.columns = columns
        for row in range(self.rows):
            self.board.append([])
            for col in range(self.columns):
                self.board[-1].append(block(EMPTY, FROZEN))        
        self.game_over = False
        self.gravity_check = False

        self.faller = faller(EMPTY, EMPTY, EMPTY, 0,0,FROZEN)
        self.faller.freeze()

    def display(self): #Display Board
        '''Used for Debugging'''
        for row in range(self.rows):
            print('|',end = "")
            for col in range(self.columns):
                self.board[row][col].print()
            print("|")
        print(EMPTY + "-" * 3 * self.columns + EMPTY)


    def advance(self): #Advance Faller
        '''game tick'''
        self.faller_drop()
        self.remove_matches()
        self.move_down()
        self.check_matches()

    def check_matches(self):
        '''check for mathces'''
        self.horizontal_check()
        self.vertical_check()
        self.diagonal_check_down()
        self.diagonal_check_up()

    def matches_exist(self) -> bool:
        '''If there are any matched blocks'''
        for row in range(self.rows):
            for col in range(self.columns):
                if self.board[row][col].state == MATCH:
                    return True
        return False

    def move_down(self):
        '''move faller down'''
        self.gravity_check = True
        while self.gravity_check:
            self.gravity_check = False
            for row in range(self.rows, -1, -1):
                for col in range(self.columns):
                    if row < self.rows-1:
                        if self.board[row][col].content != EMPTY and self.board[row][col].state == FROZEN and self.board[row+1][col].content == EMPTY:
                            self.board[row+1][col] = self.board[row][col]
                            self.board[row][col] = block(EMPTY,FROZEN)
                            self.gravity_check = True



    def remove_matches(self): #Removes matched blocks and shifts above blocks down
        '''deletes matched blocks'''
        for row in range(self.rows):
            for col in range(self.columns):
                if self.board[row][col].state == MATCH:
                    self.board[row][col] = block(EMPTY,FROZEN)



    def horizontal_check(self):#Check for horizontal matches
        '''check for horizontal matches'''

        for row in range(self.rows): #For each row

            _streak_end = 0 #Denote how far streak goes
            for col_start in range(self.columns-2): #For each block in the row

                if _streak_end <= col_start: #Only if block is on the right of end of last streak
                    _check_jewel = self.board[row][col_start].content #Jewel to match against
                    if _check_jewel != EMPTY and self.board[row][col_start].matchable(): #Won't check for EMPTY matches

                        _streak_end = col_start #Reset end of streak
                        for col_end in range(col_start+1, self.columns): #Check all jewels to the right
                            if self.board[row][col_end].matchable() and self.board[row][col_end].content == _check_jewel: #Iterates so long as it is the same
                                _streak_end += 1
                            else:
                                break
                        self.match_horizontal(row,col_start,_streak_end)
                    _check_jewel = EMPTY
                    _streak_end = 0

    def match_horizontal(self, row: int, col_start: int, col_end: int): #Sets blocks as matched
        '''mark matched blocks for horizontal'''
        if col_end - col_start >= 2:
            for col in range(col_start, col_end+1):
                self.board[row][col].match()


    def vertical_check(self):#Check for vertical matches
        '''checks vertical matches'''

        for col in range(self.columns): #For each column

            _streak_end = 0 #Denote how far streak goes
            for row_start in range(self.rows-2): #For each block in the column

                if _streak_end <= row_start: #Only if block is on the below of end of last streak
                    _check_jewel = self.board[row_start][col].content #Jewel to match against
                    if _check_jewel != EMPTY and self.board[row_start][col].matchable(): #Won't check for EMPTY matches

                        _streak_end = row_start #Reset end of streak
                        for row_end in range(row_start+1, self.rows): #Check all jewels to the right
                            if self.board[row_end][col].matchable() and self.board[row_end][col].content == _check_jewel: #Iterates so long as it is the same
                                _streak_end += 1
                            else:
                                break
                        self.match_vertical(row_start,_streak_end,col)
                    _check_jewel = EMPTY
                    _streak_end = 0

    def match_vertical(self, row_start: int, row_end: int, col: int): #Sets blocks as matched
        '''marks matched vertical matches'''
        if row_end - row_start >= 2:
            for row in range(row_start, row_end+1):
                self.board[row][col].match()

    def diagonal_check_down(self):#Top left to bottom right
        '''check for matches top left to bottom right'''

        for row_start in range(self.rows): #For each row

            for col_start in range(self.columns-2): #For each column

                _check_jewel = self.board[row_start][col_start].content #Jewel to match against
                _match_length = 0
                if _check_jewel != EMPTY and self.board[row_start][col_start].matchable(): #Won't check for EMPTY matches
                    for streak_length in range(min(self.rows-row_start,self.columns-col_start)): #Check all jewels to the right
                        if self.board[row_start+streak_length][col_start+streak_length].matchable() and self.board[row_start+streak_length][col_start+streak_length].content == _check_jewel: #Iterates so long as it is the same
                            _match_length = streak_length + 1
                            continue
                        else:
                            break
                    self.match_diagonal_down(row_start,col_start,_match_length)
                    _match_length = 0
                _check_jewel = EMPTY

    def match_diagonal_down(self, row_start: int, col_start: int, match_length: int):
        '''mark matches from diagonal_check_down'''
        if match_length >=3:
            for streak_length in range(match_length):
                self.board[row_start+streak_length][col_start+streak_length].match()

    def diagonal_check_up(self):#Top right to bottom left
        '''checks for matches from bottom left to top right'''

        for row_start in range(self.rows): #For each row

            for col_start in range(self.columns-2): #For each column

                _check_jewel = self.board[row_start][col_start].content #Jewel to match against
                _match_length = 0
                if _check_jewel != EMPTY and self.board[row_start][col_start].matchable(): #Won't check for EMPTY matches
                    for streak_length in range(min(row_start+1,self.columns-col_start)): #Check all jewels to the right
                        if self.board[row_start-streak_length][col_start+streak_length].matchable() and self.board[row_start-streak_length][col_start+streak_length].content == _check_jewel: #Iterates so long as it is the same
                            _match_length = streak_length + 1
                            continue
                        else:
                            break
                    self.match_diagonal_up(row_start,col_start,_match_length)
                    _match_length = 0
                _check_jewel = EMPTY

    def match_diagonal_up(self, row_start: int, col_start: int, match_length: int):
        '''marks matches from diagonal_check_up'''
        if match_length >=3:
            for streak_length in range(match_length):
                self.board[row_start-streak_length][col_start+streak_length].match()

    def quit(self):
        '''quite game'''
        self.game_over = True

    def faller_in_action(self): #If Faller is Falling
        '''the faller is falling'''
        if self.faller.state == FALLER:
            return True
        return False

    def faller_frozen(self): #If Faller is Frozen
        '''the faller is frozen'''
        if self.faller.state == FROZEN:
            return True
        return False

    def init_faller(self, jewel1: str, jewel2: str, jewel3: str, col: int, state: int): #Create Initial Faller
        '''create faller'''
        self.faller = faller(jewel1, jewel2, jewel3, 0, col, state)
        self.place_faller()

    def place_faller(self): #Place Faller onto Board
        '''place faller on board'''
        if self.board[self.faller.row][self.faller.column].content != EMPTY:
            self.faller.land()
        self.board[self.faller.row][self.faller.column] = self.faller.j3

    def update_faller(self): #Update Faller on Board (After Rotate)
        '''update faller location on baord'''
        if self.check_valid(self.faller.row-2, self.faller.column):
            self.board[self.faller.row-2][self.faller.column] = self.faller.j1
        if self.check_valid(self.faller.row-1, self.faller.column):
            self.board[self.faller.row-1][self.faller.column] = self.faller.j2
        if self.check_valid(self.faller.row, self.faller.column):
            self.board[self.faller.row][self.faller.column] = self.faller.j3

    def clear_faller(self): #Remove Faller from Board (After Movement)
        '''clear faller from board'''
        if self.check_valid(self.faller.row-2, self.faller.column):
            self.board[self.faller.row-2][self.faller.column] = block(EMPTY, FROZEN)
        if self.check_valid(self.faller.row-1, self.faller.column):
            self.board[self.faller.row-1][self.faller.column] = block(EMPTY, FROZEN)
        if self.check_valid(self.faller.row, self.faller.column):
            self.board[self.faller.row][self.faller.column] = block(EMPTY, FROZEN)

    def faller_left(self): #Move Faller Left
        '''move faller left'''
        self.faller_move(-1)

    def faller_right(self): #Move Faller Right
        '''move faller right'''
        self.faller_move(1)

    def faller_move(self, direction: int):
        '''move faller'''
        if self.faller_in_action():
            if self.check_valid(self.faller.row-2, self.faller.column + direction): #All 3 Parts
                if self.faller_check(self.faller.row, self.faller.column + direction):
                    self.clear_faller()
                    self.board[self.faller.row-2][self.faller.column + direction] = self.faller.j1
                    self.board[self.faller.row-1][self.faller.column + direction] = self.faller.j2
                    self.board[self.faller.row][self.faller.column + direction] = self.faller.j3

                    self.faller.move(direction)

            elif self.check_valid(self.faller.row-1, self.faller.column + direction): #Only Bottom 2
                if self.faller_check(self.faller.row, self.faller.column + direction):
                    self.clear_faller()
                    self.board[self.faller.row-1][self.faller.column + direction] = self.faller.j2
                    self.board[self.faller.row][self.faller.column + direction] = self.faller.j3

                    self.faller.move(direction)

            elif self.check_valid(self.faller.row, self.faller.column + direction): #Only Bottom Jewel
                if self.faller_check(self.faller.row, self.faller.column + direction):
                    self.clear_faller()
                    self.board[self.faller.row][self.faller.column + direction] = self.faller.j3

                    self.faller.move(direction)

    def faller_drop(self): #Advance Faller
        '''drop faller/land/freeze'''
        if self.faller_in_action():
            if self.check_empty_valid(self.faller.row+1, self.faller.column): #If it has somewhere to drop

                if self.check_valid(self.faller.row-1, self.faller.column): #All 3 Jewels
                    self.clear_faller()
                    self.board[self.faller.row-1][self.faller.column] = self.faller.j1
                    self.board[self.faller.row][self.faller.column] = self.faller.j2
                    self.board[self.faller.row+1][self.faller.column] = self.faller.j3

                    self.faller.drop()

                elif self.check_valid(self.faller.row, self.faller.column): #Top Jewel still not visible
                    self.clear_faller()
                    self.board[self.faller.row][self.faller.column] = self.faller.j2
                    self.board[self.faller.row+1][self.faller.column] = self.faller.j3

                    self.faller.drop()
            else: #Go from Falling to Landed
                self.faller.land()
                if not self.check_valid(self.faller.row-2, 0): #If jewels are left above screen
                    self.game_over = True
        else: #Go from Landed to Frozen
            self.faller_freeze()

    def faller_freeze(self):
        '''freeze faller'''
        self.faller.freeze()
        if self.check_valid(self.faller.row-2,0): #Replace faller jewels with normal blocks
            self.board[self.faller.row-2][self.faller.column] = self.copy_block(self.faller.j1)
        if self.check_valid(self.faller.row-1,0): #Replace faller jewels with normal blocks
            self.board[self.faller.row-1][self.faller.column] = self.copy_block(self.faller.j2)
        if self.check_valid(self.faller.row,0): #Replace faller jewels with normal blocks
            self.board[self.faller.row][self.faller.column] = self.copy_block(self.faller.j3)
##        self.init_faller(EMPTY,EMPTY,self.board[0][0].content,0,FROZEN)
        self.faller.clear()

    def rotate_faller(self): #Rotate Faller
        '''rotate faller blocks'''
        if self.faller_in_action():
            self.faller.rotate()
            self.update_faller()

    def check_empty(self, row: int, col: int): #Check of location is empty
        '''check if location is empty'''
        if self.board[row][col].content == EMPTY:
            return True
        return False

    def check_valid(self, row: int, col: int): #Check if location is valid
        '''check if location is valid'''
        if 0 <= row < self.rows:
            if 0 <= col < self.columns:
                return True
        return False

    def check_empty_valid(self, row: int, col: int): #Check if location is valid and empty
        '''check empty and valid'''
        if self.check_valid(row,col):
            if self.check_empty(row,col):
                return True
        return False

    def faller_check(self, row: int, col: int): #Check if all 3 blocks of faller have space to move
        '''check if location is available to move faller'''        
        for r in range(max(0,row-2),row+1):
            if not self.check_empty(r,col):
                return False
        return True

    def copy_block(self, jewel: 'block') -> 'block': #Creates block with identical content/state
        '''copy block content and state'''
        return block(jewel.content, jewel.state)


class faller():

    def __init__(self, jewel1: str, jewel2: str, jewel3: str, row: int, col: int, state: int):
        '''create faller'''
        self.j1 = block(jewel1, state)
        self.j2 = block(jewel2, state)
        self.j3 = block(jewel3, state)
        self.row = row
        self.column = col
        self.state = state

    def rotate(self): #Rotates jewel orders
        '''rotate faller'''
        self._temporary_jewel = self.j3

        self.j3 = self.j2
        self.j2 = self.j1
        self.j1 = self._temporary_jewel

    def move(self, direction: int): #Move left or right
        '''move faller'''
        self.column += direction

    def drop(self): #Drop down 1
        '''drop faller'''
        self.row +=  1

    def land(self): #Change state to landed
        '''land faller'''
        self.j1.land()
        self.j2.land()
        self.j3.land()

        self.state = LANDED

    def freeze(self): #Change state to frozen
        '''freeze faller'''
        self.j1.freeze()
        self.j2.freeze()
        self.j3.freeze()

        self.state = FROZEN

    def clear(self):
        '''clear faller'''
        self.j1 = block(EMPTY, FALLER)
        self.j2 = block(EMPTY, FALLER)
        self.j3 = block(EMPTY, FALLER)
        self.row = 0
        self.column = 0
        self.state = FROZEN


class block():

    def __init__(self, content: str, state: int):
        '''create block'''
        self.content = content
        self.state = state

    def update(self, content: str): #Change contents
        '''change block contents'''
        self.content = content

    def print(self): #Print content with state annotation
        '''print block with state'''
        if self.state == 0:
            print(EMPTY + self.content + EMPTY, end = "")
        elif self.state == 1:
            print("[" + self.content + "]", end = "")
        elif self.state == 2:
            print("|" + self.content + "|", end = "")
        elif self.state == 3:
            print("*" + self.content + "*", end = "")

    def land(self): #Change state to landed
        '''land block'''
        self.state = LANDED

    def freeze(self): #Change state to frozen
        '''freeze block'''
        self.state = FROZEN

    def match(self): #Change state to matched
        '''match block'''
        self.state = MATCH

    def matchable(self) -> bool:
        '''block is valid for match check'''
        return self.state == FROZEN or self.state == MATCH
