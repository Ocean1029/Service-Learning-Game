from .tower import Tower
import pygame
from projectiles.cannonball import Cannonball

class Giraffe(Tower):
    IMAGE = pygame.image.load("assets/images/tower/giraffe.png")
    IMAGE = pygame.transform.scale(IMAGE, (40, 40))
    PRICE = 60

    def __init__(self, x, y):
        super().__init__(x, y, range_radius=90, damage=0.1, attack_speed=10.0)
        self.rect = self.IMAGE.get_rect(center=(x, y))
        self.projectile_type = Cannonball