import pygame
def blit_cover(screen, image):
    screen_width, screen_height = screen.get_size()
    img_width, img_height = image.get_size()

    # 計算要放大的比例（等比例放大到至少覆蓋螢幕）
    scale = max(screen_width / img_width, screen_height / img_height)
    new_size = (int(img_width * scale), int(img_height * scale))

    # 放大圖片
    scaled_image = pygame.transform.smoothscale(image, new_size)

    # 計算裁切區域（從中央裁出螢幕大小）
    offset_x = (new_size[0] - screen_width) // 2
    offset_y = (new_size[1] - screen_height) // 2
    source_rect = pygame.Rect(offset_x, offset_y, screen_width, screen_height)

    # 畫上螢幕
    screen.blit(scaled_image, (0, 0), source_rect)

def blit_tiled_background(screen, background_tile):
    screen_width, screen_height = screen.get_size()
    tile_width, tile_height = background_tile.get_size()

    for x in range(0, screen_width, tile_width):
        for y in range(0, screen_height, tile_height):
            screen.blit(background_tile, (x, y))
