import pygame
import constants

from managers.wave_manager import WaveManager
from towers.dart_monkey import DartMonkey
from enemies.balloon import Balloon
from utils.path import get_path_points

class GameplayScene:
    def __init__(self, scene_manager):
        self.font = pygame.font.SysFont(None, 30)
        
        self.money = 100000
        self.life = 10
        self.enemies = []
        self.towers = []
        
        self.scene_manager = scene_manager
        self.wave_manager = WaveManager()
        self.wave_manager.start_wave(0)
        
        self.path_points = get_path_points()

        self.placing_tower_class = None         # 例如 DartMonkey
        self.placing_tower_image = None         # 其對應的圖片
        self.preview_angle = 0                  # 旋轉動畫所需
        self.tower_cost = 100                   # 假設固定價格，亦可依照塔類別動態決定

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.scene_manager.switch_scene("menu")

            # 按 1：開始放置 DartMonkey
            if event.key == pygame.K_1:
                self.placing_tower_class = DartMonkey
                self.placing_tower_image = DartMonkey.IMAGE

            # 按 N 且前一波敵人已經全部消失，就開始下一波
            if event.key == pygame.K_n and not self.wave_manager.wave_in_progress and not self.wave_manager.all_waves_done:
                self.wave_manager.next_wave()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 左鍵點擊：真正放置塔
            if event.button == 1 and self.placing_tower_class:
                x, y = event.pos
                if self.money >= self.tower_cost:
                    new_tower = self.placing_tower_class(x, y)
                    self.towers.append(new_tower)
                    self.money -= self.tower_cost

                self.placing_tower_class = None
                self.placing_tower_image = None
                self.preview_angle = 0

    def update(self, dt):
        """ 每個 frame 進行遊戲狀態更新 """

        # update enemies
        for e in self.enemies:
            e.update(dt)
            if e.reached_end:
                self.life -= 1
        self.enemies = [e for e in self.enemies if e.alive]

        # update towers
        for t in self.towers:
            t.update(dt, self.enemies)

        # update wave manager
        self.wave_manager.update(dt, self.enemies)

        # 如果正在放置塔，則讓塔圖片旋轉
        if self.placing_tower_class:
            self.preview_angle += 90 * dt

        # 檢查是否遊戲結束

        if self.life <= 0:
            self.scene_manager.switch_scene("lose")

        if self.wave_manager.all_waves_done:
            self.scene_manager.switch_scene("win")

    def draw(self, screen):
        """ 負責畫出當前場景的一切 """
        screen.fill(constants.WHITE)
        # 先畫出路線（以方便看出敵人路徑）
        if len(self.path_points) > 1:
            pygame.draw.lines(screen, (0, 128, 0), False, self.path_points, 5)
        for e in self.enemies:
            e.draw(screen)
        for t in self.towers:
            t.draw(screen)

        wave_text = self.font.render(f"Waves: {self.wave_manager.current_wave + 1}", True, constants.BLACK)
        money_text = self.font.render(f"Money: {self.money}", True, constants.BLACK)
        life_text = self.font.render(f"Life: {self.life}", True, constants.BLACK)
        info_text = self.font.render("[1] Place DartMonkey   [N] Next Round [ESC] Back", True, constants.BLACK)

        screen.blit(wave_text, (300, 10))
        screen.blit(money_text, (300, 40))
        screen.blit(life_text, (300, 70))
        screen.blit(info_text, (300, 100))

        if self.placing_tower_class:
            mx, my = pygame.mouse.get_pos()
            
            # 旋轉 + 半透明
            rotated_image = pygame.transform.rotate(self.placing_tower_image, self.preview_angle)
            rotated_image.set_alpha(150)

            # 將旋轉後的圖片置中在滑鼠座標
            preview_rect = rotated_image.get_rect(center=(mx, my))
            screen.blit(rotated_image, preview_rect)

        pygame.display.flip()
