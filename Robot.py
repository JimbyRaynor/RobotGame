import pgzrun, math, random, pygame as pg

WIDTH = 860
HEIGHT = 540
level = 1
game_state = 0 # 0 is play, 1 is gameover

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
player.shootx = 0
player.shooty = 0
player.shooting = False
player.fire_timer = 0
player.score = 0
player.highscore = 800
fire_rate = 0.20
enemyspeed = 0.2

try: 
   hifile = open("robothiscore.dat","r")
except:
   print("No highscore file ... will create later")
else:
    try:
         player.highscore = int(hifile.readline())
    except:
         player.highscore = 800
    hifile.close()

Enemy = []

def create_enemy():
    Enemy.clear()
    for i in range(level+10):
      x =  random.randint(play_Area.left,play_Area.right)
      y =  random.randint(play_Area.top,play_Area.bottom)
      Enemy.append(createactor("t1.png", (x, y), 0,0,enemyspeed))

create_enemy()
bullets = []
sprites = []



def checkInput():
     if keyboard.left:  player.directionx = -1
     if keyboard.right: player.directionx  = 1
     if keyboard.up:    player.directiony = -1
     if keyboard.down:  player.directiony  = 1
     if keyboard.d: player.shootx = 1
     if keyboard.a: player.shootx = -1
     if keyboard.s: player.shooty = 1
     if keyboard.w: player.shooty = -1

def moveplayer():
    player.x += player.directionx * player.speed
    player.y += player.directiony * player.speed
    player.directionx  = 0
    player.directiony  = 0
    # Clamp the position
    if player.y - 16 < play_Area.top:      player.y = play_Area.top + 16
    elif player.y + 16 > play_Area.bottom: player.y = play_Area.bottom - 16
    if player.x - 16 < play_Area.left:     player.x = play_Area.left + 16
    elif player.x + 16 > play_Area.right:  player.x = play_Area.right - 16

def shoot(dt):
    if any([keyboard[keys.W], keyboard[keys.A], keyboard[keys.S], keyboard[keys.D]]):
        player.shooting = True
    else:
        player.shooting = False
        player.fire_timer = fire_rate
    
    if player.shooting == True:
        player.fire_timer += dt
        if player.fire_timer > fire_rate:
            player.score -= 5
            if player.score < 0: player.score = 0
            bullet = createactor("lazer.png", player.pos, player.shootx,player.shooty,15)
            bullet.angle = (math.atan2(-player.shooty, player.shootx) / (math.pi/180)) - 45
            bullets.append(bullet)
            player.fire_timer = 0
            player.shootx = 0
            player.shooty = 0

def checkcollisions():
    for b in bullets:
        for T1 in Enemy:
            if b in bullets:   # bullet could collide with two or more robots 
               if b.collidepoint(T1.center):
                  sprites.append(createactor("t1split",T1.pos,-b.directiony,b.directionx,10)) # (-y,x).(x,y) = 0 and so perpendicular
                  sprites.append(createactor("t1split",T1.pos,b.directiony,-b.directionx,10))  # (y,-x).(x,y) = 0 and so perpendicular
                  Enemy.remove(T1)
                  bullets.remove(b)
                  player.score += 15
                  if player.score > player.highscore:
                      player.highscore = player.score
    
def moveenemy():
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

def update(dt):
    global level, game_state, enemyspeed
    if game_state == 0:
       checkInput()
       moveplayer()
       shoot(dt)
       checkcollisions()
       moveenemy()
       if player.health <= 0 and (game_state == 0):
            game_state = 1
            player.health = 0
            hifile = open("robothiscore.dat","w")
            hifile.write(str(player.highscore))
            hifile.close()
       if len(Enemy) < 1 :
         level = level + 1
         create_enemy()
         player.x = WIDTH//2
         player.y = HEIGHT//2
         if level <= 5:
            enemyspeed += 0.2
         else:
            enemyspeed += 0.1
    if (keyboard.c) and (game_state == 1):
      game_state = 0
      player.health = 100
      player.x = WIDTH//2
      player.y = HEIGHT//2
      player.score = 0
      level = 1
      enemyspeed = 0.2
      create_enemy()
      
def draw():
    screen.blit(bg, (0, 0))
    screen.draw.text("Level: "+str(level),(410,10),fontsize=30)
    screen.draw.text("Score: "+str(player.score),(10,10),fontsize=30)
    screen.draw.text("High Score: "+str(player.highscore),(670,10),fontsize=30)
    screen.draw.text("Movement: Arrow keys                Fire: W,A,S,D",(200,510),fontsize=30)
    screen.draw.text("Health: "+str(player.health),(10,40),fontsize=30)
    player.draw()
    for a in Enemy+sprites+bullets:
        a.draw()
    if game_state == 1:
        screen.draw.text("Game Over ",(40,200),owidth=0.5, ocolor=(255,0,0),color=(255,255,0),fontsize=200)
        screen.draw.text("Press   c  to play again",(50,350),owidth=0.5, ocolor=(0,0,255),color=(0,255,255),fontsize=100)
          
pgzrun.go()
