
# managers/wave_manager.py
import pygame
from enemies.red_balloon import RedBalloon

class WaveManager:
    def __init__(self):
        self.current_wave = 0
        self.spawn_timer = 0
        self.wave_in_progress = False
        self.enemies_to_spawn = 0

        # 先用一個簡易清單定義每波敵人： (氣球類型, 數量)
        self.waves = [
            [(RedBalloon, 5)],
            [(RedBalloon, 10)],
        ]

    def start_wave(self, wave_index):
        if wave_index < len(self.waves):
            self.current_wave = wave_index
            # 計算本波總需生成的敵人總數
            self.spawn_list = []
            for balloon_class, count in self.waves[wave_index]:
                self.spawn_list += [balloon_class for _ in range(count)]
            self.wave_in_progress = True
            self.spawn_timer = 0
        else:
            self.wave_in_progress = False

    def update(self, dt, enemies):
        if not self.wave_in_progress:
            return

        self.spawn_timer += dt
        # 假設每 1 秒生成一隻敵人
        if self.spawn_timer >= 1.0 and self.spawn_list:
            balloon_class = self.spawn_list.pop(0)
            new_balloon = balloon_class()
            enemies.append(new_balloon)
            self.spawn_timer = 0

        # 如果清單空了且場上敵人都被清除，表示這波結束
        if not self.spawn_list and all(not e.alive for e in enemies):
            self.wave_in_progress = False

    def next_wave(self):
        self.start_wave(self.current_wave + 1)
