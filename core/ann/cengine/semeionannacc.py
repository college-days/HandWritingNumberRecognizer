import math
import os
from calcUtil import initList
from calcUtil import getNetOutput
from calcUtil import updateHiddenWeight
from calcUtil import updateOutputWeight
import multiprocessing
import time

SAMPLENUMBER = 1593
INPUTNODENUMBER = 256
HIDDENNODENUMBER = 3
ANNSTEP = 0.001
ANNPRECISION = 0.000001
MAXTIME = 33333

class Hidden_node:
    def __init__(self):
        self.input = []
        self.weight = initList(INPUTNODENUMBER)
    
    def getSigmoid(self, net):
        sigmoid = 1/(1 + math.exp(-1*net))
        return float(sigmoid)

    def getOutput(self):
        net = 0
        for i in xrange(INPUTNODENUMBER):
            net += float(self.input[i]) * float(self.weight[i])
        return float(self.getSigmoid(net))
    
    def getOutputNew(self):
        return getNetOutput(self.input, self.weight)

    def updateWeight(self, delta, weight):
        output = self.getOutputNew()
        for i in xrange(len(self.input)):
            deltaWeight = float(output) * (float(1) - float(output)) * float(delta) * float(weight) * float(ANNSTEP) * float(self.input[i])
            self.weight[i] = self.weight[i] + deltaWeight

    def updateWeightNew(self, delta, weight):
        self.weight = updateHiddenWeight(self.input, self.weight, self.getOutputNew(), ANNSTEP, delta, weight)

    def updateInput(self, input):
        self.input = [1.0] + input

class Output_node:
    def __init__(self):
        self.input = []
        self.weight = initList(HIDDENNODENUMBER)
       
    def getSigmoid(self, net):
        sigmoid = 1/(1 + math.exp(-1*net))
        return float(sigmoid)

    def getOutput(self):
        net = 0
        for i in xrange(HIDDENNODENUMBER):
            net += float(self.input[i]) * float(self.weight[i])
        return float(self.getSigmoid(net))

    def getOutputNew(self):
        return getNetOutput(self.input, self.weight)

    def updateWeight(self, prosInput):
        deltaList = []
        output = self.getOutputNew()
        for i in xrange(len(self.input)):
            delta = float(output) * (float(1) - float(output)) * (float(prosInput) - float(output))
            deltaList.append(float(delta))
            deltaWeight = float(ANNSTEP) * float(delta) * float(self.input[i])
            self.weight[i] = self.weight[i] + deltaWeight
        #return float(delta)
        return deltaList
    
    def updateWeightNew(self, prosInput):
        self.weight, deltalist = updateOutputWeight(self.input, self.weight, self.getOutputNew(), prosInput, ANNSTEP)
        return deltalist

    def updateInput(self, input):
        self.input = [1.0] + input

class Sample:
    def __init__(self):
        self.x = []
        self.y = -1

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
def loaddata(dirpath, col, currentTrainingNumber):
    dirs = os.listdir(dirpath)
    for dir in dirs:
        files = os.listdir(dirpath + dir)
        for file in files:
            sample = Sample()
            sample.x = parse_image(dirpath + dir + '/' + file)
            print len(sample.x)
            #sample.num = int(dir[0])
            if int(dir[0]) == int(currentTrainingNumber):
                sample.y = 1
            else:
                sample.y = 0
            col.append(sample)

def mainprocess(k):
    source = "./semeionsamples/"
    #for k in xrange(10):
    trainingSamples = []
    hiddenList = []
    loaddata(source, trainingSamples, k)

    for m in xrange(HIDDENNODENUMBER):
        hiddenNode = Hidden_node()
        hiddenList.append(hiddenNode)

    outputNode = Output_node()
    
    #E = 0
    updateTime = 0
    while updateTime < MAXTIME:
        E = 0
        updateTime += 1
        print '%d ann time %d' % (int(k), int(updateTime))
        startTime = time.time()
        
        for i in xrange(SAMPLENUMBER):
            for j in xrange(HIDDENNODENUMBER):
                hiddenList[j].updateInput(trainingSamples[i].x)
            outputNode.updateInput([hiddennode.getOutputNew() for hiddennode in hiddenList])
            deltaList = outputNode.updateWeightNew(trainingSamples[i].y)
            for t in xrange(HIDDENNODENUMBER):
                hiddenList[t].updateWeightNew(deltaList[t], outputNode.weight[t])
            outputNode.updateInput([hiddennode.getOutputNew() for hiddennode in hiddenList])
            finaloutput = outputNode.getOutputNew()

            E += (float(finaloutput) - float(trainingSamples[i].y))**2
        
        E = float(E)/2
        print 'E is %f' % float(E)
        print time.time() - startTime

        errorBasePath = "./annerror/"
        if os.path.exists(errorBasePath):
            pass
        else:
            os.makedirs(errorBasePath)

        file = open(errorBasePath + "%d.txt" % int(k), "a")
        file.write(str(E))
        file.write('\n')
        file.close()

        if E < ANNPRECISION:
            break
        else:
            pass

    basepath = "./annresult/%d/" % int(k)
    if os.path.exists(basepath):
        pass
    else:
        os.makedirs(basepath)
    
    for i in xrange(len(hiddenList)):
        file = open(basepath + "%d_hidden.txt" % int(i), "w")
        for item in hiddenList[i].weight:
            print 'write'
            file.write(str(item))
            file.write('\n')
        file.close()

    file = open(basepath + "output.txt", "w")
    for item in outputNode.weight:
        print 'write'
        file.write(str(item))
        file.write('\n')
    file.close()

if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=10)
    for i in xrange(10):
        pool.apply_async(mainprocess, (i, ))
    pool.close()
    pool.join()
    print 'train ann is done'
