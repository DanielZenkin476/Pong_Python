from random import randint, uniform

import pygame
from pygame.sprite import Sprite
from settings import *
from random import choice

class Player(Sprite):
    def __init__(self,groups,ball_sprites):
        super().__init__(groups)
        self.image = pygame.Surface(SIZE['paddle'],pygame.SRCALPHA)
        pygame.draw.rect(self.image,COLORS['paddle'], pygame.Rect((0,0),SIZE['paddle']),0,10)
        self.rect = self.image.get_rect(center = POS['player'])
        self.speed = SPEED['player']
        self.direction = 0# 1 for down -1 for up
        self.old_rect = self.rect.copy()

        self.hp = 3

    def coll_screen(self):
        if (self.rect.bottom >= WINDOW_HEIGHT and self.direction > 0) or (
                self.rect.top <= 0 and self.direction < 0):
            self.direction = 0

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction = (int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP]))  # x direction


    def move(self,dt):
        self.rect.y += self.direction * self.speed * dt

    def update(self,dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.coll_screen()
        self.move(dt)

class Ball(Sprite):
    def __init__(self,groups,paddle_sprites):
        super().__init__(groups)
        self.image = pygame.Surface(SIZE['ball'], pygame.SRCALPHA)# makes rect invisible
        pygame.draw.circle(self.image,COLORS['ball'],center = (SIZE['ball'][0]/2,SIZE['ball'][1]/2),radius = SIZE['ball'][0]/2)
        self.rect = self.image.get_rect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
        self.speed = SPEED['ball']
        self.direction = pygame.Vector2(choice((1,-1)),uniform(.5,.8)* choice((1,-1)))
        if self.direction: self.direction.normalize()
        self.paddle_sprites = paddle_sprites
        self.old_rect = self.rect.copy()

    def collision(self,direction):
        for paddle in self.paddle_sprites:
            if paddle.rect.colliderect(self.rect):
                if direction == 'x':
                    if self.rect.right > paddle.rect.left and self.old_rect.right <= paddle.old_rect.left:# right of ball left of paddle
                        self.rect.right = paddle.rect.left
                        self.direction.x = -self.direction.x
                    elif paddle.rect.right > self.rect.left and paddle.old_rect.right <= self.old_rect.left:# left of ball right of paddle
                        self.rect.left = paddle.rect.right
                        self.direction.x = -self.direction.x
                elif direction == 'y': #direction is y
                    if self.rect.bottom > paddle.rect.top and self.old_rect.bottom <= paddle.old_rect.top:# up for ball, down for paddle
                        self.rect.bottom = paddle.rect.top
                        self.direction.y = -self.direction.y
                    elif paddle.rect.bottom > self.rect.top and paddle.old_rect.bottom <= self.old_rect.top:# up for ball, down for paddle
                        self.rect.top = paddle.rect.bottom
                        self.direction.y = -self.direction.y


    def coll_screen(self):
        if (self.rect.bottom >= WINDOW_HEIGHT and self.direction.y > 0) or (
                self.rect.top <= 0 and self.direction.y < 0):
            self.direction.y = -self.direction.y
        if (self.rect.right >= WINDOW_WIDTH and self.direction.x > 0) or (self.rect.left <= 0 and self.direction.x < 0):
            self.direction.x =- self.direction.x

    def move(self,dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('x')
        self.rect.y += self.direction.y * self.speed * dt
        self.collision('y')


    def update(self,dt):
        self.old_rect = self.rect.copy()
        self.move(dt)
        self.coll_screen()


