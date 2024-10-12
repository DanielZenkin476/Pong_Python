import pygame

from settings import *
from sprites import Player


class Allsprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()

    def draw(self):
        for sprite in self:# draw shadow

            for i in range(1,6):
                 self.screen.blit(sprite.shadow_image,sprite.rect.topleft+ pygame.Vector2((i,i)))
        for sprite in self:# draw object
            self.screen.blit(sprite.image,sprite.rect)
