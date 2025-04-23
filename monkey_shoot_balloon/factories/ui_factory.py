# factories/ui_factory.py
import os
import pygame
import constants
from UI.pause_button import PauseButton
from UI.restart_button import RestartButton
from UI.tower_UI_button import TowerUIButton
from managers.UI_manager import UIManager

class UIFactory:
    def __init__(self, tower_classes, on_tower_select):
        self.tower_classes = tower_classes
        self.on_tower_select = on_tower_select
        self._pause_button = None
        self._restart_button = None

    def _load_scaled_icon(self, filename):
        icon = pygame.image.load(os.path.join(constants.UI_PATH, filename)).convert_alpha()
        return pygame.transform.smoothscale(icon, (40, 40))

    def create_ui_manager(self):
        icon_coin  = self._load_scaled_icon("coin.png")
        icon_heart = self._load_scaled_icon("heart.png")
        icon_wave  = self._load_scaled_icon("flag.png")

        bar_width = 200
        bar_x = constants.SCREEN_WIDTH - bar_width
        start_y = 250
        btn_width = bar_width - 40
        btn_height = 80
        gap_y = 30

        tower_buttons = [
            TowerUIButton(
                x=bar_x + 20,
                y=start_y + i * (btn_height + gap_y),
                width=btn_width,
                height=btn_height,
                tower_cls=tower_cls,
                on_click=self.on_tower_select
            )
            for i, tower_cls in enumerate(self.tower_classes)
        ]

        # self._pause_button = PauseButton(x=50, y=50)
        self._restart_button = RestartButton(x=50, y=50)

        return UIManager(
            pause_button=self._pause_button,
            restart_button=self._restart_button,
            tower_buttons=tower_buttons,
            icon_coin=icon_coin,
            icon_heart=icon_heart,
            icon_wave=icon_wave,
        )
