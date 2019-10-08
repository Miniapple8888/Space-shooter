import pygame
from Laser import Laser
from LaserEnemy import LaserEnemy

def playgame(game):
	# Repainting screen
	game.clear_screen()

	# draw ship
	game.player.render()

	# Display game stats
	game.display_game_stats()

	# Event player dies
	if game.player.health <= 0:
		game.gameover = True
		# sound effect gameover
		game.sfx['gameover'].play()

	# TODO add game over when time runs out in game, Limit Time is 30
	# game.playtime --> variable tracks time in game

	# Events with user input
	# if pressed keys is left
	if game.pressedkeys[pygame.K_LEFT]:
		game.player.move_left(game.seconds)
	# if pressed keys is right
	if game.pressedkeys[pygame.K_RIGHT]:
		game.player.move_right(game.seconds)
	# if pressed keys is down
	if game.pressedkeys[pygame.K_DOWN]:
		game.player.move_down(game.seconds)
	# if pressed keys is up
	if game.pressedkeys[pygame.K_UP]:
		game.player.move_up(game.seconds)
	# if pressed keys is space
	if game.pressedkeys[pygame.K_SPACE]:
		# when delay is done, player can shoot
		if game.player.can_shoot() == True:
			# laser is spawned
			laser = Laser(game.player.pos_x, game.player.pos_y, game.screen)
			game.lasers.append(laser)
			# sound effect laser
			game.sfx['laser'].play()

	# TODO player can shoot with a different key, Key = 1
	# Look at example above, we can shoot with the space key
	# You can copy down code too!

	# TODO create laser_damage variable with the value of 25

	# updates laser 
	for laser in game.lasers:
		bounds = laser.update(game.seconds)
		if bounds is False:
			# deletes laser from game once it is out of the screen
			game.lasers.remove(laser)
		else:
			# laser hits one of the enemies
			hit = laser.hit(game.enemies)
			if hit:
				# laser is deleted
				game.lasers.remove(laser)
				# health enemy goes down
				hit.health = hit.health - 25
				# sound effect hit
				game.sfx['hit'].play()

	# updates enemy laser
	for laserEnemy in game.lasersEnemy:
		bounds = laserEnemy.update(game.seconds)
		if bounds is False:
			# deletes laser from game once it is out of the screen
			game.lasersEnemy.remove(laserEnemy)
		else:
			# laser hits the player
			hit = laserEnemy.hit(game.player.pos_x, game.player.pos_y)
			if hit:
				# laser is deleted
				game.lasersEnemy.remove(laserEnemy)
				# health player goes down
				game.player.health = game.player.health - 25
				# sound effect hit
				game.sfx['hit'].play()

	# updates enemy
	for enemy in game.enemies:
		enemy.update(game.seconds)
		# enemy dies at zero HP
		if enemy.health <= 0:
			# enemy is deleted
			game.enemies.remove(enemy)
			game.score = game.score + 50
			# sound effect explosion
			game.sfx['explosion'].play()
		# if enemy can shoot, shoot
		if enemy.can_shoot():
			laserEnemy = LaserEnemy(enemy, game.screen)
			game.lasersEnemy.append(laserEnemy)

	# when all enemies die, level up!
	if len(game.enemies) == 0:
		game.level_up()
		# TODO add to game score when level up, value of 50