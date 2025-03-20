from .tower import Tower
import pygame

class Elephant(Tower):
    IMAGE = pygame.image.load("assets/images/tower/elephant.png")
    # resize
    IMAGE = pygame.transform.scale(IMAGE, (40, 40))
        
    def __init__(self, x, y):
        super().__init__(x, y, range_radius=120, damage=1, attack_speed=1.0)
        # 先用正方形代替
        self.rect = self.IMAGE.get_rect(center=(x, y))

    
    def attack(self, enemy):
        # dart_monkey 可能是單體攻擊
        enemy.take_damage(self.damage)
