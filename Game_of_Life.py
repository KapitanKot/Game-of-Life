import sys, pygame, random
from pygame.locals import *
from random import *

class GameOfLife(object):
    """Main"""
    
    def __init__(self, width = 40, height = 40, size = 10):
        pygame.init()
        self.started = False
        self.board = Board(width * size, height * size)
        self.population = Population(width, height, size)
        self.clock = pygame.time.Clock()

    def events(self):
        """Event handler"""
        for event in pygame.event.get():

            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
                
            if event.type == MOUSEBUTTONDOWN:
                self.population.mouse()

            if event.type == KEYDOWN and event.key == K_RETURN:
                self.started = True

            if event.type == KEYDOWN and event.key == K_s:
                self.started = False

            if event.type == KEYDOWN and event.key == K_r:
                self.started = False
                self.population.reset()

            if event.type == KEYDOWN and event.key == K_f:
                self.started = False
                self.population.random()

    def run(self):
        """Main loop"""
        while not self.events():
            self.board.draw(self.population)
            if self.started:
                self.population.cycle()
            self.clock.tick(15)
            
class Board(object):
    
    def __init__(self, width, height):
        """Window"""
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((self.width, self.height + 18), 0, 32)
        font = pygame.font.Font('C:\Windows\Fonts\Arial.ttf', 12)
        self.text = font.render('Start (Enter)      Stop (S)      Reset (R)      Random (F)', True, (255, 255, 255))
        pygame.display.set_caption('Game of Life')

    def draw(self, *args):
        """Draw elements"""
        background = (0, 0, 0)
        self.window.fill(background)
        pygame.draw.rect(self.window, (255, 255, 255), (0, self.height+1, self.width, 3), 1)
        self.window.blit(self.text, (1, self.height+4))
        for arg in args:
            arg.drawSurface(self.window)
            
        pygame.display.update()

class Population(object):
    """Cell population"""

    def __init__(self, width = 40, height = 40, size = 10):
        self.size = size
        self.width = width
        self.height = height
        self.generation = self.wipeGeneration()

    def reset(self):
        self.generation = self.wipeGeneration()

    def random(self):
        for x in range(len(self.generation)):
            for y in range(len(self.generation[0])):
                self.generation[x][y] = randrange(0,2) 

    def wipeGeneration(self):
        """Make and return empty population matrix"""
        temp = [0] * self.height
        for i in range(self.height):
            temp[i] = [0] * self.width
        return temp

    def mouse(self):
        """Kill or alive cell"""
        key = pygame.mouse.get_pressed()
        mx, my = pygame.mouse.get_pos()
        if mx <= (self.width * self.size) and my <= (self.height * self.size):

            mx //= self.size
            my //= self.size
     
            if key[0] == 1: self.generation[mx][my] = 1
            elif key[2] == 1: self.generation[mx][my] = 0

    def aliveCells(self):
        """Return alive cells"""
        for x in range(len(self.generation)):
            for y in range(len(self.generation[0])):
                if self.generation[x][y] == 1:
                    yield x, y

    def drawSurface(self, surface):
        """Draw cell on board"""
        for x,y in self.aliveCells():
            size = (self.size, self.size)
            position = (x * self.size, y * self.size)
            color = (255, 255, 255)
            pygame.draw.rect(surface, color, (position, size), 1)

    def neighbours(self, x, y):
        """Return neighbours"""

        for neighboursX in range(x-1, x+2):
            for neighboursY in range(y-1, y+2):
                if neighboursX == x and neighboursY == y:
                    continue
                if neighboursX >= self.width:
                    neighboursX = 0
                elif neighboursX < 0:
                    neighboursX = self.width -1
                if neighboursY >= self.height:
                    neighboursY = 0
                elif neighboursY < 0:
                    neighboursY = self.height -1

                yield self.generation[neighboursX][neighboursY]

    def cycle(self):
        """Next generation"""

        nextGen = self.wipeGeneration()
        for x in range(len(self.generation)):
            for y in range(len(self.generation[0])):
                count = sum(self.neighbours(x, y))
                if count == 3:
                    nextGen[x][y] = 1
                elif count == 2:
                    nextGen[x][y] = self.generation[x][y]
                else:
                    nextGen[x][y] = 0

        self.generation = nextGen

if __name__ == "__main__":
    game = GameOfLife(80, 80)
    game.run()
