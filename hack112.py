from cmu_cs3_graphics import *
from PIL import Image
import math, copy, random, time

#################################################
# Helper functions from: https://www.cs.cmu.edu/~112/notes/notes-variables-and-functions.html#RecommendedFunctions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

##################################################

def onAppStart(app):
    app.time=0
    app.bossTimerJump=0
    app.bossTimerAtk=0
    app.stepsPerSecond=100
    app.meme = False
    app.gameOver = False
    app.pause = False
    app.win = False
    app.lose = False
    app.start = False
    if app.meme: #if we doing it, having meme images
        app.knightpic=Image.open('amongus.png')
    #(fix draw stuff here)
    else:
        #knightpic from https://hollowknight.fandom.com/wiki/Knight?file=The+Knight+Idle.png
        app.knightpic= Image.open('knight.png')
    #loading in images, from same folder
    #backgroundim from: https://hollowknight.fandom.com/wiki/False_Knight?file=Screenshot_HK_False_Knight_01.png
    app.backgroundim =Image.open('background.png')
    app.backgroundim = CMUImage(app.backgroundim)
    #bosspic from: https://villains.fandom.com/wiki/False_Knight?file=False_Knight.png
    #facing right
    app.bosspic=Image.open('boss.png')
    #deadboss from: https://hollowknight.fandom.com/wiki/False_Knight?file=False+Knight+Unmasked.png
    #facing right
    app.deadboss=Image.open('deadboss.png')
    # app.deadknight=Image.open('deadknight.png')
    #game over screen from: https://hollowknight.fandom.com/wiki/Steel_Soul_Mode?file=Steel_Soul_Game_Over.png
    app.gameoverimg =CMUImage(Image.open('gameOver.png'))
    #image from: https://www.reddit.com/r/HollowKnight/comments/ld7tgb/i_did_it_thats_the_only_after_credits_massage/
    app.gameoverWin = CMUImage(Image.open('gameOverWin.png'))
    #attack image from: https://drive.google.com/drive/folders/1kyg661EDV45McoJQNmwbIXqYgniN48PU
    app.knightattack=Image.open('knightAtk.png')
    #image from: https://frictionlit.org/july-staff-picks-action-adventure-games-k-drama-grim-reapers-and-podcasts/
    app.startScreen = CMUImage(Image.open('startScreen.jpg'))
    #image from: https://interfaceingame.com/screenshots/hollow-knight-game-menu/
    app.pauseMenu = CMUImage(Image.open('pauseMenu.jpg'))
    
    app.bossatkCounter = 0
    #boss images from: https://www.spriters-resource.com/pc_computer/hollowknight/sheet/132959/
    bossatkNames = ['bossdab.png', 'bossjump.png','bossland.png']
    bossatkImages=[]
    for im in bossatkNames:
        for i in range(8): bossatkImages.append(Image.open(im))

    app.bossatk = 3*[app.bosspic]+ bossatkImages  +8*[bossatkImages[-1]]
    

    #boss atk images from: https://www.spriters-resource.com/pc_computer/hollowknight/sheet/132959/
    app.bossBasicAtk = 5*[Image.open('bossBasicAtk1.png')]+5*[ Image.open('bossBasicAtk2.png')]+15*[Image.open('bossBasicAtk3.png')]+5*[app.bosspic]

    #character info or objects
    #knight
    knightHeight, knightWidth = app.knightpic.height,app.knightpic.width
    knightX = app.width/16; knightY = 502
    app.knight=Knight(knightX, knightY, knightHeight, knightWidth)
    
    #boss
    bossHeight, bossWidth = app.bosspic.height, app.bosspic.width
    bossX = app.width*(1/2) 
    bossY = 502
    app.boss=Boss(bossX, bossY, bossHeight, bossWidth)
   
