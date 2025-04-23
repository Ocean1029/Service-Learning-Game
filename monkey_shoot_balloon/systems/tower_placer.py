import pygame
import constants
from towers.elephant import Elephant
from towers.monkey import Monkey
from towers.giraffe import Giraffe
from towers.parrot import Parrot
from utils.placement import can_place_tower

class TowerPlacer:
    def __init__(self, tower_classes):
        self.selected_class = None
        self.preview_image = None
        self.preview_angle = 0
        self.tower_classes = tower_classes
        self.key_to_tower = {
            pygame.K_1: Elephant,
            pygame.K_2: Monkey,
            pygame.K_3: Giraffe,
            pygame.K_4: Parrot,
        }


    def select(self, tower_cls):
        self.selected_class = tower_cls
        self.preview_image = tower_cls.IMAGE
        self.preview_angle = 0

    def reset(self):
        self.selected_class = None
        self.preview_image = None
        self.preview_angle = 0

    def update(self, dt):
        if self.selected_class:
            self.preview_angle += 90 * dt

    def handle_event(self, event, money, path_points, towers, ui_rects):        
        if event.type == pygame.KEYDOWN:
            self.reset()
            tower_cls = self.key_to_tower.get(event.key)
            if tower_cls and money >= tower_cls.PRICE:
                self.select(tower_cls)
        
        if event.type == pygame.MOUSEBUTTONDOWN: # 左鍵點擊：真正放置塔
            if self.selected_class:
                x, y = event.pos
                if can_place_tower(x, y, self.selected_class, path_points, towers, ui_rects):
                    tower = self.selected_class(x, y)
                    self.reset()
                    return tower
        
        return None

    def draw_preview(self, screen, path_points, towers, ui_rects):
        if self.selected_class: # 如果正在放置塔，class 不為 None 則繼續判斷
            range_radius = self.selected_class(0,0).range_radius
            circle_color = constants.LIGHT_TRANSPARENT_BLUE

            mx, my = pygame.mouse.get_pos()
            rotated_image = pygame.transform.rotate(self.preview_image, self.preview_angle)
            # 旋轉 + 半透明

            circle_surface = pygame.Surface(
            (range_radius*2, range_radius*2), pygame.SRCALPHA)
            pygame.draw.circle(
                circle_surface, circle_color, (range_radius, range_radius), range_radius)
            screen.blit(circle_surface, (mx - range_radius, my - range_radius))

            if not can_place_tower(mx, my, self.selected_class, path_points, towers, ui_rects):
                # 若近到不允許放置，就把透明度設為 20%
                rotated_image.set_alpha(50)   # 50 / 255
            else:
                # 否則預設為 50% 透明度
                rotated_image.set_alpha(128)

            # 將旋轉後的圖片置中在滑鼠座標
            preview_rect = rotated_image.get_rect(center=(mx, my))
            screen.blit(rotated_image, preview_rect)

    