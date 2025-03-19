# game.py
import pygame
import constants
from scene_manager import SceneManager

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        pygame.display.set_caption("Monkey Shoot Balloon - Basic Demo")
        self.clock = pygame.time.Clock()
        self.running = True

        self.scene_manager = SceneManager()

    def run(self):
        while self.running:
            dt = self.clock.tick(constants.FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                self.scene_manager.handle_events(event)

    def update(self, dt):
        self.scene_manager.update(dt)

    def draw(self):
        self.scene_manager.draw(self.screen)
        pygame.display.flip()
