# adapted from wireframe code twinstickshooter.py
import pgzrun

import pygame as pg
import math

import random

WIDTH = 860
HEIGHT = 540

level = 10

bg = pg.image.load("images/arena.png").convert()
play_Area = Rect((0, 0), (WIDTH, HEIGHT))

player = Actor("robot.png", center=(WIDTH//2, HEIGHT//2), anchor=('center', 'center'))

Enemy = []

def create_enemy():
    global Enemy
    Enemy = []
    for i in range(level):
      x =  random.randint(play_Area.left,play_Area.right)
      y =  random.randint(play_Area.top,play_Area.bottom)
      Enemy.append(Actor("t1.png", center=(x, y), anchor=('center', 'center')))

pl_movement = [0, 0]
pl_move_speed = 2
robotspeed = 0.2
pl_rotation = [0, 0]
create_enemy()
shooting = False

bullets = []
upsplit = []
downsplit = []
bullet_speed = 15
fire_rate = 0.15
fire_timer = 0

def checkInput():
     if keyboard.left:  pl_movement[0] = -1
     if keyboard.right: pl_movement[0] = 1
     if keyboard.up:    pl_movement[1] = -1
     if keyboard.down:  pl_movement[1] = 1
     if keyboard.d: pl_rotation[0] = 1
     if keyboard.a: pl_rotation[0] = -1
     if keyboard.s: pl_rotation[1] = 1
     if keyboard.w: pl_rotation[1] = -1

def update(dt):
    global shooting, bullets, fire_timer, level

    # Movement every frame
    checkInput()
    player.x += pl_movement[0] * pl_move_speed
    player.y += pl_movement[1] * pl_move_speed
    pl_movement[0] = 0
    pl_movement[1] = 0
    # Clamp the position
    if player.y - 16 < play_Area.top:
        player.y = play_Area.top + 16
    elif player.y + 16 > play_Area.bottom:
        player.y = play_Area.bottom - 16
    if player.x - 16 < play_Area.left:
        player.x = play_Area.left + 16
    elif player.x + 16 > play_Area.right:
        player.x = play_Area.right - 16

    if any([keyboard[keys.W], keyboard[keys.A], keyboard[keys.S], keyboard[keys.D]]):
        shooting = True
    else:
        shooting = False
        fire_timer = fire_rate
    

    if shooting == True:
        desired_angle = (math.atan2(-pl_rotation[1], pl_rotation[0]) / (math.pi/180)) - 45
        fire_timer += dt
        if fire_timer > fire_rate:
            bullet = Actor("lazer.png", center=player.pos, anchor=('center', 'center'))
            bullet.direction = pl_rotation.copy()                                           
            bullet.angle = desired_angle
            bullets.append(bullet)
            fire_timer = 0
            pl_rotation[1] = 0
            pl_rotation[0] = 0
    
    bullets_to_remove = []
    for b in bullets:
        b.x += b.direction[0] * bullet_speed 
        b.y += b.direction[1] * bullet_speed
        if not b.colliderect(play_Area):
            bullets_to_remove.append(b)
        for T1 in Enemy:
          if b.collidepoint(T1.center):
             bullets_to_remove.append(b)
             vu = Actor("t1split", center=T1.pos, anchor=('center', 'center'))
             vu.splitdirection = b.direction
             upsplit.append(vu)
             vd = Actor("t1split", center=T1.pos, anchor=('center', 'center'))
             downsplit.append(vd)
             vd.splitdirection = b.direction
             Enemy.remove(T1)
    
    for b in bullets_to_remove:
        if b in bullets:
             bullets.remove(b)
    for T1 in Enemy:
       if player.x < T1.x:
           T1.x = T1.x-robotspeed
       elif player.x > T1.x:
           T1.x = T1.x+robotspeed   
       if player.y > T1.y:
           T1.y = T1.y+robotspeed
       elif player.y < T1.y:
           T1.y = T1.y-robotspeed
    for Ex in upsplit:
        Ex.y = Ex.y + 10*Ex.splitdirection[0]
        Ex.x = Ex.x - 10*Ex.splitdirection[1]
        if not Ex.colliderect(play_Area):
            upsplit.remove(Ex)
    for Ex in downsplit:
        Ex.y = Ex.y - 10*Ex.splitdirection[0]
        Ex.x = Ex.x + 10*Ex.splitdirection[1]
        if not Ex.colliderect(play_Area):
            downsplit.remove(Ex)
        
 
    if len(Enemy) < 1 :
        level = level + 1
        create_enemy()
        

def draw():
    screen.blit(bg, (0, 0))
    screen.draw.text("Level "+str(level),(10,10),owidth=0.5, ocolor=(255,0,0),color=(255,255,0),fontsize=300)
    player.draw()
    for b in bullets:
        b.draw()
    for t in Enemy:
         t.draw()
    for ex in upsplit:
        ex.draw()
    for ex in downsplit:
        ex.draw()

pgzrun.go()
