from .tower import Tower
import pygame
from projectiles.cannonball import Cannonball
class Monkey(Tower):
    IMAGE = pygame.image.load("assets/images/tower/monkey.png")
    IMAGE = pygame.transform.scale(IMAGE, (40, 40))
    PRICE = 100
    
    def __init__(self, x, y):
        super().__init__(x, y, range_radius=150, damage=0.2, attack_speed=5.0)
        # 先用正方形代替
        self.rect = self.IMAGE.get_rect(center=(x, y))
        self.projectile_type = Cannonball


