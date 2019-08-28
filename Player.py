import pygame

class Player():

	height, width = (50, 50)
	health = 500
	dx, dy = (150, 150)
	shootingDelay = 500
	shoot = True
	startTime = 0

	# Spawns new player
	def __init__(self, surface, sprite):
		self.sprite = sprite
		self.surface = surface
		self.surfaceRect = self.surface.get_rect()
		self.pos_x = (self.surfaceRect.width - 50)/2
		self.pos_y = (self.surfaceRect.height - 50)
		self.render()

	def render(self):
		self.surface.blit(self.sprite, (self.pos_x, self.pos_y))

	def move_left(self, seconds):
		# checks boundaries first
		if self.pos_x > 30:
			self.pos_x -= self.dx * seconds

	def move_right(self, seconds):
		# checks boundaries first
		if self.pos_x < (self.surfaceRect.width - 30 - self.width):
			self.pos_x += self.dx * seconds

	def move_down(self, seconds):
		# checks boundaries first
		if self.pos_y < (self.surfaceRect.height - 10 - self.height):
			self.pos_y += self.dy * seconds

	def move_up(self, seconds):
		# check boundaries before moving
		if self.pos_y > (self.surfaceRect.height - 350):
			self.pos_y -= self.dy * seconds

	# returns True if enemy can shoot
	def can_shoot(self):
		now = pygame.time.get_ticks()
		if self.shoot == True:
			self.startTime = now
			self.shoot = False
			return True
		# in the range of 1 seconds, player fires a new bullet
		if self.shoot == False and now - self.startTime >= self.shootingDelay:
			self.shoot = True
			self.startTime = 0
		return False
