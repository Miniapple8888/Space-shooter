import pygame
from random import *

class Enemy():

	health = 100
	height = 50
	width = 50
	enemy_dx = 75
	enemy_shoot = True
	start_time = 0
	shooting_delay = 2000

	def __init__(self, surface):
		surface_rect = surface.get_rect()
		self.enemy_pos_x = randrange(11, surface_rect.width - 11)
		self.enemy_pos_y = 50
		pygame.draw.rect(surface, (0, 0, 0), (self.enemy_pos_x, self.enemy_pos_y, self.width, self.height))
		self.future_x = randrange(11, surface_rect.width - 11)

	def draw_enemy(self, surface, seconds):
		# check if out of bounds
		surface_rect = surface.get_rect()
		if (self.enemy_pos_x > 10) and (self.enemy_pos_x < surface_rect.width - 10):
			# move according to player's position
			if self.future_x >= self.enemy_pos_x:
				self.enemy_pos_x += self.enemy_dx * seconds
			elif self.future_x <= self.enemy_pos_x:
				self.enemy_pos_x -= self.enemy_dx * seconds
		# generate new future x once reached
		if self.future_x >= self.enemy_pos_x and self.future_x <= self.enemy_pos_x + 5:
			self.future_x = randrange(11, surface_rect.width - 11)
		pygame.draw.rect(surface, (0, 0, 0), (self.enemy_pos_x, self.enemy_pos_y, self.width, self.height))

	# returns True if enemy can shoot
	def can_shoot(self):
		if self.enemy_shoot == True:
			self.start_time = pygame.time.get_ticks()
			self.shooting_delay = randrange(2500, 3500)
			self.enemy_shoot = False
			return True
		# every 1 second, the enemy fires a new bullet
		if self.enemy_shoot == False and pygame.time.get_ticks() - self.start_time >= self.shooting_delay:
			self.enemy_shoot = True
			self.start_time = 0
		return False