# scenes/menu_scene.py
import pygame
import constants
import os

class MenuScene:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.font = pygame.font.SysFont(None, 48)
        
        # Load the menu image from the Background_scene folder
        image_path = os.path.join("assets", "images", "Background_scene", "Menu_scene.png")
        try:
            self.menu_image = pygame.image.load(image_path).convert_alpha()
            # Scale the image to fit the screen
            self.menu_image = pygame.transform.scale(self.menu_image, (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        except pygame.error:
            # Fallback if image can't be loaded
            print(f"Could not load image: {image_path}")
            self.menu_image = None

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            # 按 Esc 或 Enter 進入遊戲
            if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                # 按 Enter 進入遊戲
                self.scene_manager.switch_scene("gameplay")

    def update(self, dt):
        pass

    def draw(self, screen):
        # Display the menu scene background image
        if self.menu_image:
            # Fill the entire screen with the image
            screen.blit(self.menu_image, (0, 0))
        else:
            # Fallback to simple background and text if image isn't available
            screen.fill(constants.GRAY)
            title_text = self.font.render("Menu", True, constants.BLACK)
            info_text = self.font.render("Press [Enter] to start", True, constants.BLACK)
            screen.blit(title_text, (constants.SCREEN_WIDTH//2 - title_text.get_width()//2, 200))
            screen.blit(info_text, (constants.SCREEN_WIDTH//2 - info_text.get_width()//2, 300))
        
        pygame.display.flip()
