import pygame

class Commerce(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprite = pygame.image.load('assets/character/Male/Male 01-1.png')
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x-20, y-20]
        self.rect.topleft = self.position

    def get_image(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite, (0, 0), (x, y, 32, 32))
        return image