def onStep(app): 
    if (app.gameOver or app.pause or not app.start):
        return
    if (app.boss.getHealth()<=0):
        app.gameOver = True
        app.win = True
    elif (app.knight.getHealth()<=0):
        app.gameOver = True
        app.lose = True
    if (not app.start):
        app.pause = True
    if (app.start):
        app.time+=1

    if app.knight.attackframe>0:
        app.knight.attackframe-=1
    
    if app.time%75==0:
        app.boss.attackKnight(app,app.knight)
        print('attack')
    if app.bossTimerAtk==29:
        app.knight.isAttacking=False
        app.bossTimerAtk=0
    if app.boss.isAttacking:
        app.bossTimerAtk+=1
    
    if app.boss.dy != 0:
        app.boss.isJumping=True
        app.boss.loc[0] -= app.boss.dx
        app.boss.loc[1] -= app.boss.dy
        app.boss.dy -= 2
        app.bossTimerJump+=1
            
    if app.boss.loc[1] + app.boss.height >= 502:
        app.boss.loc[1] = 502 - app.boss.height
        app.boss.dy = 0
        app.bossTimerJump=0
        app.boss.isJumping = False
    
    if app.knight.jumpTime >= 10:
        app.knight.jumping = False
    if app.knight.dy != 0 and app.knight.jumping == True:
        app.knight.loc[1] -= app.knight.dy
    elif app.knight.dy != 0 and app.knight.jumping == False:
        app.knight.loc[1] -= app.knight.dy
        app.knight.dy -= 11
    
    #gravity limit on the knight (does not apply to the boss)
#    if app.knight.dy <= -10:
#        app.knight.dy = -10

    #502 is y coordinate of bottom of knight
    if app.knight.loc[1] + app.knight.height >= 502:
        app.knight.loc[1] = 502 - app.knight.height
        app.knight.dy = 0
        app.knight.jumpTime = 0 
  
def onKeyHold(app, keys):
    if (not app.start):
        app.time = 0
    if (app.gameOver or not app.start or app.pause):
        return
    if 'left' in keys:
        #move knight left (depends on char speed)
        app.knight.move(app.width, app.height,-1,0)
        app.knight.setDir('left')
        # if outOfBounds(app,app.knight.getLoc()):
        #     app.knight.move(1,0)
    if "right" in keys:
        #move knight right
        app.knight.move(app.width,app.height,1,0)
        app.knight.setDir('right')
    if "z" in keys:
        if app.knight.loc[1] >= 502 - app.knight.height:
            app.knight.jumping = True
            app.knight.loc[1] -= 1
        if app.knight.jumpTime<30 and app.knight.jumping == True:
            app.knight.jump()
            app.knight.jumpTime+=1
    else:
        app.knight.jumping = False

def onKeyPress(app, key):
    if (app.gameOver):
        if (key=='space'):
            onAppStart(app)
        return
    if (not app.start):
        if (key=='space'):
            app.pause = False
            app.start = True
    if(key == 'x' and app.start and not app.paused):
        app.knight.attackBoss(app.boss)
    if (key == 'escape'):
        app.pause = not app.pause
    # if (key == 'tab'):
    #     app.start = False
    #if (key == 'z'):
    #    app.knight.jump()
    # if (key == 'tab'):
    #     app.meme = True
    
def onKeyRelease(app, key):
    if (key == 'z'):
        app.knight.jumping = False

# changes movement, attack, and jump

def outOfBounds(app,L):
    x,y=L
    return not(x>0 and x<app.width and y>0 and y<app.height)

################################ Classes ####################################
class Knight():
    def __init__(self, x, y, height, width):
        self.attackframe=0
        self.height, self.width = height, width
        self.color = 'blue'
        self.loc = [x, y]
        self.health=5
        self.speed=20
        self.attack=5
        self.dir="right"
        self.iframe=[0,False]
        self.hitbox = [self.loc[0]-self.width,self.loc[1]-self.height,self.loc[0]+self.width,self.loc[1]+self.height]
        self.dy = 0
        self.jumpTime = 0
        self.jumping = False
        #[0] = left, [1] = top, [2] = right, [3] = bottom

    def getBounds(self):
        return self.width, self.height

    def getDir(self): return self.dir
    def setDir(self,dir):  self.dir=dir

    def hitbox(self):
        self.hitbox = [self.loc[0]-self.width,self.loc[1]-self.height,self.loc[0]+self.width,self.loc[1]+self.height]        
        return self.hitbox

    def getHealth(self):
        return self.health
        
    def getLoc(self):
        return self.loc

    def getSpeed(self): #not sure if this is needed
        return self.speed

    def damageBoss(self, x):
        self.health -= x

    def attackBoss(self,boss):
        self.attackframe=5
        if (boss.loc[0] - self.width <= self.loc[0] <= boss.loc[0] + boss.width and 
            boss.loc[1] - self.height <= self.loc[1] <= boss.loc[1] + boss.height):
            boss.takeDamage(self.attack)
            
    
    def move(self,maxx,maxy,dx,dy):
        for i in range(self.speed):
            if (self.loc[0]+dx)>0 and (self.loc[0]+self.width)+dx<maxx: #stay in range
                self.loc[0]+=dx
            if (self.loc[1])+dy>0 and (self.loc[1]+self.height)+dy<maxy: #stay in range
                self.loc[1]+=dy
        # if outOfBounds(app,self.loc()):pass
    
    def takeDamage(self, int):
        self.health-=int
        # if self.iframe[1]:
        #     self.iframe[0]-=1
        #     if self.iframe[0]==0: self.iframe[1]=False
        # else: 
        #     self.health-=int
        #     self.iframe=[5,True]

    def heal(self,int):
        self.health+=int

    def jump(self):
        self.jumping == True
        self.dy = 20

