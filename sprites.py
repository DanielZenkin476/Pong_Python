from random import randint

import pygame
from pygame.sprite import Sprite
from settings import *

class Player(Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.image = pygame.Surface(SIZE['paddle'])
        pygame.surface.Surface.fill(self.image,COLORS['paddle'])
        self.rect = self.image.get_rect(center = POS['player'])
        self.speed = SPEED['player']
        self.direction = 0# 1 for down -1 for up
        self.hp = 3

    def coll_screen(self):
        if (self.rect.bottom > WINDOW_HEIGHT and self.direction > 0) or (
                self.rect.top < 0 and self.direction < 0):
            self.direction = 0

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction = (int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP]))  # x direction

    def move(self,dt):
        self.coll_screen()
        self.rect.y += self.direction * self.speed * dt

    def update(self,dt):
        self.input()
        self.move(dt)

class Ball(Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.image = pygame.Surface(SIZE['ball'])
        pygame.surface.Surface.fill(self.image,COLORS['ball'])
        self.rect = self.image.get_rect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
        self.speed = SPEED['ball']
        self.direction = pygame.Vector2(1,1)
        if self.direction: self.direction.normalize()

    def coll_screen(self):
        if (self.rect.bottom > WINDOW_HEIGHT and self.direction.y > 0) or (
                self.rect.top < 0 and self.direction.y < 0):
            self.direction.y = -self.direction.y
        if (self.rect.right > WINDOW_WIDTH and self.direction.x > 0) or (self.rect.left < 0 and self.direction.x < 0):
            self.direction.x =- self.direction.x


    def update(self,dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.coll_screen()
        self.rect.y += self.direction.y * self.speed * dt
        self.coll_screen()

