import pygame
from .projectile import Projectile
from effects.piercer_falsh import PiercerFlash

class Piercer(Projectile):
    IMAGE = pygame.image.load("assets/images/projectile/piercer.png")
    IMAGE = pygame.transform.scale(IMAGE, (10, 10))

    def __init__(self, x, y, target_x, target_y, tower, effect_manager):
        """
        x, y:   專案物生成位置（猴子所在位置）
        target_x, target_y:  瞄準的敵人當下位置
        speed:  飛行速度
        damage: 傷害
        """
        super().__init__(x, y, target_x, target_y, tower, effect_manager, speed=1200.0)
        self.rect = self.IMAGE.get_rect(center=(x, y))
        self.aoe_range = 0
    
    def hit(self):
        super().hit()
        self.effect_manager.add(PiercerFlash(self.x, self.y))