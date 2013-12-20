import math
import os
import numpy as np
import pylab as pl
import cPickle

source = "../pretreat_statistic/semeionsamples/"

class Fisher:
    def __init__(self, trainNumber):
        self.trainNumber = trainNumber
        self.class1 = np.array(self.getData())
        self.class2 = np.array(self.loadData())
        self.total = np.array(self.loadAll())

    def parse_image(self, path):
        sampleList = []
        fp = open(path, "r") 
        for line in fp:
            line = line[:-1]
            sampleList += line
        sampleList = [float(item) for item in sampleList]
        return sampleList

    def getData(self):
        dataMatrix = []
        dirs = os.listdir(source)
        for dir in dirs:
            if int(dir[0]) == self.trainNumber:
                files = os.listdir(source + dir)
                for file in files:
                    data = self.parse_image(source + dir + '/' + file)
                    dataMatrix.append(data)
                return dataMatrix
            else:
                pass
    
    def loadData(self):
        dataMatrix = []
        dirs = os.listdir(source)
        for dir in dirs:
            if int(dir[0]) == self.trainNumber:
                pass
            else:
                files = os.listdir(source + dir)
                for file in files:
                    data = self.parse_image(source + dir + '/' + file)
                    dataMatrix.append(data)
        return dataMatrix

    def loadAll(self):
        dataMatrix = []
        dirs = os.listdir(source)
        for dir in dirs:
            files = os.listdir(source + dir)
            for file in files:
                data = self.parse_image(source + dir + '/' + file)
                dataMatrix.append(data)
        return dataMatrix
    
    def test(self):
        print self.class1.shape
        print self.class2.shape
        print self.total.shape

    def process(self):
        self.mean1 = self.class1.mean(axis=0)
        self.mean2 = self.class2.mean(axis=0)
        self.mean = self.total.mean(axis=0)
                
        self.origin1 = self.class1.copy()
        self.origin2 = self.class2.copy()
        
        height1, width1 = self.class1.shape
        height2, width2 = self.class2.shape

        for i in xrange(height1):
            self.class1[i] = self.class1[i] - self.mean1

        for i in xrange(height2):
            self.class2[i] = self.class2[i] - self.mean2
        
        self.s1 = np.zeros((width1, width1))
        self.s2 = np.zeros((width2, width2))
        
        for i in xrange(height1):
            data = self.class1[i].tolist()
            data = np.array(data)[np.newaxis]
            #self.s1 += data * data.T
            self.s1 += np.dot(data.T, data)
        
        for i in xrange(height2):
            data = self.class2[i].tolist()
            data = np.array(data)[np.newaxis]
            #self.s2 += data * data.T
            self.s2 += np.dot(data.T, data)
        
        self.s1 = (height1 * self.s1) / (height1+height2)
        self.s2 = (height2 * self.s2) / (height1+height2)

        self.sw = self.s1 + self.s2

        self.u1 = np.array((self.mean1 - self.mean).tolist())[np.newaxis]
        self.u2 = np.array((self.mean2 - self.mean).tolist())[np.newaxis]

        self.sb1 = (height1 * np.dot(self.u1.T, self.u1)) / (height1 + height2)
        self.sb2 = (height2 * np.dot(self.u2.T, self.u2)) / (height1 + height2)
        self.sb = self.sb1 + self.sb2
        
        self.final = np.dot(np.linalg.inv(self.sw), self.sb)
        eig_values, eig_vectors = np.linalg.eig(self.final)
    
        indices = eig_values.argsort()[::-1]
        evecs = eig_vectors[:, indices]
        evals = eig_values[indices]
        
        self.w = evecs.T[0]

        class1result = np.dot(self.origin1, self.w)
        class2result = np.dot(self.origin2, self.w)
        
        flag = 1 if class1result.mean() > class2result.mean() else 0
        sepline = (class1result.mean() + class2result.mean()) /2

        fig1 = pl.figure(1)
        x1 = range(height1)
        y1 = class1result.tolist()
        x2 = range(height2)
        y2 = class2result.tolist()
        linex = range(max([height1, height2])+1)
        liney = (np.ones(len(linex))*sepline).tolist()
        pl.plot(x1, y1, 'or')
        pl.plot(x2, y2, 'og')
        pl.plot(linex, liney)
        #pl.show()
        basePath = "./ldaresult/"
        if os.path.exists(basePath):
            pass
        else:
            os.makedirs(basePath)
        imagePath = basePath + "%d.png" % int(self.trainNumber)
        fig1.savefig(imagePath)
        pl.close()

        return sepline, flag, self.w

class Verify:
    def __init__(self, verifyNumber, sepline, flag, mapvector):
        self.verifyNumber = verifyNumber
        self.sepline = sepline
        self.flag = flag
        self.mapvector = mapvector
        self.data = np.array(self.getData())

    def parse_image(self, path):
        sampleList = []
        fp = open(path, "r") 
        for line in fp:
            line = line[:-1]
            sampleList += line
        sampleList = [float(item) for item in sampleList]
        return sampleList

    def getData(self):
        dataMatrix = []
        dirs = os.listdir(source)
        for dir in dirs:
            if int(dir[0]) == self.verifyNumber:
                files = os.listdir(source + dir)
                for file in files:
                    data = self.parse_image(source + dir + '/' + file)
                    dataMatrix.append(data)
                return dataMatrix
            else:
                pass
        
    def getResult(self):
        self.y = np.dot(self.data, self.mapvector)
        correct = 0
        if flag == 1:
            for item in self.y:
                if float(item) > float(self.sepline):
                    correct += 1
                else:
                    pass
        else:
            for item in self.y:
                if float(item) < float(self.sepline):
                    correct += 1
                else:
                    pass

        return float(correct) / float(self.data.shape[0])

class MapVectorCache:
    def __init__(self, sepline, flag, mapvector):
        self.sepline = sepline
        self.flag = flag
        self.mapvector = mapvector
    
    def getResult(self):
        return self.sepline, self.flag, self.mapvector

if __name__ == '__main__':
    if os.path.isfile("./mapcache.pickle"):
        with open("./mapcache.pickle", "rb") as cacheData:
            mapcache = cPickle.load(cacheData)
    else:
        with open('./mapcache.pickle', 'wb') as cacheData:
            mapcache = []
            for i in xrange(10):
                fisher = Fisher(i)
                sepline, flag, mapvector = fisher.process()
                cache = MapVectorCache(sepline, flag, mapvector)
                mapcache.append(cache)
            cPickle.dump(mapcache, cacheData)
 
    #file = open("./ldaresult.txt", "a+")
    file = open("./ldaresult.txt", "w")
    for i in xrange(len(mapcache)):
        sepline, flag, mapvector = mapcache[i].getResult()
        verify = Verify(i, sepline, flag, mapvector)
        result = verify.getResult()
        file.write("lda %d accuracy ---> %f\n" % (int(i), result))
    file.close()

