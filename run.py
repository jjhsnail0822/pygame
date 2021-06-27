import pygame
import sys
from pygame.locals import *
import random
import numpy as np

width=800
height=600
white = (255,255,255)
black = (0,0,0)
fps = 60
sec_per_asteroid = 1
tank_width=150
tank_height=100
asteroid_width=50
asteroid_height=50
bullet_width=30
bullet_height=30
max_asteroid_division=5

class Object:
    def __init__(self, hp, x, y, image, size_x, size_y):
        self.hp=hp
        self.x=x
        self.y=y
        self.image=image
        self.size_x=size_x
        self.size_y=size_y
    def resizeImage(self, resize_x, resize_y):
        self.image=pygame.transform.scale(self.image,(resize_x,resize_y))
    def view(self):
        screen.blit(self.image,(self.x,self.y))
    def move(self,plus_x,plus_y):
        if self.x+plus_x<0 or self.x+plus_x>(width-self.size_x) \
        or self.y+plus_y<0 or self.y+plus_y>(height-self.size_y):
            return False
        else:
            self.x=self.x+plus_x
            self.y=self.y+plus_y
            return True
    def isCollided(self,obj1, obj2):
        if obj1.x < obj2.x+obj2.size_x \
        and obj1.y < obj2.y+obj2.size_y \
        and obj1.x+obj1.size_x > obj2.x \
        and obj1.y+obj1.size_y > obj2.y:
            return True
        else:
            return False

class Asteroid(Object):
    acceleration=0.1
    speed=1
    def __init__(self, hp, x, y, image):
        Object.__init__(self,hp,x,y,image, asteroid_width, asteroid_height)
        self.bounced=False
        self.angle=random.random()*np.pi
        randomSize=random.random()+0.5
        self.size_x=int(randomSize*asteroid_width)
        self.size_y=int(randomSize*asteroid_height)
        self.resizeImage(self.size_x,self.size_y)
    def fall(self):
        self.speed+=self.acceleration
        self.y+=self.speed
    def bounceMove(self):
        self.x-=self.speed*np.cos(self.angle)
        self.y-=self.speed*np.sin(self.angle)

class Tank(Object):
    speed=10
    flipped=False
    def __init__(self, hp, x, y, image,):
        Object.__init__(self,hp,x,y,image, tank_width, tank_height)
        self.resizeImage(tank_width,tank_height)
    def move(self,plus_x,plus_y):
        super().move(plus_x,plus_y)
        if plus_x>0 and not self.flipped:
            self.flipped=True
            self.image=pygame.transform.flip(self.image,True,False)
        elif plus_x<0 and self.flipped:
            self.flipped=False
            self.image=pygame.transform.flip(self.image,True,False)

class Bullet(Object):
    speed=30
    power=50
    def __init__(self, hp, x, y, image,):
        Object.__init__(self,hp,x,y,image, bullet_width, bullet_height)
        self.resizeImage(bullet_width,bullet_height)

def randomPosX(wsize):
    return random.randrange(0,width-wsize)

pygame.init()

pygame.display.set_caption('운석 어쩌고 게임')
screen = pygame.display.set_mode((width,height),0,32)
clock = pygame.time.Clock()

background_image=pygame.image.load('seoulstation.jpg')
bg = Object(100,0,0,background_image,width,height)
bg.resizeImage(width,height)

tank1=Tank(100,width-tank_width,height-tank_height,pygame.image.load('tank.png'))
asteroid_image=pygame.image.load('asteroid.png')
bullet_image=pygame.image.load('bullet.png')

asteroidsList=[]
bulletsList=[]

makeAsteroids=0

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                temp_bullet=Bullet(100,tank1.x+tank1.size_x//2,tank1.y,bullet_image)
                bulletsList.append(temp_bullet)
    keys=pygame.key.get_pressed()
    if keys[K_LEFT]:
        tank1.move(-tank1.speed,0)
    elif keys[K_RIGHT]:
        tank1.move(tank1.speed,0)
    elif keys[K_UP]:
        tank1.move(0,-tank1.speed)
    elif keys[K_DOWN]:
        tank1.move(0,+tank1.speed)
    makeAsteroids+=1
    if makeAsteroids>=sec_per_asteroid*fps:
        makeAsteroids=0
        temp_asteroid=Asteroid(100,randomPosX(asteroid_width),0,asteroid_image)
        asteroidsList.append(temp_asteroid)
    screen.fill(white)
    bg.view()
    tank1.view()

    for bullet in bulletsList[:]:
        if bullet.y<=0 or bullet.hp<=0:
            bulletsList.remove(bullet)
    for asteroid in asteroidsList[:]:
        if asteroid.y<0 or asteroid.hp<=0:
            asteroidsList.remove(asteroid)
        elif asteroid.y>=height-asteroid.size_y:
            asteroid.bounced=True

    for asteroid in asteroidsList:
        if asteroid.bounced:
            asteroid.bounceMove()
        else:
            asteroid.fall()
        asteroid.view()
    for bullet in bulletsList:
        bullet.y=bullet.y-bullet.speed
        temp_asteroid_list=[]
        for asteroid in asteroidsList:
            if bullet.isCollided(bullet,asteroid):
                asteroid.hp-=bullet.power
                bullet.hp=0
                if asteroid.hp<=0:
                    for i in range(max_asteroid_division):
                        temp_asteroid=Asteroid(random.randrange(1,100),asteroid.x,asteroid.y,asteroid_image)
                        temp_asteroid.speed=asteroid.speed
                        temp_asteroid_list.append(temp_asteroid)
        if temp_asteroid_list:
            for temp_asteroid in temp_asteroid_list:
                asteroidsList.append(temp_asteroid)
        bullet.view()
    pygame.display.update()
    clock.tick(fps)