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
		