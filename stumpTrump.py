from os import chdir
from sys import path 

path.append('resources/controls')

import MotionControl
import cv2
import sys
from random import randint
import pygame
from time import time

#converts images to pygame objects
def imgsetup(img, w, h, setCol):
    temp = pygame.image.load(img).convert()
    if setCol:
        temp.set_colorkey((255, 255, 255))
    temp = pygame.transform.scale(temp, (w, h))
    return temp


chdir('resources/controls')
#control variables
cap = cv2.VideoCapture(0)
size = int(cap.get(4)/2)
hieght = cap.get(4)
width = cap.get(3)
cascPathf = "haarcascade_frontalface_default.xml"
controls = MotionControl.MotionControl(cap, cascPathf)

#pygame variables
pygame.init()
SIZE = [1920, 1080]
canvas = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Motion Game")
canvas.fill((255, 255, 255))
trump = [None, None, None, None, None, None, None, None]
alivetrump = [True, True, True]
chdir("..")
trump[0] = imgsetup("trump1.png", 200, 200, True)
trump[1] = imgsetup("trump2.png", 200, 200, True)
trump[2] = imgsetup("trump3.png", 200, 200, True)
trump[3] = imgsetup("trumpbaby_1.png", 200, 300, True)
trump[4] = imgsetup("trumpbaby_1.png", 300, 300, True)
trump[5] = imgsetup("trumpbaby_2.png", 300, 300, True)
trump[6] = imgsetup("trumpbaby_3.png", 300, 300, True)
trump[7] = imgsetup("explosion.png", 1920, 1080, True)
player = imgsetup("sol.png", 50, 100, True)
background = imgsetup("usa.png", 1920, 1080, False)
font = pygame.font.Font(None, 36)
healthfont = pygame.font.Font(None, 16)


if "-a" in sys.argv:
	sys.argv=["-v", "-p"]

start = True
level = 1
if "-l" in sys.argv:
    start = False
    level = 11
if "-x" in sys.argv:
    start = False
    level = 10
    
hx, hy = 0, 0
baseLine = None
aboveBL = True 
tid = 0
nextlvl = True
hitsize = 200
ghx, ghy = None, None
tpos = [[int(width/2), 0], [randint(50, width-100), 0], [randint(50, width-100), 0]]
tsize = [[100, 100], [100, 100], [100, 100]]
hit = [0, 0, 0]
bhit = 0
nextlvl = True 
img=[]
health = 100
mbhealth = 25
bosshealth = 25 
lvlstrt = 0
win = False
bossstrt = 0
strtcount = 0
temp = 0

