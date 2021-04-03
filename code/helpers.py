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

def load_image(_filepath):
	
	return pygame.image.load(_filepath).convert_alpha()


def load_sound(_filepath):

	return pygame.mixer.Sound(_filepath)


def find_start_pos(
	_filepath_map,
	_tile_size_width,
	_tile_size_height,
	_char):
	
	current_top = 0
	current_left = 0
	
	with open(
		_filepath_map,
		"r") as filehandle:
		contents = filehandle.read()
		for row in contents.splitlines():
			for col in row:	
				if col is _char:
					
					return [
						current_left + _tile_size_width / 2,
						current_top + _tile_size_height / 2]
				
				current_left += _tile_size_width
				
			current_left = 0
			current_top += _tile_size_height