from random import randint, uniform

import pygame
from pygame.sprite import Sprite
from settings import *
from random import choice

# sprites file
# paddle - base class for player or CPU
class Paddle(Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.image = pygame.Surface(SIZE['paddle'], pygame.SRCALPHA)# get image for paddle - a rectangle
        pygame.draw.rect(self.image, COLORS['paddle'], pygame.Rect((0, 0), SIZE['paddle']), 0, 10) #draw paddle
        self.rect = self.image.get_rect(center=POS['player'])# set rect for paddle
        self.direction = 0  # 1 for down -1 for up
        self.old_rect = self.rect.copy()# save self as copy in old_rect
        self.hp = 3
        #shadow image
        self.shadow_image = self.image.copy()
        pygame.draw.rect(self.shadow_image, COLORS['paddle shadow'], pygame.Rect((0, 0), SIZE['paddle']), 0, 10)

    def coll_screen(self):
        # check for collision with screen
        if (self.rect.bottom >= WINDOW_HEIGHT and self.direction > 0) or (
                self.rect.top <= 0 and self.direction < 0):
            self.direction = 0

    def move(self,dt):
        # move paddle
        self.rect.y += self.direction * self.speed * dt

    def input(self):
        #get input
        keys = pygame.key.get_pressed()
        self.direction = (int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP]))  # x direction


    def update(self,dt):
        #update function
        self.old_rect = self.rect.copy()
        self.input()
        self.coll_screen()
        self.move(dt)

class Player(Paddle):
    # player class - inherits all from paddle
    def __init__(self,groups):
        super().__init__(groups)
        self.rect = self.image.get_rect(center=POS['player'])
        self.speed = SPEED['player']

class Opponent(Paddle):
    # CPU class - inherits all and overrides input with simple 2 ifs.
    def __init__(self,groups,ball):
        super().__init__(groups)
        self.rect = self.image.get_rect(center=POS['opponent'])
        self.speed = SPEED['opponent']
        self.ball = ball# the ball that is being used for the game

    def input(self):
        # input based on ball reletive location to paddle
        self.direction = 0
        if self.rect.centery > self.ball.rect.centery:
            self.direction = -1
        if self.rect.centery < self.ball.rect.centery:
            self.direction = 1

class Ball(Sprite):
    # Ball class
    def __init__(self,groups,paddle_sprites):
        # init function - first part is same as paddle - just with a ball
        super().__init__(groups)
        self.image = pygame.Surface(SIZE['ball'], pygame.SRCALPHA)
        pygame.draw.circle(self.image,COLORS['ball'],center = (SIZE['ball'][0]/2,SIZE['ball'][1]/2),radius = SIZE['ball'][0]/2)
        self.rect = self.image.get_rect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
        #shadow surface
        self.shadow_image = self.image.copy()
        pygame.draw.circle(self.shadow_image,COLORS['ball shadow'],center = (SIZE['ball'][0]/2,SIZE['ball'][1]/2),radius = SIZE['ball'][0]/2)
        # ball variables
        self.speed = 0
        self.direction = pygame.Vector2(choice((1,-1)),uniform(.5,.8)* choice((1,-1))) # direction vector - random
        if self.direction: self.direction.normalize() # if not 0 - normalize so value of vector || is 1

        self.paddle_sprites = paddle_sprites# get paddles for collisions

        self.old_rect = self.rect.copy() # save self rect in old_rect
        self.score_change = 0

        self.spawn_time = pygame.time.get_ticks()
        self.spawn_interval = 1500

    def spawn_check(self):# check if firing interval has passed., if so ball starts moving
        current_time = pygame.time.get_ticks()
        interval = current_time - self.spawn_time
        if interval > self.spawn_interval:
            self.speed = SPEED['ball']

    def ball_reset(self): # resets the ball to starting position
        self.rect.center =pygame.Vector2(WINDOW_WIDTH/2,WINDOW_HEIGHT/2)
        self.direction = pygame.Vector2(choice((1, -1)), uniform(.5, .8) * choice((1, -1)))
        if self.direction: self.direction.normalize()
        self.old_rect = self.rect.copy()
        self.speed =0
        self.spawn_time = pygame.time.get_ticks()

    def collision(self,direction):
        # function to check collisions with paddles, and adjust direction as needed
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
        # function to check collisions with screen
        if (self.rect.bottom >= WINDOW_HEIGHT and self.direction.y > 0) or (
                self.rect.top <= 0 and self.direction.y < 0):
            self.direction.y = -self.direction.y
        if (self.rect.right >= WINDOW_WIDTH and self.direction.x > 0):# -1 means point for enemy
            self.direction.x =- self.direction.x
            self.score_change = -1
        elif (self.rect.left <= 0 and self.direction.x < 0):# + 1 means point for player
            self.direction.x = - self.direction.x
            self.score_change =1
        return 0


    def move(self,dt):
        # function moves ball in X direction , checks for collisions on x direction, then the same at Y direction
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('x')
        self.rect.y += self.direction.y * self.speed * dt
        self.collision('y')

    def update(self,dt):
        # update function
        if self.speed == 0: self.spawn_check()
        self.score_change = 0
        self.old_rect = self.rect.copy()
        self.move(dt)
        self.coll_screen()



