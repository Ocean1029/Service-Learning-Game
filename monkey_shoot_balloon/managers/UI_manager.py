import pygame
import constants

class UIManager:
    def __init__(self, pause_button, tower_buttons, icon_coin, icon_heart, icon_wave, ui_font):
        self.pause_button = pause_button
        self.tower_buttons = tower_buttons
        self.icon_coin = icon_coin
        self.icon_heart = icon_heart
        self.icon_wave = icon_wave
        self.ui_font = ui_font

    def handle_event(self, event, money):
        self.pause_button.handle_event(event)
        for btn in self.tower_buttons:
            btn.handle_event(event, money)

    def is_paused(self):
        return self.pause_button.is_paused()

    def draw(self, screen, money, life, wave):
        self.draw_tower_sidebar(screen, self.tower_buttons, money)
        self.pause_button.draw(screen)

        icon_pos_x = constants.SCREEN_WIDTH - 160
        y_gap = 60

        # 金幣
        screen.blit(self.icon_coin, (icon_pos_x, 20))
        money_txt = self.ui_font.render(str(money), True, constants.WHITE)
        screen.blit(money_txt, (icon_pos_x + 60, 20))

        # 生命
        screen.blit(self.icon_heart, (icon_pos_x, 20 + y_gap))
        life_txt = self.ui_font.render(str(life), True, constants.WHITE)
        screen.blit(life_txt, (icon_pos_x + 60, 20 + y_gap))

        # 波次
        screen.blit(self.icon_wave, (icon_pos_x, 20 + 2 * y_gap))
        wave_txt = self.ui_font.render(str(wave), True, constants.WHITE)
        screen.blit(wave_txt, (icon_pos_x + 60, 20 + 2 * y_gap))

    def draw_tower_sidebar(self, screen, tower_buttons, money):
        bar_width = 200
        bar_x = constants.SCREEN_WIDTH - bar_width

        # 背景底色＋圓角＋陰影邊框
        bar_rect = pygame.Rect(bar_x, 0, bar_width, constants.SCREEN_HEIGHT)
        pygame.draw.rect(screen, (42, 55, 42), bar_rect, border_radius=0)  # 深綠底

        # 側邊線（亮色或立體感）
        pygame.draw.line(screen, (70, 100, 70), (bar_x, 0), (bar_x, constants.SCREEN_HEIGHT), 4)

        # 繪製按鈕
        for btn in tower_buttons:
            btn.draw(screen, money)

    def get_ui_rects(self):
        # 獲取所有 UI 元件的矩形區域，並包含 sidebar 的矩形
        ui_rects = [self.pause_button.rect]
        ui_rects.extend(btn.rect for btn in self.tower_buttons)
        ui_rects.append(pygame.Rect(constants.SCREEN_WIDTH - 200, 0, 200, constants.SCREEN_HEIGHT))
        return ui_rects