class Boss:
    def __init__(self, x, y, height, width):
        self.height, self.width = height, width
        self.loc = [x,y]
        self.height=height
        self.width=width
        self.health=65
        self.speed=10
        self.dir="left"
        self.movetime=0
        self.hitbox = [self.loc[0]-self.width,self.loc[1]-self.height,self.loc[0]+self.width,self.loc[1]+self.height]
        self.isAttacking = False
        self.dy = 0
        self.dx = 0
        self.isJumping = False
        #[0] = left, [1] = top, [2] = right, [3] = bottom
    
    def getBounds(self):
        return self.width, self.height
        
    def hitbox(self):
        self.hitbox = [self.loc[0]-self.width,self.loc[1]-self.height,self.loc[0]+self.width,self.loc[1]+self.height]
        return self.hitbox

    def getHealth(self):
        return self.health
        
    def getLoc(self):
        return self.loc

    def getSpeed(self): #not sure if this is needed
        return self.speed

    def getDir(self): return self.dir
    def setDir(self,dir):  self.dir=dir

    def takeDamage(self, x):
        self.health -= x
    
    def jump(self,knight):
        # self.xspeed=[] #jump a certain height
        self.dy = 31
        targetX = knight.loc[0] + knight.width/2 
        self.dx = (self.loc[0] - targetX) / 50

    def attackKnight(self,app,knight):
        # atk=random.randint(1,10) #we want a random attack
        if (self.loc[0] - knight.width <= knight.loc[0] <= self.loc[0] + self.width and
            self.loc[1] - knight.height <= knight.loc[1] <= self.loc[1] + self.height):
            # if self.isAttacking==False and self.isJumping==False:
            self.isAttacking=True
            self.normalAttack(knight)
                # if atk >9:
                #     return self.bigAttack(knight) #define 
                # if atk >4:
                #     return self.smallAttack(knight) #define
                # else:
                #     return self.normalAttack(knight) #define
        elif self.isJumping == False: #jump towards knightselfisJumping == False:
            self.isJumping = True
            self.jump(knight)
            if knight.loc[0] >self.getLoc()[0]:
                self.dir="right"
            else: 
                self.dir="left"
    
    # def bigAttack(self, knight):
    #     #play animation
    #     knight.takeDamage(1)
    
    # def smallAttack(self, knight):
    #     #play animation
    #     knight.takeDamage(1)

    def normalAttack(self, knight):
        knight.takeDamage(1)
    
