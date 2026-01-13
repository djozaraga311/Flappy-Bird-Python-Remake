import pygame

#contains bird animations and physics
class Bird(pygame.sprite.Sprite):
    pygame.mixer.init()
    def __init__(self, x, y):
        super().__init__() #initialize Sprite superclass to use methods such as group (will be used in main.py)

        #load sprites
        self.images = [
            pygame.image.load("assets/images/redbird-midflap.png").convert_alpha(),
            pygame.image.load("assets/images/redbird-downflap.png").convert_alpha(),
            pygame.image.load("assets/images/redbird-midflap.png").convert_alpha(),
            pygame.image.load("assets/images/redbird-upflap.png").convert_alpha()
                      ]

        #making bird sprite slightly bigger
        for i in range(len(self.images)):
            w, h = self.images[i].get_size()
            self.images[i] = pygame.transform.smoothscale(self.images[i], (int(w * 1.15), int(h*1.15)))


        self.index = 0 #which sprite from the list
        self.counter = 0 #control animation speed

        self.image = self.images[self.index] #represents the current sprite, in this case midflap
        self.rect = self.image.get_rect() #store position for collision, movement, etc.
        self.rect.center = [x, y] #initial position
        self.vel = 0
        self.clicked = False
        self.fail = False
        self.collision = False
        self.punchSound = pygame.mixer.Sound("assets/audio/punch.mp3")
        self.death = pygame.mixer.Sound("assets/audio/sfx_die.mp3")

    # MOVEMENT
    def jump(self):

        # gravity
        self.vel += 0.5
        if self.rect.bottom < 415:  #while the bird is above  ground,
            self.rect.y += int(self.vel) #add the velocity to the y position of the bird to move down.
            self.fail = False
        else: #stop movement if the bird hits the ground
            self.rect.bottom = 415
            #self.vel = 0
            self.fail = True


        # prevent jumping above the screen
        if self.rect.top <= 0:
            self.rect.top = 0

        ''' This is to let the bird jump off the ground but idk if that's allowed in the original game
        if self.rect.bottom >= 409:
            self.rect.bottom = 409
            self.vel = 0
        '''
        # jump
        if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            self.clicked = True
            self.vel = -10 #negative velocity goes up
            if not self.fail:
                self.flapping()

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

    # Flapping animation
    def flying(self):
        self.counter += 1
        flap_cooldown = 5

        # uses two variables to control animation speed
        # every 5 frames, the sprite changes
        if self.counter > flap_cooldown:
            self.counter = 0
            self.index += 1  # change to the next sprite in images[]

            # prevent out of bounds error
            if self.index >= len(self.images):
                self.index = 0


    #sounds
    def flapping(self):
        flapSound = pygame.mixer.Sound("assets/audio/sfx_wing.mp3")
        flapSound.play()

    def rotate(self):
        #whatever sprite the group is on, it will be rotated as it is clicked
        #rotate(image source, angle)
        #follows gravity, rotate up but then slowly fall down
        if not self.fail:
            self.angle = self.vel * -3
        self.image = pygame.transform.rotate(self.images[self.index], self.angle) #update the rotation angle via vel value


    def update(self, in_game, animate_only = False): #contains the necessary methods for the bird sprites while the game runs
        # plays flying animation at game start menu
        #when the game starts (passed from main.py), you can jump.
        #rotate doesn't need to be a part of the if statement since it depends on the ability to jump.
        # unable to jump --> bird doesn't rotate

        if not self.fail:
            self.flying()
            self.rotate()
            self.jump()

        else:
            if not self.collision:
                self.punchSound.play()

                self.death.play()
                self.collision = True

            self.vel += 0.5
            self.rect.y += int(self.vel)

            self.angle = self.vel * -10
            if self.angle >= -90:
                self.image = pygame.transform.rotate(self.images[self.index], self.angle)

            if self.rect.bottom >= 410:
                self.rect.bottom = 410


