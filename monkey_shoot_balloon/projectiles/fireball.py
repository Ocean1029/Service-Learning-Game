import pygame
from .projectile import Projectile
from effects.fireball_falsh import FireballFlash



class Fireball(Projectile):
    IMAGE = pygame.image.load("assets/images/projectile/fireball.png")

    orig_width = IMAGE.get_width()
    orig_height = IMAGE.get_height()

    new_width = 30
    new_height = int(orig_height * (new_width / orig_width))  # 等比例縮放
    
    IMAGE = pygame.transform.scale(IMAGE, (new_width, new_height))
    
    def __init__(self, x, y, target_x, target_y, tower, effect_manager):
        """
        x, y:   專案物生成位置（猴子所在位置）
        target_x, target_y:  瞄準的敵人當下位置
        speed:  飛行速度
        damage: 傷害
        """
        super().__init__(x, y, target_x, target_y, tower, effect_manager, speed=300.0)
        # 將照片的方向調整為朝向目標
        self.angle = self.calculate_angle(target_x, target_y)
        self.image = pygame.transform.rotate(self.IMAGE, self.angle)
        self.rect = self.image.get_rect(center=(x, y))
        self.aoe_range = 80

    def draw(self, screen):
        # 先繼承父類的draw方法
        super().draw(screen)
        for i, (tx, ty) in enumerate(self.trail):
            alpha = int(255 * (i + 1) / len(self.trail))
            trail_surf = pygame.Surface((6, 6), pygame.SRCALPHA)
            pygame.draw.circle(trail_surf, (255, 100, 0, alpha), (3, 3), 3)
            screen.blit(trail_surf, (tx, ty))

    def hit(self):
        super().hit()
        self.effect_manager.add(FireballFlash(self.x, self.y))