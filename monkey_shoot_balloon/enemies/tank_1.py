# enemies/red_balloon.py
from .enemy import Enemy
import pygame
class Tank1(Enemy):
    IMAGE = pygame.image.load("assets/images/enemy/tank1.png")
    IMAGE = pygame.transform.scale(IMAGE, (40, 40))
    def __init__(self, path_points):
        super().__init__(path_points=path_points, health=1.5, speed=150, reward=15)
        self.rect = self.IMAGE.get_rect()
        self.rect.center = (int(self.x), int(self.y))