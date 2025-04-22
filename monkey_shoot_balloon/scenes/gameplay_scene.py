import os
import pygame
import constants
import random

from managers.wave_manager import WaveManager
from managers.path_manager import PathManager
from managers.effect_manager import EffectManager
from decors.decor import Decor
from UI.UI_button import UIButton
from towers.elephant import Elephant
from towers.monkey import Monkey
from towers.giraffe import Giraffe
from towers.parrot import Parrot
from towers.tower import Tower
from utils.path import is_point_near_path
from utils.image_scaler import blit_tiled_background
from projectiles.fireball import Fireball
from projectiles.cannonball import Cannonball


class GameplayScene:
    def __init__(self, scene_manager):
        
        tower_classes = [Elephant, Monkey, Giraffe, Parrot]
        
        self.money = constants.INITIAL_MONEY
        self.life = constants.INITIAL_LIVES
        self.enemies = []
        self.towers = []
        self.projectiles = []
    
        self.scene_manager = scene_manager
        self.path_manager = PathManager()   
        self.effect_manager = EffectManager()
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

        size = (40, 40) # 圖示大小
        self.icon_coin  = pygame.transform.smoothscale(self.icon_coin,  size)
        self.icon_heart = pygame.transform.smoothscale(self.icon_heart, size)
        self.icon_wave  = pygame.transform.smoothscale(self.icon_wave,  size)

        self.font = pygame.font.SysFont(None, 30)
        self.ui_font = pygame.font.Font(constants.UI_FONT, 40)
        
        self.decor_images = self.load_decor_images()
        self.decorations = self.generate_decorations(0) 

        self.tower_buttons = []

        
        bar_width = 200
        bar_x = constants.SCREEN_WIDTH - bar_width
        start_y = 250          # 距離頂端的起始位置
        btn_width = bar_width - 40  # 留左右 padding
        btn_height = 80
        gap_y = 30

        self.tower_buttons = []  # 清空舊的按鈕列表
        for i, tower_cls in enumerate(tower_classes):
            btn = UIButton(
                x=bar_x + 20,  # 留左右 padding
                y=start_y + i * (btn_height + gap_y),
                width=btn_width,
                height=btn_height,
                tower_cls=tower_cls,
                font=self.ui_font,
                on_click=self.select_tower
            )
            self.tower_buttons.append(btn)

        
        def load_tile(name):
            img = pygame.image.load(os.path.join(constants.TILE_PATH, name)).convert_alpha()
            img = pygame.transform.smoothscale(img, (constants.TILE_SIZE, constants.TILE_SIZE))
            return img

        # base tiles
        self.tile_images = {
            "straight_h": load_tile("road_straight_full1.png"),
            "straight_h2": load_tile("road_straight_full2.png"),
            "straight_short": load_tile("road_straight_short.png"),
            "curve": load_tile("corner_tl.png"),
            "funnel": load_tile("road_funnel.png"),
            "full": load_tile("road_full_tile.png"),
            "diagonal": load_tile("road_curve_diagonal.png")
        }

        # rotated curve variants
        self.tile_images.update({
            "curve_0": self.tile_images["curve"],
            "curve_90": pygame.transform.rotate(self.tile_images["curve"], -90),
            "curve_180": pygame.transform.rotate(self.tile_images["curve"], 180),
            "curve_270": pygame.transform.rotate(self.tile_images["curve"], 90),
        })

        # 將直線 tile 的垂直版本加入字典，並旋轉
        self.tile_images.update({
            "straight_v": pygame.transform.rotate(self.tile_images["straight_h"], 90),
            "straight_v2": pygame.transform.rotate(self.tile_images["straight_h2"], 90),
            "straight_short_v": pygame.transform.rotate(self.tile_images["straight_short"], 90),
        })

    def spawn_projectile(self, tower_x, tower_y, enemy_x, enemy_y, tower):
        p = tower.projectile_type(
            tower_x, tower_y, enemy_x, enemy_y, tower, self.effect_manager)
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

            if event.key == pygame.K_4:
                if self.money < Parrot.PRICE:
                    return
                self.placing_tower_class = Parrot
                self.placing_tower_image = Parrot.IMAGE

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

        # update effect manager
        self.effect_manager.update(dt)

        # 如果正在放置塔，則讓塔圖片旋轉
        if self.placing_tower_class:
            self.preview_angle += 90 * dt

        if self.life <= 0:
            self.scene_manager.switch_scene("lose")

        if self.wave_manager.all_waves_done:
            self.scene_manager.switch_scene("win")

    def check_projectile_collisions(self):
        """ 檢查飛行物與敵人之間的碰撞（支援 AoE） """
        for p in self.projectiles:
            if not p.alive:
                continue

            for e in self.enemies:
                if e.alive and p.alive and p.rect.colliderect(e.rect):
                    p.hit()
                    center_x, center_y = p.rect.center

                    if p.aoe_range == 0:
                        e.take_damage(p.damage)
                        if not e.alive:
                            self.money += e.reward

                    # 若為 AoE → 傷害範圍內所有敵人
                    if p.aoe_range > 0:
                        for target in self.enemies:
                            if target.alive:
                                dist_sq = (target.rect.centerx - center_x) ** 2 + (target.rect.centery - center_y) ** 2
                                if dist_sq <= p.aoe_range ** 2:
                                    target.take_damage(p.damage)
                                    if not target.alive:
                                        self.money += target.reward
                    break  # 碰撞後就不再檢查其他敵人
                                
                    

    def draw(self, screen):
        self.draw_background(screen) # 畫背景
        self.draw_decorations(screen) # 畫裝飾物
        self.draw_path_tile(screen) # 畫路徑
        self.draw_objects(screen) # 畫所有物件
        self.draw_ui(screen) # 畫 UI
        self.draw_interval_ui(screen) # 畫波次間隔條
        self.draw_path_end(screen) # 畫路徑結尾的木屋
        self.draw_placing_tower(screen) # 畫放置中的塔
        
        pygame.display.flip()

    def draw_background(self, screen):
        
        # 引入圖片 constants.BACKGROUND_IMAGE
        background_image = pygame.image.load(constants.BACKGROUND_IMAGE).convert()
        blit_tiled_background(screen, background_image)
    
    def draw_path_tile(self, screen):
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
        self.effect_manager.draw(screen)

    def draw_ui(self, screen):

        def draw_tower_sidebar(screen, tower_buttons, money, ui_font):
            bar_width = 200
            bar_x = constants.SCREEN_WIDTH - bar_width

            # 背景底色＋圓角＋陰影邊框
            bar_rect = pygame.Rect(bar_x, 0, bar_width, constants.SCREEN_HEIGHT)
            pygame.draw.rect(screen, (42, 55, 42), bar_rect, border_radius=0)  # 深綠底

            # 側邊線（亮色或立體感）
            pygame.draw.line(screen, (70, 100, 70), (bar_x, 0), (bar_x, constants.SCREEN_HEIGHT), 4)

            # 繪製按鈕
            button_y_offset = 80
            for btn in tower_buttons:
                btn.draw(screen, money)
                button_y_offset += 80  # 視 btn 大小調整

        draw_tower_sidebar(screen, self.tower_buttons, self.money, self.ui_font)

        icon_pos_x = constants.SCREEN_WIDTH - 160
        y_gap = 60

        # 金幣
        screen.blit(self.icon_coin, (icon_pos_x, 20))
        money_txt = self.ui_font.render(str(self.money), True, constants.WHITE)
        screen.blit(money_txt, (icon_pos_x + 60, 20))

        # 生命
        screen.blit(self.icon_heart, (icon_pos_x, 20 + y_gap))
        life_txt = self.ui_font.render(str(self.life), True, constants.WHITE)
        screen.blit(life_txt, (icon_pos_x + 60, 20 + y_gap))

        # 波次
        screen.blit(self.icon_wave, (icon_pos_x, 20 + 2 * y_gap))
        wave_txt = self.ui_font.render(str(self.wave_manager.current_wave), True, constants.WHITE)
        screen.blit(wave_txt, (icon_pos_x + 60, 20 + 2 * y_gap))


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

    
    def draw_path_tile(self, screen):
        def expand_path_points(waypoints, step=64):
            """ 將每對連續點之間插值成一段段固定距離的 path 點 """
            expanded = []
            for i in range(len(waypoints) - 1):
                x1, y1 = waypoints[i]
                x2, y2 = waypoints[i + 1]
                dx, dy = x2 - x1, y2 - y1
                dist = max(1, int((dx**2 + dy**2)**0.5))
                steps = dist // step
                for s in range(steps):
                    t = s / steps
                    x = int(x1 + dx * t)
                    y = int(y1 + dy * t)
                    expanded.append((x, y))
            expanded.append(waypoints[-1])
            return expanded


        def get_tile_type(prev, curr, nxt):
            """
            prev, curr, nxt: 三個點座標 (x, y)
            回傳值： "straight_h" / "straight_v" / "curve_0" / "curve_90" / "curve_180" / "curve_270"
            其中 0° 圖示是左上角的彎 (左→上)。
            """

            # 1. 先計算向量
            dx1, dy1 = curr[0] - prev[0], curr[1] - prev[1]
            dx2, dy2 = nxt[0]  - curr[0], nxt[1]  - curr[1]

            # 2. 正規化：只留下水平或垂直主方向
            def norm(dx, dy):
                if abs(dx) > abs(dy):
                    return (1, 0) if dx > 0 else (-1, 0)
                else:
                    return (0, 1) if dy > 0 else (0, -1)

            dir1, dir2 = norm(dx1, dy1), norm(dx2, dy2)

            curve_mapping = {
                # 0°: 左→上
                ((-1, 0), (0, 1)): "curve_0",
                ((0, -1), (1, 0)): "curve_0",

                # 90°: 上→右
                ((0, -1), (-1, 0)): "curve_90",
                ((1, 0), (0, 1)): "curve_90",

                # 180°: 右→下
                ((1, 0), (0, -1)): "curve_180",
                ((0, 1), (-1, 0)): "curve_180",

                # 270°: 下→左
                ((0, 1), (1, 0)): "curve_270",
                ((-1, 0), (0, -1)): "curve_270",
            }

            tile = curve_mapping.get((dir1, dir2))

            if tile:
                return tile

            # 萬一都不符合：動態回傳直線方向
            return "straight_h" if dir1[0] != 0 else "straight_v"
                
        pts = expand_path_points(self.path_points)
        if len(pts) < 2:
            return

        extended = [pts[0]] + pts + [pts[-1]] # 延長路徑，讓兩端的 tile 也能畫出來

        for i in range(1, len(extended) - 1):
            prev_pt, curr_pt, next_pt = extended[i-1], extended[i], extended[i+1]
            tile_type = get_tile_type(prev_pt, curr_pt, next_pt)
            tile_img = self.tile_images[tile_type]        
            rect = tile_img.get_rect(center=curr_pt)
            
            screen.blit(tile_img, rect)
