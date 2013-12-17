import math
import os

THETALENGTH = 256

class VerifyLogistic:
    def __init__(self, theta):
        self.x = []
        self.theta = theta

    def getSigmoid(self):
        sum = 0.0
        for i in xrange(THETALENGTH):
            sum += float(self.theta[i])*float(self.x[i])

        return float(math.exp(sum*-1))

    def getPositiveProbability(self):
        return float(1/(1 + self.getSigmoid()))

    def getNegativeProbability(self):
        sigmoid = self.getSigmoid()
        return float(sigmoid/(1 + sigmoid))

    def getResult(self):
        sigmoid = self.getSigmoid()
        positive = float(1/(1 + sigmoid))
        negative = float(sigmoid/(1 + sigmoid))
        
        print str(positive) + '---' + str(negative)

        if positive > negative:
            return True
        else:
            return False

def parse_image(path):
    sampleList = []
    fp = open(path, "r") 
    for line in fp:
        line = line[:-1]
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
            #sample.num = int(dir[0])
            if int(dir[0]) == int(currentTrainingNumber):
                sample.y = 1
            else:
                sample.y = 0
            col.append(sample)

if __name__ == '__main__':
    thetaDict = {}
    thetapath = "./logistictheta/"
    thetafiles = os.listdir(thetapath)
    for thetafile in thetafiles:
        file = open(thetapath + thetafile, "r")
        thetatemp = []
        for line in file.readlines():
            thetatemp.append(float(line[:-1]))
        #print thetatemp
        thetaDict[int(thetafile[0])] = thetatemp
        file.close()
    #for key, value in thetaDict.items():
    #    print key
    #    print '\n'
    #    print value
    #    print '--------------'

    resultFile = open("semeionlogisticresult.txt", 'w')
    #basepath = "./semeionsamples/"
    basepath = "../pretreat_statistic/semeionsamples/"
    dirs = os.listdir(basepath)
    for dir in dirs:
        files = os.listdir(basepath + dir)
        for file in files:
            print 'processing %d-%d' % (int(dir[0]), int(file.split('.')[0]))
            verify = VerifyLogistic(thetaDict[int(dir[0])])
            #loaddata(basepath + dir + '/' + file, verify.x, int(dir[0]))
            verify.x = parse_image(basepath + dir + '/' + file)
            result = verify.getResult()
            print result
            if result:
                resultFile.write('true-%d' % int(dir[0]))
                resultFile.write('\n')
            else:
                resultFile.write('false-%d' % int(dir[0]))
                resultFile.write('\n')
    resultFile.close()
