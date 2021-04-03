import math
import copy
import pygame
import random

pygame.init()

from code import helpers
from code.Explosion import Explosion


class SergantBrown(pygame.sprite.Sprite):

	def __init__(self,
		_args):
	
		super(
			SergantBrown,
			self).__init__()
			
		self.image_orig = helpers.load_image(
			_args["filepath_sergant"]) 
			
		self.image = helpers.load_image(
			_args["filepath_sergant"])
		self.rect = self.image.get_rect()
		self.rect.centerx = _args["centerx"]
		self.rect.centery = _args["centery"]
		
		self.arena = _args["arena"]
		self.char = _args["char"]
		
		self.explosions = _args["explosions"]
		self.fog = _args["fog"]
		
		self.criminals = None
		
		self.key_already_down = False
		self.mouse_already_down = False
		
		self.arena.init_matrix_for_char(self.char)
		
		self.in_movement = False
		self.current_movement_cycle = 0
		self.max_movement_cycles = 10
		self.own_pos = None
		self.next_pos = None
		
		self.walls_criminals = []

		for t in self.arena.sprites():
			if t.type == "wall":
				self.walls_criminals.append(t)	

		self.radar_cooldown = _args["radar_cooldown"]
		self.radar_cooldown_counter = _args["radar_cooldown"]
		
		# Laser
		self.laser_aim_coords = []
		self.laser_aim_angle_degrees = []
		
		# Radar
		self.radar_in_use = False
		self.radar_energy = 400
		self.radar_radius = 0
		self.radar_recharge_factor = 10
		
		self.shot_sound = helpers.load_sound(
			_args["shot_sound"])
		
		
		self.move_right = self.move_left = self.move_up = self.move_down = False
		
		self.radar_text = _args["radar_text"]
		
		self.menu_no = False
		self.shots_fired = 0
		
		
	def init_criminals(self, _criminals):
		self.criminals = _criminals
		for c in self.criminals:
			self.walls_criminals.append(c)
	
		
	def update(self, _eventlist):
		
		self.own_pos = self.arena.get_position(self.char)
		
		possible_moves = self.arena.get_possible_moves(
			self.char)
		cont = False

		for e in _eventlist:
			if e.type == pygame.KEYDOWN:  #and not self.key_already_down:
				if e.key == pygame.K_w:
					self.move_up = True
				if e.key == pygame.K_s:
					self.move_down = True
				if e.key == pygame.K_a:
					self.move_left = True
				if e.key == pygame.K_d:
					self.move_right = True

			if e.type == pygame.KEYUP:
				if e.key == pygame.K_w:
					self.move_up = False
				if e.key == pygame.K_s:
					self.move_down = False
				if e.key == pygame.K_a:
					self.move_left = False
				if e.key == pygame.K_d:
					self.move_right = False			
						
		if not self.in_movement:
			possible_next_move = None
			if self.move_up:
				possible_next_move = [self.own_pos[0]-1, self.own_pos[1]]
			if self.move_down:
				possible_next_move = [self.own_pos[0]+1, self.own_pos[1]]
			if self.move_left:
				possible_next_move = [self.own_pos[0], self.own_pos[1]-1]	
			if self.move_right:
				possible_next_move = [self.own_pos[0], self.own_pos[1]+1]				
			
			if possible_next_move is not None:
				if possible_next_move in possible_moves:
					# Move there.
					self.in_movement = True
					self.current_movement_cycle = 0
					self.next_pos = possible_next_move
					
					# elif e.type == pygame.KEYUP:
						# self.key_already_down = False
					
		if self.in_movement:
			self.move()
			
			if self.current_movement_cycle >= self.max_movement_cycles:
				self.in_movement = False
				self.arena.set_position("S", self.next_pos)

				self.current_movement_cycle = 0
				self.next_pos = None
		
		
		# Calc laser stuff.
		self.calc_laser_aim()
		
		if not self.mouse_already_down and not self.menu_no:
			if pygame.mouse.get_pressed()[0] == True:		
				self.shots_fired += 1
				self.shot_sound.play()
				self.mouse_already_down = True
				params = dict()
				params["width_range"] = [1, 3]
				params["height_range"] = [1, 3]
				params["colour"] = pygame.Color(0, 255, 0, 0)
				params["coords"] = self.laser_aim_collision_point
				params["n_particles"] = random.randint(5, 10)
				params["ttl_range"] = [5, 15]
				self.explosions.append(
					Explosion(params))
					
				for c in self.criminals:
					if c.rect.collidepoint(self.laser_aim_collision_point):
						c.kill()
						
						# Remove from list
						self.walls_criminals.remove(c)
		
		if pygame.mouse.get_pressed()[0] == False and self.mouse_already_down:
			self.mouse_already_down = False
		
		
		# Do radar stuff here.
		for e in _eventlist:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_SPACE and self.radar_cooldown_counter >= self.radar_cooldown:
					self.radar_cooldown_counter = 0
					self.radar_text.update("No")
		
		if self.radar_cooldown_counter == 0:
			self.fog.sprite.alpha = 0
		
		if self.radar_cooldown_counter < self.radar_cooldown:
			self.radar_cooldown_counter += 1
			
			if self.radar_cooldown_counter >= self.radar_cooldown:
				self.radar_text.update("Yes")
					
					
	def move(self):
	
		# Decide where to move.
		if self.own_pos[0] < self.next_pos[0]:
			# Move right.
			self.rect.move_ip(0, 5)
		elif self.own_pos[0] > self.next_pos[0]:
			# Move left
			self.rect.move_ip(0, -5)
		elif self.own_pos[1] < self.next_pos[1]:
			# Move down.
			self.rect.move_ip(5, 0)
		elif self.own_pos[1] > self.next_pos[1]:
			# Move up.
			self.rect.move_ip(-5, 0)
	
		self.current_movement_cycle += 1


	def calc_laser_aim(self):
	
		# Get pos of mouse pointer.
		mouse_xy = pygame.mouse.get_pos()
		
		# Get player pos.
		player_xy = self.rect.center
		
		# Calc angle in degrees
		self.laser_aim_angle_degrees = (math.degrees(
			math.atan2(
				mouse_xy[1] - player_xy[1],
				mouse_xy[0] - player_xy[0])) + 360) % 360
				
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
			
			if pygame.sprite.spritecollideany(cr, self.walls_criminals) is not None:
				running = False
				self.laser_aim_collision_point = cr.rect.center
			
		
		self.laser_aim_coords = [player_xy, self.laser_aim_collision_point]
		