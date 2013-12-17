import math
import os

THETALENGTH = 256

class Logistic:
    def __init__(self, currentTrainingNumber=-1):
        self.samples = []
        self.currentTrainingNumber = currentTrainingNumber
        self.step = 0.001
        self.precision = 0.000001
        self.theta = []
        # init theta
        for i in xrange(THETALENGTH):
            self.theta.append(0.0)
    
    def getSigmoid(self, i):
        sum = 0.0
        for j in xrange(THETALENGTH):
            sum += float(self.theta[j])*float(self.samples[i].x[j])

        return float(math.exp(sum*-1))

    def getFunction(self):
        sum = 1.0
        for i in xrange(len(self.samples)):
            sigmoid = self.getSigmoid(i)
            if int(self.samples[i].y) == 1:
                sum *= float(1/(1 + sigmoid))
            else:
                sum *= float(sigmoid/(1 + sigmoid))
        return float(sum)

    def getGradient(self, j):
        sum = 0.0
        for i in xrange(len(self.samples)):
            sum += (float(self.samples[i].y) - float(1/(1 + self.getSigmoid(i)))) * float(self.samples[i].x[j])

        return float(sum)
    
    def getDistance(self, theta1, theta2):
        result = math.sqrt(sum([(int(x1)-int(x2))**2 for (x1, x2) in zip(theta1, theta2)]))
        return float(result)

    def train(self):
        k = 0
        newTheta = self.theta
        fxbasepath = "./logisticlog/"
        if os.path.exists(fxbasepath):
            pass
        else:
            os.makedirs(fxbasepath)

        fxfile = open(fxbasepath + "%d.txt" % int(self.currentTrainingNumber), "w")

        while True:
            print "%d trainging %d" % (int(self.currentTrainingNumber), int(k))
            oldFx = self.getFunction()
            fxfile.write('oldFx--->' + str(oldFx))
            fxfile.write("\n")

            print "%d is %d" % (int(self.currentTrainingNumber), int(oldFx))
            for i in xrange(THETALENGTH):
                print "updating theta %d" % int(i)
                gradient = self.getGradient(i)
                fxfile.write('gradient%d--->' % int(i) + str(gradient))
                fxfile.write('\n')
                if abs(gradient) < self.precision:
                    print "theta %d is %d" % (int(i), int(self.theta[i]))
                    #continue
                else:
                    #newTheta[i] = self.theta[i] + self.step*gradient
                    newTheta[i] = self.theta[i] - self.step*gradient
            thetaDiff = self.getDistance(newTheta, self.theta)
            fxfile.write('thetadiff--->' + str(thetaDiff))
            fxfile.write('\n')
            self.theta = newTheta
            fxfile.write('newtheta--->')
            for item in self.theta:
                fxfile.write(str(item))
                fxfile.write('\t')
            fxfile.write('\n')
            newFx = self.getFunction()
            fxDiff = abs(newFx-oldFx)
            fxfile.write('fxdiff--->' + str(fxDiff))
            fxfile.write('\n')
            fxfile.write('newfx--->' + str(newFx))
            fxfile.write('\n')
            if fxDiff < self.precision or thetaDiff < self.precision:
                break
            else:
                k += 1
                #oldFx = newFx
                #self.theta = newTheta
        fxfile.close()
        basepath = "./logistictheta/"
        if os.path.exists(basepath):
            pass
        else:
            os.makedirs(basepath)

        file = open(basepath+"%d.txt" % int(self.currentTrainingNumber), "w")
        for item in self.theta:
            file.write(str(item))
            file.write("\n")
        file.close()
                    
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
            #sample.num = int(dir[0])
            if int(dir[0]) == int(currentTrainingNumber):
                sample.y = 1
            else:
                sample.y = 0
            col.append(sample)

if __name__ == '__main__':
    #source = "./semeionsamples/"
    source = "../pretreat_statistic/semeionsamples/"
    for i in xrange(10):
        logistic = Logistic(currentTrainingNumber=i)
        loaddata(source, logistic.samples, i)
        #print logistic.samples
        #print logistic.theta
        logistic.train()
