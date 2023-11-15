# Setup Python ----------------------------------------------- #
import pygame
import sys
import os
import random
import math
from copy import deepcopy

from constants import *
from player import Player
import utils

# Setup pygame/window ---------------------------------------- #
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100,32) # windows position
pygame.init()
pygame.display.set_caption('Neural Network')
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),0,32)

mainClock = pygame.time.Clock()

# Fonts ------------------------------------------------------- #
huge_font = pygame.font.SysFont("coopbl", 48)
big_font = pygame.font.SysFont("coopbl", 32)
medium_font = pygame.font.SysFont("coopbl", 26)
small_font = pygame.font.SysFont("coopbl", 20)

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
        self.last_10_max_goals = []
        self.last_10_avrage_goals = []

        self.playersNb = 500
        self.players = [Player(SCREEN) for i in range(self.playersNb)]

        self.displayed_players_proportions = 20 # 1 every X players
        self.mutation_rate = 0.1


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


    def create_new_generation(self):
        self.calculate_score()
        best_players = self.select_best_players(10)
        best_players += self.select_best_players(10)
        best_players += self.select_best_players(30)
        best_players += random.choices(self.players, k=5)
        # best_players += self.select_best_players(40)
        # best_players += random.choices(self.players, k=5)
        self.players = []
        # keep the best players unchanged
        keep_best_players = 5
        for player in best_players[:keep_best_players]:
            new_player = Player(SCREEN, player.color, deepcopy(player.brain))
            self.players.append(new_player)
        # repopulate the players with the best X with mutations
        k = self.playersNb - keep_best_players
        for player_to_copy in random.choices(best_players, k=k):
            new_player = Player(SCREEN, player_to_copy.color, deepcopy(player_to_copy.brain))
            new_player.brain.mutate(self.mutation_rate)
            self.players.append(new_player)


    def next_round(self):
        self.generation += 1

        self.last_10_max_goals.append(len(self.goals) - 1)
        if len(self.last_10_max_goals) > 10:
            self.last_10_max_goals.pop(0)

        self.last_10_avrage_goals.append(round(sum([player.current_goal_index for player in self.players]) / len(self.players), 2))
        if len(self.last_10_avrage_goals) > 10:
            self.last_10_avrage_goals.pop(0)

        self.create_new_generation()
        # reset the goals
        self.goals = []
        self.add_new_goal()
        self.add_new_goal()


    def draw_info_text(self):
        tips = (
            (f"Generation: {self.generation}", big_font, YELLOW),
            (f"FPS: {int(mainClock.get_fps())}", medium_font, WHITE),
            (f"Move remaining: {self.actions_per_round - self.current_action}", medium_font, WHITE),
            (f"Population size: {len(self.players)}", medium_font, WHITE),
            (f"Layers size: {self.players[0].brain.layers_size}", medium_font, LIGHT_BLUE),
            (f"Mutation rate: {self.mutation_rate}", medium_font, LIGHT_BLUE),
            (f"Avrage goal nb: {round(sum([player.current_goal_index for player in self.players]) / len(self.players), 2)}", medium_font, GREEN),
            (f"Avrage 10 last goals: {round(sum(self.last_10_avrage_goals) / len(self.last_10_avrage_goals), 2) if len(self.last_10_avrage_goals) != 0 else 0}", medium_font, GREEN),
            (f"Max goals nb: {len(self.goals)-1}", medium_font, WHITE),
            (f"Avrage 10 last max goals: {round(sum(self.last_10_max_goals) / len(self.last_10_max_goals), 2) if len(self.last_10_max_goals) != 0 else 0}", medium_font, WHITE),
            (f"Displayed players proportion: 1 / {self.displayed_players_proportions}", medium_font, WHITE),
        )
        pos = [10, 10]
        spacing = 8
        for text, font, color in tips:
            utils.draw_text(SCREEN, text, pos, font, color)
            pos[1] += font.get_height() + spacing

    def redraw(self):
        SCREEN.fill((22,22,22))

        # draw the goals
        for goal in self.goals:
            goal.draw(len(self.goals))

        # draw the players
        for player in self.players[::self.displayed_players_proportions]:
            player.draw()

        self.draw_info_text()

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
                if event.key == pygame.K_DOWN:
                    self.displayed_players_proportions *= 2
                    if self.displayed_players_proportions > self.playersNb:
                        self.displayed_players_proportions = self.playersNb
                if event.key == pygame.K_UP:
                    self.displayed_players_proportions //= 2
                    if self.displayed_players_proportions < 1:
                        self.displayed_players_proportions = 1



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
