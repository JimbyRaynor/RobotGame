import pgzrun, math, random, pygame as pg

WIDTH = 860
HEIGHT = 540
level = 1

bg = pg.image.load("images/arena.png").convert()
play_Area = Rect((0, 0), (WIDTH, HEIGHT))

def createactor(pngname,mypos,mydirectionx,mydirectiony,myspeed):
    a = Actor(pngname, center=mypos, anchor=('center', 'center'))
    a.directionx = mydirectionx
    a.directiony = mydirectiony
    a.speed = myspeed
    return a

player = createactor("robot.png",(WIDTH//2, HEIGHT//2),0,0,2)
player.health = 100


Enemy = []

def create_enemy():
    Enemy.clear()
    for i in range(level+10):
      x =  random.randint(play_Area.left,play_Area.right)
      y =  random.randint(play_Area.top,play_Area.bottom)
      Enemy.append(createactor("t1.png", (x, y), 0,0,0.2))

pl_shootx = 0
pl_shooty = 0
create_enemy()
shooting = False

bullets = []
sprites = []
fire_rate = 0.15
fire_timer = 0

def checkInput():
     global pl_shootx, pl_shooty
     if keyboard.left:  player.directionx = -1
     if keyboard.right: player.directionx  = 1
     if keyboard.up:    player.directiony = -1
     if keyboard.down:  player.directiony  = 1
     if keyboard.d: pl_shootx = 1
     if keyboard.a: pl_shootx = -1
     if keyboard.s: pl_shooty = 1
     if keyboard.w: pl_shooty = -1

def update(dt):
    global shooting, fire_timer, level, pl_shootx,pl_shooty
    # Movement every frame
    checkInput()
    player.x += player.directionx * player.speed
    player.y += player.directiony * player.speed
    player.directionx  = 0
    player.directiony  = 0
    # Clamp the position
    if player.y - 16 < play_Area.top:      player.y = play_Area.top + 16
    elif player.y + 16 > play_Area.bottom: player.y = play_Area.bottom - 16
    if player.x - 16 < play_Area.left:     player.x = play_Area.left + 16
    elif player.x + 16 > play_Area.right:  player.x = play_Area.right - 16

    if any([keyboard[keys.W], keyboard[keys.A], keyboard[keys.S], keyboard[keys.D]]):
        shooting = True
    else:
        shooting = False
        fire_timer = fire_rate
    
    if shooting == True:
        fire_timer += dt
        if fire_timer > fire_rate:
            bullet = createactor("lazer.png", player.pos, pl_shootx,pl_shooty,15)
            bullet.angle = (math.atan2(-pl_shooty, pl_shootx) / (math.pi/180)) - 45
            bullets.append(bullet)
            fire_timer = 0
            pl_shootx = 0
            pl_shooty = 0
    
    for b in bullets:
        for T1 in Enemy:
            if b in bullets:   # bullet could collide with two or more robots 
               if b.collidepoint(T1.center):
                  sprites.append(createactor("t1split",T1.pos,-b.directiony,b.directionx,10)) # (-y,x).(x,y) = 0 and so perpendicular
                  sprites.append(createactor("t1split",T1.pos,b.directiony,-b.directionx,10))  # (y,-x).(x,y) = 0 and so perpendicular
                  Enemy.remove(T1)
                  bullets.remove(b)
    
    for T1 in Enemy:
       if player.x < T1.x:   T1.directionx = -1
       elif player.x > T1.x: T1.directionx = 1
       if player.y > T1.y:   T1.directiony = 1
       elif player.y < T1.y: T1.directiony = -1
       if player.colliderect(T1): player.health = player.health - 1

    for a in Enemy+sprites+bullets:
        a.y = a.y + a.directiony*a.speed
        a.x = a.x + a.directionx*a.speed
        if not a.colliderect(play_Area):
            if a in sprites: sprites.remove(a)
            if a in Enemy: Enemy.remove(a)
            if a in bullets: bullets.remove(a)
      
    if len(Enemy) < 1 :
        level = level + 1
        create_enemy()
        
def draw():
    screen.blit(bg, (0, 0))
    screen.draw.text("Level "+str(level),(310,10),owidth=0.5, ocolor=(255,0,0),color=(255,255,0),fontsize=100)
    screen.draw.text("Movement: Arrow keys                Fire: W,A,S,D",(200,510),fontsize=30)
    screen.draw.text("Health: "+str(player.health),(700,10),fontsize=30)
    player.draw()
    for a in Enemy+sprites+bullets:
        a.draw()
        
pgzrun.go()
