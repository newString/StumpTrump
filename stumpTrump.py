import cv2
import sys
from random import randint
import pygame
from time import time
from os import chdir
chdir('resources')
pygame.init()
SIZE = [1920, 1080]
canvas = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Motion Game")
#canvas = pygame.Surface(screen.get_size())
#nvas = canvas.convert()
canvas.fill((255, 255, 255))

trump = [None, None, None, None, None, None, None, None]
alivetrump = [True, True, True]
trump[0] = pygame.image.load("trump1.png").convert()
trump[0].set_colorkey((255, 255, 255))
trump[0] = pygame.transform.scale(trump[0], (200, 200))
trump[1] = pygame.image.load("trump2.png").convert()
trump[1].set_colorkey((255, 255, 255))
trump[1] = pygame.transform.scale(trump[1], (200, 200))
trump[2] = pygame.image.load("trump3.png").convert()
trump[2].set_colorkey((255, 255, 255))
trump[2] = pygame.transform.scale(trump[2], (200, 200))
trump[3] = pygame.image.load("trumpbaby_1.png").convert()
trump[3].set_colorkey((255, 255, 255))
trump[3] = pygame.transform.scale(trump[3], (200, 300))

trump[4] = pygame.image.load("trumpbaby_1.png").convert()
trump[4].set_colorkey((255, 255, 255))
trump[4] = pygame.transform.scale(trump[4], (300, 300))
trump[5] = pygame.image.load("trumpbaby_2.png").convert()
trump[5].set_colorkey((255, 255, 255))
trump[5] = pygame.transform.scale(trump[5], (300, 300))
trump[6] = pygame.image.load("trumpbaby_3.png").convert()
trump[6].set_colorkey((255, 255, 255))
trump[6] = pygame.transform.scale(trump[6], (300, 300))
trump[7] = pygame.image.load("explosion.png").convert()
trump[7].set_colorkey((255, 255, 255))
trump[7] = pygame.transform.scale(trump[7], (1920, 1080))

player = pygame.image.load("sol.png").convert()
player.set_colorkey((255, 255, 255))
player = pygame.transform.scale(player, (50, 100))

background = pygame.image.load("usa.png").convert()
background = pygame.transform.scale(background, (1920, 1080))

if "-a" in sys.argv:
	sys.argv=["-v", "-p"]
level = 1
if "-l" in sys.argv:
    level = 11
if "-x" in sys.argv:
    level = 10
    
cap = cv2.VideoCapture(0)
size = int(cap.get(4)/2)
hieght = cap.get(4)
width = cap.get(3)
hx, hy = 0, 0
Current = None
Previous = None
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
bosshealth = 15
lvlstrt = 0
win = False
font = pygame.font.Font(None, 36)
bossstrt = 0
while True:
        canvas.fill((255, 255, 255))
        canvas.blit(background, (0, 0))
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
                text = font.render("LEVEL: "+str(level), 1, (0, 255, 0))
                textpos = text.get_rect()
                textpos.centerx = canvas.get_rect().centerx
                textpos.centery = canvas.get_rect().centery
                canvas.blit(text, textpos)
        pygame.draw.line(canvas, (0, 255, 0), (0, 0), (int(health*SIZE[0]/100), 0), 10)
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
        _, frame = cap.read()

	Current = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = Current
        cascPathf = "haarcascade_frontalface_default.xml"
	faceCascade = cv2.CascadeClassifier(cascPathf)
        faces = []
        if aboveBL:
            aboveBL = False     
            while (len(faces)==0):
                faces = faceCascade.detectMultiScale(gray)
            print "detection"
            maxA = [0, faces[0][2]*faces[0][3]]
            for i in xrange(len(faces)):
                if faces[i][2]*faces[i][3]>maxA[1]:
                    maxA = [i, faces[i][2]*faces[i][3]]
	    hx, hy, w, h = faces[maxA[0]][0], faces[maxA[0]][1], faces[maxA[0]][2], faces[maxA[0]][3]
            baseLine = hy+h

        Current = cv2.GaussianBlur(Current, (21, 21), 0)
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
                tpos = [100, 0]
                scaledpos = [int((width - tpos[0])*SIZE[0]/width), int(tpos[1]*SIZE[1]/hieght)]
            nextlvl = False
        else:
            for i in xrange(level):
                scaledpos.append(0)
        if level!=11:
            for tid in xrange(level):
                #tsize[tid][0]+=10
                #tsize[tid][1]+=10
                #tpos[tid][0]-=5
                tpos[tid][1]+=5
                if level==10:
                    tpos[tid][1]+=5
                if alivetrump[tid]:
                    cv2.rectangle(frame, (tpos[tid][0], tpos[tid][1]+100), (tpos[tid][0]+100, tpos[tid][1]+200), (0, 0, 255), 2) 
                    #scaledsize[tid] = [int(tsize[tid][0]*SIZE[0]/width), int(tsize[tid][1]*SIZE[1]/hieght)]
                    scaledpos[tid] = [int((width - tpos[tid][0])*SIZE[0]/width), int(tpos[tid][1]*SIZE[1]/hieght)]
                    #trump[tid] = pygame.transform.scale(trump[tid], (scaledsize[tid][0], scaledsize[tid][1]))
                    canvas.blit(trump[img[tid]], scaledpos[tid])
        else:
            cv2.rectangle(frame, (tpos[0], tpos[1]), (tpos[0]+200, tpos[1]+200), (255, 0, 0), 2)
            pygame.draw.line(canvas, (255, 0, 0), (0, 10), (int(bosshealth*SIZE[0]/15), 10), 10)
            tpos[1]+=1
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
        if Previous is None:
		Previous = Current
		continue

	frameDelta = cv2.absdiff(Previous, Current)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
	thresh = cv2.dilate(thresh, None, iterations=2)
	(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
 
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
                    if x in range(tpos[0], tpos[0]+100) and y in range(tpos[1], tpos[1]+100):
                        bhit+=1
                if x in range(0, int(width)/2) and y in range(0, baseLine):
                    mvRight+=1
                if x in range(int(width)/2, int(width)) and y in range(0, baseLine):
                    mvLeft+=1
                yavg+=(y+(h/2))
                xavg+=(x+(w/2))
                counter += 1
		#cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
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
                if hit[tid]>=10:
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
                if hit[tid]>=10:
                    print "you couldn't stump the trump!"
                    health-=5
                    hit[tid] = 0
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
            if bhit>=15:
                bosshealth-=1
                if bosshealth == 0:
                    print "you win!"
                    win = True
                    canvas.blit(trump[7], (0, 0))
                    if win:
                        pygame.display.flip()
                        continue
        if mvLeft>=5:
            hx+=mvLeft
        if mvRight>=5:
            hx-=mvRight
        moved = False
        if mvLeft>=5 or mvRight>=5:
            moved = True
        if baseLine is not None:
            cv2.line(frame, (0, baseLine), (int(width), baseLine), (0, 255, 0), 2)
        if counter>0:	
	    yavg/=counter
            xavg/=counter

        frame = cv2.flip(frame, 1)	
	
        if "-v" in sys.argv:
	    cv2.imshow("Detected motion", frame)
            #cv2.imshow("fd", frameDelta)	
	Previous = Current
        if level==10 and not nextlvl:
            ghx = int((width-hx)*SIZE[0]/width)
            ghy = int(hieght-100)#baseLine#int(hy*SIZE[1]/hieght)
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
