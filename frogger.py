import pygame
import random as Random
from pygame.locals import *
from sys import exit

pygame.init()

#Mengatur Screen
screen = pygame.display.set_mode((448,550), 0,32)

#Menginput Gambar
bg = './images/bg.png'
frog = './images/sprite_sheets_up.png'
arrived = './images/arrived.png'
car1 = './images/car1.png'
car2 = './images/car2.png'
car3 = './images/car3.png'
car4 = './images/car4.png'
car5 = './images/car5.png'
platform= './images/platform.png'

bg = pygame.image.load(bg)
s_frog = pygame.image.load(frog)
s_arrived = pygame.image.load(arrived)
s_car1 = pygame.image.load(car1)
s_car2 = pygame.image.load(car2)
s_car3 = pygame.image.load(car3)
s_car4 = pygame.image.load(car4)
s_car5 = pygame.image.load(car5)
s_platform = pygame.image.load(platform)

#Mengatur Font Huruf
namafont = pygame.font.get_default_font()
font_game = pygame.font.SysFont(namafont, 70)
font_info = pygame.font.SysFont(namafont, 25)
font_menu = pygame.font.SysFont(namafont, 35)

#Efek Suara
suaramenabrak = pygame.mixer.Sound('./sounds/nabrak.wav')
suaraair = pygame.mixer.Sound('./sounds/air.wav')
suaratiba = pygame.mixer.Sound('./sounds/success.wav')
suaragame = pygame.mixer.Sound('./sounds/main sound.mp3')

pygame.display.set_caption('Frogger')
clock = pygame.time.Clock()


class Object():
    def __init__(self,posisi,sprite):
        self.sprite = sprite
        self.posisi = posisi

    def draw(self):
        screen.blit(self.sprite,(self.posisi))

    def rect(self):
        return Rect(self.posisi[0],self.posisi[1],self.sprite.get_width(),self.sprite.get_height())


class Frog(Object):
    def __init__(self,posisi,s_frog):
        self.sprite = s_frog
        self.posisi = posisi
        self.lives = 5
        self.animation_counter = 0
        self.animation_tick = 1
        self.way = "UP"
        self.can_move = 1

    def updateSprite(self,key_pressed):
        if self.way != key_pressed:
            self.way = key_pressed
            if self.way == "up":
                frog_filename = './images/sprite_sheets_up.png'
                self.sprite = pygame.image.load(frog_filename)
            elif self.way == "down":
                frog_filename = './images/sprite_sheets_down.png'
                self.sprite = pygame.image.load(frog_filename)
            elif self.way == "left":
                frog_filename = './images/sprite_sheets_left.png'
                self.sprite = pygame.image.load(frog_filename)
            elif self.way == "right":
                frog_filename = './images/sprite_sheets_right.png'
                self.sprite = pygame.image.load(frog_filename)


    def moveFrog(self,key_pressed, key_up):
        if self.animation_counter == 0 :
            self.updateSprite(key_pressed)
        self.incAnimationCounter()
        if key_up == 1:
            if key_pressed == "up":
                if self.posisi[1] > 39:
                    self.posisi[1] = self.posisi[1]-13
            elif key_pressed == "down":
                if self.posisi[1] < 473:
                    self.posisi[1] = self.posisi[1]+13
            if key_pressed == "left":
                if self.posisi[0] > 2:
                    if self.animation_counter == 2 :
                        self.posisi[0] = self.posisi[0]-13
                    else:
                        self.posisi[0] = self.posisi[0]-14
            elif key_pressed == "right":
                if self.posisi[0] < 401:
                    if self.animation_counter == 2 :
                        self.posisi[0] = self.posisi[0]+13
                    else:
                        self.posisi[0] = self.posisi[0]+14

    def animateFrog(self,key_pressed,key_up):
        if self.animation_counter != 0 :
            if self.animation_tick <= 0 :
                self.moveFrog(key_pressed,key_up)
                self.animation_tick = 1
            else :
                self.animation_tick = self.animation_tick - 1

    def setPos(self,posisi):
        self.posisi = posisi

    def decLives(self):
        self.lives = self.lives - 1

    def cannotMove(self):
        self.can_move = 0

    def incAnimationCounter(self):
        self.animation_counter = self.animation_counter + 1
        if self.animation_counter == 3 :
            self.animation_counter = 0
            self.can_move = 1

    def frogDead(self,game):
        self.setPosisiToInitialPosisi()
        self.decLives()
        game.resetTime()
        self.animation_counter = 0
        self.animation_tick = 1
        self.way = "UP"
        self.can_move = 1

    def setPosisiToInitialPosisi(self):
        self.posisi = [207, 475]

    def draw(self):
        current_sprite = self.animation_counter * 30
        screen.blit(self.sprite,(self.posisi),(0 + current_sprite, 0, 30, 30 + current_sprite))

    def rect(self):
        return Rect(self.posisi[0],self.posisi[1],30,30)

