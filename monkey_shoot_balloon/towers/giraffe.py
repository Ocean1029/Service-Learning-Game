from .tower import Tower
import pygame

class Giraffe(Tower):
    IMAGE = pygame.image.load("assets/images/tower/giraffe.png")
    IMAGE = pygame.transform.scale(IMAGE, (40, 40))
    PRICE = 50

    def __init__(self, x, y):
        super().__init__(x, y, range_radius=50, damage=0.3, attack_speed=3.0)
        # 先用正方形代替
        self.rect = self.IMAGE.get_rect(center=(x, y))

    def attack(self, enemy):
        # dart_monkey 可能是單體攻擊
        enemy.take_damage(self.damage)
