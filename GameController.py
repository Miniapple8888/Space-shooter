import pygame
import os
from Helpers import write
from Helpers import color
from Laser import Laser
from Player import Player
from Enemy import Enemy
from LaserEnemy import LaserEnemy

class Game():

	score = 0
	level = 1
	enemies = []
	lasers = []
	lasersEnemy = []
	gameover = False
	won = False
	playing = False
	levels = [0, 5, 10, 15, 20, 25]

	def __init__(self, width, height, fps):

		# initialize mixer to avoid sound lag
		pygame.mixer.pre_init(44100, -16, 2, 2048)
		pygame.init()
		self.width = width
		self.height = height
		self.fps = fps
		self.clock = pygame.time.Clock()
		self._display_surf = pygame.display.set_mode((self.width, self.height), pygame.HWSURFACE | pygame.DOUBLEBUF)
		self._running = True
		self.load()
		pygame.display.set_icon(self.playerShip)

	# Loads assets
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
				"gameover": pygame.mixer.Sound(os.path.join(folder, "gameover.wav")),
				"won": pygame.mixer.Sound(os.path.join(folder, "won.wav"))
			}
			# plays music endlessly
			pygame.mixer.music.play(-1)
		except:
			msg = "Unfortunately we could load one of the files."
			raise Exception(UserWarning, msg)

	# fills the screen with blackness
	def clear_screen(self):
		self.background.fill(color("black"))

	# Display game stats
	def display_game_stats(self):
		# Current level
		write(self.background, "LEVEL: %s" % (self.level), 24, color("white"), (0, 0))
		# Current Health
		write(self.background, "HEALTH: %s" % (self.player.health), 24, color("white"), (200, 0))
		# Current score
		write(self.background, "SCORE: %s" % (self.score), 24, color("white"), (400, 0))

	# level up: spawns new wave of enemy
	def level_up(self):
		self.level += 1
		# if player has completed all levels, wins
		if self.level > len(self.levels) - 1:
			self.won = True
			# Sound effect won
			self.sfx['won'].play()
		else:
			# spawns a certain number of enemy according to the level
			for x in range(0, self.levels[self.level]):
				enemy = Enemy(self.background, self.enemyShip)
				self.enemies.append(enemy)
			# sound effect level up
			self.sfx['level_up'].play()

	# self-explanatory
	def starting_screen(self):

		self.background = pygame.Surface(self._display_surf.get_size())
		self.clear_screen()
		self.background = self.background.convert()
		self.player = Player(self.background, self.playerShip)
		write(self.background, "SPACE SHOOTERS", 54, color("white"), (155, 100))
		write(self.background, "PRESS ENTER TO START", 32, color("white"), (190, 200))

	# Game mode
	def play(self):

		# Repainting screen
		self.clear_screen()

		# draw ship
		#draw_ship(self.ship_pos_x, self.ship_pos_y, self.background, self.playerShip)
		self.player.render()

		# Display game stats
		self.display_game_stats()

		# Event player dies
		if self.player.health <= 0:
			self.gameover = True
			# sound effect gameover
			self.sfx['gameover'].play()

		# Events with user input
		# if pressed keys is left
		if self.pressedkeys[pygame.K_LEFT]:
			self.player.move_left(self.seconds)
		# if pressed keys is right
		if self.pressedkeys[pygame.K_RIGHT]:
			self.player.move_right(self.seconds)
		# if pressed keys is down
		if self.pressedkeys[pygame.K_DOWN]:
			self.player.move_down(self.seconds)
		# if pressed keys is up
		if self.pressedkeys[pygame.K_UP]:
			self.player.move_up(self.seconds)
		# if pressed keys is space
		if self.pressedkeys[pygame.K_SPACE]:
			# when delay is done, player can shoot
			if self.player.can_shoot() == True:
				# laser is spawned
				laser = Laser(self.player.pos_x, self.player.pos_y, self.background)
				self.lasers.append(laser)
				# sound effect laser
				self.sfx['laser'].play()

		# updates laser 
		for laser in self.lasers:
			bounds = laser.update(self.seconds)
			if bounds is False:
				# deletes laser from game once it is out of the screen
				self.lasers.remove(laser)
			else:
				# laser hits one of the enemies
				hit = laser.hit(self.enemies)
				if hit:
					# laser is deleted
					self.lasers.remove(laser)
					# health enemy goes down
					hit.health -= 25
					# sound effect hit
					self.sfx['hit'].play()

		# updates enemy laser
		for laserEnemy in self.lasersEnemy:
			bounds = laserEnemy.update(self.seconds)
			if bounds is False:
				# deletes laser from game once it is out of the screen
				self.lasersEnemy.remove(laserEnemy)
			else:
				# laser hits the player
				hit = laserEnemy.hit(self.player.pos_x, self.player.pos_y)
				if hit:
					# laser is deleted
					self.lasersEnemy.remove(laserEnemy)
					# health player goes down
					self.player.health -= 25
					# sound effect hit
					self.sfx['hit'].play()

		# updates enemy
		for enemy in self.enemies:
			enemy.update(self.seconds)
			# enemy dies at zero HP
			if enemy.health <= 0:
				# enemy is deleted
				self.enemies.remove(enemy)
				self.score += 50
				# sound effect explosion
				self.sfx['explosion'].play()
			# if enemy can shoot, shoot
			if enemy.can_shoot():
				laserEnemy = LaserEnemy(enemy, self.background)
				self.lasersEnemy.append(laserEnemy)

		# when all enemies die, level up!
		if not self.enemies:
			self.level_up()

	# resets all game values
	def reset(self):
		self.score = 0
		self.level = 1
		self.enemies = []
		self.lasers = []
		self.lasersEnemy = []
		self.gameover = False
		self.won = False
		self.player = Player(self.background, self.playerShip)

	def game_over(self):
		# Repainting screen
		self.clear_screen()
		write(self.background, "GAMEOVER!", 54, color("red"), (200, 100))
		write(self.background, "SCORE: %s" % (self.score), 32, color("white"), (235, 200))
		write(self.background, "PRESS ENTER TO PLAY AGAIN!", 32, color("white"), (150, 250))
		self.player = []

	def winning_screen(self):
		# Repainting screen
		self.clear_screen()
		write(self.background, "YOU WON!", 54, color("green"), (210, 100))
		write(self.background, "SCORE: %s" % (self.score), 32, color("white"), (235, 200))
		write(self.background, "PRESS ENTER TO PLAY AGAIN!", 32, color("white"), (150, 250))
		self.player = []

	# Game execution
	def run(self):

		self.starting_screen()

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

			# get user input
			self.pressedkeys = pygame.key.get_pressed()
			
			# Enter game mode if user presses enter and game over is false
			if self.playing is True and self.gameover == False and self.won == False:
				self.play()
			else:
				if self.pressedkeys[pygame.K_RETURN]:
					self.playing = True
					self.reset()

			if self.gameover is True:
				self.game_over()
			elif self.won is True:
				self.winning_screen()
			
			# Renders game
			self._display_surf.blit(self.background, (0, 0))
			pygame.display.set_caption("FPS: %s" % (self.clock.get_fps()))
			pygame.display.update()

