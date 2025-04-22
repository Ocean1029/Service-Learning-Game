# path_manager.py
import random, constants

class PathManager:
    def __init__(self):
        self.path_points = None          # 目前這局使用的座標列表
        self.mode = constants.PATH_MODE

    # ---------- 入口 ----------
    def get(self):
        """回傳本局路徑，若尚未生成就生成一次"""
        if self.path_points is None:
            if self.mode == "static":
                self.path_points = [list(p) for p in constants.STATIC_PATH]
            else:
                self.path_points = self.generate_random_path()
        return self.path_points

    def reset(self):
        self.path_points = None

    # ---------- 內部 ----------
    def generate_random_path(self):
        """Generate a random path for enemies to follow"""
        screen_width = 800
        screen_height = 600
        
        # Start position is always at the top of the screen
        start_x = random.randint(30, 150)
        path = [[start_x, 0]]
        
        # Number of waypoints (between 7 and 12)
        num_points = random.randint(7, 12)
        
        current_x, current_y = start_x, 0
        
        # Generate waypoints
        for i in range(num_points):
            # Decide direction: horizontal or vertical movement
            if i % 2 == 0:  # Even indices: move vertically
                # Don't go beyond the bottom of the screen
                max_y = min(current_y + 200, screen_height - 50)
                
                # Check if we have a valid range for random selection
                if current_y + 50 >= max_y:
                    # If no valid range, just move to the maximum allowed position
                    new_y = max_y
                else:
                    new_y = random.randint(current_y + 50, max_y)
                    
                path.append([current_x, new_y])
                current_y = new_y
            else:  # Odd indices: move horizontally
                # Choose left or right movement, but ensure we stay within bounds
                if current_x < screen_width / 2:
                    # More likely to move right if in left half
                    direction = random.choices([-1, 1], weights=[30, 70])[0]
                else:
                    # More likely to move left if in right half
                    direction = random.choices([-1, 1], weights=[70, 30])[0]
                
                distance = random.randint(80, 250)
                
                # Make sure we stay within screen bounds
                if direction == 1:  # moving right
                    new_x = min(current_x + distance, screen_width - 30)
                else:  # moving left
                    new_x = max(current_x - distance, 30)
                
                path.append([new_x, current_y])
                current_x = new_x
        
        # Ensure the path ends at the bottom of the screen
        # If the last movement was horizontal, add a final vertical movement
        if path[-1][1] < screen_height - 50:
            path.append([path[-1][0], screen_height])
        
        return path