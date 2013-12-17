import os
import math
from calcUtil import getNetOutput

INPUTNODENUMBER = 256
HIDDENNODENUMBER = 3

class Sample:
    def __init__(self):
        self.x = []
        self.y = -1

class Hidden_node:
    def __init__(self, input, weight):
        self.input = [1.0] + input
        self.weight = weight
    
    def getSigmoid(self, net):
        sigmoid = 1/(1 + math.exp(-1*net))
        return float(sigmoid)

    def getOutput(self):
        net = 0
        for i in xrange(INPUTNODENUMBER + 1):
            net += float(self.input[i]) * float(self.weight[i])
        return float(self.getSigmoid(net))
    
    def getOutputNew(self):
        return getNetOutput(self.input, self.weight)

class Output_node:
    def __init__(self, input, weight):
        self.input = [1.0] + input
        self.weight = weight
       
    def getSigmoid(self, net):
        sigmoid = 1/(1 + math.exp(-1*net))
        return float(sigmoid)

    def getOutput(self):
        net = 0
        for i in xrange(HIDDENNODENUMBER + 1):
            net += float(self.input[i]) * float(self.weight[i])
        return float(self.getSigmoid(net))
    
    def getOutputNew(self):
        return getNetOutput(self.input, self.weight)

class Verify:
    def __init__(self, verifynumber):
        self.verifynumber = verifynumber
        self.hiddenParam = self.loadHiddenParam()
        self.outputParam = self.loadOutputParam()
        self.hiddenNodeList = []

    def decision(self, target):
        for i in xrange(len(self.hiddenParam)):
            hiddennode = Hidden_node(target, self.hiddenParam[i])
            self.hiddenNodeList.append(hiddennode)

        outputnode = Output_node([hidden.getOutputNew() for hidden in self.hiddenNodeList], self.outputParam)
        result = outputnode.getOutputNew()
        self.hiddenNodeList = []
        #print result
        if result > 0.5:
            #print 'yes'
            return True
        else:
            #print 'no'
            return False

    def loadHiddenParam(self):
        basepath = "./annresult/%d/" % int(self.verifynumber)   
        params = []
        for i in xrange(3):
            param = []
            file = open(basepath + "%d_hidden.txt" % (int(i)))
            for line in file.readlines():
                param.append(float(line[:-1]))
            file.close()
            params.append(param)
        return params

    def loadOutputParam(self):
        basepath = "./annresult/%d/" % int(self.verifynumber)
        param = []
        file = open(basepath + "output.txt")
        for line in file.readlines():
            param.append(float(line[:-1]))
        file.close()
        return param

def parse_image(path):
    sampleList = []
    fp = open(path, "r") 
    for line in fp:
        line = line[:-1]
        #print line
        #sampleList += line.replace('1', '9')
        sampleList += line
    return sampleList

if __name__ == '__main__':
    #source = "../pretreat_statistic/semeionsamples/"
    source = "./semeionsamples/"
    verifyList = []
    for i in xrange(10):
        verify = Verify(i)
        verifyList.append(verify)
    
    resultFile = open("./semeionannresult.txt", "w")
    dirs = os.listdir(source)
    for dir in dirs:
        files = os.listdir(source + dir)
        for file in files:
            #print 'processing %d-%d' % (int(dir[0]), int(file.split('.')[0]))
            target = parse_image(source + dir + '/' + file) 
            resultnum = -1
            for i in xrange(10):
                result = verifyList[i].decision(target)
                if result:
                    resultnum = i
                    break
                else:
                    pass
            if resultnum == int(dir[0]):
                resultFile.write("true-%d" % int(dir[0]))
                resultFile.write('\n')
                #print 'yes'
            else:
                resultFile.write("false-%d" % int(dir[0]))
                resultFile.write('\n')
                print 'no'
    resultFile.close()
                    

