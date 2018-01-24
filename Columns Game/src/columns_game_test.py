#Longinus Pun: 90955222

import pygame, random, sys
import columns_rules_test as cr

#Colors
BACKGROUND = pygame.Color(41, 49, 52)
WHITE = pygame.Color(255,255,255)
BLACK = pygame.Color(0,0,0)
YELLOW = pygame.Color(255,255,0)

A = pygame.Color(255,0,0) #Red
B = pygame.Color(255,127,0) #Orange
C = pygame.Color(135,135,90) #Tan
D = pygame.Color(255,0,127) #Pink
E = pygame.Color(255,0,255) #Purple
F = pygame.Color(0,255,0) #Lime
G = pygame.Color(0,255,255) #Cyan
H = pygame.Color(0,127,255) #Light Blue
I = pygame.Color(0,0,255) #Blue
J = pygame.Color(28,172,12) #Green

ROWS = 12
COLUMNS = 6

##JEWELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
JEWELS = ['A', 'B', 'C', 'D', 'E', 'F']

def content_color(content: str) -> 'Color':
    '''Return pygame.Color for jewel content'''
    colors = dict()
    colors[cr.EMPTY] = WHITE
    colors['A'] = A
    colors['B'] = B
    colors['C'] = C
    colors['D'] = D
    colors['E'] = E
    colors['F'] = F
    colors['G'] = G
    colors['H'] = H
    colors['I'] = I
    colors['J'] = J

    return colors[content]


class ColumnsGame:

    def __init__(self):
        '''initialization'''
        self._running = True
        self._state = cr.game_state(ROWS,COLUMNS)
        self._size = (300,600)        
        


    def run(self) -> None:
        '''Run method'''
        pygame.init()

        self._resize_surface(self._size)

        clock = pygame.time.Clock()
        

        self._redraw()
        tick = 0
        while self._running:
            self._running = not self._state.game_over
            clock.tick(60)
            self._handle_events()
            self._redraw()
            if tick%60 == 0:
                self._state.advance()
                tick = 0
            self._create_faller()
            tick +=1

        pygame.quit()
        print(self._state.score)
        sys.exit()

    def _handle_events(self) -> None:
        '''handles quiting, resizing, and key presses'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end_game()
            elif event.type == pygame.VIDEORESIZE:
                self._resize_surface(event.size)
            elif event.type == pygame.KEYDOWN:
                self._on_key_down(event.key)

    def _redraw(self) -> None:
        '''Draw window'''
        surface = pygame.display.get_surface()

        surface.fill(BACKGROUND)

        self._size = surface.get_size()

        self._draw_board()
        pygame.display.flip()

    def _draw_board(self) -> None:
        '''Draws board'''
        for row in range(self._state.rows):
            for col in range(self._state.columns):
                self._draw_block(self._state.board[row][col], (col,row))

    def _draw_block(self, block: cr.block, location: (int, int)) -> None:
        '''Draws individual blocks given block and position'''
        surface = pygame.display.get_surface()
        x, y = location

        block_loc = pygame.Rect((x/COLUMNS)*self._size[0]+1, (y/ROWS)*self._size[1]+1, (self._size[0]/COLUMNS)-1,(self._size[1]/ROWS)-1)

        if block.state == cr.FROZEN:
            pygame.draw.rect(surface, content_color(block.content), block_loc)
        elif block.state == cr.MATCH:
            pygame.draw.rect(surface, BLACK, block_loc)
        elif block.state == cr.FALLER:
            pygame.draw.rect(surface, content_color(block.content), block_loc)
            pygame.draw.rect(surface, BLACK, block_loc, 1)
        elif block.state == cr.LANDED:
            pygame.draw.rect(surface, content_color(block.content), block_loc)
            pygame.draw.rect(surface, YELLOW, block_loc, 1)

    def _end_game(self) -> None: 
        '''Quit Game'''
        self._running = False

    def _resize_surface(self, size: (int, int)) -> None:
        '''Resize window'''
        pygame.display.set_mode(size, pygame.RESIZABLE)

    def _on_key_down(self, key):
        '''Action for each key press'''
        if key == pygame.K_SPACE:
            self._state.rotate_faller()
        elif key == pygame.K_RIGHT:
            self._state.faller_right()
        elif key == pygame.K_LEFT:
            self._state.faller_left()
        elif key == pygame.K_DOWN:
            self._state.advance()

    def _create_faller(self):
        '''Creates random faller once previous one is complete'''
        if self._state.faller_frozen() and not self._state.matches_exist():
            self._state.init_faller(random.choice(JEWELS),random.choice(JEWELS),random.choice(JEWELS),random.choice(range(COLUMNS)),cr.FALLER)
        
            
if __name__ == '__main__':
    ColumnsGame().run()
