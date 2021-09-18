import pygame

class textCoin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.color = (255, 239, 75)
        self.text = '0'
        self.nb = 0
        self.font = pygame.font.SysFont("freesansbold.ttf", 36)
        self.textSurf = self.font.render(self.text, 1, self.color)
        self.image = pygame.Surface((30, 30))
        self.rect = self.image.get_rect()
        self.rect.topleft = [x-100, y+40]
        self.image.set_colorkey([0, 0, 0])
        self.W = self.textSurf.get_width()
        self.H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [30/2 - self.W/2, 30/2 - self.H/2])
        self.x = x
        self.y = y

    def updateNumber(self):
        with open("coin.txt", "r") as f:
            self.nb = f.read(5)
            self.nb = ''.join(x for x in self.nb if x.isprintable())

        self.text = '{}'.format(str(self.nb))
        self.textSurf = self.font.render(self.text, 1, self.color)
        self.image = pygame.Surface((30, 30))
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x-15, self.y+30]
        self.W = self.textSurf.get_width()
        self.H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [30/2 - self.W/2, 30/2 - self.H/2])