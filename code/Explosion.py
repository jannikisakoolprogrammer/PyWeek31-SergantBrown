#    Sergant Brown - LaserTag Traning - A game written using Python and Pygame for PyWeek #31
#    Copyright (C) 2021  Master47
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
			
		
		