
# managers/wave_manager.py
import pygame
from enemies.tank_1 import Tank1
from enemies.tank_2 import Tank2

class WaveManager:
    def __init__(self):
        self.current_wave = 0
        self.spawn_timer = 0
        self.wave_in_progress = False
        self.enemies_to_spawn = 0
        self.all_waves_done = False

        # 用定義每波敵人：[敵人類型, 數量)
        self.waves = [
            [[Tank1, 5]],
            [[Tank1, 5],[Tank2, 5]],
            [[Tank1, 10],[Tank2, 10]],
            [[Tank1, 15],[Tank2, 15]],
            [[Tank1, 20],[Tank2, 10]],
            [[Tank2, 25]],
            [[Tank1, 15],[Tank2, 20]],
            [[Tank1, 25],[Tank2, 25]],
            [[Tank1, 30],[Tank2, 30]],
            [[Tank2, 40]],
            [[Tank1, 50]]
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
        

    def update(self, dt, enemies):
        if not self.wave_in_progress:
            if(self.current_wave >= len(self.waves)-1):
                self.all_waves_done = True
            return

        self.spawn_timer += dt
        # 假設每 1 秒生成一隻敵人
        if self.spawn_timer >= 0.5 and self.spawn_list:
            balloon_class = self.spawn_list.pop(0)
            new_balloon = balloon_class()
            enemies.append(new_balloon)
            self.spawn_timer = 0

        if not self.spawn_list and all(not e.alive for e in enemies):
            self.wave_in_progress = False

    def next_wave(self):
        self.start_wave(self.current_wave + 1)
