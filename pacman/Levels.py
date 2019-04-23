
import pygame
import sys
import random
import time
from pygame.locals import *

NUMLEVELS = 1

class Wall(pygame.sprite.Sprite):
	def __init__(self, x, y, width, height, color):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([width, height])
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.rect.left = x
		self.rect.top = y


class Food(pygame.sprite.Sprite):
	def __init__(self, x, y, width, height, color, bg_color):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([width, height])
		self.image.fill(bg_color)
		self.image.set_colorkey(bg_color)
		pygame.draw.ellipse(self.image, color, [0, 0, width, height])
		self.rect = self.image.get_rect()
		self.rect.left = x
		self.rect.top = y



class Player(pygame.sprite.Sprite):
	def __init__(self, x, y, role_image_path):
		pygame.sprite.Sprite.__init__(self)
		self.role_name = role_image_path.split('/')[-1].split('.')[0]
		self.base_image = pygame.image.load(role_image_path).convert()
		self.image = self.base_image.copy()
		self.rect = self.image.get_rect()
		self.rect.left = x
		self.rect.top = y
		self.prev_x = x
		self.prev_y = y
		self.base_speed = [30, 30]
		self.speed = [0, 0]
		self.is_move = False
		self.tracks = []
		self.tracks_loc = [0, 0]

	def changeSpeed(self, direction):
		if direction[0] < 0:
			self.image = pygame.transform.flip(self.base_image, True, False)
		elif direction[0] > 0:
			self.image = self.base_image.copy()
		elif direction[1] < 0:
			self.image = pygame.transform.rotate(self.base_image, 90)
		elif direction[1] > 0:
			self.image = pygame.transform.rotate(self.base_image, -90)
		self.speed = [direction[0] * self.base_speed[0], direction[1] * self.base_speed[1]]
		return self.speed

	def update(self, wall_sprites, gate_sprites):
		if not self.is_move:
			return False
		x_prev = self.rect.left
		y_prev = self.rect.top
		self.rect.left += self.speed[0]
		self.rect.top += self.speed[1]
		is_collide = pygame.sprite.spritecollide(self, wall_sprites, False)
		if gate_sprites is not None:
			if not is_collide:
				is_collide = pygame.sprite.spritecollide(self, gate_sprites, False)
		if is_collide:
			self.rect.left = x_prev
			self.rect.top = y_prev
			return False
		return True

	def randomDirection(self):
		return random.choice([[-0.5, 0], [0.5, 0], [0, 0.5], [0, -0.5]])



