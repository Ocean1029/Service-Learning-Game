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

        size = (24, 24)
        self.icon_coin  = pygame.transform.smoothscale(self.icon_coin,  size)
        self.icon_heart = pygame.transform.smoothscale(self.icon_heart, size)
        self.icon_wave  = pygame.transform.smoothscale(self.icon_wave,  size)

        # 數字字體 (可用系統字或自訂字體)
        self.ui_font = pygame.font.Font(None, 26) 
        

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

            # 按 N 且前一波敵人已經全部消失，就開始下一波
            if event.key == pygame.K_n and not self.wave_manager.wave_in_progress and not self.wave_manager.all_waves_done:
                self.wave_manager.next_wave()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 左鍵點擊：真正放置塔
            if self.placing_tower_class:
                x, y = event.pos

                if is_point_near_path(x, y, self.path_points, constants.MARGIN):
                    return
                
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
        """ 負責畫出當前場景的一切 """
        screen.fill(constants.WHITE)
        # 先畫出路線（以方便看出敵人路徑）
        if len(self.path_points) > 1:
            pygame.draw.lines(screen, (0, 128, 0), False, self.path_points, 5)
        for e in self.enemies:
            e.draw(screen)
        for t in self.towers:
            t.draw(screen)
        for p in self.projectiles:
            p.draw(screen)

        icon_pos_x = 700
        # -------- 金錢 --------
        screen.blit(self.icon_coin, (icon_pos_x, 12))
        money_txt = self.ui_font.render(str(self.money), True, constants.BLACK)
        screen.blit(money_txt, (icon_pos_x + 28, 12))       # 圖示右側 4px

        # -------- 生命 --------
        screen.blit(self.icon_heart, (icon_pos_x, 48))
        life_txt = self.ui_font.render(str(self.life), True, constants.BLACK)
        screen.blit(life_txt, (icon_pos_x + 28, 48))

        # -------- 波次 --------
        screen.blit(self.icon_wave, (icon_pos_x, 84))
        wave_txt = self.ui_font.render(str(self.wave_manager.current_wave + 1), True, constants.BLACK)
        screen.blit(wave_txt, (icon_pos_x + 28, 84))

        if self.placing_tower_class:
            mx, my = pygame.mouse.get_pos()
            rotated_image = pygame.transform.rotate(self.placing_tower_image, self.preview_angle)
            # 旋轉 + 半透明
            if is_point_near_path(mx, my, self.path_points, constants.MARGIN):
                # 若近到不允許放置，就把透明度設為 20%
                rotated_image.set_alpha(50)   # 50 / 255
            
            else:
                # 否則預設為 50% (或你想要的值)
                rotated_image.set_alpha(128)

            # 將旋轉後的圖片置中在滑鼠座標
            preview_rect = rotated_image.get_rect(center=(mx, my))
            screen.blit(rotated_image, preview_rect)

        pygame.display.flip()
