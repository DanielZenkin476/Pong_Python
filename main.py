#this project uses files by CodeClear - https://github.com/clear-code-projects/5games

import random
import pygame
from Tools.scripts.dutree import display
from fontTools.merge.util import current_time
from sympy.core.random import randint ,choice
from random import randint, uniform
from pygame.sprite import Sprite
from settings import *
from sprites import *


class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.running = True
        self.FPS_target = 99
        #sprites
        self.all_sprites = pygame.sprite.Group()
        self.paddle_sprites = pygame.sprite.Group()
        self.ball_sprites = pygame.sprite.Group()
        self.player = Player((self.all_sprites,self.paddle_sprites))
        self.ball = Ball(self.all_sprites,self.paddle_sprites)
        self.enemy = Opponent((self.all_sprites,self.paddle_sprites),self.ball)
        #score
        self.score = {'player': 0,"opponent": 0,}


    def display_score(self):
        score_player = self.font.render('health: ' + str(self.player.hp), True, 'red')
        hp_rect = hp_surt.get_rect(topleft=(10, 10))
        self.screen.blit(hp_surt, hp_rect)
        pygame.draw.rect(self.screen, 'red', hp_rect.inflate(20, 15), 5, 10)




    def gameloop(self):
        while self.running:
            #dt calc
            dt = self.clock.tick(self.FPS_target) /1000
            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
            #fill screen
            self.screen.fill(COLORS['bg'])
            self.all_sprites.update(dt)



            self.all_sprites.draw(self.screen)

            pygame.display.update()
        pygame.quit()

if __name__ == '__main__':# to run only main file to avoid future messups
    game = Game()
    game.gameloop()
