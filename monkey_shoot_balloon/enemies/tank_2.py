# enemies/red_balloon.py
from .enemy import Enemy
import pygame

class Tank2(Enemy):
    IMAGE = pygame.image.load("assets/images/enemy/tank2.png")
    IMAGE = pygame.transform.scale(IMAGE, (40, 40))
    def __init__(self, path_points):
        super().__init__(path_points=path_points, health=7, speed=100, reward=25)
        # 先用圓形代替
        self.rect = self.IMAGE.get_rect()
        self.rect.center = (int(self.x), int(self.y))