# scenes/end_scene.py

import pygame
import constants

class EndScene:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.font = pygame.font.SysFont(None, 48)

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            # 例如按下任何鍵返回主選單
            self.scene_manager.switch_scene("menu")

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill((150, 150, 150))
        end_text = self.font.render("Congratulation!!!", True, constants.BLACK)
        info_text = self.font.render("Press any key to return to menu", True, constants.BLACK)

        screen.blit(
            end_text, 
            (constants.SCREEN_WIDTH//2 - end_text.get_width()//2, 200)
        )
        screen.blit(
            info_text,
            (constants.SCREEN_WIDTH//2 - info_text.get_width()//2, 300)
        )
        pygame.display.flip()
