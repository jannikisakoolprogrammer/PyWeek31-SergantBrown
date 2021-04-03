import math
import copy
import pygame
pygame.init()

from code import helpers
from code.Explosion import Explosion
import random


class Criminal(pygame.sprite.Sprite):

	def __init__(self,
		_args):
	
		super(
			Criminal,
			self).__init__()
			
		self.image_orig = helpers.load_image(
			_args["filepath"]) 			
			
		self.image = helpers.load_image(
			_args["filepath"])
		self.rect = self.image.get_rect()
		self.rect.centerx = _args["centerx"]
		self.rect.centery = _args["centery"]
		
		#self.sensor_energy = _args["sensor_energy"]
		#self.sensor_max_energy = _args["sensor_max_energy"]
		#self.sensor_stepping = _args["sensor_stepping"]
		#self.sensor_timeout = _args["sensor_timeout"]
		#self.sensor_timer = self.sensor_timeout
		
		#self.shoot_timeout = _args["shoot_timeout"]
		
		#self.random_movement_duration_max = _args["random_movement_duration_max"]
		#self.random_movement_duration_timer = _args["random_movement_duration_timer"]
		#self.random_movement_single_move_length = _args["random_movement_single_move_length"]
		
		#self.precise_movement_duration = _args["precise_movement_duration"]
		
		#self.sergant_found = False
		
		#self.shoot_interval_min = _args["shoot_interval_min"]
		#self.shoot_interval_max = _args["shoot_interval_max"]
		#self.one_move_distance = _args["one_move_distance"] # Pixels
		#self.one_move_distance_max = _args["one_move_distance"] # Pixels
		
		#self.player_seen_after_last_sensor_use = False
		#self.sergant_found = False
		
		self.sergant = _args["sergant"]
		self.window = _args["window"]
		self.arena_tiles = _args["arena_tiles"]
		self.arena = _args["arena"]
		self.radar = pygame.sprite.Sprite()
		self.char = _args["char"]
		
		self.arena.init_matrix_for_char(self.char)
		
		self.walls = []			

		for t in self.arena_tiles:
			if t.type == "wall":
				self.walls.append(t.rect)
				
		self.walls_sergant = []
		
		for t in self.arena.sprites():
			if t.type == "wall":
				self.walls_sergant.append(t)

		self.walls_sergant.append(self.sergant)
		
		self.route_found = False
		self.route = dict()
		self.route_value = None
		self.own_pos = None
		self.movement_cycles_per_step = 25
		self.current_movement_cycle = 1
		self.max_route_value = 0
		self.in_movement = False
		self.player_pos = None
		
		self.radar_wait_interval = _args["radar_wait_interval"]
		self.radar_wait_interval_timer = _args["radar_wait_interval"] # Intially the same.
		self.radar_used = False
		self.radar_can_be_used = True
		self.in_random_movement = False
		self.movement_cycles_per_step_random = 25
		self.current_movement_cycle_random = 1
		self.next_random_movement = None
		
		# Laser
		self.explosions = _args["explosions"]
		self.laser_aim_coords = []
		self.laser_aim_angle_degrees = []		
	

	#def sensor_can_be_used_again(self):
