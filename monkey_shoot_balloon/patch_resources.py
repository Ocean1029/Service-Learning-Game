# patch_resources.py
import sys, os, pygame

def resource_path(relative_path):
    """無論開發或打包都能正確定位資源"""
    try:
        base = sys._MEIPASS  # PyInstaller 解壓後的臨時資料夾
    except AttributeError:
        base = os.path.abspath(".")
    return os.path.join(base, relative_path)

# 把原本的 load/sound/musci.load 先存起來
_original_image_load     = pygame.image.load
_original_mixer_sound    = pygame.mixer.Sound
_original_music_load     = pygame.mixer.music.load

# 全局覆寫
pygame.image.load        = lambda fn: _original_image_load(resource_path(fn))
pygame.mixer.Sound       = lambda fn: _original_mixer_sound(resource_path(fn))
pygame.mixer.music.load  = lambda fn: _original_music_load(resource_path(fn))
