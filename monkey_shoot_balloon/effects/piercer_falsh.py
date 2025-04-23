import pygame
import constants

class PiercerFlash:
    def __init__(self, x, y, duration=0.15, max_radius=10):
        self.x = x
        self.y = y
        self.life = duration         # 剩餘生命時間（秒）
        self.total_duration = duration
        self.max_radius = max_radius

    def update(self, dt):
        self.life -= dt

    def draw(self, screen):
        if self.life <= 0:
            return

        progress = 1 - (self.life / self.total_duration)
        radius = int(self.max_radius * progress)
        alpha = int(255 * (1 - progress))

        surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (255,255,255 , alpha), (radius, radius), radius)
        screen.blit(surf, (self.x - radius, self.y - radius))
