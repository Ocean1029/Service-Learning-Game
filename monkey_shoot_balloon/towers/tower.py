import pygame
import math

class Tower:
    IMAGE = None
    PRICE = 0
    def __init__(self, x, y, range_radius=100, damage=1, attack_speed=1.0):
        self.x = x
        self.y = y
        
        self.range_radius = range_radius
        self.damage = damage
        self.attack_speed = attack_speed 

        self.cooldown = 0 
        self.rect = None
        self.target_enemy = None

    def update(self, dt, enemies):
        if self.cooldown > 0:
            self.cooldown -= dt

        if self.cooldown <= 0:
            self.target_enemy = self.find_target_in_range(enemies)
            if self.target_enemy is None:
                return 
            else:
                self.cooldown = 1.0 / self.attack_speed

    def find_target_in_range(self, enemies):
        """ 找到最近或最前面的敵人，也可依照你想要的策略選擇目標 """
        in_range = []
        for e in enemies:
            if e.alive:
                dist = math.hypot(e.x - self.x, e.y - self.y)
                if dist <= self.range_radius:
                    in_range.append(e)
        
        if in_range:
            return min(in_range, key=lambda e: math.hypot(e.x - self.x, e.y - self.y))
        return None


    def draw(self, screen):
        shadow_surface = pygame.Surface((self.range_radius*2, self.range_radius*2), pygame.SRCALPHA)
        pygame.draw.circle(shadow_surface, (0, 0, 0, 60), (self.range_radius, self.range_radius), 10)
        screen.blit(shadow_surface, (self.x - self.range_radius, self.y - self.range_radius))

        # 畫塔圖片
        screen.blit(self.IMAGE, self.IMAGE.get_rect(center=(self.x, self.y)))

