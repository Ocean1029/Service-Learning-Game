# enemies/red_balloon.py
from .enemy import Enemy
import pygame
class RedBalloon(Enemy):
    IMAGE = pygame.Surface((20, 20))
    IMAGE.fill((255, 0, 0))
    def __init__(self):
        super().__init__(health=1, speed=100)
        self.rect = self.IMAGE.get_rect()
        self.rect.center = (int(self.x), int(self.y))