# enemies/red_balloon.py
from .enemy import Enemy
import pygame

class Tank4(Enemy):
    IMAGE = pygame.image.load("assets/images/enemy/principal.png")
    IMAGE = pygame.transform.scale(IMAGE, (60, 60))
    def __init__(self, path_points):
        super().__init__(path_points=path_points, health=100, speed=100, reward=500)
        # 先用圓形代替
        self.rect = self.IMAGE.get_rect()
        self.rect.center = (int(self.x), int(self.y))