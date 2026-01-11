import pygame
import math
from bird_class import Bird
from pipes_class import Pipe
from menu_class import button
import random

pygame.init()

clock = pygame.time.Clock()
FPS = 60

#window dimensions
sc_width = 800
sc_height = 457

#create game window
screen = pygame.display.set_mode((sc_width, sc_height))
pygame.display.set_caption("Flappy Bird")

#background assets
bg = pygame.image.load("assets/images/bg.png").convert()
ground = pygame.image.load("assets/images/ground.png").convert()
scoreSound = pygame.mixer.Sound("assets/audio/sfx_point.mp3")



scaledGR = pygame.transform.smoothscale(ground, (1479/7, 481/7)) #use scaled version as it fits the screen

#define game variables
scroll = 0 #variable for horizontal movement
gr_scroll = 0
bg_width = bg.get_width()
gr_width = scaledGR.get_width()
score = 0
high_score = 0
pass_pipe = False
run = True
in_game = False
game_over = False


#image doesn't actually fit the window size, so calculate the number of
#duplicate images to fill the window, with a buffer of 1
tiles = math.ceil(sc_width / bg_width) + 1
grTiles = math.ceil(sc_width/gr_width) + 1

#create a bird
newBird = Bird(150, 228)
bird_group = pygame.sprite.Group()
bird_group.add(newBird)

#pipes
pipe_group = pygame.sprite.Group()
#draws the first pair of pipes
btm_pipe = Pipe(800, int(sc_height / 2), -1)
top_pipe = Pipe(800, int(sc_height / 2), 1)
pipe_frequency = 1500  # 1 1/2 seconds a new pipe
last_pipe = pygame.time.get_ticks() #get the timing of the pipes

#main menu assets
startButton = pygame.image.load("assets/images/playbutton.png").convert_alpha()
w, h = startButton.get_size()
startButton = pygame.transform.scale(startButton, (int(w/2), int(h/2)))
start = button(startButton, (sc_width/2, sc_height/2))
clicked = False
title = pygame.image.load("assets/images/title.png").convert_alpha()
w, h, = title.get_size()
title = pygame.transform.scale(title, (int(w/2), int(h/2)))
titleScreen = button(title, (sc_width/2, sc_height/4))
lastClick = pygame.time.get_ticks()
click_frequency = 50


#game over screen assets
restart = pygame.image.load("assets/images/restart.png").convert_alpha()
restartButton = button(restart, (sc_width/2, 400))

game_over_sprite = pygame.image.load("assets/images/game_over.png").convert_alpha()
go_w, go_h = game_over_sprite.get_size()
scaled_game_over = pygame.transform.scale(game_over_sprite, (int(go_w * 3), int(go_h * 3)))
game_over_screen = button(scaled_game_over, (sc_width/2, 75))

board = pygame.image.load("assets/images/scoreboard.png").convert_alpha()
board_w, board_h = board.get_size()
s_board = pygame.transform.scale_by(board, 1.5)
scoreboard = button(s_board, (sc_width/2, sc_height/2))

#medals
platinum = pygame.image.load("assets/images/platinum.png").convert_alpha()
gold = pygame.image.load("assets/images/gold.png").convert_alpha()
silver = pygame.image.load("assets/images/silver.png").convert_alpha()
bronze = pygame.image.load("assets/images/bronze.png").convert_alpha()

w, h = platinum.get_size()
platinum_scaled = pygame.transform.scale(platinum, ((w*1.6), (h*1.6)))

w, h = gold.get_size()
gold_scaled = pygame.transform.scale(gold, ((w*1.6), (h*1.6)))

w, h = silver.get_size()
silver_scaled = pygame.transform.scale(silver, ((w*1.5), (h*1.5)))

w, h = bronze.get_size()
bronze_scaled = pygame.transform.scale(bronze, ((w*1.6), (h*1.6)))



#scores
font = pygame.font.SysFont('Fixedsys', 60)
white = (255, 255, 255)
scoreboard_font = pygame.font.SysFont('Fixedsys', 45)


#main game loop functions

#drawing the score
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col) #render the font into an image
    screen.blit(img, (x, y))

#restarting the game
def reset_game():

    #empty groups and restart bird position
    pipe_group.empty()
    bird_group.empty()
    bird = Bird(150, 228)
    bird_group.add(bird)
    score = 0

    return bird, score



