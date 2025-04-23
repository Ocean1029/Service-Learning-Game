import pygame

class PauseButton:
    def __init__(self, x, y, radius=20):
        self.x = x
        self.y = y
        self.radius = radius
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        self._paused = False  # 只做視覺標記用，不主導邏輯切換

    def draw(self, screen):
        # 圓形背景
        pygame.draw.circle(screen, (200, 200, 200), (self.x, self.y), self.radius)

        # 畫「暫停 ||」或「播放 ▶」圖示
        if self._paused:
            bar_w = self.radius // 4
            bar_h = self.radius
            spacing = bar_w + 2
            pygame.draw.rect(screen, (50, 50, 50), (self.x - spacing, self.y - bar_h//2, bar_w, bar_h))
            pygame.draw.rect(screen, (50, 50, 50), (self.x + spacing - bar_w, self.y - bar_h//2, bar_w, bar_h))
        else:
            # 畫播放 ▶ 三角形
            triangle = [
                (self.x - self.radius // 3, self.y - self.radius // 2),
                (self.x - self.radius // 3, self.y + self.radius // 2),
                (self.x + self.radius // 2, self.y)
            ]
            pygame.draw.polygon(screen, (50, 50, 50), triangle)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True  # 有被點到
        return False

    def set_paused(self, value: bool):
        self._paused = value
