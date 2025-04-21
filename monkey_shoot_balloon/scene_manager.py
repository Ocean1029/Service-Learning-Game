# scene_manager.py
from scenes.menu_scene import MenuScene
from scenes.gameplay_scene import GameplayScene
from scenes.win_scene import WinScene
from scenes.lose_scene import LoseScene
from utils.path import reset_path

class SceneManager:
    def __init__(self):
        self.scenes = {}
        # 初始化並記錄各個場景
        self.scenes = {
            "menu": MenuScene(self),
            "gameplay": GameplayScene(self),
            "win": WinScene(self),
            "lose": LoseScene(self)
        }
        # 預設場景
        self.current_scene = self.scenes["menu"]

    def handle_events(self, event):
        self.current_scene.handle_events(event)

    def update(self, dt):
        self.current_scene.update(dt)

    def draw(self, screen):
        self.current_scene.draw(screen)

    def switch_scene(self, scene_name):
        if scene_name in self.scenes:
            self.current_scene = self.scenes[scene_name]

    def reset_gameplay(self):
        """建立一個『全新的』GameplayScene，覆蓋舊的"""
        # Reset the path before creating a new gameplay scene
        reset_path()
        self.scenes["gameplay"] = GameplayScene(self)

