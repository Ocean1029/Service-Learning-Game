import pygame

def to_grayscale(surface):
    grayscale = surface.copy()
    arr = pygame.PixelArray(grayscale)
    for x in range(grayscale.get_width()):
        for y in range(grayscale.get_height()):
            r, g, b, a = grayscale.unmap_rgb(arr[x, y])
            gray = int(0.3 * r + 0.59 * g + 0.11 * b)
            arr[x, y] = (gray, gray, gray, a)
    del arr
    return grayscale