import pygame
import random
import webbrowser


pygame.init()

explosion = pygame.mixer.Sound("explosion.wav")
pygame.mixer.music.load("Orbital Colossus.mp3")

display_W = 800
display_H = 600
game_display = pygame.display.set_mode((display_W,display_H))
ship_W = 75
ship_H = 99
pygame.display.set_caption('Spacer')
fps = 60
black = (0,0,0)
white = (255,255,255)
perpul = (155,0,155)
bright_perpul = (255,0,255)
red = (200,0,0)
bright_red = (255,0,0)
green = (0,200,0)
bright_green = (0,255,0)
shipimg = pygame.image.load('playerShip1_green.png')
background = pygame.image.load('darkPurple.png')
bg = pygame.transform.scale(background,(display_W,display_H))
asteroid = pygame.image.load('meteorBrown_big1.png')
ship2 = pygame.image.load('playerShip2_green.png')
#MAX_Y_SPEED = 8
#MAX_A_COUNT =5
asteroid_H = 101
asteroid_W = 84
clock = pygame.time.Clock()
pause = True

def quit_game():
    pygame.quit()
    quit()


def donate():
    new = 2

    url = "https://www.paypal.com/donate/?token=NHKmYklIxyXX1cFRvxu-1v49WBQ7K7dUfP7isfflZ3Nrl4j5RXrkgi63MBhjGYgmAnnALm&country.x=US&locale.x=US"
    webbrowser.open(url , new = new)

def asteroids_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: " + str(count), True, black)
    game_display.blit(text, (0, 0))

def asteroids(ax, ay, num,rx,ry):
    game_display.blit(asteroid, (ax, ay))
    for a in range(num):
        game_display.blit(asteroid,(rx,ry))


def ship(x,y):
    game_display.blit(shipimg,(x,y))



def text_objects(text, font):
    textSuface = font.render(text, True, black)
    return textSuface, textSuface.get_rect()

def crash():

    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosion)

    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects("You Crashed!", largeText)
    TextRect.center = ((display_W / 2), (display_H / 2))
    game_display.blit(TextSurf, TextRect)

    while True:
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
              pygame.quit()
              quit()

       Button("Play Again", 150, 450, 100, 50, green, bright_green, gameloop)
       Button("Quit!", 550, 450, 100, 50, red, bright_red, quit_game)
       Button("Donate", 350, 450, 100, 50, perpul, bright_red, donate)

       pygame.display.flip()
       clock.tick(15)





def Button(msg,x,y,w,h,ic,ac,action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(game_display,ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()

    else:
        pygame.draw.rect(game_display,ic, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x+ (w/2)),(y+ (h/2)))
    game_display.blit(textSurf, textRect)



def unpause():
    global pause
    pause = False
    pygame.mixer.music.unpause()

def paused():
    pygame.mixer.music.pause()

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        largeText = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects('Paused', largeText)
        TextRect.center = ((display_W / 2), (display_H / 2))
        game_display.blit(TextSurf, TextRect)

        Button("Continue",150,450,100,50,green,bright_green,unpause)
        Button("Quit!",550, 450, 100, 50,red,bright_red,quit_game)
        Button("Donate", 350, 450, 100, 50, perpul, bright_red, donate)

        pygame.display.flip()
        clock.tick(15)



def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        game_display.blit(bg, (0, 0))
        largeText = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects('Spacer', largeText)
        TextRect.center = ((display_W / 2), (display_H / 2))
        game_display.blit(TextSurf, TextRect)

        Button("New Game",150,450,100,50,green,bright_green,gameloop)
        Button("Quit!",550, 450, 100, 50,red,bright_red,quit_game)
        Button("Donate", 350, 450, 100, 50, perpul, bright_red, donate)

        pygame.display.flip()
        clock.tick(15)
#lx,ly,bolts,rlx,rly

def gameloop():
    pygame.mixer.music.play(-1)
    x = (display_W * 0.45)
    y = (display_H * 0.8)
    ax = random.randrange(0, display_W)
    ay = -600
    rx = random.randrange(0, display_W)
    ry = -650


    a_speed = 3
    a_count = 0
    x_change = 0

    gameExit = False


    dodged = 0

    global pause
    #main game loop
    while not gameExit:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5 - dodged/2
                elif event.key == pygame.K_RIGHT:
                    x_change = 5 + dodged/2
                elif event.key == pygame.K_p:
                    pause = True
                    paused()
                elif event.key == pygame.K_SPACE:
                    pass
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                    x_change = 0


        x += x_change

        game_display.blit(bg,(0,0))
        ship(x,y)

        if x > display_W - ship_W or x < 0:
           crash()

        if ay > display_H:
            ay = 0 - asteroid_H
            ax = random.randrange(0, display_W)
            a_speed += 1
            dodged += 1
            a_count += 1

        if ry > display_H:
            ry = 0 - asteroid_H
            rx = random.randrange(0, display_W)
            a_count += 1
        '''
       
        if a_speed > MAX_Y_SPEED:
            a_speed = MAX_Y_SPEED
        if a_count > MAX_A_COUNT:
            a_count = MAX_A_COUNT
        '''

        if y < ay + asteroid_H:
            if x > ax and x < ax + asteroid_W or x + ship_W > ax and x + ship_W < ax + asteroid_W:
                crash()


        if y < ry + asteroid_H:
            if x > rx and x < rx + asteroid_W or x + ship_W > rx and x + ship_W < rx + asteroid_W:
                crash()

        asteroids_dodged(dodged)
        asteroids(ax,ay,a_count,rx,ry)
        ay += a_speed
        ry += a_count
        ry += a_speed

        #render graphics
        pygame.display.flip()
        #Frames Per Second
        clock.tick(fps)

game_intro()
gameloop()
pygame.quit()
quit()