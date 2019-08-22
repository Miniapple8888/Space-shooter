import pygame
import os
from Helpers import write
from Helpers import draw_ship
from Laser import Laser
from Enemy import Enemy
from LaserEnemy import LaserEnemy

class App():

	score = 0
	health = 1000
	level = 1
	enemies = []
	lasers = []
	lasersEnemy = []
	gameover = False
	playing = False
	ship_dx = 150
	ship_dy = 150
	new_level = True
	levels = [0, 5, 10, 15]
	canShoot = True
	start_time = 0

	def __init__(self, width, height, fps):
		# initialize mixer to avoid sound lag
		pygame.mixer.pre_init(44100, -16, 2, 2048)
		pygame.init()
		self.width = width
		self.height = height
		self.fps = fps
		self.clock = pygame.time.Clock()
		self.ship_pos_x = (self.width-50)/2
		self.ship_pos_y = self.height - 50

	def load(self):
		folder = "assets"
		try:
			# load sprites
			self.playerShip = pygame.image.load(os.path.join(folder, "bgbattleship.png"))
			self.playerShip = self.playerShip.convert_alpha()
			self.enemyShip = pygame.image.load(os.path.join(folder, "UFOalien.png"))
			self.enemyShip = self.enemyShip.convert_alpha()
			# load music
			music = os.path.join(folder, "space-game-theme-loop.wav")
			pygame.mixer.music.load(music)
			self.sfx = {
				"laser": pygame.mixer.Sound(os.path.join(folder, "laser-shoot.wav")),
				"hit": pygame.mixer.Sound(os.path.join(folder, "hit.wav")),
				"explosion": pygame.mixer.Sound(os.path.join(folder, "explosion.wav")),
				"level_up": pygame.mixer.Sound(os.path.join(folder, "level_up.wav")),
				"gameover": pygame.mixer.Sound(os.path.join(folder, "gameover.wav"))
			}
			# plays music endlessly
			pygame.mixer.music.play(-1)
		except:
			msg = "Unfortunately we could load one of the files."
			raise Exception(UserWarning, msg)

	def play(self):

		# Repainting screen
		self.background.fill((0, 0, 0))

		# draw ship
		draw_ship(self.ship_pos_x, self.ship_pos_y, self.background)
		self.background.blit(self.playerShip, (self.ship_pos_x, self.ship_pos_y))
		# Display game stats
		# Current level
		self.background.blit(write("LEVEL: %s" % (self.level), 24, (255, 255, 255)), (0, 0))
		# Current Health
		self.background.blit(write("HEALTH: %s" % (self.health), 24, (255, 255, 255)), (200, 0))
		# Current score
		self.background.blit(write("SCORE: %s" % (self.score), 24, (255, 255, 255)), (400, 0))

		# Countdown before starting the round


		# Events with Health
		# If health player == 0
		if self.health <= 0:
			# ship explode
			# sound effect explosion
			# Gameover screen
			self.gameover = True
			# sound effect gameover
			self.sfx['gameover'].play()
		# If health enemy == 0
		# enemy explode
		# sound effect explosion
		# score goes up

		# Events with user input
		# if pressed keys is left
		if self.pressedkeys[pygame.K_LEFT]:
			# check boundaries before moving
			if self.ship_pos_x > 1:
				# move to the left
				self.ship_pos_x -= self.ship_dx * self.seconds
		# if pressed keys is right
		if self.pressedkeys[pygame.K_RIGHT]:
			# check boundaries before moving
			if self.ship_pos_x < (self.width - 10 - 50):
				# move to the right
				self.ship_pos_x += self.ship_dx * self.seconds
		# if pressed keys is down
		if self.pressedkeys[pygame.K_DOWN]:
			# check boundaries before moving
			if self.ship_pos_y < (self.height - 10 - 50):
				# move down
				self.ship_pos_y += self.ship_dy * self.seconds
		# if pressed keys is up
		if self.pressedkeys[pygame.K_UP]:
			# check boundaries before moving
			if self.ship_pos_y > (self.height - 350):
				# move up
				self.ship_pos_y -= self.ship_dy * self.seconds
		# if pressed keys is space
		if self.pressedkeys[pygame.K_SPACE]:
			# fire event: fire sound is played
			# a laser is spawned
			# should be a delay when the laser is spawned
			if self.canShoot == True:
				laser = Laser(self.ship_pos_x, self.ship_pos_y, self.background)
				self.lasers.append(laser)
				self.start_time = pygame.time.get_ticks()
				self.canShoot = False
				self.sfx['laser'].play()

		if self.canShoot == False and pygame.time.get_ticks() - self.start_time >= 500:
			self.canShoot = True
			self.start_time = 0

		# updates laser movement from player
		for laser in self.lasers:
			bounds = laser.draw_laser(self.background, self.seconds)
			if bounds is False:
				self.lasers.remove(laser)
			else:
				# a collision happens once
				hit = laser.hit(self.enemies)
				if hit:
					# laser is deleted
					self.lasers.remove(laser)
					# health enemy goes down
					hit.health -= 25
					# sound effect hit
					self.sfx['hit'].play()

		# updates laser movement from player
		for laser in self.lasersEnemy:
			bounds = laser.draw_laser(self.background, self.seconds)
			if bounds is False:
				self.lasersEnemy.remove(laser)
			else:
				# a collision happens once
				hit = laser.hit(self.ship_pos_x, self.ship_pos_y)
				if hit:
					# laser is deleted
					self.lasersEnemy.remove(laser)
					# health player goes down
					self.health -= 25
					# sound effect hit
					self.sfx['hit'].play()
		# Events with collision
		# if a laser collides with player
		# Health player goes down
		# sound effect damage
		# laser destroyed
		# if a laser collides with enemy
		# Health enemy goes down
		# sound effect damage
		# laser destroyed
		# if a laser goes out of bound
		# laser destroyed

		# spawns a certain number of enemy according to the level
		if self.new_level:
			for x in range(0, self.levels[self.level]):
				enemy = Enemy(self.background)
				self.enemies.append(enemy)
			self.new_level = False
			# level up sound effect
			self.sfx['level_up'].play()

		# updates movement enemy
		for enemy in self.enemies:
			enemy.draw_enemy(self.background, self.seconds)
			self.background.blit(self.enemyShip, (enemy.enemy_pos_x, enemy.enemy_pos_y))
			# enemy dies at zero HP
			if enemy.health <= 0:
				self.enemies.remove(enemy)
				self.score += 50
				# sound effect explosion
				self.sfx['explosion'].play()
			# if enemy can shoot, shoot
			if enemy.can_shoot():
				laserEnemy = LaserEnemy(enemy.enemy_pos_x, enemy.enemy_pos_y, self.background)
				self.lasersEnemy.append(laserEnemy)

		# spawns new wave when all enemies die
		if not self.enemies:
			self.new_level = True
			self.level += 1

	def reset(self):
		self.score = 0
		self.health = 1000
		self.level = 1
		self.enemies = []
		self.lasers = []
		self.lasersEnemy = []
		self.gameover = False
		self.ship_dx = 150
		self.ship_dy = 150
		self.new_level = True
		self.canShoot = True
		self.start_time = 0

	def run(self):

		self._display_surf = pygame.display.set_mode((self.width, self.height), pygame.HWSURFACE | pygame.DOUBLEBUF)
		self._running = True

		# load all assets
		self.load()

		# black background
		self.background = pygame.Surface(self._display_surf.get_size())
		self.background.fill((0, 0, 0))
		self.background = self.background.convert()
		# draw ship
		draw_ship(self.ship_pos_x, self.ship_pos_y, self.background)
		self.background.blit(self.playerShip, (self.ship_pos_x, self.ship_pos_y))
		# Starting screen
		self.background.blit(write("SPACE SHOOTERS", 54, (255, 255, 255)), (155, 100))
		self.background.blit(write("PRESS ENTER TO START", 32, (255, 255, 255)), (190, 200))

		# while game is running
		while self._running:

			milliseconds = self.clock.tick(self.fps)
			self.seconds = milliseconds / 1000.0

			# Quit event
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self._running = False
				elif event.type == pygame.K_ESCAPE:
					self._running = False

			self.pressedkeys = pygame.key.get_pressed()
			
			if self.playing is True and self.gameover == False:
				# enter game mode
				self.play()
			else:
				if self.pressedkeys[pygame.K_RETURN]:
					self.playing = True
					# reset values
					self.reset()

			if self.gameover is True:
				# Repainting screen
				self.background.fill((0, 0, 0))
				self.background.blit(write("GAMEOVER!", 54, (255, 0, 0)), (200, 100))
				self.background.blit(write("SCORE: %s" % (self.score), 32, (255, 255, 255)), (235, 200))
				self.background.blit(write("PRESS ENTER TO PLAY AGAIN!", 32, (255, 255, 255)), (150, 250))
			self._display_surf.blit(self.background, (0, 0))
			pygame.display.set_caption("FPS: %s" % (self.clock.get_fps()))
			pygame.display.update()

