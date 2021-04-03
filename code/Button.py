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
