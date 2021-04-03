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

from code.Text import Text


class Button(pygame.sprite.Sprite):

	def __init__(self,
		_args_active,
		_args_inactive,
		_return_value):
	
		super(
			Button,
			self).__init__()
			
		self.active = Text(_args_active)
		self.inactive = Text(_args_inactive)
		self.return_value = _return_value
		self.state = "inactive"
			
		self.image = self.inactive.image
		self.rect = self.inactive.rect
	
	
	def update(self):
		
		if self.rect.collidepoint(pygame.mouse.get_pos()):
			self.state = "active"
			self.image = self.active.image
			self.rect = self.active.rect
			
			if pygame.mouse.get_pressed()[0]:
				return self.return_value
		else:
			self.state = "inactive"
			self.image = self.inactive.image
			self.rect = self.inactive.rect
		
		return None
