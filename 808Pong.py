import pygame
import random
import time

#// initialise pygame and mixer
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()

#// load sounds
kick_sound = pygame.mixer.Sound('sound/kick.wav')
snare_sound = pygame.mixer.Sound('sound/snare.wav')
openh_sound = pygame.mixer.Sound('sound/openh.wav')
closedh_sound = pygame.mixer.Sound('sound/closedh.wav')
cowbell_sound = pygame.mixer.Sound('sound/cowbell.wav')

display_width = 640
display_height = 480

black = (0,0,0)
red = (255,0,0)
white = (255,255,255)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('808 Pong')
clock = pygame.time.Clock()

smallText = pygame.font.Font('freesansbold.ttf', 35)
largeText = pygame.font.Font('freesansbold.ttf', 70)


def shape(color, x, y, w, h):
    pygame.draw.rect(gameDisplay, color, [x, y, w, h])

def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def player_score_display(text):
    TextSurf, TextRect = text_objects(text, smallText)
    TextRect.center = ((display_width * 0.7), (display_height * 0.15))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()

def bot_score_display(text):
    TextSurf, TextRect = text_objects(text, smallText)
    TextRect.center = ((display_width * 0.3), (display_height * 0.15))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()

def win_text(text):
    TextSurf, TextRect = text_objects(text, smallText)
    TextRect.center = ((display_width * 0.5), (display_height * 0.5))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()

def game_loop():
    
    #// player attributes
    playerw = 10
    playerh = 100
    playerx = display_width - playerw
    playery = (display_height - playerh)/2
    playery_change = 0
    player_score = 0
    #// bot attributes
    botw = 10
    both = 100
    botx = 0
    boty = (display_height - both)/2
    bot_score = 0
    #// ball attributes
    ballw = 15
    ballh = 15
    ballx = (display_width - ballw)/2
    bally = (display_height - ballh)/2
    ball_speedx = 10
    ball_speedy = random.randrange(0, 3)
    #// wall attributes
    wallw = display_width
    wallh = 5
    wallx = 0
    wally_top = 0
    wally_bottom = display_height - wallh

    linew = 3
    lineh = display_height
    linex = display_width/2
    liney = 0
    
    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    playery_change = -10
                elif event.key == pygame.K_DOWN:
                    playery_change = 10

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    playery_change = 0

        gameDisplay.fill(black)

        shape(red, wallx, wally_top, wallw, wallh)
        shape(red, wallx, wally_bottom, wallw, wallh)
        shape(red, linex, liney, linew, lineh)
        shape(red, playerx, playery, playerw, playerh)
        shape(red, botx, boty, botw, both)
        shape(red, ballx, bally, ballw, ballh)

        player_score_display(str(player_score))
        bot_score_display(str(bot_score))

        playery += playery_change
        ballx += ball_speedx
        bally += ball_speedy

        #// extra sound rules
        if ballx > display_width/2 - 5 and ballx < display_width/2 +5:
            pygame.mixer.Sound.play(snare_sound)
        
        
        #// hyper-intelligent AI
        if ballx < display_width * 0.7 and ballx > 0:
            if boty + both/2 != bally:
                boty += (bally - (boty + both/2)) * 0.085

        #// paddle ball rules
        if ballx > playerx and bally + ballh > playery and bally < playery + playerh:          
            pygame.mixer.Sound.play(kick_sound)
            if bally + ballh < playery + playerh/2:
                ball_speedy = - ((playery + playerh/2) - (bally + ballh)) * 0.2
            if bally > playery + playerh/2:
                ball_speedy = ((bally) - (playery + playerh/2)) * 0.2
            ball_speedx *= -1
            
        if ballx < botx and bally + ballh > boty and bally < boty + both:
            pygame.mixer.Sound.play(kick_sound)
            if bally + ballh < boty + both/2:
                ball_speedy = ((boty + both/2) - (bally + ballh)) * 0.2
            if bally > boty + both/2:
                ball_speedy = ((bally) - (boty + both/2)) * 0.2
            ball_speedx *= -1
            
        if ballx > display_width:
            pygame.mixer.Sound.play(cowbell_sound)
            bot_score += 1
            ballx = (display_width - ballh)/2
            ball_speedx = ball_speedx * -1
            ball_speedy = random.randrange(0, 3)

        if ballx < 0 - ballw:
            pygame.mixer.Sound.play(cowbell_sound)
            player_score += 1
            ballx = (display_width - ballh)/2
            ball_speedx = ball_speedx * -1
            ball_speedy = random.randrange(0, 3)

        if player_score >= 10:
            win_text('You Win!')
            time.sleep(3)
            player_score = 0
            bot_score = 0
        elif bot_score >= 10:
            win_text('You Lose :(')
            time.sleep(3)
            player_score = 0
            bot_score = 0

        if bally < 0 + wallh or bally > display_height - wallh:
            pygame.mixer.Sound.play(openh_sound)
            ball_speedy = ball_speedy * -1

        #// paddle height rules
        if playery < 0 + wallh:
            pygame.mixer.Sound.play(closedh_sound)
            playery += 2
            playery_change = 0

        if playery + playerh > display_height - wallh:
            pygame.mixer.Sound.play(closedh_sound)
            playery -= 2
            playery_change = 0

        if boty < 0 + wallh:
            pygame.mixer.Sound.play(closedh_sound)
            boty += 2

        if boty + both > display_height - wallh:
            pygame.mixer.Sound.play(closedh_sound) 
            boty -= 2
        
        pygame.display.update()
        clock.tick(60)

game_loop()
pygame.quit()
quit()
