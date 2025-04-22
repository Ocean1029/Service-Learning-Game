
# scenes/menu_scene.py
import pygame
import constants

class MenuScene:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.font = pygame.font.SysFont(None, 48)

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            # 按 Esc 或 Enter 進入遊戲
            if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                # 按 Enter 進入遊戲
                self.scene_manager.switch_scene("gameplay")

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill(constants.GRAY)
        title_text = self.font.render("Menu", True, constants.BLACK)
        info_text = self.font.render("Press [Enter] to start", True, constants.BLACK)
        screen.blit(title_text, (constants.SCREEN_WIDTH//2 - title_text.get_width()//2, 200))
        screen.blit(info_text, (constants.SCREEN_WIDTH//2 - info_text.get_width()//2, 300))
