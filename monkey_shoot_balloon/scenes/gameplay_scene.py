import pygame
import constants
import random

from managers.wave_manager import WaveManager
from managers.path_manager import PathManager
from decors.decor import Decor
from UI.UI_button import UIButton
from towers.elephant import Elephant
from towers.monkey import Monkey
from towers.giraffe import Giraffe
from utils.path import is_point_near_path
from projectiles.projectile import Projectile
import os

# UI 圖片路徑

class GameplayScene:
    def __init__(self, scene_manager):
        self.font = pygame.font.SysFont(None, 30)
        
        self.money = constants.INITIAL_MONEY
        self.life = constants.INITIAL_LIVES
        self.enemies = []
        self.towers = []
        self.projectiles = []
    
        self.scene_manager = scene_manager
    
        
        self.path_manager = PathManager()   
        self.path_points = self.path_manager.get() # 取得路徑座標
        self.path_manager.reset()                    # 重置路徑，讓它可以隨機生成

        self.wave_manager = WaveManager(self.path_manager) # 取得路徑物件
        self.wave_manager.start_wave(0)


        self.placing_tower_class = None         # 正在放置的塔類別
        self.placing_tower_image = None         # 其對應的圖片
        self.preview_angle = 0                  # 旋轉動畫所需

        self.icon_coin  = pygame.image.load(os.path.join(constants.UI_PATH, "coin.png")).convert_alpha()
        self.icon_heart = pygame.image.load(os.path.join(constants.UI_PATH, "heart.png")).convert_alpha()
        self.icon_wave  = pygame.image.load(os.path.join(constants.UI_PATH, "flag.png")).convert_alpha()

        size = (40, 40)
        self.icon_coin  = pygame.transform.smoothscale(self.icon_coin,  size)
        self.icon_heart = pygame.transform.smoothscale(self.icon_heart, size)
        self.icon_wave  = pygame.transform.smoothscale(self.icon_wave,  size)

        # 數字字體 (可用系統字或自訂字體)
        self.ui_font = pygame.font.Font(None, 40) 
        
        self.decor_images = self.load_decor_images()
        self.decorations = self.generate_decorations(10) 

        self.tower_buttons = []

        tower_classes = [Elephant, Monkey, Giraffe]
        start_x = 40
        for i, tower_cls in enumerate(tower_classes):
            btn = UIButton(
                x=start_x + i*140,
                y=constants.SCREEN_HEIGHT - 70,
                width=120,
                height=60,
                tower_cls=tower_cls,
                font=self.ui_font,
                on_click=self.select_tower
            )
            self.tower_buttons.append(btn)

    def spawn_projectile(self, tower_x, tower_y, enemy_x, enemy_y, tower):
        p = Projectile(tower_x, tower_y, enemy_x, enemy_y, tower)
        self.projectiles.append(p)
    
    def handle_events(self, event):

        for btn in self.tower_buttons:
            btn.handle_event(event, self.money)

        if event.type == pygame.KEYDOWN:
            # 洗掉放置塔的狀態
            self.placing_tower_class = None
            self.placing_tower_image = None
            self.preview_angle = 0

            if event.key == pygame.K_ESCAPE:
                self.scene_manager.switch_scene("menu")
            
            if event.key == pygame.K_1:
                if self.money < Elephant.PRICE:
                    return
                
                self.placing_tower_class = Elephant
                self.placing_tower_image = Elephant.IMAGE
            
            if event.key == pygame.K_2:
                if self.money < Monkey.PRICE:
                    return
                self.placing_tower_class = Monkey
                self.placing_tower_image = Monkey.IMAGE
                
            if event.key == pygame.K_3:
                if self.money < Giraffe.PRICE:
                    return
                self.placing_tower_class = Giraffe
                self.placing_tower_image = Giraffe.IMAGE

            # # 按 N 且前一波敵人已經全部消失，就開始下一波
            # if event.key == pygame.K_n and not self.wave_manager.wave_in_progress and not self.wave_manager.all_waves_done:
            #     self.wave_manager.next_wave()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 左鍵點擊：真正放置塔
            if self.placing_tower_class:
                x, y = event.pos
                
                for btn in self.tower_buttons:
                    if btn.rect.collidepoint(event.pos):
                        return  # ⛔ 點在 UI 上，不能放塔！

                if not self.can_place_tower(x, y, self.placing_tower_class):
                    return       
                
                # 放置塔
                self.money -= self.placing_tower_class.PRICE
                new_tower = self.placing_tower_class(x, y)
                self.towers.append(new_tower)
                
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

        # update projectiles
        for p in self.projectiles:
            p.update(dt)
        self.check_projectile_collisions()
        self.projectiles = [p for p in self.projectiles if p.alive]

        # update towers
        for t in self.towers:
            t.update(dt, self.enemies)
            if t.target_enemy: # 如果在更新後，冷卻完畢且有母標，就產生飛行物朝向敵人
                self.spawn_projectile(t.x, t.y, t.target_enemy.x, t.target_enemy.y, t)
                t.target_enemy = None

        # update wave manager
        self.wave_manager.update(dt, self.enemies)


        # 如果正在放置塔，則讓塔圖片旋轉
        if self.placing_tower_class:
            self.preview_angle += 90 * dt

        if self.life <= 0:
            self.scene_manager.switch_scene("lose")

        if self.wave_manager.all_waves_done:
            self.scene_manager.switch_scene("win")

    def check_projectile_collisions(self):
        """ 檢查飛行物與敵人之間的碰撞 """
        for p in self.projectiles:
            if not p.alive:
                continue
            # 可用 bounding circle, 或 rect.colliderect
            for e in self.enemies:
                if e.alive and p.alive:
                    # 簡單示範：用 rect 碰撞檢查
                    if p.rect.colliderect(e.rect):
                        # 命中
                        e.take_damage(p.damage)
                        p.hit()  # Projectile 自己標記死亡
                    if not e.alive:
                        self.money += e.reward

    def draw(self, screen):
        self.draw_background(screen) # 畫背景
        self.draw_decorations(screen) # 畫裝飾物
        self.draw_path(screen) # 畫路徑
        self.draw_objects(screen) # 畫所有物件
        self.draw_ui(screen) # 畫 UI
        self.draw_interval_ui(screen) # 畫波次間隔條
        self.draw_path_end(screen) # 畫路徑結尾的木屋
        self.draw_placing_tower(screen) # 畫放置中的塔
        
        pygame.display.flip()

    def draw_background(self, screen):
        
        top_color = (180, 220, 180)
        bottom_color = (100, 160, 100)
        height = constants.SCREEN_HEIGHT

        for y in range(height):
            ratio = y / height
            r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
            g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
            b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (constants.SCREEN_WIDTH, y))
    
    def draw_path(self, screen):
        if len(self.path_points) >= 2:
            # 陰影底線（深）
            pygame.draw.lines(screen, (40, 100, 40), False, self.path_points, 20)
            # 主體中線（草色）
            pygame.draw.lines(screen, (80, 160, 80), False, self.path_points, 14)
            # 白中線
            pygame.draw.lines(screen, (255, 255, 255), False, self.path_points, 2)

    def draw_decorations(self, screen):
        for d in self.decorations:
            d.draw(screen)
        
    def draw_objects(self, screen):
        for e in self.enemies:
            e.draw(screen)
        for t in self.towers:
            t.draw(screen)
        for p in self.projectiles:
            p.draw(screen)
        

    def draw_interval_ui(self, screen):
        """波次間隔倒數條 + 文字"""

        if self.wave_manager.wave_in_progress or self.wave_manager.all_waves_done:
            return  # 戰鬥中或已通關就不用畫

        # --- 參數 ---
        center_x = constants.SCREEN_WIDTH // 2
        base_y   = constants.SCREEN_HEIGHT - 120     # 距底 120px，可自行調
        bar_w, bar_h = 300, 20                       # 倒數條尺寸
        ratio = self.wave_manager.get_interval_ratio()
        remain = int(self.wave_manager.wave_interval - self.wave_manager.inter_wave_timer + 0.999)

        # --- 底框 ---
        pygame.draw.rect(
            screen, (70, 70, 70),
            pygame.Rect(center_x - bar_w//2, base_y, bar_w, bar_h), border_radius=6)

        # --- 進度條（橘色）---
        fill_w = int(bar_w * (1 - ratio))
        pygame.draw.rect(
            screen, (255, 165, 0),
            pygame.Rect(center_x - bar_w//2, base_y, fill_w, bar_h), border_radius=6)

        # --- 邊框 ---
        pygame.draw.rect(
            screen, (255, 255, 255),
            pygame.Rect(center_x - bar_w//2, base_y, bar_w, bar_h), 2, border_radius=6)


    def draw_ui(self, screen):
        icon_pos_x = 600

        bar_height = 80
        bar_rect = pygame.Rect(0, constants.SCREEN_HEIGHT - bar_height, constants.SCREEN_WIDTH, bar_height)
        pygame.draw.rect(screen, (60, 90, 60), bar_rect)

        for btn in self.tower_buttons:
            btn.draw(screen, self.money)

        # -------- 金錢 --------
        screen.blit(self.icon_coin, (icon_pos_x, 20))
        money_txt = self.ui_font.render(str(self.money), True, constants.BLACK)
        screen.blit(money_txt, (icon_pos_x + 60, 20))       # 圖示右側 4px

        # -------- 生命 --------
        screen.blit(self.icon_heart, (icon_pos_x, 80))
        life_txt = self.ui_font.render(str(self.life), True, constants.BLACK)
        screen.blit(life_txt, (icon_pos_x + 60, 80))

        # -------- 波次 --------
        screen.blit(self.icon_wave, (icon_pos_x, 140))
        wave_txt = self.ui_font.render(str(self.wave_manager.current_wave), True, constants.BLACK)
        screen.blit(wave_txt, (icon_pos_x + 60, 140))

    def draw_placing_tower(self, screen):
        if self.placing_tower_class: # 如果正在放置塔，class 不為 None 則繼續判斷
            range_radius = self.placing_tower_class(0,0).range_radius
            circle_color = (0, 180, 255, 80)  # 淡藍半透明

            mx, my = pygame.mouse.get_pos()
            rotated_image = pygame.transform.rotate(self.placing_tower_image, self.preview_angle)
            # 旋轉 + 半透明

            circle_surface = pygame.Surface(
            (range_radius*2, range_radius*2), pygame.SRCALPHA)
            pygame.draw.circle(
                circle_surface, circle_color, (range_radius, range_radius), range_radius)
            screen.blit(circle_surface, (mx - range_radius, my - range_radius))

            if not self.can_place_tower(mx, my, self.placing_tower_class):
                # 若近到不允許放置，就把透明度設為 20%
                rotated_image.set_alpha(50)   # 50 / 255
            
            else:
                # 否則預設為 50% 透明度
                rotated_image.set_alpha(128)

            # 將旋轉後的圖片置中在滑鼠座標
            preview_rect = rotated_image.get_rect(center=(mx, my))
            screen.blit(rotated_image, preview_rect)

    def draw_path_end(self, screen):
        # 在路徑的尾端放上 wood cabin 圖片
        if self.path_points:
            cabin_image = pygame.image.load(constants.PATH_END_IMAGE).convert_alpha()
            cabin_image = pygame.transform.scale(cabin_image, (50, 50))
            cabin_rect = cabin_image.get_rect(center=self.path_points[-1])
            screen.blit(cabin_image, cabin_rect)

    def can_place_tower(self, x, y, tower_cls):
        """回傳 True 代表可放置"""
        # 1) 路徑安全距
        if is_point_near_path(x, y, self.path_points, constants.MARGIN):
            return False

        # 2) 與其它塔不重疊
        tmp_rect = tower_cls.IMAGE.get_rect(center=(x, y))

        # 讓碰撞判定稍微寬鬆，可把 rect 縮小 2~4 px 再檢查
        tmp_rect_shrink = tmp_rect.inflate(-4, -4)

        for t in self.towers:
            if tmp_rect_shrink.colliderect(t.rect):
                return False
        return True
    
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

    def select_tower(self, tower_cls):
        self.placing_tower_class = tower_cls
        self.placing_tower_image = tower_cls.IMAGE
        self.preview_angle = 0