while run:
    start.fade()
    titleScreen.fade()

    start.update(screen)
    titleScreen.update(screen)

    clock.tick(FPS) #60 fps

    #Check game conditions on whether to start/restart/quit flappy bird
    for event in pygame.event.get():
        #press x to quit
        if event.type == pygame.QUIT:
            run = False

        #get current mouse position
        mouse_pos = pygame.mouse.get_pos()

        #start menu
        if not game_over and not in_game:
            if pygame.mouse.get_pressed()[0]==1 and clicked == False:
                clicked = True
                if start.rect.collidepoint(mouse_pos):
                    in_game = True
        if pygame.mouse.get_pressed()[0]==0 and clicked == True:
            clicked = False

        #check if the user wants to restart the game
        if game_over:
            current_click = pygame.time.get_ticks()

            # only allow a new click if enough time has passed (cooldown)
            if current_click - lastClick > click_frequency:

                # Restart button clicked
                if pygame.mouse.get_pressed()[0] == 1 and clicked == False:
                    clicked = True
                    lastClick = current_click  # start cooldown

                    if restartButton.rect.collidepoint(mouse_pos):
                        # reset everything and go back to menu
                        newBird, score = reset_game()
                        game_over = False
                        in_game = False  # show menu

            # reset clicked when mouse is released
            if pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False

                if pygame.mouse.get_pressed()[0]==0 and clicked == True:

                        clicked = False

    if not newBird.fail or (in_game and not newBird.fail):
        scroll -= 0.5
        gr_scroll -= 4

    else:
        newBird.fail = True

    #draw scrolling background as part of the menu
    for i in range(0, tiles):
        # current tile *  background width + scrolling
        screen.blit(bg, (i * bg_width + scroll, 0))

    # separate scroll for the ground, it will scroll faster than the bg
    for i in range(0, grTiles):
        screen.blit(scaledGR, (i * gr_width + gr_scroll, 419))

    # reset the scrolling
    # when scroll's absolute value is less than the background width, reset to 0
    if abs(scroll) > bg_width:
        scroll = 0

    # when ground scroll's abs value is less than the ground width, reset to 0
    if abs(gr_scroll) > gr_width:
        gr_scroll = 0

    #when the game runs but isn't playing, show the start menu
    #reset menu's opacity values
    if not in_game and not newBird.fail:
        # reset menu buttons
        start.alpha = 255
        start.fading = False
        titleScreen.alpha = 255
        titleScreen.fading = False
        start.update(screen)
        titleScreen.update(screen)


    if in_game:
        #remove the start screen once you click play
        if not game_over and not start.fading:
            start.fade()
            titleScreen.fade()
        start.update(screen)
        titleScreen.update(screen)

        current = pygame.time.get_ticks()
        pipe_group.draw(screen)
        pipe_group.update(not newBird.fail) #will only keep scrolling if the bird hasn't died

            #compare frequency and the difference between the current and last tick
            #spawn another pair of pipes

        if current - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(800, int(sc_height / 2) + pipe_height, -1)
            top_pipe = Pipe(800, int(sc_height / 2) +pipe_height , 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = current


        #separate scroll for the ground, it will scroll faster than the bg
        for i in range (0, grTiles):
            screen.blit(scaledGR, (i * gr_width + gr_scroll, 419))




        #reset the scrolling
        #when scroll's absolute value is less than the background width, reset to 0
        if abs(scroll) > bg_width:
            scroll = 0

        #when ground scroll's abs value is less than the ground width, reset to 0
        if abs(gr_scroll) > gr_width:
            gr_scroll = 0

        # bird animation needs to play at all times, unless the game ends
        bird_group.draw(screen)
        bird_group.update(in_game)


        #score check
        #check if there are any pipes present (check the group)
        if len(pipe_group)>0:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
                and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
                and pass_pipe == False:
                pass_pipe = True
            if pass_pipe == True:
                if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                    score+=1
                    if score > high_score:
                        high_score = score
                    scoreSound.play()
                    pass_pipe = False

            #control when the score shows
            if not newBird.fail:
                draw_text(str(score), font, white, int(sc_width / 2), 20)


        #check for pipe collision
        for pipe in pipe_group:
            if newBird.rect.colliderect(pipe.rect):
                game_over = True
                newBird.fail = True

        #separate logic to end the game once the bird hits the ground
        if newBird.fail == True:
            game_over = True

    #show game over screen
    if game_over:

        restartButton.update(screen)
        game_over_screen.update(screen)
        scoreboard.update(screen)
        draw_text(str(score), scoreboard_font, white, 500, 195)
        draw_text(str(high_score), scoreboard_font, white, 500, 260)

        if score >= 10 and score < 20:

            screen.blit(bronze_scaled, (270, 205))

        elif score >= 20 and score < 30:
            screen.blit(silver_scaled, (270, 205))

        elif score >= 30 and score < 40:
            screen.blit(gold_scaled, (270, 205))

        elif score >= 40:
            screen.blit(platinum_scaled, (270, 205))




    pygame.display.update()

pygame.quit()
import pygame
import math
from bird_class import Bird
from pipes_class import Pipe
from menu_class import button
import random

pygame.init()

clock = pygame.time.Clock()
FPS = 60

#window dimensions
sc_width = 800
sc_height = 457

#create game window
screen = pygame.display.set_mode((sc_width, sc_height))
pygame.display.set_caption("Flappy Bird")

#background assets
bg = pygame.image.load("assets/images/bg.png").convert()
ground = pygame.image.load("assets/images/ground.png").convert()
scoreSound = pygame.mixer.Sound("assets/audio/sfx_point.mp3")



scaledGR = pygame.transform.smoothscale(ground, (1479/7, 481/7)) #use scaled version as it fits the screen

#define game variables
scroll = 0 #variable for horizontal movement
gr_scroll = 0
bg_width = bg.get_width()
gr_width = scaledGR.get_width()
score = 0
high_score = 0
pass_pipe = False
run = True
in_game = False
game_over = False


#image doesn't actually fit the window size, so calculate the number of
#duplicate images to fill the window, with a buffer of 1
tiles = math.ceil(sc_width / bg_width) + 1
grTiles = math.ceil(sc_width/gr_width) + 1

#create a bird
newBird = Bird(150, 228)
bird_group = pygame.sprite.Group()
bird_group.add(newBird)

#pipes
pipe_group = pygame.sprite.Group()
#draws the first pair of pipes
btm_pipe = Pipe(800, int(sc_height / 2), -1)
top_pipe = Pipe(800, int(sc_height / 2), 1)
pipe_frequency = 1500  # 1 1/2 seconds a new pipe
last_pipe = pygame.time.get_ticks() #get the timing of the pipes

#main menu assets
startButton = pygame.image.load("assets/images/playbutton.png").convert_alpha()
w, h = startButton.get_size()
startButton = pygame.transform.scale(startButton, (int(w/2), int(h/2)))
start = button(startButton, (sc_width/2, sc_height/2))
clicked = False
title = pygame.image.load("assets/images/title.png").convert_alpha()
w, h, = title.get_size()
title = pygame.transform.scale(title, (int(w/2), int(h/2)))
titleScreen = button(title, (sc_width/2, sc_height/4))
lastClick = pygame.time.get_ticks()
click_frequency = 50


#game over screen assets
restart = pygame.image.load("assets/images/restart.png").convert_alpha()
restartButton = button(restart, (sc_width/2, 400))

game_over_sprite = pygame.image.load("assets/images/game_over.png").convert_alpha()
go_w, go_h = game_over_sprite.get_size()
scaled_game_over = pygame.transform.scale(game_over_sprite, (int(go_w * 3), int(go_h * 3)))
game_over_screen = button(scaled_game_over, (sc_width/2, 75))

board = pygame.image.load("assets/images/scoreboard.png").convert_alpha()
board_w, board_h = board.get_size()
s_board = pygame.transform.scale_by(board, 1.5)
scoreboard = button(s_board, (sc_width/2, sc_height/2))

#medals
platinum = pygame.image.load("assets/images/platinum.png").convert_alpha()
gold = pygame.image.load("assets/images/gold.png").convert_alpha()
silver = pygame.image.load("assets/images/silver.png").convert_alpha()
bronze = pygame.image.load("assets/images/bronze.png").convert_alpha()

w, h = platinum.get_size()
platinum_scaled = pygame.transform.scale(platinum, ((w*1.6), (h*1.6)))

w, h = gold.get_size()
gold_scaled = pygame.transform.scale(gold, ((w*1.6), (h*1.6)))

w, h = silver.get_size()
silver_scaled = pygame.transform.scale(silver, ((w*1.5), (h*1.5)))

w, h = bronze.get_size()
bronze_scaled = pygame.transform.scale(bronze, ((w*1.6), (h*1.6)))



#scores
font = pygame.font.SysFont('Fixedsys', 60)
white = (255, 255, 255)
scoreboard_font = pygame.font.SysFont('Fixedsys', 45)


#main game loop functions

#drawing the score
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col) #render the font into an image
    screen.blit(img, (x, y))

