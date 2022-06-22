import cv2
from handtrackingMin import handDetector
 
cap = cv2.VideoCapture(0) # capturing video
# Dimensions
cap.set(3, 1280) 
cap.set(4, 720)

detector = handDetector() # creating hand detector object

cx,cy,w,h=100,100,200,200 # dimensions of userchoicebox

class DragUserChoiceBox():
    def __init__(self,color,posCenter,size=[200,200]):
        self.color=color
        self.posCenter=posCenter
        self.size=size
    
    def update(self,cursor):
        cx,cy=self.posCenter
        w,h=self.size
        # If index finger tip is in rectangle region
        if (cx-w//2)<cursor[1]<(cx+w//2) and (cy-h//2)<cursor[2]<(cy+h//2):
                colorR=(0,255,0)
                self.posCenter=cursor[1],cursor[2]

class paletteStructure():
    def __init__(self,center1,center2,center3,size1=[400,150],size2=[400,200],size3=[400,300],color1=(255,0,0),color2=(0,255,0),color3=(0,0,255)):
        self.center1=center1
        self.size1=size1
        self.center2=center2
        self.size2=size2
        self.center3=center3
        self.size3=size3
        self.color1=color1
        self.color2=color2
        self.color3=color3
             
    def update(self,cursor,rect):
        cx1,cy1=self.center1
        cx2,cy2=self.center2
        cx3,cy3=self.center3
        w1,h1=self.size1
        w2,h2=self.size2
        w3,h3=self.size3
        # if user choice box is near 1st palette
        if (cx1-w1//2)<cursor[0]<(cx1+w1//2) and (cy1-h1//2)<cursor[1]<(cy1+h1//2):
                self.fill1(rect.color)
        # if user choice box is near 2nd palette
        if (cx2-w2//2)<cursor[0]<(cx2+w2//2) and (cy2-h2//2)<cursor[1]<(cy2+h2//2):
                self.fill2(rect.color)
        # if user choice box is near 3rd palette
        if (cx3-w3//2)<cursor[0]<(cx3+w3//2) and (cy3-h3//2)<cursor[1]<(cy3+h3//2):
                self.fill3(rect.color)
    
    def fill1(self,color):
        self.color1=color
        rect.posCenter=[150,150]
    def fill2(self,color):
        self.color2=color
        rect.posCenter=[150,150]
    def fill3(self,color):
        self.color3=color
        rect.posCenter=[150,150]
    

rect=DragUserChoiceBox((192,34,155),[150,150]) # position is 150,150
palette=paletteStructure([1000,125],[1000,300],[1000,550])
while True:
    success, img = cap.read()
    img=cv2.flip(img,1)
    img = detector.findHands(img)
    lmList, _ = detector.findPosition(img)
    if lmList:
        l,_,_=detector.findDistance(8,12,img)
        if l<30: 
            cursor=lmList[8] # index finger landmark
            # calling update here
            rect.update(cursor)
        palette.update(rect.posCenter,rect)
     
    # To draw user choice box    
    cx,cy=rect.posCenter
    w,h=rect.size
    cv2.rectangle(img,(cx-w//2,cy-h//2),(cx+w//2,cy+h//2),rect.color,cv2.FILLED)
    
    # To draw Palette
    px1,py1=palette.center1
    px2,py2=palette.center2
    px3,py3=palette.center3
    w1,h1=palette.size1
    w2,h2=palette.size2
    w3,h3=palette.size3

    cv2.rectangle(img,(px1-w1//2,py1-h1//2),(px1+w1//2,py1+h1//2),palette.color1,cv2.FILLED)
    cv2.rectangle(img,(px2-w2//2,py2-h2//2),(px2+w2//2,py2+h2//2),palette.color2,cv2.FILLED)
    cv2.rectangle(img,(px3-w3//2,py3-h3//2),(px3+w3//2,py3+h3//2),palette.color3,cv2.FILLED)
    
    cv2.putText(img,"rgb: "+str((palette.color1)),(px1-w1//2,py1),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2)
    cv2.putText(img,"rgb: "+str((palette.color2)),(px2-w2//2,py2),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2)   
    cv2.putText(img,"rgb: "+str((palette.color3)),(px1-w3//2,py3),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2)
    
    cv2.imshow("Image",img)
    cv2.waitKey(1)