class Decor:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
        self.rect = image.get_rect(center=(x, y))
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
