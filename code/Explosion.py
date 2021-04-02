import pygame
pygame.init()

from code import helpers

import random


class Explosion(pygame.sprite.Group):

	def __init__(self,
		_args):
	
		super(
			Explosion,
			self).__init__()
		
		self.width_range = _args["width_range"]
		self.height_range = _args["height_range"]
		self.colour = _args["colour"]
		self.coords = _args["coords"]
		
		self.n_particles = _args["n_particles"]
		self.ttl_range = _args["ttl_range"]
		
		for x in range(self.n_particles):
			sp = pygame.sprite.Sprite()
			sp.image = pygame.Surface((
				random.randint(self.width_range[0], self.width_range[1]),
				random.randint(self.height_range[0], self.height_range[1])))
			sp.rect = sp.image.get_rect()
			sp.rect.center = self.coords
			sp.image.fill(self.colour)

			sp.ttl_range = random.randint(self.ttl_range[0], self.ttl_range[1])
			sp.ttl_counter = 0
			self.add(sp)
		
		
	def update(self):
	
		for sp in self.sprites():
			if sp.ttl_counter <= sp.ttl_range:
				sp.rect.centerx += random.choice((-2, 2))
				sp.rect.centery += random.choice((-2, 2))
				sp.ttl_counter += 1
			else:
				sp.kill()
			
		
		