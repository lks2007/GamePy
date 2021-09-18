import pygame

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprite = pygame.image.load('assets/coin/Coin_Gems/MonedaD.png')
        self.image = self.get_image(0, 0)
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.image.set_colorkey([0, 0, 0])
        self.image.set_alpha(0)
        self.rect = self.image.get_rect()
        self.position = [x-35, y-40]
        self.visible = True

    def update(self):
        self.rect.topleft = self.position

        if self.visible == True:
            self.image.set_alpha(255)
        else:
            self.image.set_alpha(0)        

    def get_image(self, x, y):
        image = pygame.Surface([16, 16])
        image.blit(self.sprite, (0, 0), (x, y, 16, 16))
        return image