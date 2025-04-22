
# managers/wave_manager.py
from enemies.tank_1 import Tank1
from enemies.tank_2 import Tank2
from enemies.tank_3 import Tank3
import constants

class WaveManager:
    def __init__(self, path_manager):
        self.current_wave = 0
        self.spawn_timer = 0
        self.wave_in_progress = False
        self.enemies_to_spawn = 0
        self.all_waves_done = False
        self.path_points = path_manager.get()

        # 用定義每波敵人：[敵人類型, 數量)
        self.waves = [
            [],
            [[Tank1, 5]],
            [[Tank2, 3], [Tank1, 5]],
            [[Tank1, 5], [Tank2, 5], [Tank1, 5], [Tank3, 1]],
            [[Tank3, 3], [Tank1, 5], [Tank2, 5], [Tank3, 2]],
            []
        ]

        self.wave_interval     = 4.0    # 波與波的間隔秒數
        self.inter_wave_timer  = 4.0     # 倒數計時器

    def start_wave(self, wave_index):
        self.current_wave = wave_index
        
        self.spawn_list = []
        for enemy_class, count in self.waves[wave_index]:
            self.spawn_list += [enemy_class for _ in range(count)]
        self.wave_in_progress = True
        self.spawn_timer = 0
        

    def update(self, dt, enemies):
        if not self.wave_in_progress:
            # 如果所有 waves 都完成，則不再更新
            if(self.current_wave >= len(self.waves)-1):
                self.all_waves_done = True
                return

            # 如果還有波數未完成，則開始倒數
            self.inter_wave_timer += dt
            if self.inter_wave_timer >= self.wave_interval:
                self.start_wave(self.current_wave + 1)   # 自動開下一波
            return
        
        self.spawn_timer += dt
        if self.spawn_timer >= constants.ENEMY_SPAWN_RATE and self.spawn_list:
            enemy_class = self.spawn_list.pop(0)
            new_enemy = enemy_class(path_points=self.path_points)
            enemies.append(new_enemy)
            self.spawn_timer = 0

        if not self.spawn_list and all(not e.alive for e in enemies):
            self.wave_in_progress = False
            self.inter_wave_timer = 0.0     # 開始倒數


    def next_wave(self):
        self.start_wave(self.current_wave + 1)

    def get_interval_ratio(self) -> float:
        """
        回傳 0~1 之間的比值，
        0 表示剛清完波 (倒數尚未開始)，
        1 表示倒數已滿 (下一波準備啟動)。
        """
        if self.wave_in_progress or self.all_waves_done:
            return 0.0
        return min(self.inter_wave_timer / self.wave_interval, 1.0)
