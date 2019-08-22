import pygame

def write(text, fontsize, colour):
	myfont = pygame.font.SysFont("None", fontsize)
	mytext = myfont.render(text, True, colour)
	mytext = mytext.convert_alpha()
	return mytext

def draw_ship(pos_x, pos_y, surface):
	pygame.draw.rect(surface, (0, 0, 0), (pos_x, pos_y, 50, 50))