#restarting the game
def reset_game():

    #empty groups and restart bird position
    pipe_group.empty()
    bird_group.empty()
    bird = Bird(150, 228)
    bird_group.add(bird)
    score = 0

    return bird, score



while run:
    start.fade()
    titleScreen.fade()

    start.update(screen)
    titleScreen.update(screen)

    clock.tick(FPS) #60 fps

    #Check game conditions on whether to start/restart/quit flappy bird
    for event in pygame.event.get():
        #press x to quit
        if event.type == pygame.QUIT:
            run = False

        #get current mouse position
        mouse_pos = pygame.mouse.get_pos()

        #start menu
        if not game_over and not in_game:
            if pygame.mouse.get_pressed()[0]==1 and clicked == False:
                clicked = True
                if start.rect.collidepoint(mouse_pos):
                    in_game = True
        if pygame.mouse.get_pressed()[0]==0 and clicked == True:
            clicked = False

        #check if the user wants to restart the game
        if game_over:
            current_click = pygame.time.get_ticks()

            # only allow a new click if enough time has passed (cooldown)
            if current_click - lastClick > click_frequency:

                # Restart button clicked
                if pygame.mouse.get_pressed()[0] == 1 and clicked == False:
                    clicked = True
                    lastClick = current_click  # start cooldown

                    if restartButton.rect.collidepoint(mouse_pos):
                        # reset everything and go back to menu
                        newBird, score = reset_game()
                        game_over = False
                        in_game = False  # show menu

            # reset clicked when mouse is released
            if pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False

                if pygame.mouse.get_pressed()[0]==0 and clicked == True:

                        clicked = False

    if not newBird.fail or (in_game and not newBird.fail):
        scroll -= 0.5
        gr_scroll -= 4

    else:
        newBird.fail = True

    #draw scrolling background as part of the menu
    for i in range(0, tiles):
        # current tile *  background width + scrolling
        screen.blit(bg, (i * bg_width + scroll, 0))

    # separate scroll for the ground, it will scroll faster than the bg
    for i in range(0, grTiles):
        screen.blit(scaledGR, (i * gr_width + gr_scroll, 419))

    # reset the scrolling
    # when scroll's absolute value is less than the background width, reset to 0
    if abs(scroll) > bg_width:
        scroll = 0

    # when ground scroll's abs value is less than the ground width, reset to 0
    if abs(gr_scroll) > gr_width:
        gr_scroll = 0

    #when the game runs but isn't playing, show the start menu
    #reset menu's opacity values
    if not in_game and not newBird.fail:
        # reset menu buttons
        start.alpha = 255
        start.fading = False
        titleScreen.alpha = 255
        titleScreen.fading = False
        start.update(screen)
        titleScreen.update(screen)


    if in_game:
        #remove the start screen once you click play
        if not game_over and not start.fading:
            start.fade()
            titleScreen.fade()
        start.update(screen)
        titleScreen.update(screen)

        current = pygame.time.get_ticks()
        pipe_group.draw(screen)
        pipe_group.update(not newBird.fail) #will only keep scrolling if the bird hasn't died

            #compare frequency and the difference between the current and last tick
            #spawn another pair of pipes

        if current - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(800, int(sc_height / 2) + pipe_height, -1)
            top_pipe = Pipe(800, int(sc_height / 2) +pipe_height , 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = current


        #separate scroll for the ground, it will scroll faster than the bg
        for i in range (0, grTiles):
            screen.blit(scaledGR, (i * gr_width + gr_scroll, 419))




        #reset the scrolling
        #when scroll's absolute value is less than the background width, reset to 0
        if abs(scroll) > bg_width:
            scroll = 0

        #when ground scroll's abs value is less than the ground width, reset to 0
        if abs(gr_scroll) > gr_width:
            gr_scroll = 0

        # bird animation needs to play at all times, unless the game ends
        bird_group.draw(screen)
        bird_group.update(in_game)


        #score check
        #check if there are any pipes present (check the group)
        if len(pipe_group)>0:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
                and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
                and pass_pipe == False:
                pass_pipe = True
            if pass_pipe == True:
                if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                    score+=1
                    if score > high_score:
                        high_score = score
                    scoreSound.play()
                    pass_pipe = False

            #control when the score shows
            if not newBird.fail:
                draw_text(str(score), font, white, int(sc_width / 2), 20)


        #check for pipe collision
        for pipe in pipe_group:
            if newBird.rect.colliderect(pipe.rect):
                game_over = True
                newBird.fail = True

        #separate logic to end the game once the bird hits the ground
        if newBird.fail == True:
            game_over = True

    #show game over screen
    if game_over:

        restartButton.update(screen)
        game_over_screen.update(screen)
        scoreboard.update(screen)
        draw_text(str(score), scoreboard_font, white, 500, 195)
        draw_text(str(high_score), scoreboard_font, white, 500, 260)

        if score >= 10 and score < 20:

            screen.blit(bronze_scaled, (270, 205))

        elif score >= 20 and score < 30:
            screen.blit(silver_scaled, (270, 205))

        elif score >= 30 and score < 40:
            screen.blit(gold_scaled, (270, 205))

        elif score >= 40:
            screen.blit(platinum_scaled, (270, 205))




    pygame.display.update()

pygame.quit()
