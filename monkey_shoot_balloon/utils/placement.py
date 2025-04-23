from utils.path import is_point_near_path
import constants

def is_on_path(x, y, path_points):
    return is_point_near_path(x, y, path_points, constants.MARGIN)

def is_on_other_tower(x, y, tower_cls, towers):
    tmp_rect = tower_cls.IMAGE.get_rect(center=(x, y)).inflate(-4, -4)
    return any(tmp_rect.colliderect(t.rect) for t in towers)

def is_on_ui(x, y, ui_rects):
    return any(r.collidepoint(x, y) for r in ui_rects)


def can_place_tower(x, y, tower_cls, path_points, towers, ui_rects):
    if is_on_path(x, y, path_points):
        return False

    if is_on_other_tower(x, y, tower_cls, towers):
        return False

    if is_on_ui(x, y, ui_rects):
        return False

    return True

