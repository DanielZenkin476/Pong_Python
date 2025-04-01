#this project uses files by CodeClear - https://github.com/clear-code-projects/5games
#Implemintation of  Pong  in Python using Pygame
# game will take a few seconds to load depending on hardware
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
#base class Game will hold all objects
class Game():

    def __init__(self):
        # Game initialization
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) # width and height taken from settings file
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock() # create clock
        self.running = True # game state
        self.FPS_target = 99 # Fps target = based on screen
        #sprites
        self.all_sprites = Allsprites() # group to hold all sprites
        self.paddle_sprites = Allsprites() # group to hold paddles (player and cpu
        self.ball_sprites = Allsprites() # ball sprites group
        self.player = Player((self.all_sprites,self.paddle_sprites))
        self.ball = Ball(self.all_sprites,self.paddle_sprites)
        self.enemy = Opponent((self.all_sprites,self.paddle_sprites),self.ball)
        #score
        # try block for reading " save file "
        try:
            with open(join('saves', 'score.txt'), 'r') as score_file:
                self.score = json.load(score_file)
        except:
            self.score = {'player': 0,"opponent": 0,}
        self.font = pygame.font.Font('font/Oxanium-Bold.ttf', 100)

        self.last_hit = [0.0,0.0]
        self.hp_cooldown = 1000

    def display_score(self):
        # dunction to display current score and line seperator in center of screen

        i=100 # i used for spacing
        # draw score itself:
        for key in self.score.keys():
            score_player = self.font.render(str(self.score[key]), True, 'white')
            score_rect = score_player.get_rect(center=(WINDOW_WIDTH / 2 +i, WINDOW_HEIGHT / 2))
            self.screen.blit(score_player, score_rect)
            i =-100

        #draw line seperator in the center of field
        pygame.draw.line(self.screen, 'white', (WINDOW_WIDTH / 2, 0), (WINDOW_WIDTH / 2, WINDOW_HEIGHT), 5 )
        pygame.draw.circle(self.screen,'white', (WINDOW_WIDTH/2,WINDOW_HEIGHT/2),30 )
        pygame.draw.circle(self.screen, COLORS['bg'], (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), 15)


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
