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


class ArenaTile(pygame.sprite.Sprite):

	def __init__(self,
		_args):
	
		super(
			ArenaTile,
			self).__init__()
			
		self.image = _args["image"]
		self.rect = self.image.get_rect()
		self.rect.top = _args["top"]
		self.rect.left = _args["left"]
		
		self.type = _args["type"]