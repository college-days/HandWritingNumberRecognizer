import os
import math
from calcUtil import getNetOutput
from filterImage import ImageFilter

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
        return result
        #if result > 0.5:
        #    return True
        #else:
        #    return False

    def loadHiddenParam(self):
        basepath = str(os.path.join(os.path.dirname(__file__), '../annresult/%d/' % int(self.verifynumber)).replace('\\', '/'))
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
        basepath = str(os.path.join(os.path.dirname(__file__), '../annresult/%d/' % int(self.verifynumber)).replace('\\', '/'))
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

def anndecision(target):
    source = str(os.path.join(os.path.dirname(__file__), '../semeionsamples/').replace('\\', '/'))
    verifyList = []
    for i in xrange(10):
        verify = Verify(i)
        verifyList.append(verify)

    resultList = []
    for i in xrange(10):
        result = verifyList[i].decision(target)
        resultList.append(result)
    resultmax = max(resultList)
    decisionNumber = resultList.index(resultmax)
    if resultmax > 0.5:
        return decisionNumber
    else:
        print 'unknown'
        return decisionNumber

if __name__ == '__main__':
    imagesource = "../testsamples/cleantha.png"
    imagefilter = ImageFilter(imagesource)
    target = imagefilter.getVectorNew()
    print anndecision(target)
