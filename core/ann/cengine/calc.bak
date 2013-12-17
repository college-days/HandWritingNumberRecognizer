import math
import numpy

def initList(length):
    list = []
    for i in xrange(length+1):
        list.append(0.0)
    return list

def getNetOutput(inputlist, weightlist):
    net = 0
    for i in xrange(len(inputlist)):
        net += float(inputlist[i]) * float(weightlist[i])
    sigmoid = 1/(1 + math.exp(-1*float(net)))

    return float(sigmoid)
    
def updateHiddenWeight(inputlist, weightlist, output, annstep, delta, weight):
    for i in xrange(len(inputlist)):
        deltaWeight = float(output) * (float(1) - float(output)) * float(delta) * float(weight) * float(annstep) * float(inputlist[i])
        weightlist[i] = weightlist[i] + deltaWeight
    return weightlist

def updateOutputWeight(inputlist, weightlist, output, prosInput, annstep):
    deltaList = []
    for i in xrange(len(inputlist)):
        delta = float(output) * (float(1) - float(output)) * (float(prosInput) - float(output))
        deltaList.append(float(delta))
        deltaWeight = float(annstep) * float(delta) * float(inputlist[i])
        weightlist[i] = weightlist[i] + deltaWeight
    #return float(delta)
    return weightlist, deltaList

def initListNew(length):
    return numpy.zeros(length)

def getNetOutputNew(inputlist, weightlist):
    net = numpy.dot(inputlist, numpy.transpose(weightlist))
    return float(1/(1 + math.exp(-1*float(net))))
