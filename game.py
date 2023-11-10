# Setup Python ----------------------------------------------- #
import pygame
import sys
import os
import random
import math
from copy import deepcopy

from player import Player


# Setup pygame/window ---------------------------------------- #
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100,32) # windows position
pygame.init()
pygame.display.set_caption('Neural Network')
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),0,32)

mainClock = pygame.time.Clock()

# Fonts ------------------------------------------------------- #
big_font = pygame.font.SysFont("coopbl", 28)
medium_font = pygame.font.SysFont("coopbl", 22)
small_font = pygame.font.SysFont("coopbl", 16)

# Classes --------------------------------------------------------- #
class Game:
    def __init__(self) -> None:
        self.generation = 1
        self.actions_per_round = 10
        self.current_action = 0

        self.goal = [random.randint(100, SCREEN.get_width() - 100), random.randint(100, SCREEN.get_height() - 100)]

        self.playersNb = 1000
        self.players = [Player(SCREEN) for i in range(self.playersNb)]


    def calculate_score(self):
        for player in self.players:
            distance = math.sqrt((player.rect.x - self.goal[0])**2 + (player.rect.y - self.goal[1])**2)
            player.score = distance

    def select_best_players(self, nb):
        self.players.sort(key=lambda x: x.score, reverse=False)
        return self.players[:nb]

    def next_round(self):
        self.generation += 1
        self.calculate_score()
        best_players = self.select_best_players(50)
        print("Generation: ", self.generation)
        print("\tBest score: ", best_players[0].score)

        self.goal = [random.randint(100, SCREEN.get_width() - 100), random.randint(100, SCREEN.get_height() - 100)]

        # repopulate the players with the best X with mutations
        self.players = []
        self.players += best_players # keep the bests players
        for i in range(self.playersNb - len(best_players)):
            player_to_copy = random.choice(best_players)
            new_player = Player(SCREEN, player_to_copy.color, deepcopy(player_to_copy.brain))
            new_player.brain.mutate(0.9)
            self.players.append(new_player)

    def redraw(self):
        SCREEN.fill((22,22,22))

        # draw the goal
        pygame.draw.circle(SCREEN, (255, 255, 255), self.goal, 40)

        # draw the players
        for player in self.players[::10]:
            player.draw()

        generation_label = big_font.render(f"Generation: {self.generation}", 1, (255,200,20))
        SCREEN.blit(generation_label, (5,5))
        fps_label = medium_font.render(f"FPS: {int(mainClock.get_fps())}", 1, (255,200,20))
        SCREEN.blit(fps_label, (5,30))
        move_remaining_label = medium_font.render(f"Move remaining: {self.actions_per_round - self.current_action}", 1, (255,200,20))
        SCREEN.blit(move_remaining_label, (5,50))

    def update(self):

        if self.current_action >= self.actions_per_round:
            self.current_action = 0
            self.next_round()
        # update players
        for player in self.players:
            player.update(self.goal[0], self.goal[1])

        self.current_action += 1

        self.redraw()

        self.buttons()



    def buttons(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                # if event.key == pygame.K_SPACE:
                #     self.next_round()



# Creation ---------------------------------------------------------#

game = Game()


def update():
    game.update()
    pygame.display.update()
    mainClock.tick(90)

if __name__ == "__main__":
    # Loop ------------------------------------------------------- #
    while True:
        update()
