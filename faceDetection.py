import cv2
import numpy





def integralImage(img):
    img1 = [ [0]*len(img[0]) for i in range(len(img)) ]
    
    for x in range(len(img)):
        for y in range(len(img[0])):
            if(x == 0):
                if(y == 0):
                    img1[x][y] = img[x][y]
                else:
                    img1[x][y] = img1[x][y-1] + int(img[x][y])
            else:
                if(y == 0):
                    img1[x][y] = int(img[x][y]) + img1[x-1][y]
                else:
                    img1[x][y] = int(img[x][y]) + img1[x-1][y] + img1[x][y-1] - img1[x-1][y-1]
    return img1

#|-----------------------------|
#|                             |
#|-----------------------------|
#|#############################|
#|-----------------------------|
def haarHor(image, row, column, h, w):
    black = sum(image, row+h//2, column, row+h-1, column+w-1)
    white = sum(image, row, column, row+h//2-1, column+w-1)
    value = (white - black)/(h*w/2)/255
    return value
    
    
#|-----------------------------|
#|                             |
#|-----------------------------|
#|#############################|
#|-----------------------------|
#|                             |
#|-----------------------------|
def haarHorLine(image, row, column, h, w):
    black = sum(image, row+h//3, column, row+h//3*2-1, column+w-1)
    white1 = sum(image, row, column, row+h//3-1, column+w-1)
    white2 = sum(image, row+h//3*2, column, row+h-1, column+w-1)
    value = (white1 + white2 - black)/(h*w/3)/255
    return value
    
#|-----------------|
#|        |########|
#|        |########|
#|        |########|
#|        |########|
#|        |########|
#|        |########|
#|        |########|
#|        |########|
#|        |########|
#|        |########|
#|-----------------|
def haarVerRight(image, row, column, h ,w):
    black = sum(image, row, column + w//2, row + h-1, column + w -1)
    white = sum(image, row, column, row+h-1, column + w//2-1)
    return (white - black)/(h*w/2)/255
    
    
#|-----------------|
#|########|        |
#|########|        |
#|########|        |
#|########|        |
#|########|        |
#|########|        |
#|########|        |
#|########|        |
#|########|        |
#|########|        |
#|-----------------|
def haarVerLeft(image, row, column, h, w):
    black = sum(image, row, column + w//2, row + h-1, column + w -1)
    white = sum(image, row, column, row+h-1, column + w//2-1)
    return (black - white)/(h*w/2)/255

#calculte sum of give points in integral image
def sum(image, row1, column1, row2, column2):
    #print('x1: ', row1-1, '  y1: ', column1 -1, '  x2: ', row2,'  y2: ', column2 )
    if(column2 > len(image[0])-1 or row2 > len(image)-1):
        return 0
    else:
        return image[row1-1][column1-1] + image[row2][column2] - image[row1-1][column2] - image[row2][column1-1]
    

#scan through the image with different sizes of square windows, size of windows grow 10% after each round of scans
def scanImage(image, rSize, cSize):
    moveR = rSize//10
    moveC = cSize//10
    if rSize <= len(image) and cSize <= len(image[0]):
        for row in range((len(image)-rSize)//moveR):
            for column in range((len(image[0])-cSize)//moveC):
                detectFace(image, row * moveR, column * moveC, rSize, cSize)
        scanImage(image, int(rSize * 1.1), int(cSize * 1.1))
        
        
#check if the new sqaure is stacking into any existing squares
def stack(slist, newQ):
    if slist == []:
        return False
    for (r,c,h,w) in slist:
        if r <= newQ[0] <= r+h and c <= newQ[1] <= c+w and w <= 1.1 * newQ[3]:
            return True
    
        if  r <= newQ[0] <= r+h and c <= newQ[1] + newQ[3] <= c+w and w <= 1.1 * newQ[3]:
            return True
            
        if r <= newQ[0] + newQ[2] <= r+h and c <= newQ[1] <= c+w and w <= 1.1 * newQ[3]:
            return True
            
        if r <= newQ[0] + newQ[2] <= r+h and c <= newQ[1] + newQ[3] <= c+w and w <= 1.1 * newQ[3]:
            return True
        
    return False

#determine if there is a face in the window
def detectFace(image, row, column, rSize, cSize):
    #detect eyebrows that should be located in top half of the square using haar(horizontal). The size of eyebrows should be about a third of the face(square). Consider that brightness of the image could effect the width of eyebrow in black white image, we use a fifth of face for eyebrows.
    #Threash hold of haar is set to black-white is 3/4 black.
    left_eyebrows = []
    eyeWidth = cSize//30*6
    eyeHeight = eyeWidth//4
    threashHold = 0.3
    moveC = eyeWidth//10
    if moveC < 1:
        moveC = 1
    moveR = 2
    for eRow in range((rSize//2 - eyeHeight)//moveR):
        for eColumn in range((cSize//2 - eyeWidth)//moveC):
            r = row + eRow * moveR
            c = column + eColumn * moveC
            if(haarHor(image, r, c, eyeWidth, eyeHeight) > threashHold):
                if(not stack(left_eyebrows, [r, c, eyeHeight, eyeWidth])):
                    left_eyebrows.append([r, c, eyeHeight, eyeWidth])
                    
                
    right_eyebrows = []
    for eRow in range((rSize//2 - eyeHeight)//moveR):
        for eColumn in range((cSize//2 - eyeWidth)//moveC):
            r = row + eRow * moveR
            c = column + eColumn * moveC + cSize//2
            if(haarHor(image, r, c, eyeWidth, eyeHeight) > threashHold):
                if(not stack(right_eyebrows, [r, c, eyeHeight, eyeWidth])):
                    right_eyebrows.append([r, c, eyeHeight, eyeWidth])
   
                    
                    
    #detect nose: nose should be located in the middle of the face(horizontally) and middle part of the face. After observing the positive images, shade of bottom of the nose is more noticable that side of nose. We detect bottom of the nose, which is also horizontal
    noses = []
    noseWidth = cSize//36*6
    noseHeight = noseWidth//3
    moveC = noseWidth//10
    if moveC < 1:
        moveC = 1
    moveR = 2
    for eRow in range((rSize//2 - noseHeight)//moveR):
        for eColumn in range((cSize//3 - noseWidth)//moveC):
            r = row + eRow * moveR + rSize//2
            c = column + eColumn * moveC + cSize//3
            if(haarHor(image, r, c, noseWidth, noseHeight) > threashHold):
                if(not stack(noses, [r, c, noseHeight, noseWidth])):
                    noses.append([r, c, noseHeight, noseWidth])
    
    #detect upper nose(the vertical part of nose). since the gray level is graetly effected by the direction of the light(shade), we detect 2 sides but if we find 1 side we say its a match
    upperNoses = []
    noseWidth = cSize//60*6
    if noseWidth<2:
        noseWidth = 2
    noseHeight = noseWidth * 4
    moveC = noseWidth//10
    if moveC < 1:
        moveC = 1
    moveR = noseHeight//10
    if moveR < 1:
        moveR = 1
        
    for eRow in range((rSize//3 - noseHeight)//moveR):
        for eColumn in range((cSize//3 - noseWidth)//moveC):
            r = row + eRow * moveR + rSize//3
            c = column + eColumn * moveC + cSize//3
            if(haarVerLeft(image, r, c, noseWidth, noseHeight) > threashHold or haarVerLeft(image, r, c, noseHeight, noseWidth) > threashHold):
                if(not stack(upperNoses, [r, c, noseHeight, noseWidth])):
                    upperNoses.append([r,c,noseHeight,noseWidth])
        
        
        
    #detect mouse: mouse should be bottem mid of the face, size should be about 1/3 of face
    mouses = []
    mouseWidth = cSize//24*6
    mouseHeight = mouseWidth//2
    moveC = mouseWidth//10
    if moveC < 1:
        moveC = 1
    moveR = 2
    for eRow in range((rSize//3 - mouseHeight)//moveR):
        for eColumn in range((cSize//3 - mouseWidth)//moveC):
            r = row + eRow * moveR + rSize//3*2
            c = column + eColumn * moveC + cSize//3
            if(haarHorLine(image, r, c, mouseWidth, mouseHeight) > threashHold):
                if(not stack(mouses, [r, c, mouseHeight, mouseWidth])):
                    mouses.append([r, c, mouseHeight, mouseWidth])
    #check if all features are detected
    if len(left_eyebrows) > 0 and len(right_eyebrows) > 0 and len(noses) > 0 and len(mouses) > 0 and len(upperNoses) > 0:
        
        if(not stack(faces, [row, column, rSize, cSize])):
            print('left eyebrows: ',len(left_eyebrows), '   right eyebrows: ', len(right_eyebrows),'   upper noses: ', len(upperNoses),'   noses: ', len(noses),'   mouses: ', len(mouses))
            faces.append([row, column, rSize, cSize])


def highlightFace(faces, img):
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0, 0), 2)
        

def findMax(faces, image0):
    img1 = numpy.zeros((len(image0), len(image0[0]), 3), dtype=numpy.uint8)
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    #remove faces inside other faces
    for (r1, c1, h1, w1) in faces:
        for face in faces:
            if(r1 == face[0] and c1 == face[1] and h1 == face[2] and w1 == face[3]):
                continue
            elif(r1 > face[0] and c1 > face[1] and h1 > face[2] and w1 > face[3]):
                faces.remove(face)
    for (r, c, h ,w) in faces:
        addone(img1, r, c, h, w)
    max = 0
    for y in range(len(img1[0])):
        for x in range(len(img1)):
            if img1[x][y] > max:
                max = img1[x][y]
    for y in range(len(img1[0])):
        for x in range(len(img1)):
            if img1[x][y] == max:
                image0 = 0
    print(len(faces))
    cv2.imshow('faceless', img1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imshow('faceless', image0)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    
def addone(image, r, c, h, w):
    for y in range(len(image[0])):
        for x in range(len(image)):
            if(x <= c <= x+w and y <= r <= y+h):
                image[x][y] += 2

faces = []
name = input('Please input file name for face detection')
image0 = cv2.imread(name)
grayImage = cv2.cvtColor(image0, cv2.COLOR_BGR2GRAY)
intImg = integralImage(grayImage)
scanImage(intImg, 50, 40)
print(len(faces))
#findMax(faces, image0)
for (x, y, size1, size2) in faces:
    cv2.rectangle(image0, (y, x), (y+size2, x+size1), (255,0,0), 2)
    cv2.imshow('face', image0)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    


#test and correct haar fitlers and sum()
#test = [[1,1,1,1,1,1,1,1,1,1,1],
#        [1,1,1,1,1,1,1,1,1,1,1],
#        [1,1,1,1,1,1,1,1,1,1,1],
#        [1,1,1,1,1,1,1,1,1,1,1],
#        [1,1,1,1,1,1,1,1,1,1,1],
#        [1,1,1,1,1,1,1,1,1,1,1],
#        [1,1,1,1,1,1,1,1,1,1,1],
#        [1,1,1,1,1,1,1,1,1,1,1],
#        [1,1,1,1,1,1,1,1,1,1,1]]

#intTest = integralImage(test)
#for line in intTest:
#    print(line)
#print(haarHor(intTest, 2, 3, 4,4))
#print(haarHorLine(intTest, 2,3, 6, 6))
#print(haarVer(intTest, 2, 3, 4, 4))

