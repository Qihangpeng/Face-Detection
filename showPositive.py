import cv2

f = open('positive/list.txt', 'r')
file = f.read()
list = file.split('\n')
list = list[:-1]
f.close()
f = open('positive/info.txt', 'r')
file = f.read()
info = file.split('\n')
info = info[:-1]
f.close()
print('List of images showing')
print(list)
for i in range(len(list)):
    coords = info[i].split(' ')
    for j in range(1, int(info[i][0])+1):
        image = cv2.imread('positive/'+list[i])
        cv2.rectangle(image, (int(coords[j*4-3]), int(coords[j*4-2])), (int(coords[j*4-3]) + int(coords[j*4-1]) ,int(coords[j*4-2]) + int(coords[j*4])), (0, 255, 0), 2)
        cv2.imshow(list[i], image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    

    
