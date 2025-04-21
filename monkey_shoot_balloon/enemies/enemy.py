class Enemy:
    IMAGE = None
    def __init__(self, path_points, health=1, speed=60, reward=10):
        self.health = health
        self.speed = speed
        self.reward = reward

        self.path = path_points
        self.current_path_index = 0
        self.x, self.y = self.path[0]

        self.alive = True
        self.rect = None # 給子類別實作

        self.reached_end = False

    def update(self, dt):
        # 如果已死亡則不再更新
        if not self.alive:
            return

        # 取得路徑的下一個目標點
        if self.current_path_index < len(self.path):
            target_x, target_y = self.path[self.current_path_index]
            dx = target_x - self.x
            dy = target_y - self.y

            dist = (dx**2 + dy**2)**0.5
            if dist != 0:
                # 移動方向單位向量
                dir_x = dx / dist
                dir_y = dy / dist
                # 移動
                move_dist = self.speed * dt
                self.x += dir_x * move_dist
                self.y += dir_y * move_dist

                # 更新碰撞矩形
                if self.rect:
                    self.rect.center = (int(self.x), int(self.y))

                # 檢查是否抵達下一個路徑點
                if dist < move_dist:
                    self.current_path_index += 1
            else:
                self.current_path_index += 1
        else:
            self.reached_end = True
            self.alive = False

    def draw(self, screen):
        if self.alive and self.IMAGE and self.rect:
            screen.blit(self.IMAGE, self.rect)

    def take_damage(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.alive = False
