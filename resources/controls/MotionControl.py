import cv2
class MotionControl:
    Previous = None
    Current = None
    cap = None
    frame = None
    faceCascade = None
    fgbg = cv2.BackgroundSubtractorMOG()

    def __init__(Self, cap, cascPathf):
        Self.cap = cap
        Self.faceCascade = cv2.CascadeClassifier(cascPathf)


    def setFrame(Self):
        _, Self.frame = Self.cap.read()
        #Self.frame = Self.fgbg.apply(Self.frame)
        Self.Current = cv2.cvtColor(Self.frame, cv2.COLOR_BGR2GRAY)

    def getFace(Self):
        faces = []
        while (len(faces)==0):
            Self.setFrame() 
            print "detecting"
            faces = Self.faceCascade.detectMultiScale(Self.Current)
        print "detection"
        maxA = [0, faces[0][2]*faces[0][3]]
        for i in xrange(len(faces)):
            if faces[i][2]*faces[i][3]>maxA[1]:
               maxA = [i, faces[i][2]*faces[i][3]]
        return faces[maxA[0]][0], faces[maxA[0]][1], faces[maxA[0]][2], faces[maxA[0]][3]
    
    def getMotion(Self):
        Self.Current = cv2.GaussianBlur(Self.Current, (21, 21), 0)
        if Self.Previous is None:
                Self.Previous = Self.Current    
                return False, None 
        frameDelta = cv2.absdiff(Self.Previous, Self.Current)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        Self.Previous = Self.Current
        return True, cnts

    def show(Self, title):
        cv2.flip(Self.frame, 1)
        cv2.imshow(title, Self.frame)

    def drawBaseLine(Self, width, baseLine):
        cv2.line(Self.frame, (0, baseLine), (int(width), baseLine), (0, 255, 0), 2)

    def rectangle(Self, a, b, c, d):
        cv2.rectangle(Self.frame, a, b, c, d)
