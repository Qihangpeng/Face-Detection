f1 = open('positive/coordinates.txt', 'r')
f2 = open('positive/info.txt', 'w')

list = f1.read()
lines = list.split('\n')
for line in lines:
    sets = line.split(' ')
    sets.remove('')
    count = int(len(sets)/2)
    if count != 0:
        
        string = str(count)
        for i in range(0, count):
            w = int(sets[i*2+1].split(',')[0]) - int(sets[i*2].split(',')[0])
            h = int(sets[i*2+1].split(',')[1]) - int(sets[i*2].split(',')[1])
            string += ' ' + sets[i*2].split(',')[0] + ' ' + sets[i*2].split(',')[1] + ' ' + str(w) + ' ' + str(h)
        f2.write(string + '\n')
f1.close()
f2.close()
