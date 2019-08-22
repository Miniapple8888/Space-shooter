import pygame

class LaserEnemy():

	enemy = "Player"
	width = 5
	height = 35
	laser_dy = 100

	def __init__(self, pos_x, pos_y, surface):
		enemy_height = 50
		self.laser_pos_x = pos_x + 20
		self.laser_pos_y = pos_y + enemy_height
		pygame.draw.rect(surface, (235, 50, 50), (self.laser_pos_x, self.laser_pos_y, self.width, self.height))

	def draw_laser(self, surface, seconds):
		# first check boundaries
		surface_rect = surface.get_rect()
		if self.laser_pos_y < surface_rect.height + 10:
			# laser can move
			self.laser_pos_y += self.laser_dy * seconds
			pygame.draw.rect(surface, (235, 50, 50), (self.laser_pos_x, self.laser_pos_y, self.width, self.height))
			return True
		else:
			# It's out of bounds
			return False

	def hit(self, ship_pos_x, ship_pos_y):
		# if same height as player
		if self.laser_pos_y + self.height >= ship_pos_y and self.laser_pos_y + self.height <= ship_pos_y + 50:
			# if it hits the player (same x)
			if self.laser_pos_x >= ship_pos_x and self.laser_pos_x <= ship_pos_x + 50:
				return True
		else:
			return False