################################ Graphics ####################################
def redrawAll(app):
    #background
    drawBoard(app)
    
    #characters
    drawKnight(app)
    drawBoss(app)

    #health bars
    drawHealth(app, 0,0,5,app.knight.getHealth())
    drawHealth(app, app.width-65*10,0,65*10,app.boss.getHealth())

    #hitboxes
    drawHitboxes(app)
    
    #start screen
    if not app.start:
        drawImage(app.startScreen, 0, 0, width=app.width, height=app.height)
        drawLabel('Press space to start', app.width/2, app.height*(7/8), fill='white', size=30, font='monospace')
    #game over screens
    if app.gameOver:
        #win screen
        if app.win: 
            drawImage(app.gameoverWin, 0, 0, width=app.width, height=app.height)
            drawRect(app.width/2-350/2, app.height*(6/8), 350, 100, fill='black')
            drawLabel('Press space to play again', app.width/2+10, app.height*(6.5/8), fill='white', size=30, font='monospace')     
        #lose screen
        elif app.lose:
            drawImage(app.gameoverimg, 0,0, width=app.width, height=app.height)
            drawRect(app.width/2-350/2, app.height*(6/8), 350, 100, fill='black')
            drawLabel('Press space to play again', app.width/2+10, app.height*(6/8), fill='white', size=30, font='monospace')  
    #pause screen
    if app.start and app.pause:
        drawImage(app.pauseMenu, 0, 0, width=app.width, height=app.height)
        drawRect(app.width/2-100, app.height/2-70, 200, 140, fill='black')
        drawLabel('esc to unpause', app.width/2, app.height/2-30, fill='white', font='monospace', size=17)   
        # drawLabel('tab for menu', app.width/2, app.height/2-10, fill='white', font='monospace', size=17)   
        drawLabel('h for help', app.width/2, app.height/2+10, fill='white', font='monospace', size=17)
    
    drawLabel('Made by sun garden', app.width/2, app.height-20, fill='white', font='monospace', size=17)   

def drawBoard(app):
    drawImage(app.backgroundim, 0,0, width=app.width, height=app.height)

def drawHealth(app, x, y, maxhealth, health):
    #draw rect takes in (leftX, topY, width, height)
    drawRect(x,y,maxhealth*10,10, fill="grey")
    if (health>0):
        drawRect(x,y,health*10,10, fill="red")

def drawKnight(app):
    x,y=app.knight.getLoc()
    width, height = app.knight.getBounds()
    if app.knight.getDir()=="right":
        if app.knight.attackframe>0:
            b=copy.copy(app.knightattack)
            drawImage(CMUImage(tran(app,b)),x, y,width=app.knightattack.width/2,height=app.knightpic.height)
        drawImage(CMUImage(app.knightpic),x, y)
    else:
        if app.knight.attackframe>0:
            drawImage(CMUImage(app.knightattack),x-width*2, y,width=app.knightattack.width/2,height=app.knightpic.height)
        a=copy.copy(app.knightpic)
        drawImage(CMUImage(tran(app,a)),x, y)

def drawBoss(app):
    x,y=app.boss.getLoc()
    if app.boss.isJumping:#in air
        a=app.bossatk[app.bossTimerJump%35]
        if app.boss.getDir()=="right":
            drawImage(CMUImage(a),x,y-(a.height)/2)
        else:
            b=copy.copy(a)
            drawImage(CMUImage(tran(app,b)),x, y-(a.height)/2)
    elif app.boss.isAttacking:
        a=app.bossBasicAtk[(app.bossTimerAtk)%30]
        if app.boss.getDir()=="right":
            drawImage(CMUImage(a),x,502-a.height)
        else:
            b=copy.copy(a)
            drawImage(CMUImage(tran(app,b)),x, 502-a.height)
    
    else:
        if app.boss.getDir()=="right":
            drawImage(CMUImage(app.bosspic),x, y)
        else:
            a=copy.copy(app.bosspic)
            drawImage(CMUImage(tran(app,a)),x, y)
    # if app.isBossAtking:
    #     for image in app.bossatk:
    #         drawImage(CMUImage(image),x,y)

def drawHitboxes(app):
    drawCircle(app.boss.loc[0], app.boss.loc[1], 15, fill = "red")
    drawCircle(app.knight.loc[0], app.knight.loc[1], 15, fill = "red")
    drawLine(app.boss.loc[0], 0, app.boss.loc[0], 3000, fill="red")
    drawLine(app.boss.loc[0] + app.boss.width, 0, app.boss.loc[0] + app.boss.width, 3000, fill="red")
    drawLine(app.knight.loc[0] + app.knight.width, 0, app.knight.loc[0] + app.knight.width, 3000, fill="red")
    drawLine(app.knight.loc[0], 0, app.knight.loc[0], 3000, fill="red")

def tran(app,image):
    return image.transpose(Image.FLIP_LEFT_RIGHT)

def runHollowKnight():
    print('Running Hollow Knight!')
    runApp(width=1200, height=600)
    
runHollowKnight()