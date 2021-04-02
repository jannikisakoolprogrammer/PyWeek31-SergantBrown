import pygame
pygame.init()

def load_image(_filepath):
	
	return pygame.image.load(_filepath).convert_alpha()


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