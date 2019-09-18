import pygame
from random import *

class Enemy():

	health = 100
	height = 50
	width = 50
	dx = 75
	shoot = False
	startTime = 0
	shootingDelay = randrange(2500, 3000)

	# Spawns new enemy
	def __init__(self, surface, sprite):
		self.surface = surface
		self.surfaceRect = self.surface.get_rect()
		self.pos_x = randrange(12, self.surfaceRect.width - 11 - self.width)
		self.pos_y = 50
		self.future_x = randrange(12, self.surfaceRect.width - 11 - self.width)
		self.sprite = sprite

	def render(self):
		self.surface.blit(self.sprite, (self.pos_x, self.pos_y))

	# updates movement of enemy
	def update(self, seconds):
		# check if out of bounds
		if (self.pos_x >= 5) and (self.pos_x < self.surfaceRect.width - 11 - self.width):
			# Moves toward a randomly generated position
			if self.future_x >= self.pos_x:
				self.pos_x += self.dx * seconds
			elif self.future_x <= self.pos_x:
				self.pos_x -= self.dx * seconds
		# generate new future x once reached
		if self.future_x >= self.pos_x and self.future_x <= self.pos_x + 5:
			self.future_x = randrange(12, self.surfaceRect.width - 11 - self.width)
		# draws the enemy
		self.render()

	# returns True if enemy can shoot
	def can_shoot(self):
		if self.shoot == True:
			self.startTime = pygame.time.get_ticks()
			self.shootingDelay = randrange(2500, 3500)
			self.shoot = False
			return True
		# in the range of 2 seconds to 3 seconds, the enemy fires a new bullet
		if self.shoot == False and pygame.time.get_ticks() - self.startTime >= self.shootingDelay:
			self.shoot = True
			self.startTime = 0
		return False