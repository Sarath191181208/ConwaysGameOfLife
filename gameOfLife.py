import pygame
import pygame_gui
import random
import os
import json
import numpy as np
import threading

pygame.init()
clock = pygame.time.Clock()
WIN = pygame.display.set_mode((720, 601))
pygame.display.set_caption('conways Game Of life')
FPS = 20
manager = pygame_gui.UIManager(
    (WIN.get_width(), WIN.get_height()), './themePygame_gui.json')

# TODO:  start


def PYtxt(txt: str, fontSize: int = 28, font: str = 'freesansbold.ttf', fontColour: tuple = (0, 0, 0)):
    return (pygame.font.Font(font, fontSize)).render(txt, True, fontColour)


def save(board):
    if not os.path.exists('./saveBoard.json'):
        with open('./saveBoard.json', 'a') as outfile:
            json_object = json.dumps({})
            outfile.write(json_object)
    with open('./saveBoard.json', 'r+') as outfile:
        boardState = {}
        boardState['board'] = {}
        helperDic = {}
        for row in board.cubes:
            for cube in row:
                if cube.value == 1:
                    x, y = cube.row, cube.col
                    key = str(x)+','+str(y)
                    helperDic[key] = cube.value
        boardState['board'][0] = helperDic
        boardState['board']['rows'] = board.rows
        boardState['board']['cols'] = board.cols

        file_data = json.load(outfile)
        outfile.seek(0, 0)
        outfile.truncate()
        file_data.update(boardState)
        outfile.write(json.dumps(file_data, indent=4))

# loads the saved json if it exists


def load(board):
    if os.path.exists('./saveBoard.json'):
        data = json.load(open('./saveBoard.json'))
        data = data['board']
        if board.rows == data['rows'] and board.cols == data['cols']:
            # board clear has a property noAnimation which doesnt play animation
            board.reset()
            for items in data['0']:
                items = items.split(',')
                x = int(items[0])
                y = int(items[1])
                board.cubes[x][y].value = 1
            board.draw()


WHITE = (215, 215, 215)
GREAY = (70, 70, 70)
BLACK = (0, 0, 0)
BLUE = (10, 40, 100)
checksClr = BLUE
boardClr = WHITE
txtClr = GREAY


def createbuttons():

    buttons = {


        'clear_button': {
            'text': 'Clear',
            'tool_tip_text': 'clear the board or   (c : key)'
        },

        'save_button': {
            'text': 'Save',
            'tool_tip_text': 'saves the board or   (s : key)'
        },

        'run_button': {
            'text': 'Start',
            'tool_tip_text': '"start the visualisation (space : key)"'
        },
        'load_button': {
            'text': 'Load',
            'tool_tip_text': 'loads the saved board or (l : key)'
        },
        'create_button': {
            'text': 'Create',
            'tool_tip_text': 'creates a random maze or (m : key)'
        }

    }
    row_items = ((WIN.get_width()-board.width)-10)//60
    col_items = len(buttons)//row_items
    row_gap = (((WIN.get_width()-board.width)/row_items) - 60)/2
    col_gap = (((WIN.get_height())/col_items-40))
    start = board.width
    y = -40
    n = 1
    y_count = 1

    # creating buttons
    for name in buttons:
        globals()[name] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((start+n*row_gap, y + y_count*col_gap), (60, 40)), text=buttons[name]['text'],
                                                       manager=manager, tool_tip_text=None)

        # updating so the buttons will go next to each other
        start += 60
        n += 1
        # if the buttons fill the  whole width then they are pushed down
        if start+n*row_gap > WIN.get_width() - 60:
            start = board.width
            n = 1
            y_count += 1
            y += 40


