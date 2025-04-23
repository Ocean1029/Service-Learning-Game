import os
import random
import pygame
import constants

from utils.path import is_point_near_path
from decors.decor import Decor

# 不推薦使用這個 function

class DecorManager:
    def __init__(self):
        self.decor_images = self.load_decor_images(self)
        self.decorations = []

    def update(self, dt):
        for e in self.effects:
            e.update(dt)
        self.effects = [e for e in self.effects if e.life > 0]

    def draw(self, screen):
        for e in self.effects:
            e.draw(screen)

    def load_decor_images(self):
            decor_imgs = []
            for filename in os.listdir(constants.DECOR_PATH):
                if filename.endswith(".png"):
                    img = pygame.image.load(os.path.join(constants.DECOR_PATH, filename)).convert_alpha()
                    img = pygame.transform.smoothscale(img, (40, 40))
                    decor_imgs.append(img)
            return decor_imgs
    
    def generate_decorations(self, count):
        decorations = []
        tries = 0

        while len(decorations) < count and tries < count * 5:
            tries += 1
            x = random.randint(40, constants.SCREEN_WIDTH - 40)
            y = random.randint(40, constants.SCREEN_HEIGHT - 40)

            # 避開路徑
            if is_point_near_path(x, y, self.path_points, margin=constants.MARGIN):
                continue
            
            # 避開右上角 UI 區域
            if x > constants.SCREEN_WIDTH - 150 and y < 200:
                continue

            image = random.choice(self.decor_images)
            image.set_alpha(128)
            
            decorations.append(Decor(image, x, y))
        return decorations