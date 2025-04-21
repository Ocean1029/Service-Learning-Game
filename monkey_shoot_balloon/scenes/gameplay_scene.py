import pygame
import constants

from managers.wave_manager import WaveManager
from towers.elephant import Elephant
from towers.monkey import Monkey
from towers.giraffe import Giraffe
from utils.path import get_path_points, is_point_near_path
from projectiles.projectile import Projectile
import os

UI_PATH = "assets/images/UI"
class GameplayScene:
    def __init__(self, scene_manager):
        self.font = pygame.font.SysFont(None, 30)
        
        self.money = constants.INITIAL_MONEY
        self.life = constants.INITIAL_LIVES
        self.enemies = []
        self.towers = []
        self.projectiles = []
        
        self.scene_manager = scene_manager
        self.wave_manager = WaveManager()
        self.wave_manager.start_wave(0)
        
        self.path_points = get_path_points()

        self.placing_tower_class = None         # 正在放置的塔類別
        self.placing_tower_image = None         # 其對應的圖片
        self.preview_angle = 0                  # 旋轉動畫所需

        self.icon_coin  = pygame.image.load(os.path.join(UI_PATH, "coin.png")).convert_alpha()
        self.icon_heart = pygame.image.load(os.path.join(UI_PATH, "heart.png")).convert_alpha()
        self.icon_wave  = pygame.image.load(os.path.join(UI_PATH, "flag.png")).convert_alpha()

        size = (40, 40)
        self.icon_coin  = pygame.transform.smoothscale(self.icon_coin,  size)
        self.icon_heart = pygame.transform.smoothscale(self.icon_heart, size)
        self.icon_wave  = pygame.transform.smoothscale(self.icon_wave,  size)

        # 數字字體 (可用系統字或自訂字體)
        self.ui_font = pygame.font.Font(None, 40) 
        

    def spawn_projectile(self, tower_x, tower_y, enemy_x, enemy_y, tower):
        p = Projectile(tower_x, tower_y, enemy_x, enemy_y, tower)
        self.projectiles.append(p)
    
    def handle_events(self, event):
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
        self.draw_objects(screen) # 畫所有物件
        self.draw_ui(screen) # 畫 UI
        self.draw_interval_ui(screen) # 畫波次間隔條
        self.draw_placing_tower(screen) # 畫放置中的塔
        
        pygame.display.flip()

    def draw_background(self, screen):
        
        screen.fill((150, 150, 150))

        # 畫路徑
        if len(self.path_points) > 1:
            pygame.draw.lines(screen, (0, 128, 0), False, self.path_points, 5)
        
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
        if self.placing_tower_class:
            mx, my = pygame.mouse.get_pos()
            rotated_image = pygame.transform.rotate(self.placing_tower_image, self.preview_angle)
            # 旋轉 + 半透明
            if not self.can_place_tower(mx, my, self.placing_tower_class):
                # 若近到不允許放置，就把透明度設為 20%
                rotated_image.set_alpha(50)   # 50 / 255
            
            else:
                # 否則預設為 50% 透明度
                rotated_image.set_alpha(128)

            # 將旋轉後的圖片置中在滑鼠座標
            preview_rect = rotated_image.get_rect(center=(mx, my))
            screen.blit(rotated_image, preview_rect)


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