class Grid():
    def __init__(self, cols: int = 4, rows: int = 4, width: int = 400, height: int = 400, WIN=None):
        self.rows = cols
        self.cols = rows
        self.WIN = WIN
        self.cubes = [
            [Cube(0, i, j, width, height, self.cols, self.rows, self.WIN)
             for j in range(self.cols)]
            for i in range(self.rows)
        ]
        self.width = width
        self.height = height
        self.draw()

    def randomBoard(self):
        for x in range(self.rows):
            for y in range(self.cols):
                self.cubes[x][y].delete()
                self.cubes[x][y].value = random.randint(0, 1)
                self.cubes[x][y].draw()
        self.draw()

    def draw(self, win=None):
        win = self.WIN

        background = pygame.Surface((self.width,self.height))
        win.blit(background,(0,0))

        rowGap = self.height / self.rows
        colGap = self.width / self.cols
        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw()
        thick = 1
        # pygame.draw.line(win, (0, 0, 0), (i * rowGap, 0),i * rowGap, self.height), thick)
        for i in range(self.rows+1):
            pygame.draw.line(win, BLACK, (0, i*rowGap),
                             (self.height, rowGap*i), thick)
        for i in range(self.cols+1):
            pygame.draw.line(win, BLACK, (i*colGap, 0), (colGap*i, self.width))
        pygame.display.update()

    def Conway(self):
        board.draw()
        helper = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for i in range(len(self.cubes)):
            for j in range(len(self.cubes[0])):
                cube = self.cubes[i][j]
                neighbours = cube.get_neighbours(self.cubes)
                if cube.value == 0 and neighbours == 3:
                    helper[i][j] = 1
                elif (cube.value == 1) and (neighbours < 2 or neighbours > 3):
                    helper[i][j] = 0
                else:
                    helper[i][j] = cube.value

        for x in range(len(helper)):
            for y in range(len(helper[0])):
                self.cubes[x][y].value = helper[x][y]

        # next = np.ndarray(shape=(self.size))
        # for x in range(self.rows):
        #     for y in range(self.columns):
        #         state = self.grid_array[x][y]
        #         neighbours = self.get_neighbours(x, y)
        #         if state == 0 and neighbours == 3:
        #             next[x][y] = 1
        #         elif state == 1 and (neighbours < 2 or neighbours > 3):
        #             next[x][y] = 0
        #         else:
        #             next[x][y] = state
        # self.grid_array = next

    def reset(self):
        for row in self.cubes:
            for cube in row:
                cube.value = 0
        board.draw()

    def clicked(self, i, j):
        if i < 0 or j < 0 or i >= self.rows or j >= self.cols:
            return -1
        self.cubes[i][j].clicked()

    def delete(self, x, y):
        if x < 0 or y < 0 or x >= self.rows or y >= self.cols:
            return -1
        self.cubes[x][y].delete()


class Cube():
    def __init__(self, value, row, col, width, height, cols, rows, WIN):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.cols = cols
        self.rows = rows
        self.WIN = WIN

    def draw(self):
        rowGap = self.height / self.rows
        colGap = self.width / self.cols
        x = self.col * colGap
        y = self.row * rowGap
        if self.value == 1:
            pygame.draw.rect(
                self.WIN, BLACK, pygame.Rect(x, y, colGap, rowGap))
        else:
            pygame.draw.rect(
                self.WIN, WHITE, pygame.Rect(x+1, y+1, colGap-2, rowGap-2))

    def get_neighbours(self, board):
        total = 0
        x, y = self.row, self.col
        for i in range(max(0, x-1), min(self.rows, x+2)):
            for j in range(max(0, y-1), min(self.cols, y+2)):
                total += board[i][j].value
        total -= self.value
        return total

    def clickAnimation(self, sub=0):
        '''animation for cube  when clicked
        :param subtract a value for speed calc
        '''
        rowGap = self.height / self.rows
        colGap = self.width / self.cols
        x = self.col * colGap
        y = self.row * rowGap
        width = colGap - 10 - sub
        while True:
            width += 0.05
            pygame.draw.rect(self.WIN, BLACK,
                             pygame.Rect(x+(colGap-width)/2, y+(colGap-width)/2, width, width))
            pygame.display.update()
            if width >= colGap:
                break
        self.draw()

    def clicked(self):
        self.value = 1
        self.clickAnimation(-6)
        pygame.display.update()

    def delete(self):
        self.value = 0
        self.draw()
        pygame.display.update()


board = Grid(40, 40, WIN.get_height()-1, WIN.get_height()-1, WIN)
board.draw()
Widgetsbackground = pygame.Surface(
    (WIN.get_width()-board.width, WIN.get_height()))
Widgetsbackground.fill(WHITE)
createbuttons()
WIN.blit(Widgetsbackground,(board.width+1,0))
manager.draw_ui(WIN)
pygame.display.update()

def updateWidgetsPannel(time_delta):
    global Widgetsbackground , board , WIN
    manager.update(time_delta)
    WIN.blit(Widgetsbackground, (board.width+1, 0))
    manager.draw_ui(WIN)
    pygame.display.update()



runGameOfLife = False
run = True
while run:

    clock.tick(FPS)
    time_delta = clock.tick(FPS)/1000.0

    # checks for left click
    if pygame.mouse.get_pressed()[0]:
        x, y = pygame.mouse.get_pos()
        gap = board.width // board.rows
        y //= gap
        x //= gap
        board.clicked(y, x)

    # checks for right click
    elif pygame.mouse.get_pressed()[2]:
        x, y = pygame.mouse.get_pos()
        gap = board.width // board.rows
        y //= gap
        x //= gap
        board.delete(y, x)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:

                # this is written here because we need to click even if mouse clicks is off
                if event.ui_element == create_button:
                    board.randomBoard()
                if event.ui_element == save_button:
                    save(board)
                if event.ui_element == load_button:
                    load(board)
                if event.ui_element == run_button:
                    runGameOfLife = not runGameOfLife
                if event.ui_element == clear_button:
                    runGameOfLife = False
                    board.reset()

        manager.process_events(event)

    if runGameOfLife:
        board.Conway()

    th = threading.Thread(target=updateWidgetsPannel(time_delta))
    th.start()
    th.join()





pygame.quit()
