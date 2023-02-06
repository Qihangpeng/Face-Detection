import cv2

def locate(event, x, y, flag, param):
    if (event == cv2.EVENT_LBUTTONDOWN):
        info.write(str(x) + ',' + str(y) + ' ')
        
        


f = open('positive/list.txt','r')
list = f.read().splitlines()
f.close()
info = open('positive/coordinates.txt','w')
print('list of positive png(s): ')
print(list)
for name in list:
    image = cv2.imread('positive/'+name)
    cv2.imshow(name, image)
    cv2.setMouseCallback(name, locate)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    info.write('\n')
info.close()




