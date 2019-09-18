import pygame
from Helpers import color

class LaserEnemy():

	width = 5
	height = 35
	dy = 100

	# spawns new laser enemy
	def __init__(self, enemy, surface):
		self.pos_x = enemy.pos_x + 20
		self.pos_y = enemy.pos_y + enemy.height
		self.surface = surface
		self.surfaceRect = self.surface.get_rect()
		self.render()

	def render(self):
		pygame.draw.rect(self.surface, color("red"), (self.pos_x, self.pos_y, self.width, self.height))

	# updates movement of laser
	# returns False if it falls out of bound
	def update(self, seconds):
		# first check boundaries
		if self.pos_y < self.surfaceRect.height + 10:
			# laser can move
			self.pos_y += self.dy * seconds
			self.render()
			return True
		else:
			# It's out of bounds
			return False

	# detects collision with the ship of the player
	# returns True if it hits
	def hit(self, ship_pos_x, ship_pos_y):
		# if same height as player
		if self.pos_y + self.height >= ship_pos_y and self.pos_y + self.height <= ship_pos_y + 50:
			# if it hits the player (same x)
			if self.pos_x >= ship_pos_x and self.pos_x <= ship_pos_x + 50:
				return True
		else:
			return False