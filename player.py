import pygame
import random
from brain import Brain

class Player:
	def __init__(self, surface, color=None, brain=None):
		self.surface = surface
		self.size = 40
		self.movingSpeed = 30
		self.pos = [self.surface.get_width()//2 - self.size//2, self.surface.get_height()//2 - self.size//2]
		self.rect = pygame.rect.Rect(self.pos[0], self.pos[1], self.size, self.size)
		if color:
			self.color = self.mutate_color(color, 0.8)

		else:
			self.color = (random.randint(0,200), random.randint(0,200), random.randint(0,200))
		if brain:
			self.brain = brain
		else:
			self.brain = Brain()
		self.score = 0


	def mutate_color(self, color: tuple, mutation_rate: float) -> tuple:
		color = list(color)
		for i in range(len(color)):
			if random.random() < mutation_rate:
				color[i] += random.randint(-22, 22)
				if color[i] > 255:
					color[i] = 255
				if color[i] < 0:
					color[i] = 0
		return color

	def update(self, goalPosX, goalPosY):
		# pos are intepolated between 0 and 1
		x = self.rect.x / self.surface.get_width()
		y = self.rect.y / self.surface.get_height()
		goalPosX = goalPosX / self.surface.get_width()
		goalPosY = goalPosY / self.surface.get_height()

		moveDirections = self.brain.update(x, y, goalPosX, goalPosY)
		moveUp = moveDirections[0] > 0.5
		moveDown = moveDirections[1] > 0.5
		moveRight = moveDirections[2] > 0.5
		moveLeft = moveDirections[3] > 0.5

		self.move(moveUp, moveDown, moveRight, moveLeft)

	def draw(self):
		pygame.draw.rect(self.surface, self.color, self.rect)

	def move(self, moveUp: bool, moveDown: bool, moveRight: bool, moveLeft:bool):
		if moveUp:
			self.pos[1] -= self.movingSpeed
		if moveDown:
			self.pos[1] += self.movingSpeed
		self.rect.y = self.pos[1]
		if self.rect.y < 0:
			self.rect.y = 0
		if self.rect.y > self.surface.get_height() - self.size:
			self.rect.y = self.surface.get_height() - self.size
		if moveRight:
			self.pos[0] += self.movingSpeed
		if moveLeft:
			self.pos[0] -= self.movingSpeed
		self.rect.x = self.pos[0]
		if self.rect.x < 0:
			self.rect.x = 0
		if self.rect.x > self.surface.get_width() - self.size:
			self.rect.x = self.surface.get_width() - self.size

