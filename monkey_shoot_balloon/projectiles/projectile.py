import pygame
import math

class Projectile:
    IMAGE = pygame.Surface((7, 7))
    IMAGE.fill((50,50,50))

    def __init__(self, x, y, target_x, target_y, tower):
        """
        x, y:   專案物生成位置（猴子所在位置）
        target_x, target_y:  瞄準的敵人當下位置
        speed:  飛行速度
        damage: 傷害
        """
        self.x = x
        self.y = y
        self.speed = 600.0  # 飛行速度
        self.damage = tower.damage  # 傷害
        self.alive = True

        # 朝向目標的方向
        dx = target_x - x
        dy = target_y - y
        dist = math.hypot(dx, dy)
        if dist == 0:
            dist = 1
        self.vx = dx / dist * self.speed
        self.vy = dy / dist * self.speed

        self.rect = self.IMAGE.get_rect(center=(int(self.x), int(self.y)))

    def update(self, dt):
        if not self.alive:
            return
        # 根據 vx, vy 移動
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.rect.center = (int(self.x), int(self.y))

        # 如果飛出螢幕，也可以將它標記為死亡（避免浪費記憶體）
        # 假設螢幕大小 800 x 600
        if (self.rect.right < 0 or self.rect.left > 800 or 
            self.rect.bottom < 0 or self.rect.top > 600):
            self.alive = False

    def draw(self, screen):
        if self.alive:
            screen.blit(self.IMAGE, self.rect)

    def hit(self):
        self.alive = False
