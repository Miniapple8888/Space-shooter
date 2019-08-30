import pygame
import os
from Helpers import write
from Helpers import color
from Laser import Laser
from Player import Player
from Enemy import Enemy
from LaserEnemy import LaserEnemy
from PlayGame import playgame

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
		self.screen.fill(color("black"))

	# Display game stats
	def display_game_stats(self):
		# Current level
		write(self.screen, "LEVEL: %s" % (self.level), 24, color("white"), (0, 0))
		# Current Health
		write(self.screen, "HEALTH: %s" % (self.player.health), 24, color("white"), (200, 0))
		# Current score
		write(self.screen, "SCORE: %s" % (self.score), 24, color("white"), (400, 0))

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
				enemy = Enemy(self.screen, self.enemyShip)
				self.enemies.append(enemy)
			# sound effect level up
			self.sfx['level_up'].play()

	# self-explanatory
	def starting_screen(self):

		self.screen = pygame.Surface(self._display_surf.get_size())
		self.clear_screen()
		self.screen = self.screen.convert()
		self.player = Player(self.screen, self.playerShip)
		write(self.screen, "SPACE SHOOTERS", 54, color("white"), (155, 100))
		write(self.screen, "PRESS ENTER TO START", 32, color("white"), (190, 200))

	# Game mode
	def play(self):

		playgame(self)
		

	# resets all game values
	def reset(self):
		self.score = 0
		self.level = 1
		self.enemies = []
		self.lasers = []
		self.lasersEnemy = []
		self.gameover = False
		self.won = False
		self.player = Player(self.screen, self.playerShip)

	def game_over(self):
		# Repainting screen
		self.clear_screen()
		write(self.screen, "GAMEOVER!", 54, color("red"), (200, 100))
		write(self.screen, "SCORE: %s" % (self.score), 32, color("white"), (235, 200))
		write(self.screen, "PRESS ENTER TO PLAY AGAIN!", 32, color("white"), (150, 250))
		self.player = []

	def winning_screen(self):
		# Repainting screen
		self.clear_screen()
		write(self.screen, "YOU WON!", 54, color("green"), (210, 100))
		write(self.screen, "SCORE: %s" % (self.score), 32, color("white"), (235, 200))
		write(self.screen, "PRESS ENTER TO PLAY AGAIN!", 32, color("white"), (150, 250))
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
			self._display_surf.blit(self.screen, (0, 0))
			pygame.display.set_caption("FPS: %s" % (self.clock.get_fps()))
			pygame.display.update()

