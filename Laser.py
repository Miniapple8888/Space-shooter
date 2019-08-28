import pygame
from Helpers import color

class Laser():

	width = 5
	height = 35
	dy = 100

	# Spawns new laser
	def __init__(self, ship_pos_x, ship_pos_y, surface):
		self.pos_x = ship_pos_x + 20
		self.pos_y = ship_pos_y - self.height
		self.surface = surface
		self.render()

	def render(self):
		pygame.draw.rect(self.surface, color("yellow"), (self.pos_x, self.pos_y, self.width, self.height))

	# updates movement of laser
	# return False if out of bounds
	def update(self, seconds):
		# first check boundaries
		if self.pos_y > -10:
			# laser can move
			self.pos_y -= self.dy * seconds
			self.render()
			return True
		else:
			# It's out of bounds
			return False

	# Detects collision with the enemy
	# Returns the enemy if collision and False otherwise
	def hit(self, enemies):
		# if same height as enemy
		if self.pos_y <= 100:
			# loop through enemies
			for enemy in enemies:
				# if it hits an enemy
				if (self.pos_x >= enemy.pos_x) and (self.pos_x <= enemy.pos_x + enemy.width):
					return enemy
		else:
			return False