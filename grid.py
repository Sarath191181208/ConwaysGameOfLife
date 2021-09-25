import pygame 
from colors import *
import random
import json
import os 
from timer import Timer 

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

        self.runGameOfLife = False
        self.conway_timer = Timer(0.1, func=lambda:self.Conway(), loop=True)

        self.btn_timer = Timer(0.2)

        self.color = VIOLET

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

        thick = 0
        # pygame.draw.line(win, (0, 0, 0), (i * rowGap, 0),i * rowGap, self.height), thick)
        for i in range(self.rows+1):
            pygame.draw.line(win, VIOLET_TINT, (0, i*rowGap),
                             (self.height, rowGap*i), thick)
        for i in range(self.cols+1):
            pygame.draw.line(win, VIOLET_TINT, (i*colGap, 0), (colGap*i, self.width))
        # pygame.display.update()
                # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw()

    def Conway(self):
        self.draw()
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

    def start(self):
        if not self.btn_timer.start:
            self.runGameOfLife = not self.runGameOfLife
            self.conway_timer.stop_timer()
            self.btn_timer.start_timer()

    def clear(self):
        for row in self.cubes:
            for cube in row:
                cube.value = 0
        self.runGameOfLife = False
        self.draw()

    def clicked(self, i, j):
        if self.runGameOfLife:
            return
        if i < 0 or j < 0 or i >= self.rows or j >= self.cols:
            return -1
        self.cubes[i][j].clicked(self.color)

    def delete(self, x, y):
        if x < 0 or y < 0 or x >= self.rows or y >= self.cols:
            return -1
        self.cubes[x][y].delete()
    
    def update(self):
        self.conway_timer.update()
        self.btn_timer.update()

        for row in self.cubes:
            for cube in row:
                cube.update()

        if self.runGameOfLife and not self.conway_timer.start:
            self.conway_timer.start_timer()

        self.draw()

    def save(self):

        if not os.path.exists('./saveBoard.json'):
            with open('./saveBoard.json', 'a') as outfile:
                json_object = json.dumps({})
                outfile.write(json_object)

        with open('./saveBoard.json', 'r+') as outfile:

            boardState = {}
            boardState['board'] = {}
            helperDic = {}

            for row in self.cubes:
                for cube in row:

                    if cube.value == 1:
                        x, y = cube.row, cube.col
                        key = str(x)+','+str(y)
                        helperDic[key] = cube.value

            boardState['board'][0] = helperDic
            boardState['board']['rows'] = self.rows
            boardState['board']['cols'] = self.cols

            file_data = json.load(outfile)
            outfile.seek(0, 0)
            outfile.truncate()

            file_data.update(boardState)
            outfile.write(json.dumps(file_data, indent=4))

    def load(self):
        if os.path.exists('./saveBoard.json'):
            data = json.load(open('./saveBoard.json'))
            data = data['board']
            if self.rows == data['rows'] and self.cols == data['cols']:
                # board clear has a property noAnimation which doesnt play animation
                self.clear()
                for items in data['0']:
                    items = items.split(',')
                    x = int(items[0])
                    y = int(items[1])
                    self.cubes[x][y].value = 1
                self.draw()


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

        self.cube_width = 0
        self.animate = False
        self.color = VIOLET

    def draw(self):
        rowGap = self.height / self.rows
        colGap = self.width / self.cols
        x = self.col * colGap
        y = self.row * rowGap
        if self.value == 1:
            pygame.draw.rect(
                self.WIN, self.color, pygame.Rect(x, y, colGap, rowGap))
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
        self.cube_width += 1

        pygame.draw.rect(self.WIN, BLACK,
                            pygame.Rect(x+(colGap-self.cube_width)/2, y+(colGap-self.cube_width)/2, self.cube_width, self.cube_width))

        if self.cube_width >= colGap:
            self.cube_width = colGap
            self.animate = False

        self.draw()

    def clicked(self,color):
        self.value = 1
        self.color = color
        self.cube_width = 0
        self.animate = True

    def update(self):
        if self.animate:
            self.clickAnimation()
        
    def delete(self):
        self.value = 0
        self.draw()
        pygame.display.update()

