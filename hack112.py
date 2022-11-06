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
    app.stepsPerSecond=24

    app.time=0
    app.bossTimerJump=0
    app.bossTimerAtk=0
    app.gameOver = False
    app.pause = False
    app.help = False
    app.win = False
    app.lose = False
    app.start = False
    app.isMeme = False
    app.onGround = False

    #loading in images, from same folder
    #backgroundim from: https://hollowknight.fandom.com/wiki/False_Knight?file=Screenshot_HK_False_Knight_01.png
    app.backgroundim =Image.open('background.png')
    app.backgroundim = CMUImage(app.backgroundim)
    #knightpic from https://hollowknight.fandom.com/wiki/Knight?file=The+Knight+Idle.png
    app.knightpic= Image.open('knight.png')
    #bosspic from: https://villains.fandom.com/wiki/False_Knight?file=False_Knight.png
    #facing right
    app.bosspic=Image.open('boss.png')
    # #deadboss from: https://hollowknight.fandom.com/wiki/False_Knight?file=False+Knight+Unmasked.png
    # #facing right
    # app.deadboss=Image.open('deadboss.png')
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
    #music: False Knight, Christopher Larkin, Hollow Knight Original Soundtrack (2017)
    app.music = Sound('https://vgmsite.com/soundtracks/hollow-knight-original-soundtrack/iqtelxkifc/04.%20False%20Knight.mp3')
    #music: Title Theme, Christopher LarkinHollow Knight Original Soundtrack (2017)
    # app.startMusic = Sound('file:///C:/Users/sunny/Downloads/hack112/hollow%20knight%20theme.mp3')
    #rockstar sound credit: https://archive.org/details/AllStar, technically credit to singer: Smash Mouth
    app.rockstar=Sound('https://ia600306.us.archive.org/16/items/AllStar/SmashMouth-AllStar.mp3')
    
    app.bossatkCounter = 0
    #boss images from: https://www.spriters-resource.com/pc_computer/hollowknight/sheet/132959/
    bossatkNames = ['bossdab.png', 'bossjump.png','bossland.png']
    bossatkImages=[]
    for im in bossatkNames:
        for i in range(8): bossatkImages.append(Image.open(im))

    app.bossatk = 3*[app.bosspic]+ bossatkImages  +10*[bossatkImages[-1]]
    

    #boss atk images from: https://www.spriters-resource.com/pc_computer/hollowknight/sheet/132959/
    app.bossBasicAtk = 5*[Image.open('bossBasicAtk1.png')]+5*[ Image.open('bossBasicAtk2.png')]+15*[Image.open('bossBasicAtk3.png')]+5*[app.bosspic]

    init(app)

def init(app):
    app.time=0
    app.bossTimerJump=0
    app.bossTimerAtk=0
    app.isMeme = False
    app.win, app.lose = False,False
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
    if app.gameOver == False and app.pause == False and app.help == False:
        takeStep(app)
        

def takeStep(app):
    if (not app.start):
        #app.startMusic.play(loop=True)
        app.pause = True
    if (app.start):
        app.time+=1
        if app.time==1000: app.time=0
        #app.startMusic.pause()
        if app.isMeme:
            app.rockstar.play(loop=True)
            app.music.pause()
        else:
            app.music.play(loop=True)
            app.rockstar.pause()
    if (app.gameOver or app.pause or not app.start):
        if app.isMeme:
            app.rockstar.pause()
        else:
            app.music.pause()
    if (app.boss.getHealth()<=0):
        app.gameOver = True
        app.win = True
    elif (app.knight.getHealth()<=0):
        app.gameOver = True
        app.lose = True

    if app.knight.attackframe>0:
        app.knight.attackframe-=1
    
    if app.time%75==0 and app.time!=0:
        app.boss.attackKnight(app,app.knight)
    if app.bossTimerAtk>=29:
        app.boss.isAttacking=False
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
    
    if app.knight.jumpTime >= 8:
        app.knight.jumping = False
    
    if app.knight.dy != 0 and app.knight.jumping == True:
        app.knight.loc[1] -= app.knight.dy

    elif app.knight.dy != 0 and app.knight.jumping == False:
        app.knight.loc[1] -= app.knight.dy
        app.knight.dy -= 14
    
    #gravity limit on the knight (does not apply to the boss)
    if app.knight.dy <= -51:
        app.knight.dy = -51

    #502 is y coordinate of bottom of knight
    if app.knight.loc[1] + app.knight.height >= 502:
        app.knight.loc[1] = 502 - app.knight.height
        app.knight.dy = 0
        app.onGround = True

