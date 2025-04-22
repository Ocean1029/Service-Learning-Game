import math
import constants
class Projectile:
    IMAGE = None

    def __init__(self, x, y, target_x, target_y, tower, effect_manager, speed=800.0):
        """
        x, y:   專案物生成位置（猴子所在位置）
        target_x, target_y:  瞄準的敵人當下位置
        speed:  飛行速度
        damage: 傷害
        """
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = tower.damage  # 傷害
        self.alive = True
        self.trail = []  # projectile 初始化時加這行
        self.effect_manager = effect_manager

        # 朝向目標的方向
        dx = target_x - x
        dy = target_y - y
        dist = max(1, math.hypot(dx, dy))
        self.vx = dx / dist * self.speed
        self.vy = dy / dist * self.speed

        self.rect = self.IMAGE.get_rect(center=(int(self.x), int(self.y)))

    def update(self, dt):
        if not self.alive:
            return
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.rect.center = (int(self.x), int(self.y))

        if (self.x < 0 or self.x > constants.SCREEN_WIDTH or
            self.y < 0 or self.y > constants.SCREEN_HEIGHT):
            self.alive = False

        self.trail.append((self.x, self.y))
        if len(self.trail) > 5:  # 最多保留 5 個點
            self.trail.pop(0)

    def draw(self, screen):
        if self.alive:
            screen.blit(self.IMAGE, self.rect)

    def hit(self):
        self.alive = False

    def calculate_angle(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        angle = math.degrees(math.atan2(dy, dx))
        return angle
