# enemies/red_balloon.py
from .enemy import Enemy
import pygame

class Tank3(Enemy):
    IMAGE = pygame.image.load("assets/images/enemy/tank3.png")
    IMAGE = pygame.transform.scale(IMAGE, (40, 40))
    def __init__(self, path_points):
        super().__init__(path_points=path_points, health=20, speed=120, reward=20)
        # 先用圓形代替
        self.rect = self.IMAGE.get_rect()
        self.rect.center = (int(self.x), int(self.y))