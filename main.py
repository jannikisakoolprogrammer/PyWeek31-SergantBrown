import os
import pygame
import time
import copy
pygame.init()

from code.Arena import Arena
from code.SergantBrown import SergantBrown
from code.Criminal import Criminal
from code.Fog import Fog
from code.Text import Text
from code.Button import Button

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
ORANGE = pygame.Color(255, 150, 0)

FPS = 30

ARENA_DIR = "maps"
ARENA_FILE = "map5.txt"

IMAGE_DIR = "graphics"
WALL_FILE = "wall.png"
SERGANT_FILE = "sergant.png"
CRIMINAL_FILE = "criminal.png"

MUSIC_DIR = "music"
MUSIC = "chilled.mp3"

SOUND_DIR = "sounds"
SERGANT_SHOT_SOUND = "shot_player.wav"
CRIMINAL_SHOT_SOUND = "shot_criminal.wav"

FONT_DIR = "fonts"
FONT = "ZillaSlab-Regular.ttf"

ARENA_TILE_DICT = {
	"#": os.path.join(
		os.getcwd(),
		IMAGE_DIR,
		WALL_FILE)}
		

class MainGame(object):
	
	def __init__(self):
		self.window = pygame.display.set_mode((
			WINDOW_WIDTH,
			WINDOW_HEIGHT))
		
		self.clock = pygame.time.Clock()
		
		pygame.mixer.music.load(
			os.path.join(
				os.getcwd(),
				MUSIC_DIR,
				MUSIC))
		pygame.mixer.music.play(-1)		
	
	
	def run(self):
	
		level_filenames = []
		
		for filename in os.listdir(
			os.path.join(
				os.getcwd(),
				ARENA_DIR)):
				
				level_filenames.append(filename)
				
		n_levels = len(level_filenames)
		n_cnt = 0
		
		complete_results = dict()
		complete_results["shots_fired"] = 0
		complete_results["time"] = 0
		complete_results["n_enemies"] = 0
		
		for filename in level_filenames:
			# Show intro screen.
			self.level_intro_screen(filename)
			
			# Now load and run the game.
			game = Game(self.window, self.clock, filename)
			result = game.run()
			
			n_cnt += 1
			
			if result["win"] is False:
				self.game_over_screen()
				Arena.matrixes = dict()
				break
			else:
				complete_results["shots_fired"] += result["shots_fired"]
				complete_results["time"] += result["time"]	
				complete_results["n_enemies"] += result["n_enemies"]
				Arena.matrixes = dict()
				
				self.level_outro_screen()
			
		pygame.mouse.set_visible(True)

		if n_cnt == n_levels and result["win"] == True:
			self.win_screen(complete_results)
			# You did it!!
			# Show outro screen with info such as time and accuracy.  Let player enter their name.
	
	
	def title_screen(self):
	
		args = dict()
		args["static_text"] = "Sergant Brown - LaserTag Training"
		args["dynamic_text"] = ""
		args["filepath_font"] = os.path.join(
			os.getcwd(),
			FONT_DIR,
			FONT)
		args["font_size"] = 60
		args["fg_colour"] = YELLOW
		args["bg_colour"] = None
		args["centerx"] = WINDOW_WIDTH / 2
		args["centery"] = 100
		title_text = Text(args)
		
		# Yes button.
		args = dict()
		args["static_text"] = "Start"
		args["dynamic_text"] = ""
		args["filepath_font"] = os.path.join(
			os.getcwd(),
			FONT_DIR,
			FONT)
		args["font_size"] = 30
		args["fg_colour"] = YELLOW
		args["bg_colour"] = None
		args["centerx"] = WINDOW_WIDTH / 2
		args["centery"] = 300
		
		args2 = copy.deepcopy(args)
		args2["fg_colour"] = ORANGE
		start_button = Button(args2, args, "start")	

		# No button.
		args = dict()
		args["static_text"] = "Exit"
		args["dynamic_text"] = ""
		args["filepath_font"] = os.path.join(
			os.getcwd(),
			FONT_DIR,
			FONT)
		args["font_size"] = 30
		args["fg_colour"] = YELLOW
		args["bg_colour"] = None
		args["centerx"] = WINDOW_WIDTH / 2
		args["centery"] = 400
		
		args2 = copy.deepcopy(args)
		args2["fg_colour"] = ORANGE
		exit_button = Button(args2, args, "exit")	
		
		ret_value = None
		running = True
		while running:
			eventlist = pygame.event.get()
			ret_value = start_button.update()
			if ret_value == "start":
				self.run()
				
			ret_value = exit_button.update()
			if ret_value == "exit":
				running = False
			
			
			self.window.fill(BLACK)
			self.window.blit(
				title_text.image,
				title_text.rect)
				
			self.window.blit(
				start_button.image,
				start_button.rect)
				
			self.window.blit(
				exit_button.image,
				exit_button.rect)				
			
			pygame.display.update()
			self.clock.tick(FPS)
			
		pygame.event.get()
		pygame.event.clear()
	
	
	def level_intro_screen(self, _map_name):
		args = dict()
		args["static_text"] = ""
		args["dynamic_text"] = os.path.splitext(_map_name.capitalize())[0]
		args["filepath_font"] = os.path.join(
			os.getcwd(),
			FONT_DIR,
			FONT)
		args["font_size"] = 40
		args["fg_colour"] = YELLOW
		args["bg_colour"] = None
		args["centerx"] = WINDOW_WIDTH / 2
		args["centery"] = WINDOW_HEIGHT / 2
		map_text = Text(args)
		
		self.window.fill(BLACK)
		self.window.blit(
			map_text.image,
			map_text.rect)
		
		pygame.display.update()
		time.sleep(2)
	
	
	def level_outro_screen(self):
		args = dict()
		args["static_text"] = "Well done."
		args["dynamic_text"] = ""
		args["filepath_font"] = os.path.join(
			os.getcwd(),
			FONT_DIR,
			FONT)
		args["font_size"] = 40
		args["fg_colour"] = YELLOW
		args["bg_colour"] = None
		args["centerx"] = WINDOW_WIDTH / 2
		args["centery"] = WINDOW_HEIGHT / 2
		map_text = Text(args)
		
		self.window.fill(BLACK)
		self.window.blit(
			map_text.image,
			map_text.rect)
		
		pygame.display.update()
		time.sleep(2)
	
	
	def game_over_screen(self):
		args = dict()
		args["static_text"] = "You've lost.  Please try again."
		args["dynamic_text"] = ""
		args["filepath_font"] = os.path.join(
			os.getcwd(),
			FONT_DIR,
			FONT)
		args["font_size"] = 40
		args["fg_colour"] = YELLOW
		args["bg_colour"] = None
		args["centerx"] = WINDOW_WIDTH / 2
		args["centery"] = WINDOW_HEIGHT / 2
		map_text = Text(args)
		
		self.window.fill(BLACK)
		self.window.blit(
			map_text.image,
			map_text.rect)
		
		pygame.display.update()
		time.sleep(2)
	
	
	def win_screen(self, _results):
		args = dict()
		args["static_text"] = "Congratulations!  You've beaten all levels."
		args["dynamic_text"] = ""
		args["filepath_font"] = os.path.join(
			os.getcwd(),
			FONT_DIR,
			FONT)
		args["font_size"] = 40
		args["fg_colour"] = YELLOW
		args["bg_colour"] = None
		args["centerx"] = WINDOW_WIDTH / 2
		args["centery"] = 100
		congrats_text = Text(args)
		
		args = dict()
		args["static_text"] = "Time in seconds:"
		args["dynamic_text"] = (_results["time"] / FPS)
		args["filepath_font"] = os.path.join(
			os.getcwd(),
			FONT_DIR,
			FONT)
		args["font_size"] = 30
		args["fg_colour"] = YELLOW
		args["bg_colour"] = None
		args["centerx"] = WINDOW_WIDTH / 2
		args["centery"] = 300
		time_text = Text(args)
		
		args = dict()
		args["static_text"] = "Accuracy in %:"
		args["dynamic_text"] = (_results["n_enemies"] / _results ["shots_fired"] * 100)
		args["filepath_font"] = os.path.join(
			os.getcwd(),
			FONT_DIR,
			FONT)
		args["font_size"] = 30
		args["fg_colour"] = YELLOW
		args["bg_colour"] = None
		args["centerx"] = WINDOW_WIDTH / 2
		args["centery"] = 400
		accuracy_text = Text(args)		
		
		# Ok button.
		args = dict()
		args["static_text"] = "Ok"
		args["dynamic_text"] = ""
		args["filepath_font"] = os.path.join(
			os.getcwd(),
			FONT_DIR,
			FONT)
		args["font_size"] = 30
		args["fg_colour"] = YELLOW
		args["bg_colour"] = None
		args["centerx"] = WINDOW_WIDTH / 2
		args["centery"] = 500
		
		args2 = copy.deepcopy(args)
		args2["fg_colour"] = ORANGE
		ok_button = Button(args2, args, "ok")	
		
		
		ret_value = None
		running = True
		while running:
			eventlist = pygame.event.get()
			ret_value = ok_button.update()
			if ret_value == "ok":
				running = False
			
			
			self.window.fill(BLACK)
			self.window.blit(
				congrats_text.image,
				congrats_text.rect)
				
			self.window.blit(
				time_text.image,
				time_text.rect)
				
			self.window.blit(
				accuracy_text.image,
				accuracy_text.rect)	

			self.window.blit(
				ok_button.image,
				ok_button.rect)	
			
			pygame.display.update()
			self.clock.tick(FPS)
			
		pygame.event.get()
		pygame.event.clear()
		

