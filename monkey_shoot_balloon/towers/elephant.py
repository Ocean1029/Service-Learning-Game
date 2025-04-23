from .tower import Tower
import pygame
from projectiles.fireball import Fireball

class Elephant(Tower):
    IMAGE = pygame.image.load("assets/images/tower/elephant.png")
    IMAGE = pygame.transform.scale(IMAGE, (40, 40))
    PRICE = 250
    
    def __init__(self, x, y):
        super().__init__(x, y, range_radius=180, damage=1, attack_speed=1.0)
        # 先用正方形代替
        self.rect = self.IMAGE.get_rect(center=(x, y))
        self.projectile_type = Fireball

    