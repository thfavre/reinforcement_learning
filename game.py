# Setup Python ----------------------------------------------- #
import pygame
import sys
import os
import random
import math
from copy import deepcopy
import threading

from player import Player


# Setup pygame/window ---------------------------------------- #
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100,32) # windows position
pygame.init()
pygame.display.set_caption('Windows open')
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),0,32)

mainClock = pygame.time.Clock()

# Fonts ------------------------------------------------------- #
main_font = pygame.font.SysFont("coopbl", 22)


# Variables ------------------------------------------------------- #


# Constantes -------------------------------------------------------#


# Classes --------------------------------------------------------- #
class Game:
    def __init__(self) -> None:
        self.generation = 0
        self.shouldDraw = True
        self.mouseControl = False
        self.autoNextRound = True
        # goal of the player, to be at x=400 and y=300
        self.goal = [random.randint(100, SCREEN.get_width() - 100), random.randint(100, SCREEN.get_height() - 100)]

        self.playersNb = 1000
        self.players = [Player(SCREEN) for i in range(self.playersNb)]


    def calculateScore(self):
        for player in self.players:
            distance = math.sqrt((player.rect.x - self.goal[0])**2 + (player.rect.y - self.goal[1])**2)
            player.score = distance

    def selectBests(self, nb):
        self.players.sort(key=lambda x: x.score, reverse=False)
        return self.players[:nb]

    def nextRound(self):
        self.calculateScore()
        self.generation += 1
        print("Generation: ", self.generation)

        bests = self.selectBests(50)
        print("\tBest score: ", bests[0].score)
        self.goal = [random.randint(100, SCREEN.get_width() - 100), random.randint(100, SCREEN.get_height() - 100)]
        # repopulate the players with the best X with mutations
        self.players = []
        for i in range(self.playersNb):
            toCopy = random.choice(bests)

            newPlayer = Player(SCREEN, toCopy.color)
            # newPlayer.brain = bests[random.randint(0, len(bests) - 1)].brain
            # make a deep copy of the brain
            newPlayer.brain = deepcopy(toCopy.brain)
            if i > 5: # mutate all but the first 5
                newPlayer.brain.mutate(random.random() / 2)
            self.players.append(newPlayer)
        if self.autoNextRound:
            self.timer = threading.Timer(1, self.nextRound)
            self.timer.start()


    def update(self):
        # draw the goal
        pygame.draw.circle(SCREEN, (255, 255, 255), self.goal, 40)
        # update players
        for player in self.players:
            if self.mouseControl:
                self.goal = pygame.mouse.get_pos()
            player.update(self.goal[0], self.goal[1])
        self.buttons()
        if self.shouldDraw:
            for player in self.players[::10]:
                player.draw()


    def buttons(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    self.nextRound()
                    print("Generation: ", self.generation)
                if event.key == pygame.K_d:
                    self.shouldDraw = not self.shouldDraw
                if event.key == pygame.K_m:
                    self.mouseControl = not self.mouseControl
                if event.key == pygame.K_n:
                    self.autoNextRound = not self.autoNextRound



# Creation ---------------------------------------------------------#

game = Game()


# Functions ------------------------------------------------------- #
def redraw():
    SCREEN.fill((22,22,22))
    fps_label = main_font.render(f"FPS: {int(mainClock.get_fps())}", 1, (255,200,20))
    SCREEN.blit(fps_label, (5,5))






def update():
    game.update()
    pygame.display.update()
    mainClock.tick(90)


# Loop ------------------------------------------------------- #
while True:
    # mouse_x, mouse_y = pygame.mouse.get_pos()
    # pygame.mouse.get_pressed()

     # keys_pressed = pygame.key.get_pressed()
     # if keys_pressed[pygame.K_LEFT]:


    # draw --------------------------------------------- #
    redraw()

    # Buttons ------------------------------------------------ #
    # buttons()

    # Update ------------------------------------------------- #
    update()
