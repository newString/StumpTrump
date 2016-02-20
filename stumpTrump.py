import cv2
import pyautogui
import sys
from random import randint
from os import system as cmd
import pygame

pygame.init()
SIZE = [1920, 1080]
canvas = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Motion Game")
#canvas = pygame.Surface(screen.get_size())
#nvas = canvas.convert()
canvas.fill((255, 255, 255))

trump = [None, None, None]
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
hitsize = 200
ghx, ghy = None, None
while True:
        canvas.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
	        break	
	if pygame.key.get_pressed()[pygame.K_ESCAPE]:
		exit()
        if pygame.key.get_pressed()[pygame.K_r]:
            aboveBL = True
            baseLine = False
            tx = randint(10, int(width))
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
                if x in range(0, int(width)/2) and y in range(0, baseLine):
                    mvRight+=1
                if x in range(int(width)/2, int(width)) and y in range(0, baseLine):
                    mvLeft+=1
                yavg+=(y+(h/2))
		xavg+=(x+(w/2))
                counter += 1
		#cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
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
