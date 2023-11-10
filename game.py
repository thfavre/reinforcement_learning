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
huge_font = pygame.font.SysFont("coopbl", 44)
big_font = pygame.font.SysFont("coopbl", 28)
medium_font = pygame.font.SysFont("coopbl", 22)
small_font = pygame.font.SysFont("coopbl", 16)

# Classes --------------------------------------------------------- #

class Goal:
    def __init__(self, surface, nb) -> None:
        self.surface = surface
        size = 60
        self.pos = [random.randint(size, self.surface.get_width() - size), random.randint(size, self.surface.get_height() - size)]
        self.rect = pygame.rect.Rect(self.pos[0], self.pos[1], size, size)
        self.nb = nb

    def draw(self, total_goals_nb):
        if self.nb == total_goals_nb - 1: # current goal
            color = (20, 200, 10)
        elif self.nb == total_goals_nb: # future goal
            color = (200, 200, 200)
        else: # past goal
            color = (100, 10, 10)
        pygame.draw.rect(self.surface, color, self.rect)
        nb_label = huge_font.render(f"{self.nb}", 1, (255,255,255))
        SCREEN.blit(nb_label, (self.rect.centerx - nb_label.get_width()//2, self.rect.centery - nb_label.get_height()//2))

    def collide(self, rect):
        return self.rect.colliderect(rect)

class Game:
    def __init__(self) -> None:
        self.generation = 1
        self.actions_per_round = 100
        self.current_action = 0

        self.goals = []
        self.add_new_goal()
        self.add_new_goal()

        self.playersNb = 500
        self.players = [Player(SCREEN) for i in range(self.playersNb)]

    def add_new_goal(self):
        self.goals.append(Goal(SCREEN, len(self.goals) + 1))

    def calculate_score(self):
        for player in self.players:
            # calculate the distance between the player and the first goal
            distance = math.sqrt((player.rect.centerx - self.goals[player.current_goal_index].rect.centerx)**2 + (player.rect.centery - self.goals[player.current_goal_index].rect.centery)**2)
            player.current_goal_index += 1
                # add the distance between the remaining goals
            while player.current_goal_index < len(self.goals) - 1 :
                distance += math.sqrt((self.goals[player.current_goal_index].rect.centerx - self.goals[player.current_goal_index + 1].rect.centerx)**2 + (self.goals[player.current_goal_index].rect.centery - self.goals[player.current_goal_index + 1].rect.centery)**2)
                player.current_goal_index += 1


            player.score = distance # the lower the better

    def select_best_players(self, nb):
        self.players.sort(key=lambda x: x.score, reverse=False)
        return self.players[:nb]

    def next_round(self):
        self.generation += 1
        self.calculate_score()
        best_players = self.select_best_players(50)
        print("Generation: ", self.generation)
        print("\tBest score: ", best_players[0].score)

        self.goals = []
        self.add_new_goal()
        self.add_new_goal()

        # repopulate the players with the best X with mutations
        self.players = []
        # self.players += best_players # keep the bests players # it doesn't work because the players are the same objects
        for i in range(self.playersNb ): # - len(best_players)
            player_to_copy = random.choice(best_players)
            new_player = Player(SCREEN, player_to_copy.color, deepcopy(player_to_copy.brain))
            new_player.brain.mutate(0.4)
            self.players.append(new_player)

    def redraw(self):
        SCREEN.fill((22,22,22))

        # draw the goals
        for goal in self.goals:
            goal.draw(len(self.goals))

        # draw the players
        for player in self.players[::20]:
            player.draw()

        generation_label = big_font.render(f"Generation: {self.generation}", 1, (255,200,20))
        SCREEN.blit(generation_label, (10,10))
        fps_label = medium_font.render(f"FPS: {int(mainClock.get_fps())}", 1, (255,200,20))
        SCREEN.blit(fps_label, (10,35))
        move_remaining_label = medium_font.render(f"Move remaining: {self.actions_per_round - self.current_action}", 1, (255,200,20))
        SCREEN.blit(move_remaining_label, (10,55))
        player_nb_label = medium_font.render(f"Population size: {len(self.players)}", 1, (255,200,20))
        SCREEN.blit(player_nb_label, (10,75))
        layers_size_label = medium_font.render(f"Layers size: {self.players[0].brain.layers_size}", 1, (255,200,20))
        SCREEN.blit(layers_size_label, (10,95))
        max_goals_nb_label = medium_font.render(f"Max goals nb: {len(self.goals)-1}", 1, (255,200,20))
        SCREEN.blit(max_goals_nb_label, (10,115))

    def update(self):

        if self.current_action >= self.actions_per_round:
            self.current_action = 0
            self.next_round()
        # update players
        for player in self.players:
            player.update(self.goals[player.current_goal_index].rect.center, self.goals[player.current_goal_index + 1].rect.center)
            if self.goals[player.current_goal_index].collide(player.rect):
                player.current_goal_index += 1
                if player.current_goal_index >= len(self.goals) - 1: # -1 because the last goal is the future goal
                    self.add_new_goal()

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
    mainClock.tick(1000)

if __name__ == "__main__":
    # Loop ------------------------------------------------------- #
    while True:
        update()
