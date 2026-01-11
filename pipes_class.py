import pygame

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        super().__init__() #initialize Sprite superclass to use methods such as group
        self.image = pygame.image.load('assets/images/pipe.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]
        pipe_gap = 160  # initial gap size


        #poisition -1 or 1, either up or down position for the pipe
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True) #flip on x axis
            self.rect.bottomleft = [x, y-int(pipe_gap/2)]

        if position == -1:
            self.rect.topleft = [x, y+int(pipe_gap/2)]

    def update(self, pipeScr):
        if pipeScr:
            self.rect.x -= 4
        if self.rect.right < 0:
            self.kill() #remove the pipe once offscreen