class Enemy(Object):
    def __init__(self,posisi,sprite_enemy,way,factor):
        self.sprite = sprite_enemy
        self.posisi = posisi
        self.way = way
        self.factor = factor

    def move(self,speed):
        if self.way == "right":
            self.posisi[0] = self.posisi[0] + speed * self.factor
        elif self.way == "left":
            self.posisi[0] = self.posisi[0] - speed * self.factor


class Platform(Object):
    def __init__(self,posisi,s_platform,way):
        self.sprite = s_platform
        self.posisi = posisi
        self.way = way

    def move(self,speed):
        if self.way == "right":
            self.posisi[0] = self.posisi[0] + speed
        elif self.way == "left":
            self.posisi[0] = self.posisi[0] - speed


class Game():
    def __init__(self,speed,level):
        self.speed = speed
        self.level = level
        self.points = 0
        self.time = 30
        self.gameInit = 0

    def incLevel(self):
        self.level = self.level + 1

    def incSpeed(self):
        self.speed = self.speed + 1

    def incPoints(self,points):
        self.points = self.points + points

    def decTime(self):
        self.time = self.time - 1

    def resetTime(self):
        self.time = 30


#Fungsi umum
def drawList(list):
    for i in list:
        i.draw()

def moveList(list,speed):
    for i in list:
        i.move(speed)

def destroyEnemys(list):
    for i in list:
        if i.posisi[0] < -80:
            list.remove(i)
        elif i.posisi[0] > 516:
            list.remove(i)

def destroyPlatforms(list):
    for i in list:
        if i.posisi[0] < -100:
            list.remove(i)
        elif i.posisi[0] > 448:
            list.remove(i)

def createEnemys(list,enemys,game):
    for i, tick in enumerate(list):
        list[i] = list[i] - 1
        if tick <= 0:
            if i == 0:
                list[0] = (40*game.speed)/game.level
                posisi_init = [-55,436]
                enemy = Enemy(posisi_init,s_car1,"right",1)
                enemys.append(enemy)
            elif i == 1:
                list[1] = (30*game.speed)/game.level
                posisi_init = [506, 397]
                enemy = Enemy(posisi_init,s_car2,"left",2)
                enemys.append(enemy)
            elif i == 2:
                list[2] = (40*game.speed)/game.level
                posisi_init = [-80, 357]
                enemy = Enemy(posisi_init,s_car3,"right",2)
                enemys.append(enemy)
            elif i == 3:
                list[3] = (30*game.speed)/game.level
                posisi_init = [516, 318]
                enemy = Enemy(posisi_init,s_car4,"left",1)
                enemys.append(enemy)
            elif i == 4:
                list[4] = (50*game.speed)/game.level
                posisi_init = [-56, 280]
                enemy = Enemy(posisi_init,s_car5,"right",1)
                enemys.append(enemy)

def createPlatform(list,platforms,game):
    for i, tick in enumerate(list):
        list[i] = list[i] - 1
        if tick <= 0:
            if i == 0:
                list[0] = (30*game.speed)/game.level
                posisi_init = [-100,200]
                platform = Platform(posisi_init,s_platform,"right")
                platforms.append(platform)
            elif i == 1:
                list[1] = (30*game.speed)/game.level
                posisi_init = [448, 161]
                platform = Platform(posisi_init,s_platform,"left")
                platforms.append(platform)
            elif i == 2:
                list[2] = (40*game.speed)/game.level
                posisi_init = [-100, 122]
                platform = Platform(posisi_init,s_platform,"right")
                platforms.append(platform)
            elif i == 3:
                list[3] = (40*game.speed)/game.level
                posisi_init = [448, 83]
                platform = Platform(posisi_init,s_platform,"left")
                platforms.append(platform)
            elif i == 4:
                list[4] = (20*game.speed)/game.level
                posisi_init = [-100, 44]
                platform = Platform(posisi_init,s_platform,"right")
                platforms.append(platform)

def carChangeRoad(enemys):
    enemy = Random.choice(enemys)
    initialPosisi = enemy.posisi[1]

    choice = Random.randint(1,2)
    if (choice % 2 == 0):
        enemy.posisi[1] = enemy.posisi[1] + 39
    else :
        enemy.posisi[1] = enemy.posisi[1] - 39

    if enemy.posisi[1] > 436:
        enemy.posisi[1] = initialPosisi
    elif enemy.posisi[1] < 280:
        enemy.posisi[1] = initialPosisi


def frogOnTheStreet(frog,enemys,game):
    for i in enemys:
        enemyRect = i.rect()
        frogRect = frog.rect()
        if frogRect.colliderect(enemyRect):
            suaramenabrak.play()
            frog.frogDead(game)

def frogInTheLake(frog,platforms,game):
    #Jika katak berada di bawah platform, maka aman = 1
    aman = 0
    wayPlatform = ""
    for i in platforms:
        platformRect = i.rect()
        frogRect = frog.rect()
        if frogRect.colliderect(platformRect):
            aman = 1
            wayPlatform = i.way

    if aman == 0:
        suaraair.play()
        frog.frogDead(game)

    elif aman == 1:
        if wayPlatform == "right":
            frog.posisi[0] = frog.posisi[0] + game.speed

        elif wayPlatform == "left":
            frog.posisi[0] = frog.posisi[0] - game.speed