while True:
    canvas.fill((255, 255, 255))
    canvas.blit(background, (0, 0))
    if start:
        text = None
        if temp%2==0:
            text = font.render("PUNCH HERE TO PLAY", 1, (255, 0, 0))
        else:
            text = font.render("PUNCH HERE TO PLAY!")
        textpos = text.get_rect()
        textpos.centerx = canvas.get_rect().centerx
        textpos.centery = canvas.get_rect().centery
        canvas.blit(text, textpos)
    if level == 10:
        #print "BOSS WAVE"
        if bossstrt==0:
            bossstrt = time()
        if time()-bossstrt<3:
            text = font.render("DODGE THE TRUMPS", 1, (255, 0, 0))
            textpos = text.get_rect()
            textpos.centerx = canvas.get_rect().centerx
            textpos.centery = canvas.get_rect().centery
            canvas.blit(text, textpos)
    else:
        if nextlvl:
            lvlstrt = time()
        if time()-lvlstrt<3:
            if level!=11:
                text = font.render("LEVEL: "+str(level), 1, (0, 255, 0))
            else:
                text = font.render("ULTIMATE TRUMP", 1, (255, 0, 0))
            textpos = text.get_rect()
            textpos.centerx = canvas.get_rect().centerx
            textpos.centery = canvas.get_rect().centery
            canvas.blit(text, textpos)
    pygame.draw.line(canvas, (0, 255, 0), (0, 0), (int(health*SIZE[0]/100), 0), 20)
    text = healthfont.render("HEALTH", 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = canvas.get_rect().centerx
    textpos.centery = 8
    canvas.blit(text, textpos)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break	
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
    	exit()
    if pygame.key.get_pressed()[pygame.K_r]:
        aboveBL = True
        baseLine = False
    if win:
        font = pygame.font.Font(None, 72)
        text = font.render("YOU WON!", 1, (0, 0, 255))
        textpos = text.get_rect()
        textpos.centerx = canvas.get_rect().centerx
        textpos.centery = canvas.get_rect().centery
        canvas.blit(trump[7], (0, 0))
        canvas.blit(text, textpos)
        pygame.display.flip()
        continue
    controls.setFrame()
    faces = []
    if aboveBL:
        aboveBL = False     
        hx, hy, w, h = controls.getFace()
        baseLine = hy+h
        print baseLine

    
    scaledpos = []
    if nextlvl:
        tpos = []
        img=[]
        hit=[]
        alivetrump = []
        for i in xrange(3):
            trump[i] = pygame.image.load("trump"+str(i+1)+".png").convert()
            trump[i].set_colorkey((255, 255, 255))
            trump[i] = pygame.transform.scale(trump[i], (100, 100))
        for tid in xrange(level):
            scaledpos.append(0)
            hit.append(0)
            tpos.append([randint(50, width-100), 0])
            img.append(randint(0, 2))
            alivetrump.append(True)
        if level == 10:
            for i in xrange(level):
                img[i] = 3
                tpos[i][1] = -200*i
        if level==11:
            tpos = [int(width/2), 0]
            scaledpos = [int((width - tpos[0])*SIZE[0]/width), int(tpos[1]*SIZE[1]/hieght)]
        nextlvl = False
    else:
        for i in xrange(level):
            scaledpos.append(0)
    if level!=11 and not start:
        for tid in xrange(level):
            #tsize[tid][0]+=10
            #tsize[tid][1]+=10
            #tpos[tid][0]-=5
            tpos[tid][1]+=5
            if level==10:
                tpos[tid][1]+=5
            if alivetrump[tid]:
                controls.rectangle((tpos[tid][0], tpos[tid][1]+100), (tpos[tid][0]+100, tpos[tid][1]+200), (0, 0, 255), 2) 
                scaledpos[tid] = [int((width - tpos[tid][0])*SIZE[0]/width), int(tpos[tid][1]*SIZE[1]/hieght)]
                canvas.blit(trump[img[tid]], scaledpos[tid])
    elif not start:
        controls.rectangle((tpos[0], tpos[1]+100), (tpos[0]-200, tpos[1]+300), (255, 0, 0), 2)
        pygame.draw.line(canvas, (255, 0, 0), (0, 20), (int(bosshealth*SIZE[0]/mbhealth), 20), 20)
        text = healthfont.render("BOSS HEALTH", 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = canvas.get_rect().centerx
        textpos.centery = 22
        canvas.blit(text, textpos)
        tpos[1]+=2
        scaledpos = [int((width - tpos[0])*SIZE[0]/width), int(tpos[1]*SIZE[1]/hieght)]
        i=0
        if win:
            i = 7
            scaledpos = [0, 0]
        if bosshealth>10:
            i = 4
        elif bosshealth>5:
            i = 5
        else:
            i = 6
        canvas.blit(trump[i], scaledpos)
        if win:
            pygame.display.flip()
            continue
    hasPrev, cnts = controls.getMotion() 
    if not hasPrev:
        continue
    yavg = 0
    xavg = 0
    counter = 0
    mvLeft = 0
    mvRight = 0
    for c in cnts:
    	if cv2.contourArea(c)<90 or cv2.contourArea(c)>1000:
    		continue
    	(x, y, w, h) = cv2.boundingRect(c)
        if level!=11:
            for tid in xrange(level):   
                if x in range(tpos[tid][0], tpos[tid][0]+100) and y-100 in range(tpos[tid][1], tpos[tid][1]+100):
                    hit[tid]+=1
        if level==11:
            if x in range(tpos[0]-200, tpos[0]) and y in range(tpos[1]+100, tpos[1]+300):
                bhit+=1
        if x in range(0, int(width)/2) and y in range(0, baseLine):
            mvRight+=1
        if x in range(int(width)/2, int(width)) and y in range(0, baseLine):
            mvLeft+=1
        if start:
            if x in range(int(width/2)-100, int(width/2)+100) and y in range(int(hieght/2)-50, int(hieght/2)+50):
                strtcount+=1
        yavg+=(y+(h/2))
        xavg+=(x+(w/2))
        counter += 1
    	#cv2.rectangle(controls.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    if start and strtcount>10:
        start = False
        continue
    if level<10:
        for tid in xrange(level):
            if tpos[tid][1]>int(3*hieght/4):
                if alivetrump[tid]:
                    print "you couldn't stump the trump!"
                    health-=5
                if health<=0:
                    print "you lose! Final score: "+str((level-1)*10)
                    cv2.destroyAllWindows()
                    pygame.display.quit()
                    pygame.quit()
                    exit()
                alivetrump[tid] = False
    
        for tid in xrange(level):
            if hit[tid]>=10 and mvLeft<5 and mvRight<5:
                print "hit"
                alivetrump[tid] = False
                hit[tid] = 0
        remaining = False 
    
        for tid in xrange(level):
            if alivetrump[tid]:
                remaining = True
                break
    
        if not remaining:
            level+=1
            nextlvl = True
    elif level==10:
        for tid in xrange(level):
            if alivetrump[tid] and tpos[tid][1]>hieght:
                print "Nice dodge!"
                alivetrump[tid] = False
        for tid in xrange(level):
            #if hit[tid]>=10:
            #    print "you couldn't stump the trump!"
            #    health-=5
            #    hit[tid] = 0
            if health<=0:
                print "you lose! Final score: "+str((level-1)*10)
                cv2.destroyAllWindows()
                pygame.display.quit()
                pygame.quit()
                exit()
        remaining = False 
    
        for tid in xrange(level):
            if alivetrump[tid]:
                remaining = True
                break
    
        if not remaining:
            level+=1
            nextlvl = True
    else:
        if tpos[1]>hieght:
            print "you lost"
            raw_input()
        if bhit>=15 and mvLeft<5 and mvRight<5:
            bosshealth-=1
            if bosshealth == 0:
                print "you win!"
                win = True
                canvas.blit(trump[7], (0, 0))
                if win:
                    pygame.display.flip()
                    continue
            bhit = 0
    if mvLeft>=5:
        hx+=mvLeft
        if hx > width:
            hx = 0 
    if mvRight>=5:
        hx-=mvRight
        if hx < 0:
            hx = width
    moved = False
    if mvLeft>=5 or mvRight>=5:
        moved = True
    
    if baseLine is not None:
        controls.drawBaseLine(width, baseLine)
    
    if counter>0:	
        yavg/=counter
        xavg/=counter

    
    if "-v" in sys.argv:
        controls.show("Detected motion")
    if level==10 and not nextlvl:
        ghx = int((width-hx)*SIZE[0]/width)
        ghy = int(SIZE[1]-300)#baseLine#int(hy*SIZE[1]/hieght)
        for tid in xrange(level):
            if alivetrump[tid]:
                if ghx in range(scaledpos[tid][0], scaledpos[tid][0]+100):
                    if ghy in range(scaledpos[tid][1], scaledpos[tid][1]+100):
                        print "you couldn't stump the trump"
                        health-=5
                        if health<=0:
                            print "you lose"
                            cv2.destroyAllWindows()
                            pygame.display.quit()
                            pygame.quit()
                            exit()
        pygame.draw.circle(canvas, (255, 0, 0), (ghx, ghy), 10)
        canvas.blit(player, (ghx-5, ghy-5))
    pygame.display.flip()
