from .tower import Tower
import pygame
from projectiles.cannonball import Cannonball

class Parrot(Tower):
    IMAGE = pygame.image.load("assets/images/tower/parrot.png")
    IMAGE = pygame.transform.scale(IMAGE, (40, 40))
    PRICE = 140

    def __init__(self, x, y):
        super().__init__(x, y, range_radius=300, damage=0.5, attack_speed=4.0)
        self.rect = self.IMAGE.get_rect(center=(x, y))
        self.projectile_type = Cannonball