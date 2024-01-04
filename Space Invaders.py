
import pygame
import math
import random #to get random movements for the enemy
from pygame import mixer


#Initialize the pygame
pygame.init()

#Create the screen
display_width=800
display_height=600
Screen=pygame.display.set_mode((display_width,display_height))

#Background
background=pygame.image.load('background.png')

#Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1) #-1 makes it play on loop

#Title and Icon
pygame.display.set_caption("Space Invaders")
icon=pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#Score
score_value=0
font=pygame.font.Font('freesansbold.ttf',32)

textX=10
textY=10

#Game Over Text
over_Font=pygame.font.Font('freesansbold.ttf',64)


def show_score(x,y):
    score=font.render("Score: "+ str(score_value),True,(255,255,255))
    Screen.blit(score,(x,y))


def game_over_text():
    over_text=over_Font.render("GAME OVER!",True,(255,255,255))
    Screen.blit(over_text,(200,250))

#Player
playerImg=pygame.image.load('space-invaders.png')
DEFAULT_IMAGE_SIZE = (60, 60)
playerImg = pygame.transform.scale(playerImg, DEFAULT_IMAGE_SIZE)
playerX=370
playerY=480
playerX_change=0

#Enemy
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_enemies=6

for i in range(num_enemies):
    EnImg=pygame.image.load('alien.png')
    enemyImg.append(pygame.transform.scale(EnImg,(60,60)))
    enemyX.append(random.randint(0,735)) #random value between 0 and 735
    enemyY.append(random.randint(50,150))
    enemyX_change.append(2)
    enemyY_change.append(40)

#Bullet
#Ready-cant see bullet on screen
#Fire-bullet currently moving
bulletImg=pygame.image.load('bullet.png')
bulletX=0
bulletY=480
bulletX_change=0
bulletY_change=10
bullet_state="ready"

def player(x,y):
    Screen.blit(playerImg,(x,y)) #Used to draw(here the playerImg)

def enemy(x,y,i):
    Screen.blit(enemyImg[i],(x,y)) 

def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    Screen.blit(bulletImg,(x+16,y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    #Dist between 2 points formula
    distance=math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
    if distance<27:
        return True
    else:
        return False 


#Main game loop
running=True
while running:
    #RGB-Red,Blue,Green
    Screen.fill((0,0,0)) #changing color of the background

    #Background Image
    Screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type==pygame.QUIT: #If we intend to close the pygame
            running=False
    
        #If keystroke is pressed check if its left or right
        if event.type==pygame.KEYDOWN: #means the event where key is pressed
            if event.key==pygame.K_LEFT:
                playerX_change-=5
            if event.key==pygame.K_RIGHT:
                playerX_change=5
            if event.key==pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound=mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    #store the xcor of spaceship since the bullet was prev moving with the spaceship
                    bulletX=playerX
                    fire_bullet(bulletX,bulletY)
        if event.type==pygame.KEYUP: #Releasing the pressed key
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                playerX_change=0
    
    #Boundary check for spaceship
    playerX+=playerX_change
    
    if playerX<=0:
        playerX=0
    elif playerX>=740: #800-60
        playerX=740


    #Boundary Check and movements for enemy
    for i in range(num_enemies):
        #Game Over
        if enemyY[i]>440:
            for j in range(num_enemies):
                enemyY[j]=2000 #when an enemy hits all enemies move out of screen
            game_over_text()
            break

        enemyX[i]+=enemyX_change[i]
        if enemyX[i]<=0:
           enemyX_change[i]=2
           enemyY[i]+=enemyY_change[i]
        elif enemyX[i]>=740: #800-60
           enemyX_change[i]=-2
           enemyY[i]+=enemyY_change[i]
        #Collision
        collision=isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
           explosion_Sound=mixer.Sound('explosion.wav')
           explosion_Sound.play()
           bulletY=480
           bullet_state="ready"
           score_value+=1
           enemyX[i]=random.randint(0,735)
           enemyY[i]=random.randint(50,150)
        enemy(enemyX[i],enemyY[i],i)
    

    #Bullet Movement
    if bulletY<=0: #deals with the problem of only one bullet per game
        bulletY=480
        bullet_state="ready"
    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY-=bulletY_change
    
    

    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update() 