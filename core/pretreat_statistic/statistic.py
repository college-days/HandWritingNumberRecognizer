import os
source = "./semeionsamples/"
file = open("./staticResult.txt", "w")
dirs = os.listdir(source)
for dir in dirs:
    scale = len(os.listdir(source + dir))
    file.write("%d-%d" % (int(dir[0]), int(scale)))
    file.write('\n')
