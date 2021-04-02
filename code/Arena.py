import copy

import pygame
pygame.init()

from code import helpers
from code.ArenaTile import ArenaTile


class Arena(pygame.sprite.Group):

	matrixes = dict()
	
	
	def __init__(self,
		_args):
	
		super(
			Arena,
			self).__init__()
			
		self.filepath = _args["filepath"]
		self.tile_dict = _args["tile_dict"]
		self.tile_width = _args["tile_width"]
		self.tile_height = _args["tile_height"]
		self.contents = ""
		
		self.matrix = list() 
		
		current_top = 0
		current_left = 0
		
		exclusion_list = _args["exclusion_list"]
		
		with open(
			self.filepath,
			"r") as filehandle:
			
			self.contents = filehandle.read()
			self.create_matrix()
			
			for row in self.contents.splitlines():
				for col in row:	
					if col not in exclusion_list:
						tile_info = dict()
						tile_info["image"] = helpers.load_image(
									self.tile_dict[col])
						tile_info["top"] = current_top
						tile_info["left"] = current_left
						tile_info["type"] = "wall"
						
						self.add(ArenaTile(tile_info))
					
					current_left += self.tile_width
				current_left = 0
				current_top += self.tile_height
				
	
	def create_matrix(self):
		
		r = c = 0
		for row in self.contents.splitlines():
			self.matrix.append(list())
			
			for col in row:
				self.matrix[r].append(col)
				c += 1
				
			c = 0
			r += 1
			
	
	
	def get_position(self,
		_who):
		
		local_matrix = self.matrixes[_who]
		
		coords = list()
		for row in range(len(local_matrix)):
			for col in range(len(local_matrix[row])):
				if local_matrix[row][col] == _who:
					coords = [row, col]
					break
		
		return coords
		
		
	def set_position(self,
		_who,
		_coords):
		
		local_matrix = self.matrixes[_who]
		
		coords = list()
		for row in range(len(local_matrix)):
			for col in range(len(local_matrix[row])):
				if local_matrix[row][col] == _who:
					coords = [row, col]
					break
					
		local_matrix[_coords[0]][_coords[1]] = _who
		local_matrix[coords[0]][coords[1]] = " "
		
	
	def get_possible_moves(self,
		_who = None,
		_pos = None):
		
		if _who == None and _pos == None:
			return []
		
		if _who:
			# Find _who on matrix
			coords = self.get_position(_who)
		else:
			coords = _pos
			
		# Get possible moves.
		row = coords[0]
		col = coords[1]
		
		possible_moves = []
		if row == 0 and col == 0:
			# Top left position.
			if not self.is_wall(
				row+1,
				col):
				possible_moves.append(
					[row+1, col])
					
			if not self.is_wall(
				row,
				col+1):
				possible_moves.append(
					[row, col+1])
		
		elif row == len(self.matrix)-1 and col == len(self.matrix[0])-1:
			# Bottom right position.
			if not self.is_wall(
				row-1,
				col):
				possible_moves.append(
					[row-1, col])
			
			if not self.is_wall(
				row,
				col-1):
				possible_moves.append(
					[row, col-1])
		
		elif row == len(self.matrix)-1 and col == 0:
			# Bottom left corner
			if not self.is_wall(
				row-1,
				col):
				possible_moves.append(
					[row-1, col])
			
			if not self.is_wall(
				row,
				col+1):
				possible_moves.append(
					[row, col+1])

		elif row == 0 and col == len(self.matrix[0])-1:
			# Top right corner
			if not self.is_wall(
				row+1,
				col):
				possible_moves.append(
					[row+1, col])
			
			if not self.is_wall(
				row,
				col-1):
				possible_moves.append(
					[row, col-1])
		
		else:
			# Somewhere in the map.  Four sides possible.
			possible1 = [row-1, col]
			possible2 = [row+1, col]
			possible3 = [row, col-1]
			possible4 = [row, col+1]
			
			possible = [possible1, possible2, possible3, possible4]
			for p in possible:
				if not self.is_wall(
					p[0],
					p[1]):
					possible_moves.append(
						p)
		
		return possible_moves
		
		
		
		
	def is_wall(self,
		_row,
		_col):
		
		if self.matrix[_row][_col] == "#":
			return True
		else:
			return False
	
	
	def init_matrix_for_char(self,
		_char):
		
		if not _char in self.matrixes:
			self.matrixes[_char] = copy.deepcopy(self.matrix)