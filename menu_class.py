import pygame

class button(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()

        self.image = image #get a copy of the image that will let us transform it without harming the original
        self.x = pos[0]
        self.y = pos[1]
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.alpha = 255
        self.fading = False

    def fade(self):
        self.fading = True
    def update(self, screen):

        if self.fading and self.alpha > 0:
            self.alpha -=5
            if self.alpha <0:
                self.alpha = 0
                self.kill()
            self.image = self.image.copy()
            self.image.set_alpha(self.alpha)
        screen.blit(self.image, self.rect)


