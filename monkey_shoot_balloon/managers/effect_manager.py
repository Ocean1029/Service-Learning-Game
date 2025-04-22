# effect_manager.py
import pygame

class EffectManager:
    def __init__(self):
        self.effects = []

    def add(self, effect):
        self.effects.append(effect)

    def update(self, dt):
        for e in self.effects:
            e.update(dt)
        self.effects = [e for e in self.effects if e.life > 0]

    def draw(self, screen):
        for e in self.effects:
            e.draw(screen)

    def clear(self):
        self.effects.clear()
