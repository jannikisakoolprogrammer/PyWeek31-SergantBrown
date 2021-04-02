import pygame
pygame.init()

from code import helpers

import random


class Fog(pygame.sprite.Sprite):

	def __init__(self,
		_args):
	
		super(
			Fog,
			self).__init__()
	
		self.active = _args["active"]
		self.alpha_stepping = _args["alpha_stepping"]
		
		self.width = _args["width"]
		self.height = _args["height"]
		self.colour = _args["colour"]
		self.alpha = 255
		
		self.colour = pygame.Color(0, 0, 0, self.alpha)
		
		self.image = pygame.Surface((self.width, self.height), flags = pygame.SRCALPHA)
		self.image.convert_alpha()
		self.image.fill(self.colour)
		self.rect = self.image.get_rect()
		self.rect.top = 0
		self.rect.left = 0		

	
	def update(self):
	
		if self.alpha <= 250:
			self.alpha += self.alpha_stepping

		self.colour = pygame.Color(0, 0, 0, self.alpha)		
		
		self.image.fill(self.colour)
		