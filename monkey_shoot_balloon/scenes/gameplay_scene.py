import os
import pygame
import constants

from managers.wave_manager import WaveManager
from managers.path_manager import PathManager
from managers.effect_manager import EffectManager
from factories.ui_factory import UIFactory

from towers.elephant import Elephant
from towers.monkey import Monkey
from towers.giraffe import Giraffe
from towers.parrot import Parrot

from utils.image_scaler import blit_tiled_background
from systems.tower_placer import TowerPlacer
class GameplayScene:
    def __init__(self, scene_manager):
        
        self.tower_classes = [Elephant, Monkey, Giraffe, Parrot]
        self.font = pygame.font.SysFont(None, 30)
        self.ui_font = pygame.font.Font(constants.UI_FONT, 40)

        self.money = constants.INITIAL_MONEY
        self.life = constants.INITIAL_LIVES
        self.enemies = []
        self.towers = []
        self.projectiles = []

        self.tower_placer = TowerPlacer(self.tower_classes)
        self.scene_manager = scene_manager
        self.path_manager = PathManager()   
        self.effect_manager = EffectManager()
        self.path_points = self.path_manager.get() # 取得路徑座標
        self.path_manager.reset()                    # 重置路徑，讓它可以隨機生成

        self.wave_manager = WaveManager(self.path_manager) # 取得路徑物件
        self.wave_manager.start_wave(0)
        self.ui_manager = UIFactory(
            self.tower_classes, self.ui_font, self.tower_placer.select).create_ui_manager()
        self.pause_button = self.ui_manager.pause_button
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
        self.ui_manager.handle_event(event, self.money)
        
        tower = self.tower_placer.handle_event(
            event, self.money, self.path_points, self.towers, self.ui_manager.get_ui_rects())
        if tower:
            self.towers.append(tower)
            self.money -= tower.PRICE

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.pause_button.toggle_pause()
            # # 按 N 且前一波敵人已經全部消失，就開始下一波
            # if event.key == pygame.K_n and not self.wave_manager.wave_in_progress and not self.wave_manager.all_waves_done:
            #     self.wave_manager.next_wave()

        if self.pause_button.is_paused():
            self.scene_manager.switch_scene("menu")
            self.pause_button.toggle_pause() # 切換回遊戲時，恢復遊戲狀態

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

        
    def draw_objects(self, screen):
        for e in self.enemies:
            e.draw(screen)
        for t in self.towers:
            t.draw(screen)
        for p in self.projectiles:
            p.draw(screen)
        self.effect_manager.draw(screen)

    def draw_ui(self, screen):
        self.ui_manager.draw(screen, self.money, self.life, self.wave_manager.current_wave)

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
        self.tower_placer.draw_preview(screen, self.path_points, self.towers, self.ui_manager.get_ui_rects())

    def draw_path_end(self, screen):
        # 在路徑的尾端放上 wood cabin 圖片
        if self.path_points:
            cabin_image = pygame.image.load(constants.PATH_END_IMAGE).convert_alpha()
            cabin_image = pygame.transform.scale(cabin_image, (50, 50))
            cabin_rect = cabin_image.get_rect(center=self.path_points[-1])
            screen.blit(cabin_image, cabin_rect)
    
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
