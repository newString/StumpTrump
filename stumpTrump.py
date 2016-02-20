import cv2
import sys
from random import randint
import pygame

pygame.init()
SIZE = [1920, 1080]
canvas = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Motion Game")
#canvas = pygame.Surface(screen.get_size())
#nvas = canvas.convert()
canvas.fill((255, 255, 255))

trump = [None, None, None]
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

if "-a" in sys.argv:
	sys.argv=["-v", "-p"]
	
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
level = 1
nextlvl = True
hitsize = 200
ghx, ghy = None, None
tpos = [[int(width/2), 0], [randint(50, width-100), 0], [randint(50, width-100), 0]]
tsize = [[100, 100], [100, 100], [100, 100]]
hit = [0, 0, 0]
nextlvl = True 
img=[]
health = 100
while True:
        canvas.fill((255, 255, 255))
        pygame.draw.line(canvas, (0, 255, 0), (0, 0), (int(health*SIZE[0]/100), 0), 5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
	        break	
	if pygame.key.get_pressed()[pygame.K_ESCAPE]:
		exit()
        if pygame.key.get_pressed()[pygame.K_r]:
            aboveBL = True
            baseLine = False
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
            nextlvl = False
        else:
            for i in xrange(level):
                scaledpos.append(0)
        for tid in xrange(level):
            #tsize[tid][0]+=10
            #tsize[tid][1]+=10
            #tpos[tid][0]-=5
            tpos[tid][1]+=5
            if alivetrump[tid]:
                cv2.rectangle(frame, (tpos[tid][0], tpos[tid][1]), (tpos[tid][0]+100, tpos[tid][1]+100), (0, 0, 255), 2) 
                #scaledsize[tid] = [int(tsize[tid][0]*SIZE[0]/width), int(tsize[tid][1]*SIZE[1]/hieght)]
                scaledpos[tid] = [int((width - tpos[tid][0])*SIZE[0]/width), int(tpos[tid][1]*SIZE[1]/hieght)]
                #trump[tid] = pygame.transform.scale(trump[tid], (scaledsize[tid][0], scaledsize[tid][1]))
                canvas.blit(trump[img[tid]], scaledpos[tid])
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
                for tid in xrange(level):   
                    if x in range(tpos[tid][0], tpos[tid][0]+100) and y-100 in range(tpos[tid][1], tpos[tid][1]+100):
                        hit[tid]+=1
                if x in range(0, int(width)/2) and y in range(0, baseLine):
                    mvRight+=1
                if x in range(int(width)/2, int(width)) and y in range(0, baseLine):
                    mvLeft+=1
                yavg+=(y+(h/2))
                xavg+=(x+(w/2))
                counter += 1
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        for tid in xrange(level):
            if tpos[tid][1]>int(3*hieght/4):
                if alivetrump[tid]:
                    print "you couldn't stump the trump!"
                    health-=5
                if health<=0:
                    print "you lose! Final score: "+str(level*10)
                    cv2.destroyAllWindows()
                    pygame.display.quit()
                    pygame.quit()
                    exit()
                alivetrump[tid] = False
                #trump[tid] = pygame.image.load("trump"+str(tid+1)+".png").convert()
                #trump[tid].set_colorkey((255, 255, 255))
                #tpos[tid] = [randint(50, width-100), 0]
                #tsize[tid] = [100, 100]
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
            #cv2.line(frame, (0, yavg), (int(width), yavg), (255, 0, 0), 2)
	    #cv2.line(frame, (xavg, 0), (xavg, int(hieght)), (255, 0, 0), 2)

        frame = cv2.flip(frame, 1)	
	
        if "-v" in sys.argv:
	    cv2.imshow("Detected motion", frame)
            #cv2.imshow("fd", frameDelta)	
	Previous = Current
        ghx = int((width-hx)*SIZE[0]/width)
        ghy = int(hy*SIZE[1]/hieght)
        pygame.draw.circle(canvas, (0, 255, 0), (ghx, ghy), 10)
        pygame.display.flip()
