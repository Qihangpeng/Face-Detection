import cv2

f = open('list.txt', 'r')
list = f.read()
names = list.split('\n')[:-1]
print(names)
for name in names:
    image = cv2.imread(name)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow(name, gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    for x in range(len(image)):
        for y in range(len(image[0])):
            if(gray[x][y] > 0.5*255):
                gray[x][y] = 255
            else:
                gray[x][y] = 0
    cv2.imshow('a1', gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
