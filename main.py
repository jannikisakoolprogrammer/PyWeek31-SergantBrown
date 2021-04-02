import os
import pygame
pygame.init()

from code.Arena import Arena
from code.SergantBrown import SergantBrown
from code.Criminal import Criminal
from code.Fog import Fog

from code import helpers


WINDOW_WIDTH = 1350
WINDOW_HEIGHT = 750

RED = pygame.Color(255, 0, 0, 0)
DARKRED = pygame.Color(100, 0, 0, 0)
GREEN = pygame.Color(0, 255, 0, 0)
DARKGREEN = pygame.Color(0, 100, 0, 0)
BLUE = pygame.Color(0, 0, 255, 0)
YELLOW = pygame.Color(255, 255, 0, 0)
BLACK = pygame.Color(0, 0, 0, 0)
WHITE = pygame.Color(255, 255, 255, 0)
GREY = pygame.Color(100, 100, 100, 0)

FPS = 30

ARENA_DIR = "maps"
ARENA_FILE = "map5.txt"

IMAGE_DIR = "graphics"
WALL_FILE = "wall.png"
SERGANT_FILE = "sergant.png"
CRIMINAL_FILE = "criminal.png"

ARENA_TILE_DICT = {
	"#": os.path.join(
		os.getcwd(),
		IMAGE_DIR,
		WALL_FILE)}



class Game(object):
	
	def __init__(self):
		self.window = pygame.display.set_mode((
			WINDOW_WIDTH,
			WINDOW_HEIGHT))
		
		self.clock = pygame.time.Clock()
		
		self.running = False
		self.events = None
		
		# Game objects
		self.arena = pygame.sprite.Group()
		self.sergant = pygame.sprite.GroupSingle()
		self.criminals = pygame.sprite.Group()
		self.explosions = []
		
		self.fog = pygame.sprite.GroupSingle()
	
		# Prepare game objects.
		self.prepare_arena()
		self.prepare_fog()		
		self.prepare_sergant()
		self.prepare_criminals()
		self.sergant.sprite.init_criminals(self.criminals)
	
	
	def prepare_arena(self):
		
		filepath = os.path.join(
			os.getcwd(),
			ARENA_DIR,
			ARENA_FILE)
		
		args = dict()
		args["filepath"] = filepath
		args["tile_dict"] = ARENA_TILE_DICT
		args["tile_width"] = 50
		args["tile_height"] = 50
		args["exclusion_list"] = [" ", "S", "1", "2", "3", "4", "5"]
			
		self.arena = Arena(args)
	
	
	def prepare_fog(self):
	
		args = dict()
		args["width"] = WINDOW_WIDTH
		args["height"] = WINDOW_HEIGHT
		args["colour"] = pygame.Color(0, 0, 0, 0)
		args["alpha_stepping"] = 5
		args["active"] = False
		
		self.fog.sprite = Fog(args)
		
		
	def prepare_sergant(self):
	
		filepath_map = os.path.join(
			os.getcwd(),
			ARENA_DIR,
			ARENA_FILE)	
	
		start_pos_centerx_centery = helpers.find_start_pos(
			filepath_map,
			50,
			50,
			"S")
	
		filepath_sergant = os.path.join(
			os.getcwd(),
			IMAGE_DIR,
			SERGANT_FILE)
			
		args = dict()
		args["filepath_sergant"] = filepath_sergant
		args["centerx"] = start_pos_centerx_centery[0]
		args["centery"] = start_pos_centerx_centery[1]
		args["arena"] = self.arena
		args["char"] = "S"
		args["explosions"] = self.explosions
		args["fog"] = self.fog
		args["radar_cooldown"] = 150
			
		self.sergant.sprite = SergantBrown(args)
	
	
	def prepare_criminals(self):
		
		filepath_map = os.path.join(
			os.getcwd(),
			ARENA_DIR,
			ARENA_FILE)	
			
		criminals = ["1", "2", "3", "4", "5"]
		for x in criminals:
			start_pos_centerx_centery = helpers.find_start_pos(
				filepath_map,
				50,
				50,
				x)
			filepath_criminal = os.path.join(
				os.getcwd(),
				IMAGE_DIR,
				CRIMINAL_FILE)
				
			args = dict()
			args["filepath"] = filepath_criminal
			args["centerx"] = start_pos_centerx_centery[0]
			args["centery"] = start_pos_centerx_centery[1]
			args["sensor_energy"] = 400
			args["sensor_stepping"] = 5
			args["shoot_interval_min"] = 2
			args["shoot_interval_max"] = 4
			args["one_move_distance"] = 50 # pixels
			args["sergant"] = self.sergant.sprite
			args["window"] = self.window
			args["arena_tiles"] = self.arena.sprites()
			args["arena"] = self.arena
			args["char"] = x
			args["explosions"] = self.explosions
			args["radar_wait_interval"] = 150
		
				
			self.criminals.add(Criminal(args))
		
	
	def run(self):
		
		self.running = True
		
		while self.running:
		
			self.update_events()
			self.process_events()
			
			self.update_game_objects()
			
			if self.sergant.sprite == None or len(self.criminals) == 0:
				self.running = False
			
			self.fill_window_background()
			self.draw_game_objects()
			
			self.clock.tick(FPS)
			pygame.display.update()
			
		
	def update_events(self):
		
		self.events = pygame.event.get()
	
	
	def process_events(self):
		
		for e in self.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_ESCAPE:
					self.running = False
	
	
	def fill_window_background(self):
	
		self.window.fill(BLACK)
	
	
	def update_game_objects(self):
		self.sergant.update(self.events)
		self.fog.update()		
		self.criminals.update()
		for sg in self.explosions:
			sg.update()
		
	
	def draw_game_objects(self):
	
		self.arena.draw(self.window)

		self.criminals.draw(self.window)

		self.fog.draw(self.window)
		
		self.sergant.draw(self.window)		
		
		# Criminal laser and explosions.
		for c in self.criminals:
			#pygame.draw.aaline(
		#		self.window,
			#	DARKRED,
			#	c.laser_aim_coords[0],
		#		c.laser_aim_coords[1])
				
			pygame.draw.circle(
				self.window,
				RED,
				c.laser_aim_coords[1],
				2)		
		
		if self.sergant.sprite is not None:
		#	pygame.draw.aaline(
		#		self.window,
		#		DARKGREEN,
		#		self.sergant.sprite.laser_aim_coords[0],
		#		self.sergant.sprite.laser_aim_coords[1])
				
			pygame.draw.circle(
				self.window,
				GREEN,
				self.sergant.sprite.laser_aim_coords[1],
				2)	
		
		for sg in self.explosions:
			sg.draw(self.window)


game = Game()
game.run()