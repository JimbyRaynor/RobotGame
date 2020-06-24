# adapted from wireframe code twinstickshooter.py
import pgzrun

import pygame as pg
import math

WIDTH = 860
HEIGHT = 540

bg = pg.image.load("images/arena.png").convert()
play_Area = Rect((150, 75), (560, 390))

player = Actor("robot.png", center=(WIDTH//2, HEIGHT//2), anchor=('center', 'center'))
pl_movement = [0, 0]
pl_move_speed = 2

pl_rotation = [0, 0]

shooting = False

bullets = []
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
    global shooting, bullets, fire_timer

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
            bullet = {}
            bullet["actor"] = Actor("lazer.png", center=player.pos, anchor=('center', 'center'))
            bullet["direction"] = pl_rotation.copy()                                           
            bullet["actor"].angle = desired_angle
            bullets.append(bullet)
            fire_timer = 0
            pl_rotation[1] = 0
            pl_rotation[0] = 0
    
    bullets_to_remove = []
    for b in bullets:
        b["actor"].x += b["direction"][0] * bullet_speed 
        b["actor"].y += b["direction"][1] * bullet_speed
        if not b["actor"].colliderect(play_Area):
            bullets_to_remove.append(b)
    
    for b in bullets_to_remove:
        bullets.remove(b)


def draw():
    screen.blit(bg, (0, 0))
    player.draw()
    for b in bullets:
        b["actor"].draw()


pgzrun.go()
