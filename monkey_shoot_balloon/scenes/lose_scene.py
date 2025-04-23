# scenes/end_scene.py

import pygame
import constants
import os

class LoseScene:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.font = pygame.font.SysFont(None, 48)
        
        # Load the lose image from the Background_scene folder
        image_path = os.path.join("assets", "images", "Background_scene", "Losing_scene.png")
        try:
            self.lose_image = pygame.image.load(image_path).convert_alpha()
            # Scale the image to fit the screen
            self.lose_image = pygame.transform.scale(self.lose_image, (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        except pygame.error:
            # Fallback if image can't be loaded
            print(f"Could not load image: {image_path}")
            self.lose_image = None

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            # 例如按下任何鍵返回主選單
            self.scene_manager.reset_gameplay()
            self.scene_manager.switch_scene("menu")

    def update(self, dt):
        pass

    def draw(self, screen):
        # Display the losing scene background image
        if self.lose_image:
            # Fill the entire screen with the image
            screen.blit(self.lose_image, (0, 0))
        else:
            # Fallback to simple background and text if image isn't available
            screen.fill((150, 150, 150))
            end_text = self.font.render("You lose!!!", True, constants.BLACK)
            screen.blit(
                end_text, 
                (constants.SCREEN_WIDTH//2 - end_text.get_width()//2, 200)
            )
            
        
