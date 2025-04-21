import pygame
import constants

class UIButton:
    def __init__(self, x, y, width, height, tower_cls, font, on_click):
        self.rect = pygame.Rect(x, y, width, height)
        self.tower_cls = tower_cls
        self.font = font
        self.on_click = on_click  # 回呼函式
        self.hovered = False

        self.image = tower_cls.IMAGE
        self.price = tower_cls.PRICE
        self.name = tower_cls.__name__

    def draw(self, screen, money):
        color_bg = constants.GREEN if money >= self.price else (100, 100, 100)
        pygame.draw.rect(screen, color_bg, self.rect, border_radius=8)

        # 圖示
        img = pygame.transform.smoothscale(self.image, (40, 40))
        screen.blit(img, img.get_rect(center=(self.rect.centerx, self.rect.top + 25)))

        # 價格
        price_text = self.font.render(f"${self.price}", True, (0, 0, 0))
        screen.blit(price_text, (self.rect.left + 8, self.rect.bottom - 28))

    def handle_event(self, event, money):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and money >= self.price:
                self.on_click(self.tower_cls)