class Game(object):
	
	def __init__(self, _window, _clock, _level_filename):
		self.window = _window
		self.clock = _clock
		self.level_filename = _level_filename
		
		
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
		self.prepare_map_text()
		self.prepare_radar_text()
		self.prepare_sergant()
		self.prepare_criminals()
		self.sergant.sprite.init_criminals(self.criminals)
	
	
	def prepare_arena(self):
		
		filepath = os.path.join(
			os.getcwd(),
			ARENA_DIR,
			self.level_filename)
		
		args = dict()
		args["filepath"] = filepath
		args["tile_dict"] = ARENA_TILE_DICT
		args["tile_width"] = 50
		args["tile_height"] = 50
		
		# Build exclusion list dynamically.
		exclusion_list = []
		filehandle = open(filepath)
		contents = filehandle.read()		
		for row in contents.splitlines():
			for col in row:
				if col != "#" and col not in exclusion_list:
					exclusion_list.append(col)
					
		args["exclusion_list"] = exclusion_list
			
		self.arena = Arena(args)
	
	
	def prepare_fog(self):
	
		args = dict()
		args["width"] = WINDOW_WIDTH
		args["height"] = WINDOW_HEIGHT
		args["colour"] = pygame.Color(0, 0, 0, 0)
		args["alpha_stepping"] = 5
		args["active"] = False
		
		self.fog.sprite = Fog(args)
	
	
	def prepare_map_text(self):
		
		args = dict()
		args["static_text"] = "Current map:"
		args["dynamic_text"] = os.path.splitext(self.level_filename.capitalize())[0]
		args["filepath_font"] = os.path.join(
			os.getcwd(),
			FONT_DIR,
			FONT)
		args["font_size"] = 20
		args["fg_colour"] = YELLOW
		args["bg_colour"] = None
		args["centerx"] = 100
		args["centery"] = 25
		self.map_text = Text(args)
		
	
	def prepare_radar_text(self):
		
		args = dict()
		args["static_text"] = "Infrared Camera:"
		args["dynamic_text"] = "Yes"
		args["filepath_font"] = os.path.join(
			os.getcwd(),
			FONT_DIR,
			FONT)
		args["font_size"] = 20
		args["fg_colour"] = YELLOW
		args["bg_colour"] = None
		args["centerx"] = 300
		args["centery"] = 25
		self.radar_text = Text(args)
		
		
	def prepare_sergant(self):
	
		filepath_map = os.path.join(
			os.getcwd(),
			ARENA_DIR,
			self.level_filename)	
	
		start_pos_centerx_centery = helpers.find_start_pos(
			filepath_map,
			50,
			50,
			"S")
	
		filepath_sergant = os.path.join(
			os.getcwd(),
			IMAGE_DIR,
			SERGANT_FILE)
			
		filepath_shot_sound = os.path.join(
			os.getcwd(),
			SOUND_DIR,
			SERGANT_SHOT_SOUND)
			
		args = dict()
		args["filepath_sergant"] = filepath_sergant
		args["centerx"] = start_pos_centerx_centery[0]
		args["centery"] = start_pos_centerx_centery[1]
		args["arena"] = self.arena
		args["char"] = "S"
		args["explosions"] = self.explosions
		args["fog"] = self.fog
		args["radar_cooldown"] = 150
		args["shot_sound"] = filepath_shot_sound
		args["radar_text"] = self.radar_text
			
		self.sergant.sprite = SergantBrown(args)
	
	
	def prepare_criminals(self):
		
		filepath_map = os.path.join(
			os.getcwd(),
			ARENA_DIR,
			self.level_filename)	
			
		# Build list of criminals dynamically from map.
		# Build exclusion list dynamically.
		criminals = []
		filehandle = open(filepath_map)		
		contents = filehandle.read()		
		for row in contents.splitlines():
			for col in row:
				if col != "#" and col != "S" and col != " ":
					if col not in criminals:
						criminals.append(col)
		criminals.sort()

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
				
			filepath_shot_sound = os.path.join(
				os.getcwd(),
				SOUND_DIR,
				CRIMINAL_SHOT_SOUND)				
				
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
			args["shot_sound"] = filepath_shot_sound		
				
			self.criminals.add(Criminal(args))
			
	
	def run(self):

		
		self.running = True
		pygame.mouse.set_visible(False)
		
		result = dict()
		
		n_enemies = len(self.criminals)
		self.n_frames = 0
		while self.running:
		
			self.update_events()
			self.process_events()
			
			if self.running == False:
				pygame.mouse.set_visible(True)			
				if self.pause_screen() == "no":
					self.running = True
					pygame.mouse.set_visible(False)	
				self.sergant.sprite.menu_no = True
				self.sergant.sprite.button_already_down = True

			self.update_game_objects()
			
			if self.sergant.sprite is not None:
				self.sergant.sprite.menu_no = False
			
			if self.sergant.sprite == None or len(self.criminals) == 0:
				self.running = False
			
			self.fill_window_background()
			self.draw_game_objects()
			self.n_frames += 1
			self.clock.tick(FPS)
			pygame.display.update()
		
		if len(self.criminals) == 0:
			result["win"] = True
			result["shots_fired"] = self.sergant.sprite.shots_fired
			result["time"] = self.n_frames
			result["n_enemies"] = n_enemies
		else:
			result["win"] = False
		
		return result
		
		

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
				
			pygame.draw.circle(
				self.window,
				RED,
				c.laser_aim_coords[1],
				2)		
		
		if self.sergant.sprite is not None:
				
			pygame.draw.circle(
				self.window,
				GREEN,
				self.sergant.sprite.laser_aim_coords[1],
				2)	
		
		for sg in self.explosions:
			sg.draw(self.window)
			
		# Draw mouse aim.
		mouse_coords = pygame.mouse.get_pos()
		hor_line = [(mouse_coords[0]-10, mouse_coords[1]), (mouse_coords[0]+10, mouse_coords[1])]
		vert_line = [(mouse_coords[0], mouse_coords[1]-10), (mouse_coords[0], mouse_coords[1]+10)]
		pygame.draw.line(
			self.window,
			WHITE,
			hor_line[0],
			hor_line[1],
			1)
		pygame.draw.line(
			self.window,
			WHITE,
			vert_line[0],
			vert_line[1],
			1)	

		# Draw infrared meter info.
		self.window.blit(
			self.map_text.image,
			self.map_text.rect)		
		self.window.blit(
			self.radar_text.image,
			self.radar_text.rect)
			
	def pause_screen(self):

		args = dict()
		args["static_text"] = "Quit?"
		args["dynamic_text"] = ""
		args["filepath_font"] = os.path.join(
			os.getcwd(),
			FONT_DIR,
			FONT)
		args["font_size"] = 40
		args["fg_colour"] = YELLOW
		args["bg_colour"] = None
		args["centerx"] = WINDOW_WIDTH / 2
		args["centery"] = 100
		quit_text = Text(args)
		
		# Yes button.
		args = dict()
		args["static_text"] = "Yes"
		args["dynamic_text"] = ""
		args["filepath_font"] = os.path.join(
			os.getcwd(),
			FONT_DIR,
			FONT)
		args["font_size"] = 30
		args["fg_colour"] = YELLOW
		args["bg_colour"] = None
		args["centerx"] = WINDOW_WIDTH / 2
		args["centery"] = 300
		
		args2 = copy.deepcopy(args)
		args2["fg_colour"] = ORANGE
		yes_button = Button(args2, args, "yes")	

		# No button.
		args = dict()
		args["static_text"] = "No"
		args["dynamic_text"] = ""
		args["filepath_font"] = os.path.join(
			os.getcwd(),
			FONT_DIR,
			FONT)
		args["font_size"] = 30
		args["fg_colour"] = YELLOW
		args["bg_colour"] = None
		args["centerx"] = WINDOW_WIDTH / 2
		args["centery"] = 400
		
		args2 = copy.deepcopy(args)
		args2["fg_colour"] = ORANGE
		no_button = Button(args2, args, "no")	
		
		ret_value = None
		running = True
		while running:
			eventlist = pygame.event.get()
			ret_value = yes_button.update()
			if ret_value == "yes":
				running = False
				
			ret_value = no_button.update()
			if ret_value == "no":
				running = False
			
			
			self.window.fill(BLACK)
			self.window.blit(
				quit_text.image,
				quit_text.rect)
				
			self.window.blit(
				yes_button.image,
				yes_button.rect)
				
			self.window.blit(
				no_button.image,
				no_button.rect)				
			
			pygame.display.update()
			self.clock.tick(FPS)
			
		pygame.event.get()
		pygame.event.clear()
		
		return ret_value
		

main_game = MainGame()
main_game.title_screen()