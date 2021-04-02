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