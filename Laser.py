import pygame


class Laser():

	width = 5
	height = 35
	laser_dy = 100

	def __init__(self, pos_x, pos_y, surface):
		self.laser_pos_x = pos_x + 20
		self.laser_pos_y = pos_y - self.height
		pygame.draw.rect(surface, (175, 175, 50), (self.laser_pos_x, self.laser_pos_y, self.width, self.height))

	def draw_laser(self, surface, seconds):
		# first check boundaries
		if self.laser_pos_y > -10:
			# laser can move
			self.laser_pos_y -= self.laser_dy * seconds
			pygame.draw.rect(surface, (175, 175, 50), (self.laser_pos_x, self.laser_pos_y, self.width, self.height))
			return True
		else:
			# It's out of bounds
			return False

	def hit(self, enemies):
		# if same height as enemy
		if self.laser_pos_y <= 100:
			# loop through enemies
			for enemy in enemies:
				# if it hits an enemy
				if (self.laser_pos_x >= enemy.enemy_pos_x) and (self.laser_pos_x <= enemy.enemy_pos_x + enemy.width):
					return enemy
		else:
			return False