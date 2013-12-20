# -*- coding: UTF-8 -*-
import heapq
import math
import pylab as pl
import os
import numpy as np
import cPickle

class PCA:
    def __init__(self, originData, dim=50):
        self.originMatrix = np.array(originData)
        self.meanMatrix = np.array(originData)
        self.rows = self.originMatrix.shape[0]
        self.cols = self.originMatrix.shape[1]
        self.covMatrix = np.array([])
        self.eigValues = np.array([])
        self.eigVectors = np.array([])
        self.dim = dim
        print 'originMatrix.shape'
        print self.originMatrix.shape
    
    def getCovMatrix(self):
        mean = self.meanMatrix.mean(axis=0)
        height = self.meanMatrix.shape[0]
        for i in xrange(height):
            self.meanMatrix[i] = self.meanMatrix[i] - mean
        self.covMatrix = np.cov(self.meanMatrix)
        print 'covMatrix.shape'
        print self.covMatrix.shape
        #print self.covMatrix

    def getEigen(self):
        self.eigValues, self.eigVectors = np.linalg.eig(self.covMatrix)

    def test(self):
        self.getCovMatrix()
        self.getEigen()
        
        xlist = [i for i in xrange(len(self.eigValues))]
        ylist = [item for item in self.eigValues]

        indices = self.eigValues.argsort()[::-1]
        values = self.eigValues[indices]
        ylist = [item for item in values]
        pl.plot(xlist, ylist)
        pl.savefig("./eigen2.png")
        #pl.show()
        pl.close()
 
    def getResult(self):
        self.getCovMatrix()
        self.getEigen()
        
        #xlist = [i for i in xrange(len(self.eigValues))]
        #ylist = [item for item in self.eigValues]

        #pl.plot(xlist, ylist)
        #pl.savefig("./eigen1.png")
        #pl.show()

        #indices = self.eigValues.argsort()[::-1]
        #values = self.eigValues[indices]
        #ylist = [item for item in values]
        #pl.plot(xlist, ylist)
        #pl.savefig("./eigen2.png")
        #pl.show()
        
        indices = self.eigValues.argsort()[::-1]
        values = self.eigValues[indices]
        #vectors = self.eigVectors[indices]
        #只改变第二维的顺序，但不改变第一维度的顺序，因为是列向量
        vectors = self.eigVectors[:, indices]
        mapVectors = vectors[:self.dim]
        
        #print mapVectors.shape
        #print self.originMatrix.shape
        
        mapMatrix = np.dot(mapVectors, self.originMatrix)
        #print mapMatrix.shape

        return mapMatrix

class Sample:
    def __init__(self, data, num):
        self.data = [item for item in data]
        #self.data = data
        self.num = num

class VerifyPca:
    def __init__(self, sampleList, k):
        self.samples = sampleList
        self.test = []
        self.k = k

    def updateInput(self, test):
        self.test = [item for item in test]
        #print len(self.test)
    
    def calcDistance(self, list1, list2):
        return math.sqrt(sum([(x1-x2)**2 for (x1, x2) in zip(list1, list2)]))

    def getNumber(self):
        closestPoints = heapq.nsmallest(self.k, self.samples, key=lambda sample: self.calcDistance(self.test, sample.data))
        
        closestLabels = [point.num for point in closestPoints]
        print closestLabels
        if len(list(set(closestLabels))) == len(closestLabels):
            print closestLabels[0]
            return closestLabels[0]
        elif closestLabels[0] != closestLabels[1] and closestLabels[1] == closestLabels[2]:
            return closestLabels[0]
        else:
            return max(set(closestLabels), key=closestLabels.count)

def parse_image(path):
    sampleList = []
    fp = open(path, "r") 
    for line in fp:
        line = line[:-1]
        sampleList += line
    sampleList = [float(item) for item in sampleList]
    return sampleList

# load samples and tests
def loaddata(dirpath):
    data = []
    dirs = os.listdir(dirpath)
    for dir in dirs:
        files = os.listdir(dirpath + dir)
        for file in files:
            item = parse_image(dirpath + dir + '/' + file)
            data.append(item)
    #return np.array(data)
    return data

def loaddatanew(dirpath, mapMatrix):
    sampleList = []
    dirs = os.listdir(dirpath)
    for dir in dirs:
        files = os.listdir(dirpath + dir)
        for file in files:
            data = parse_image(dirpath + dir + '/' + file)
            sample = Sample(np.dot(mapMatrix, np.array(data)), int(dir[0]))
            #print len(sample.data)
            #print sample.num
            sampleList.append(sample)
    return sampleList

def pcadecision(target):
    #source = "../semeionsamples/"
    source = str(os.path.join(os.path.dirname(__file__), '../semeionsamples/').replace('\\', '/'))
    cachePath = str(os.path.join(os.path.dirname(__file__), './mapmatrix.pickle').replace('\\', '/'))
    if os.path.isfile(cachePath):
        with open(cachePath, "rb") as cacheData:
            mapMatrix = cPickle.load(cacheData)
    else:
        with open(cachePath, 'wb') as cacheData:
            trainingSamples = loaddata(source)
            #通过分析特征值分布图像eigen2.png来确定第二个参数的数值大小，也就是要取前多少个特征向量构造pca映射矩阵
            pca = PCA(trainingSamples, 50)
            #show the eigen pic just for test to get the second param to construct a pca object
            pca.test()
            mapMatrix = pca.getResult()
            cPickle.dump(mapMatrix, cacheData)
         
    sampleList = loaddatanew(source, mapMatrix)
    verify = VerifyPca(sampleList, 3)
    
    #verify.updateInput(np.dot(mapMatrix, np.array(target)))
    verify.updateInput(np.dot(mapMatrix, target))
    result = verify.getNumber()
    return result
