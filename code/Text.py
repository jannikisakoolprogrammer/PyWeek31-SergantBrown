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


class Text(pygame.sprite.Sprite):

	def __init__(self,
		_args):
	
		super(
			Text,
			self).__init__()
			
		self.static_text = _args["static_text"]
		self.dynamic_text = _args["dynamic_text"]
		self.filepath_font = _args["filepath_font"]
		self.font_size = _args["font_size"]
		self.fg_colour = _args["fg_colour"]
		self.bg_colour = _args["bg_colour"]
		self.centerx = _args["centerx"]
		self.centery = _args["centery"]

		self.font = pygame.font.Font(
			self.filepath_font,
			self.font_size)
			
		self.render_pos()
	
	
	def render_only(self):
	
		self.image = self.font.render(
			"%s %s" % (
				self.static_text,
				self.dynamic_text),
			True,
			self.fg_colour,
			self.bg_colour)
	
	
	def render_pos(self):
		
		self.render_only()
		
		self.rect = self.image.get_rect()
		self.rect.center = (self.centerx, self.centery)
	
	
	def update(self,
		_dynamic_text = None):
		
		if _dynamic_text is not None:
			self.dynamic_text = _dynamic_text
			self.render_only()
		