class Level1():
	def __init__(self):
		self.info = 'level1'

	def setupWalls(self, wall_color):
		self.wall_sprites = pygame.sprite.Group()
		wall_positions = [[0, 0, 6, 600], #左
						  [0, 0, 600, 6], #上
						  [0, 600, 606, 6],#下
						  [600, 0, 6, 606],#右
						  [300, 0, 6, 66],#shangzhong
						  [60, 60, 106, 6],
						  [440, 60, 106, 6],
						  [60, 120, 66, 6],
						  [90, 180, 6, 96],
						  [210, 120, 186, 6],#
						  [300, 120, 6, 66],
						  [480, 120, 66, 6],#
						  [510, 180, 6, 96],

						  [150, 180, 6, 186],#8
						  [150,270,36,6],
						  [450, 180, 6, 186],#8
						  [420,270,30,6],
						  [210, 360, 186, 6],#
						  [300,360,6,66],

						  [240, 240, 42, 6], #door
						  [324, 240, 42, 6],#door
						  [240, 240, 6, 66],#door
						  [240, 300, 126, 6],#door
						  [360, 240, 6, 66],#door
						  [0, 300, 66, 6],
						  [540, 300, 66, 6],
						  [60, 420, 66, 6],
						  [60, 360, 6, 186],
						  [480, 420, 66, 6],
						  [540, 360, 6, 186],
						  [60, 420, 156, 6],
						  [390, 420, 156, 6],
						  [120, 420, 6, 66],#
						  [480, 420, 6, 66],#
						  [210, 480, 186, 6],
						  [300, 480, 6, 66],
						  [120, 540, 126, 6],
						  [360, 540, 126, 6]]
		for wall_position in wall_positions:
			wall = Wall(*wall_position, wall_color)
			self.wall_sprites.add(wall)
		return self.wall_sprites

	def setupGate(self, gate_color):
		self.gate_sprites = pygame.sprite.Group()
		self.gate_sprites.add(Wall(282, 242, 42, 2, gate_color))
		return self.gate_sprites

	def setupPlayers(self, hero_image_path, ghost_images_path):
		self.hero_sprites = pygame.sprite.Group()
		self.ghost_sprites = pygame.sprite.Group()
		self.hero_sprites.add(Player(287, 439, hero_image_path))
		for each in ghost_images_path:
			role_name = each.split('/')[-1].split('.')[0]
			if role_name == 'Blinky':
				player = Player(287, 199, each)
				player.is_move = True
				player.tracks = [[0, -0.5, 4], [0.5, 0, 9], [0, 0.5, 11], [0.5, 0, 3], [0, 0.5, 7], [-0.5, 0, 11], [0, 0.5, 3],
								 [0.5, 0, 15], [0, -0.5, 15], [0.5, 0, 3], [0, -0.5, 11], [-0.5, 0, 3], [0, -0.5, 11], [-0.5, 0, 3],
								 [0, -0.5, 3], [-0.5, 0, 7], [0, -0.5, 3], [0.5, 0, 15], [0, 0.5, 15], [-0.5, 0, 3], [0, 0.5, 3],
								 [-0.5, 0, 3], [0, -0.5, 7], [-0.5, 0, 3], [0, 0.5, 7], [-0.5, 0, 11], [0, -0.5, 7], [0.5, 0, 5]]
				self.ghost_sprites.add(player)
			elif role_name == 'Clyde':
				player = Player(319, 259, each)
				player.is_move = True
				player.tracks = [[-1, 0, 2], [0, -0.5, 4], [0.5, 0, 5], [0, 0.5, 7], [-0.5, 0, 11], [0, -0.5, 7],
								 [-0.5, 0, 3], [0, 0.5, 7], [-0.5, 0, 7], [0, 0.5, 15], [0.5, 0, 15], [0, -0.5, 3],
								 [-0.5, 0, 11], [0, -0.5, 7], [0.5, 0, 3], [0, -0.5, 11], [0.5, 0, 9]]
				self.ghost_sprites.add(player)
			elif role_name == 'Inky':
				player = Player(255, 259, each)
				player.is_move = True
				player.tracks = [[1, 0, 2], [0, -0.5, 4], [0.5, 0, 10], [0, 0.5, 7], [0.5, 0, 3], [0, -0.5, 3],
								 [0.5, 0, 3], [0, -0.5, 15], [-0.5, 0, 15], [0, 0.5, 3], [0.5, 0, 15], [0, 0.5, 11],
								 [-0.5, 0, 3], [0, -0.5, 7], [-0.5, 0, 11], [0, 0.5, 3], [-0.5, 0, 11], [0, 0.5, 7],
								 [-0.5, 0, 3], [0, -0.5, 3], [-0.5, 0, 3], [0, -0.5, 15], [0.5, 0, 15], [0, 0.5, 3],
								 [-0.5, 0, 15], [0, 0.5, 11], [0.5, 0, 3], [0, -0.5, 11], [0.5, 0, 11], [0, 0.5, 3], [0.5, 0, 1]]
				self.ghost_sprites.add(player)
			elif role_name == 'Pinky':
				player = Player(287, 259, each)
				player.is_move = True
				player.tracks = [[0, -1, 4], [0.5, 0, 9], [0, 0.5, 11], [-0.5, 0, 23], [0, 0.5, 7], [0.5, 0, 3],
								 [0, -0.5, 3], [0.5, 0, 19], [0, 0.5, 3], [0.5, 0, 3], [0, 0.5, 3], [0.5, 0, 3],
								 [0, -0.5, 15], [-0.5, 0, 7], [0, 0.5, 3], [-0.5, 0, 19], [0, -0.5, 11], [0.5, 0, 9]]
				self.ghost_sprites.add(player)
		return self.hero_sprites, self.ghost_sprites
	
	def setupFood(self, food_color, bg_color):
		self.food_sprites = pygame.sprite.Group()
		for row in range(19):
			for col in range(19):
				if (row == 7 or row == 8) and (col == 8 or col == 9 or col == 10):
					continue
				else:
					food = Food(30*col+32, 30*row+32, 4, 4, food_color, bg_color)
					is_collide = pygame.sprite.spritecollide(food, self.wall_sprites, False)
					if is_collide:
						continue
					is_collide = pygame.sprite.spritecollide(food, self.hero_sprites, False)
					if is_collide:
						continue
					self.food_sprites.add(food)
		return self.food_sprites


