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
import json
from groups import *
from os.path import join

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.running = True
        self.FPS_target = 99
        #sprites
        self.all_sprites = Allsprites()
        self.paddle_sprites = Allsprites()
        self.ball_sprites = Allsprites()
        self.player = Player((self.all_sprites,self.paddle_sprites))
        self.ball = Ball(self.all_sprites,self.paddle_sprites)
        self.enemy = Opponent((self.all_sprites,self.paddle_sprites),self.ball)



        #score
        try:
            with open(join('saves', 'score.txt'), 'r') as score_file:
                self.score = json.load(score_file)
        except:
            self.score = {'player': 0,"opponent": 0,}
        self.font = pygame.font.Font('font/Oxanium-Bold.ttf', 100)

        self.last_hit = [0.0,0.0]
        self.hp_cooldown = 1000

    def display_score(self):
        i=100
        for key in self.score.keys():
            score_player = self.font.render(str(self.score[key]), True, 'white')
            score_rect = score_player.get_rect(center=(WINDOW_WIDTH / 2 +i, WINDOW_HEIGHT / 2))
            self.screen.blit(score_player, score_rect)
            i =-100

        #line seperator
        pygame.draw.line(self.screen, 'white', (WINDOW_WIDTH / 2, 0), (WINDOW_WIDTH / 2, WINDOW_HEIGHT), 5 )
        pygame.draw.circle(self.screen,'white', (WINDOW_WIDTH/2,WINDOW_HEIGHT/2),30 )
        pygame.draw.circle(self.screen, COLORS['bg'], (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), 15)
        lst = [1,2,3,4]
        lst.pop(2)

    def update_score(self):
        score_change = self.ball.score_change
        if score_change == 1:
            if self.check_hp(0):
                self.score['player'] +=  1
                self.ball.ball_reset()
        if score_change == -1:
            if self.check_hp(1):
                self.score['opponent'] +=  1
                self.ball.ball_reset()

    def check_hp(self,i):
        cur_time = pygame.time.get_ticks()
        interval = cur_time - self.last_hit[i]
        if interval > self.hp_cooldown:
            self.last_hit[i]= cur_time
            return True
        else:
            return False

    def gameloop(self):
        while self.running:
            #dt calc
            dt = self.clock.tick(self.FPS_target) /1000
            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    with open(join('saves','score.txt'),'w') as score_file:
                        json.dump(self.score,score_file)
                    pygame.quit()
            #fill screen
            self.screen.fill(COLORS['bg'])

            self.all_sprites.update(dt)
            self.update_score()

            self.display_score()
            self.all_sprites.draw()

            pygame.display.update()
        pygame.quit()

if __name__ == '__main__':# to run only main file to avoid future messups
    game = Game()
    game.gameloop()
