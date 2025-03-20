# enemies/red_balloon.py
from .balloon import Balloon
import pygame

class BlueBalloon(Balloon):
    def __init__(self):
        super().__init__(health=2, speed=200)
        # 先用圓形代替
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (int(self.x), int(self.y))