import os
import heapq
import math
from filterImage import ImageFilter

class Knn:
    def __init__(self, k=3):
        self.k = k
        self.samples = []
        self.test = []
        #source = "../semeionsamples/"
        source = str(os.path.join(os.path.dirname(__file__), '../semeionsamples/').replace('\\', '/'))
 
        self.loaddata(source, self.samples)

    def calcDistance(self, list1, list2):
        return math.sqrt(sum([(int(x1)-int(x2))**2 for (x1, x2) in zip(list1, list2)]))

    def getNumber(self):
        closestPoints = heapq.nsmallest(self.k, self.samples, key=lambda sample: self.calcDistance(self.test, sample.data))
        closestLabels = [point.num for point in closestPoints]
        print closestLabels
        #return max(set(closestLabels), key=closestLabels.count)
        if len(list(set(closestLabels))) == len(closestLabels):
            print closestLabels[0]
            return closestLabels[0]
        elif closestLabels[0] != closestLabels[1] and closestLabels[1] == closestLabels[2]:
            return closestLabels[0]
        else:
            return max(set(closestLabels), key=closestLabels.count)

    def parse_image(self, path):
        sampleList = []
        fp = open(path, "r") 
        for line in fp:
            line = line[:-1]
            #print line
            #sampleList += line.replace('1', '9')
            sampleList += line
        return sampleList

    def loaddata(self, dirpath, col):
        dirs = os.listdir(dirpath)
        for dir in dirs:
            files = os.listdir(dirpath + dir)
            for file in files:
                sample = Sample()
                sample.data = self.parse_image(dirpath + dir + '/' + file)
                sample.num = int(dir[0])
                col.append(sample)
class Sample:
    def __init__(self):
        self.data = []
        self.num = 0

if __name__ == '__main__':
    imagesource = "../testsamples/cleantha.png"
    imagefilter = ImageFilter(imagesource)
    knn = Knn(3)
    knn.test = imagefilter.getVectorNew()
    result = knn.getNumber()
    print result

