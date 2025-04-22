import pygame
import constants
from utils.gray_scale import to_grayscale

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
    # 判斷是否有足夠金錢
        is_affordable = money >= self.price

        # 底色與陰影
        base_color = constants.GREEN if is_affordable else (120, 120, 120)
        shadow_color = (30, 30, 30)
        shadow_offset = 4

        # 陰影方塊（在下面一層）
        shadow_rect = self.rect.move(shadow_offset, shadow_offset)
        pygame.draw.rect(screen, shadow_color, shadow_rect, border_radius=8)

        # 主按鈕方塊
        pygame.draw.rect(screen, base_color, self.rect, border_radius=8)

        # ICON 處理
        icon_size = 40
        icon_img = pygame.transform.smoothscale(self.image, (icon_size, icon_size))

        if not is_affordable:
            icon_img = to_grayscale(icon_img)

        icon_rect = icon_img.get_rect(center=(self.rect.centerx, self.rect.top + 35))
        screen.blit(icon_img, icon_rect)

        # 價格文字
        price_text = self.font.render(f"${self.price}", True, (0, 0, 0))
        price_bg = self.font.render(f"${self.price}", True, (255, 255, 255))

        text_pos = (self.rect.left + 8, self.rect.bottom - 28)
        screen.blit(price_bg, (text_pos[0] + 1, text_pos[1] + 1))  # 略偏移作為陰影
        screen.blit(price_text, text_pos)




    def handle_event(self, event, money):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and money >= self.price:
                self.on_click(self.tower_cls)
