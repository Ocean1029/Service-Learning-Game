import pygame

class PauseButton:
    def __init__(self, x, y, radius=20):
        self.x = x
        self.y = y
        self.radius = radius
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        self.paused = False

    def draw(self, screen):
        # 圓形背景
        pygame.draw.circle(screen, (200, 200, 200), (self.x, self.y), self.radius)
        # 畫暫停 || 符號
        bar_w = self.radius // 4
        bar_h = self.radius
        spacing = bar_w + 2
        pygame.draw.rect(screen, (50, 50, 50), (self.x - spacing, self.y - bar_h//2, bar_w, bar_h))
        pygame.draw.rect(screen, (50, 50, 50), (self.x + spacing - bar_w, self.y - bar_h//2, bar_w, bar_h))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.toggle_pause()
    
    def toggle_pause(self):
        self.paused = not self.paused
        return self.paused
    
    def is_paused(self):
        return self.paused