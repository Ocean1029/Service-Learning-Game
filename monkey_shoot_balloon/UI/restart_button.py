# UI/restart_button.py
import pygame

class RestartButton:
    def __init__(self, x, y, radius=20):
        self.x = x
        self.y = y
        self.radius = radius
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)

    def draw(self, screen):
        asset = pygame.image.load("assets/images/ui/restart.png")
        asset = pygame.transform.scale(asset, (self.radius * 2, self.radius * 2))
        screen.blit(asset, (self.x - self.radius, self.y - self.radius))

        # Draw a circle around the image
        # pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius+5, 1)
        

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