#CASES TO DEAL DAMAGE TO KNIGHT
    #if knight's hitbox collides with boss hitbox
        #case for if boss is jumping (wider hitbox with some space below to dodge)
    if app.boss.isJumping:
        if (app.boss.loc[0] - app.knight.width <= app.knight.loc[0] <= app.boss.loc[0] + app.boss.width and
            app.boss.loc[1] - app.knight.height <= app.knight.loc[1] <= app.boss.loc[1] + app.boss.height/2):
            app.knight.takeDamage(1)   
        #case for if boss is attacking (full hitbox)     
    elif app.boss.attackFrame > 11:
        if (app.boss.loc[0] - app.knight.width <= app.knight.loc[0] <= app.boss.loc[0] + app.boss.width and
            app.boss.loc[1] - app.knight.height <= app.knight.loc[1] <= app.boss.loc[1] + app.boss.height):
            app.knight.takeDamage(1)
    else:
        #case for if boss is standing still (smaller hitbox)
        if (app.boss.loc[0] + 50 <= app.knight.loc[0] <= app.boss.loc[0] + app.boss.width - app.knight.width - 50 and
            app.boss.loc[1] <= app.knight.loc[1] <= app.boss.loc[1] + app.boss.height):
            app.knight.takeDamage(1)


    #makes the boss face the knight at all times
    if app.knight.loc[0] + app.knight.width/2 >app.boss.getLoc()[0] + app.boss.width/2:
        app.boss.dir="right"
    else: 
        app.boss.dir="left"

    #counts the boss's attack frames so there's a small delay before he deals damage
    if app.boss.isAttacking == True:
        app.boss.attackFrame += 1
    if app.boss.attackFrame >= 30:
        app.boss.isAttacking = False
        app.boss.attackFrame = 0

    #iframes will count down when they're active, then deactivate at 0
    if app.knight.iframes[0] == True:
        app.knight.iframes[1] -= 1
    if app.knight.iframes[1] <= 0:
        app.knight.iframes = [False, 60]

def onKeyHold(app, keys):
    if (not app.start):
        app.time = 0
    if not (app.gameOver or not app.start or app.pause or app.help):
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

            if app.knight.jumpTime<8 and app.knight.jumping == True:
                app.knight.jump()
                app.knight.jumpTime+=1

        else:
            app.knight.jumping = False

def onKeyPress(app, key):
    if (app.gameOver):
        if (key=='space'):
            init(app)
            app.gameOver=False
    if (not app.start):
        if (key=='space'):
            app.pause = False
            app.start = True
            app.time = 0
    if(key == 'x' and app.start and not app.pause):
        app.knight.attackBoss(app.boss)
    if (key == 'escape'):
        app.pause = not app.pause
        app.help = False
    if (key == 'h' and app.pause):
        app.help = not app.help
    if (key == 'tab'):
        app.isMeme = not app.isMeme
        meme(app)
    if key == "z":
        app.onGround = False

def onKeyRelease(app, key):
    if (key == 'z') and (app.onGround):
        app.knight.jumping = False
        app.knight.dy -= 31
        app.knight.jumpTime = 0

# changes movement, attack, and jump

def outOfBounds(app,L):
    x,y=L
    return not(x>0 and x<app.width and y>0 and y<app.height)

