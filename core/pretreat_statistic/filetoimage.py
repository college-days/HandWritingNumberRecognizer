import os
import cv2
import numpy as np

def parse_image(path):
    img_map = []
    fp = open(path, "r") 
    for line in fp:
        line = line[:-1]
        img_map.append([(lambda x: 0 if int(x) == 1 else 255)(item) for item in line])
    return img_map

if __name__ == '__main__':
    source = "./semeionsamples/"
    dirs = os.listdir(source)
    for dir in dirs:
        files = os.listdir(source + dir)
        for file in files:
            print 'processing %d-%d' % (int(dir[0]), int(file.split('.')[0])) 
            result = np.array(parse_image(source + dir + '/' + file))
            basepath = "./semeionimages/%d/" % int(dir[0])
            if os.path.exists(basepath):
                pass
            else:
                os.makedirs(basepath)
            writepath = basepath + file.split('.')[0] + '.png'
            cv2.imwrite(writepath, result)