def frogArrived(frog,theyarrived,game):
    if frog.posisi[0] > 33 and frog.posisi[0] < 53:
        posisi_init = [43,7]
        createArrived(frog,theyarrived,game,posisi_init)

    elif frog.posisi[0] > 115 and frog.posisi[0] < 135:
        posisi_init = [125,7]
        createArrived(frog,theyarrived,game,posisi_init)

    elif frog.posisi[0] > 197 and frog.posisi[0] < 217:
        posisi_init = [207,7]
        createArrived(frog,theyarrived,game,posisi_init)

    elif frog.posisi[0] > 279 and frog.posisi[0] < 299:
        posisi_init = [289,7]
        createArrived(frog,theyarrived,game,posisi_init)

    elif frog.posisi[0] > 361 and frog.posisi[0] < 381:
        posisi_init = [371,7]
        createArrived(frog,theyarrived,game,posisi_init)

    else:
        frog.posisi[1] = 46
        frog.animation_counter = 0
        frog.animation_tick = 1
        frog.can_move = 1


def whereIsTheFrog(frog):
    #Ketika katak belum melewati jalan
    if frog.posisi[1] > 240 :
        frogOnTheStreet(frog,enemys,game)

    #Ketika katak sampai di sungai
    elif frog.posisi[1] < 240 and frog.posisi[1] > 40:
        frogInTheLake(frog,platforms,game)

    #Ketika katak mencapai tujuan
    elif frog.posisi[1] < 40 :
        frogArrived(frog,theyarrived,game)


def createArrived(frog,theyarrived,game,posisi_init):
    frogg_arrived = Object(posisi_init,s_arrived)
    theyarrived.append(frogg_arrived)
    suaratiba.play()
    frog.setPosisiToInitialPosisi()
    game.incPoints(10 + game.time)
    game.resetTime()
    frog.animation_counter = 0
    frog.animation_tick = 1
    frog.can_move = 1


def nextLevel(theyarrived,enemys,platforms,frog,game):
    if len(theyarrived) == 5:
        theyarrived[:] = []
        frog.setPosisiToInitialPosisi()
        game.incLevel()
        game.incSpeed()
        game.incPoints(100)
        game.resetTime()


suaragame.play(-1)
text_info = font_menu.render(('Tekan apa pun untuk memulai!'),1,(0,0,0))
gameInit = 0

while gameInit == 0:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            gameInit = 1

    screen.blit(bg, (0, 0))
    screen.blit(text_info,(20,80))
    pygame.display.update()

while True:
    gameInit = 1
    game = Game(3,1)
    key_up = 1
    frog_initial_posisi = [210,480]
    frog = Frog(frog_initial_posisi,s_frog)

    enemys = []
    platforms = []
    theyarrived = []
    ticks_enemys = [30, 0, 30, 0, 60]
    ticks_platforms = [0, 0, 30, 30, 30]
    ticks_time = 30
    pressed_keys = 0
    key_pressed = 0

    while frog.lives > 0:

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYUP:
                key_up = 1
            if event.type == KEYDOWN:
                if key_up == 1 and frog.can_move == 1 :
                    key_pressed = pygame.key.name(event.key)
                    frog.moveFrog(key_pressed,key_up)
                    frog.cannotMove()
        if not ticks_time:
            ticks_time = 30
            game.decTime()
        else:
            ticks_time -= 1

        if game.time == 0:
            frog.frogDead(game)

        createEnemys(ticks_enemys,enemys,game)
        createPlatform(ticks_platforms,platforms,game)

        moveList(enemys,game.speed)
        moveList(platforms,game.speed)

        whereIsTheFrog(frog)

        nextLevel(theyarrived,enemys,platforms,frog,game)

        text_info1 = font_info.render(('Level: {0}               Points: {1}'.format(game.level,game.points)),1,(255,255,255))
        text_info2 = font_info.render(('Time: {0}           Lifes: {1}'.format(game.time,frog.lives)),1,(255,255,255))
        screen.blit(bg, (0, 0))
        screen.blit(text_info1,(10,520))
        screen.blit(text_info2,(250,520))

        random = Random.randint(0,100)
        if(random % 100 == 0):
            carChangeRoad(enemys)

        drawList(enemys)
        drawList(platforms)
        drawList(theyarrived)

        frog.animateFrog(key_pressed,key_up)
        frog.draw()

        destroyEnemys(enemys)
        destroyPlatforms(platforms)

        pygame.display.update()
        time_passed = clock.tick(30)

    while gameInit == 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                gameInit = 0

        screen.blit(bg, (0, 0))
        text = font_game.render('GAME OVER', 1, (255, 0, 0))
        text_points = font_game.render(('Score: {0}'.format(game.points)),1,(255,0,0))
        text_restart = font_info.render('Tekan tombol apa pun untuk mengulangi game!',1,(255,0,0))
        screen.blit(text, (75, 120))
        screen.blit(text_points,(80,170))
        screen.blit(text_restart,(20,250))

        pygame.display.update()