def meme(app):
    #amongus credit: https://pixabay.com/illustrations/among-us-icon-crewmate-imposter-6008615/
    app.amongus=Image.open('amongus.png')
    #shrek credit: https://www.deviantart.com/darkwoodsx/art/shrek-head-png-2-673125213
    app.shrek=Image.open('shrek.png')

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
        self.iframes = [False,60]
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
        if self.iframes[0] == False:
            self.health-=int
            self.iframes[0] = True

    def heal(self,int):
        self.health+=int

    def jump(self):
        self.jumping == True
        self.dy = 30

class Boss:
    def __init__(self, x, y, height, width):
        self.height, self.width = height, width
        self.loc = [x,y]
        self.height=height
        self.width=width
        self.health=260
        self.speed=10
        self.dir="left"
        self.movetime=0
        self.hitbox = [self.loc[0]-self.width,self.loc[1]-self.height,self.loc[0]+self.width,self.loc[1]+self.height]
        self.isAttacking = False
        self.attackFrame = 0
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
        self.dx = (self.loc[0] + self.width/2 - targetX) / 50

    def attackKnight(self,app,knight):
        # atk=random.randint(1,10) #we want a random attack
        if (self.loc[0] - knight.width <= knight.loc[0] <= self.loc[0] + self.width and
            self.loc[1] - knight.height <= knight.loc[1] <= self.loc[1] + self.height):
            # if self.isAttacking==False and self.isJumping==False:
            self.isAttacking=True
        elif self.isJumping == False: #jump towards knightselfisJumping == False:
            self.isJumping = True
            self.jump(knight)

    
################################ Graphics ####################################
def redrawAll(app):
    #background
    drawBoard(app)
    
    #characters
    drawKnight(app)
    drawBoss(app)

    #health bars
    drawHealth(app, 50,10,5,app.knight.getHealth())
    drawHealth(app, app.width-400,10,260/10,app.boss.getHealth()/10)

    #hitboxes
    # drawHitboxes(app)
    
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
    if app.start and app.pause and not app.help:
        drawImage(app.pauseMenu, 0, 0, width=app.width, height=app.height)
        drawRect(app.width/2-100, app.height/2-70, 200, 140, fill='black')
        drawLabel('esc to unpause', app.width/2, app.height/2-30, fill='white', font='monospace', size=17)   
        drawLabel('tab & unpause for a surprise ;)', app.width/2, app.height/2-10, fill='white', font='monospace', size=17)   
        drawLabel('h for help when paused', app.width/2, app.height/2+10, fill='white', font='monospace', size=17)

    #help screen
    if app.start and app.pause and app.help:
        # drawImage(app.pauseMenu, 0, 0, width=app.width, height=app.height)        
        # drawRect(app.width/2-100, app.height/2-70, 200, 140, fill='black')
        drawRect(0, 0, app.width, app.height, fill='black')
        drawLabel('Controls:', app.width/2, app.height/2-30, fill='white', font='monospace', size=17)   
        drawLabel('Left and Right to move, Z to jump, X to attack', app.width/2, app.height/2-10, fill='white', font='monospace', size=17)   
        drawLabel('h to close help menu, Esc to pause/unpause, tab for funny stuff', app.width/2, app.height/2+10, fill='white', font='monospace', size=17)
    
    if app.start and not app.paused:
        drawLabel('Press esc to pause', app.width/2, app.height-40, fill='white', font='monospace', size=17)   
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
    if app.isMeme:
        if app.knight.getDir()=="right":
            drawImage(CMUImage(app.amongus),x, y)
        else:
            b=copy.copy(app.amongus)
            drawImage(CMUImage(tran(app,b)),x, y)

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
        a=app.bossBasicAtk[(app.bossTimerAtk)%32]
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
    if (app.isMeme):
        if app.boss.getDir()=="right":
            drawImage(CMUImage(app.shrek),x, y)
        else:
            a=copy.copy(app.shrek)
            drawImage(CMUImage(tran(app,a)),x, y)

def drawHitboxes(app):
    drawCircle(app.boss.hitbox[0], app.boss.hitbox[1], 15, fill = "red")
    drawCircle(app.knight.hitbox[0], app.knight.hitbox[1], 15, fill = "red")
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