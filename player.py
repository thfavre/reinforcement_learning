import pygame
import random
from brain import Brain

class Player:
	def __init__(self, surface, color=None):
		self.surface = surface
		self.size = 40
		self.movingSpeed = 10
		self.pos = [self.surface.get_width()//2 - self.size//2, self.surface.get_height()//2 - self.size//2]
		self.rect = pygame.rect.Rect(self.pos[0], self.pos[1], self.size, self.size)
		if color:
			# mutate the color a bit
			self.color = [color[0] + random.randint(-22, 22), color[1] + random.randint(-22, 22), color[2] + random.randint(-22, 22)]
			if self.color[0] > 255:
				self.color[0] = 255
			if self.color[1] > 255:
				self.color[1] = 255
			if self.color[2] > 255:
				self.color[2] = 255
			if self.color[0] < 0:
				self.color[0] = 0
			if self.color[1] < 0:
				self.color[1] = 0
			if self.color[2] < 0:
				self.color[2] = 0
			self.color = tuple(self.color)

		else:
			self.color = (random.randint(0,200), random.randint(0,200), random.randint(0,200))

		self.brain = Brain()
		self.score = 0

	def reset(self):
		self.pos = [self.surface.get_width()//2 - self.size//2, self.surface.get_height()//2 - self.size//2]
		self.rect = pygame.rect.Rect(self.pos[0], self.pos[1], self.size, self.size)
		self.score = 0

	def update(self, goalPosX, goalPosY):
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