#		if self.sensor_timer >= self.sensor_timeout:
#			return True
#		else:
#			return False
	
	
#	def not_in_random_movement(self):
#		if self.random_movement_duration_timer >= self.random_movement_duration_max:
#			return True
#		else:
#			return False
		self.laser_coords = [1366/2, 768/2]	
	
	def update(self):
	

		self.own_pos = self.arena.get_position(self.char)
		self.player_pos = self.arena.get_position(self.sergant.char)
		
		if not self.route_found and not self.in_random_movement:
			
			# Has the radar wait interval been reached?
			if self.radar_wait_interval_timer >= self.radar_wait_interval:
				self.radar_wait_interval_timer = 0

				self.get_movepoints_towards_player()
				
				# Laser coords towards player.
				self.laser_coords = self.sergant.rect.center			
			
			else:
				# Meanwhile, move randomly.
				self.in_random_movement = True
				
				# Random laser coords.
				self.laser_coords = [random.randint(1, 1366), random.randint(1, 768)]
		
		if self.route_found == True:
			# Move towards player using the route.
			# At the end, recalculate route.
			self.move_to_player()
	
	
		if self.radar_wait_interval_timer <= self.radar_wait_interval:
			self.radar_wait_interval_timer += 1
		
		
		if self.in_random_movement == True:
			# Move randomly.  Can also mean just staying in the same spot.
			self.move_randomly()
			
		# Calc laser stuff.
		self.calc_laser_aim()
		
		# randomly shoot
		if random.randint(1, 100) == 50:
			
			params = dict()
			params["width_range"] = [1, 3]
			params["height_range"] = [1, 3]
			params["colour"] = pygame.Color(255, 0, 0, 0)
			params["coords"] = self.laser_aim_collision_point
			params["n_particles"] = random.randint(5, 10)
			params["ttl_range"] = [5, 15]
			self.explosions.append(
				Explosion(params))
				
			if self.sergant.rect.collidepoint(self.laser_aim_collision_point):
				self.sergant.kill()

	
	def get_movepoints_towards_player(self):
		
		# Get player pos
		player_pos = self.arena.get_position(self.sergant.char)
		
		# Get own pos.
		own_pos = self.arena.get_position(self.char)
		
		# Recursively call function to find player.
		# Record steps.
		recorded = []
		recorded2 = []
		steps = {}
		recorded_new = []
		value = 0
		
		# Check if same pos as player.
		if player_pos[0] == own_pos[0] and player_pos[1] == own_pos[1]:
			# Dont do anything.
			pass
		else:
			recorded2.append(own_pos)
			steps[tuple(own_pos)] = value
			recorded.append(recorded2[0])
			
			steps = self.find_player(
				player_pos,
				steps,
				recorded,
				recorded2,
				value+1)

			for key, value in steps.items():
				if self.max_route_value < value:
					self.max_route_value = value
			
			# Now calc route to player
			dict_route = {}
			tplayer_pos = tuple(player_pos)

			if tplayer_pos in steps:
				dict_route[tplayer_pos] = steps[tplayer_pos]
				self.route = self.calc_route_to_player(
					tplayer_pos,
					own_pos,
					steps,
					dict_route)
					
				# Randomise route steps so there is more variation :)
				self.max_route_value = random.randint(
					0, self.max_route_value)

				# Now we know the steps to the player.
				self.route_found = True
		
	def find_player(self,
		_player_pos,
		_steps,
		_recorded,
		_recorded_new,
		_value):
		
		recorded_new_2 = []
	
		# Check all four directions always for each in _recorded_new
		for x in _recorded_new:
			possible_moves = self.arena.get_possible_moves(None, x)

			# Filter out any that have already been checked.
			possible_moves_filtered = []
			for possible_move in possible_moves:
				if possible_move not in _recorded:
					possible_moves_filtered.append(possible_move)
			
			recorded_new_2.extend(possible_moves_filtered)		
			# Check if player is there.
			for possible_move2 in possible_moves_filtered:
				if possible_move2 == _player_pos:
					# Player found.  Add this to the list of steps.
					_steps[tuple(possible_move2)] = _value
					return _steps
				else:
					_steps[tuple(possible_move2)] = _value
					
			_recorded.extend(possible_moves_filtered)

		val = _value + 1

		_steps = self.find_player(
			_player_pos,
			_steps,
			_recorded,
			recorded_new_2,
			val)
			
		return _steps
				
		
	def calc_route_to_player(self,
		_cur_pos,
		_own_pos,
		_steps,
		_route):
		
		# With current position, find the next position.
		# Next position needs to be distance - 1, and next to it
		# Be it up, down, left, right.
		distance = _route[_cur_pos]
		
		possible = dict()
		for key, value in _steps.items():
			if value == distance - 1:
				# print(key)
				possible[key] = value
		# print(possible)
		# Now find the correct ones.
		correct = dict()
		l = list(_cur_pos)
		
		up = (l[0]-1, l[1])
		down = (l[0]+1, l[1])
		left = (l[0], l[1]-1)
		right = (l[0], l[1]+1)
		
		possible2 = [up, down, left, right]
		# print(possible)
		found = False
		for p in possible2:
			for key, value in possible.items():
				if key == p and value == distance - 1:
					correct[key] = value
					found = True
					break
				
			if found == True:
				break
		
		# Add to route.
		_route.update(correct)
		
		# Check if own pos was found:
		for k in correct:
			_cur_pos = k
			if _cur_pos == tuple(_own_pos):
				return _route
			break
		
		# Otherwise continue to next step.
		return self.calc_route_to_player(
			_cur_pos,
			_own_pos,
			_steps,
			_route)
		
	
	def move_to_player(self):
		# if not in movement:  Update own pos.
		# If in movement:  move.
		
		if self.route_found == True:
			if not self.in_movement:
				if self.route_value == None:
					self.route_value = 0
				# print(self.max_route_value)
				# print("---------")

				if self.route_value >= self.max_route_value:
					self.route_found = False
					self.route_value = None
					self.route = dict()
					self.in_movement = False
					self.max_route_value = 0
					return

				self.route_value += 1
				# print(self.route_value)				

				# Fetch next pos from route.
				for key, value in self.route.items():
					if value == self.route_value:
						self.next_pos = key
						break
				# print(self.next_pos)
				self.in_movement = True
		
		if self.route_found:
			if self.in_movement:
				if self.next_pos is not self.own_pos:
					self.own_pos = self.arena.get_position(self.char)
					# Move.
					self.move()
					
					if self.movement_cycles_per_step == self.current_movement_cycle:
						# We have reached our destination.
						self.own_pos = self.next_pos

						# Update it now.
						self.arena.set_position(
							self.char,
							self.own_pos)
						
						self.own_pos = self.arena.get_position(self.char)
						self.in_movement = False
						self.current_movement_cycle = 0
	
	
	def move(self):
	
		# Decide where to move.
		if self.own_pos[0] < self.next_pos[0]:
			# Move right.
			self.rect.move_ip(0, 2)
		elif self.own_pos[0] > self.next_pos[0]:
			# Move left
			self.rect.move_ip(0, -2)
		elif self.own_pos[1] < self.next_pos[1]:
			# Move down.
			self.rect.move_ip(2, 0)
		elif self.own_pos[1] > self.next_pos[1]:
			# Move up.
			self.rect.move_ip(-2, 0)
	
		self.current_movement_cycle += 1
	
	
	def move_randomly(self):
		if self.next_random_movement == None:
			#self.own_pos = self.arena.get_position(self.char)
			possible_moves = self.arena.get_possible_moves(
				self.char)
				
			# Pick one.
			self.next_random_movement = random.choice(possible_moves)

		self.move_random()
		
		if self.current_movement_cycle_random >= self.movement_cycles_per_step_random:
			self.in_random_movement = False
			self.arena.set_position(self.char, self.next_random_movement)
			self.current_movement_cycle_random = 0
			self.next_random_movement = None	

			
	def move_random(self):
	
		# Decide where to move.
		if self.own_pos[0] < self.next_random_movement[0]:
			# Move right.
			self.rect.move_ip(0, 2)
		elif self.own_pos[0] > self.next_random_movement[0]:
			# Move left
			self.rect.move_ip(0, -2)
		elif self.own_pos[1] < self.next_random_movement[1]:
			# Move down.
			self.rect.move_ip(2, 0)
		elif self.own_pos[1] > self.next_random_movement[1]:
			# Move up.
			self.rect.move_ip(-2, 0)
	
		self.current_movement_cycle_random += 1		


	def calc_laser_aim(self):
	
		# Get random pos.
		mouse_xy = self.laser_coords
		
		# Get player pos.
		criminal_xy = self.rect.center
		
		# Calc angle in degrees
		self.laser_aim_angle_degrees = (math.degrees(
			math.atan2(
				mouse_xy[1] - criminal_xy[1],
				mouse_xy[0] - criminal_xy[0])) + 360) % 360
				
		# Rotate image.
		self.image = pygame.transform.rotate(
			self.image_orig,
			-self.laser_aim_angle_degrees)				
		
		# Calc collision point.
		cr = pygame.sprite.Sprite()
		cr.image = pygame.Surface((1, 1))
		cr.rect = cr.image.get_rect()
		cr.rect.center = copy.deepcopy(self.rect.center)
		
		# Now move the point along the angle until a collision with a wall occurs.
		# And of course with the criminals.
		x = float(self.rect.centerx)
		y = float(self.rect.centery)
		x_factor = math.cos(math.radians(self.laser_aim_angle_degrees)) * 2
		y_factor = math.sin(math.radians(self.laser_aim_angle_degrees)) * 2
		running = True
		
		#print(x_factor, y_factor)
		while running:
			
			x += x_factor
			y += y_factor
			
			cr.rect.centerx = x
			cr.rect.centery = y
			
			if pygame.sprite.spritecollideany(cr, self.walls_sergant) is not None:
				running = False
				self.laser_aim_collision_point = cr.rect.center
			
		
		self.laser_aim_coords = [criminal_xy, self.laser_aim_collision_point]