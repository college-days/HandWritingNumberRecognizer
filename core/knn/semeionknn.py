import os
import heapq
import math

class Knn:
    def __init__(self, source, number, k=3):
        self.source = source
        self.k = k
        self.number = number
        self.samples = []
        self.test = []

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

class Sample:
    def __init__(self):
        self.data = []
        self.num = 0

def parse_image(path):
    sampleList = []
    fp = open(path, "r") 
    for line in fp:
        line = line[:-1]
        #print line
        #sampleList += line.replace('1', '9')
        sampleList += line
    return sampleList

# load samples and tests
def loaddata(dirpath, col):
    dirs = os.listdir(dirpath)
    for dir in dirs:
        files = os.listdir(dirpath + dir)
        for file in files:
            sample = Sample()
            sample.data = parse_image(dirpath + dir + '/' + file)
            sample.num = int(dir[0])
            col.append(sample)

#def loaddataSingle(filepath, col):
#    file = open(filepath, "r")
#    sampleList = []
#    for line in file.readlines():
#        line = line[:-1]
#        sampleList.append(line)

if __name__ == '__main__':
    #source = "./semeionsamples/"
    source = "../pretreat_statistic/semeionsamples/"
    trainingSamples = []
    loaddata(source, trainingSamples)
    dirs = os.listdir(source)
    resultFile = open("semeionknnresult.txt", 'w')
    for dir in dirs:
        files = os.listdir(source + dir)
        for file in files:
            knn = Knn(source, number=int(dir[0]), k=3)
            knn.samples = trainingSamples
            knn.test = parse_image(source + dir + '/' + file)
            result = knn.getNumber()
            if int(result) == int(knn.number):
                resultFile.write('true-%d' % int(knn.number))
                resultFile.write('\n')
            else:
                resultFile.write('false-%d' % int(knn.number))
                resultFile.write('\n')
    resultFile.close()
