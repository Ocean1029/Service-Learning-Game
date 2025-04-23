from .tower import Tower
import pygame
from projectiles.piercer import Piercer

class Parrot(Tower):
    IMAGE = pygame.image.load("assets/images/tower/parrot.png")
    IMAGE = pygame.transform.scale(IMAGE, (40, 40))
    PRICE = 160

    def __init__(self, x, y):
        super().__init__(x, y, range_radius=340, damage=7.0, attack_speed=0.3)
        self.rect = self.IMAGE.get_rect(center=(x, y))
        self.projectile_type = Piercer