import cv2
import os
import numpy as np

class Sample:
    def __init__(self, data, number, id):
        self.data = data
        self.number = number
        self.id = id

class ProcessData:
    def __init__(self, source):
        self.source = source
        file = open(self.source, "rb")
        lines = file.readlines()
        file.close()
        self.lines = lines
        self.data = []

    def process(self):
        idList = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in xrange(len(self.lines)):
            print 'processing data %d' % int(i)
            line = self.lines[i]
            lables = line[-21:-1].split(' ')[:-1]
            self.label = lables.index('1')
            newline = [int(line[7*j]) for j in xrange(256)]
            if self.label == 0:
                sample = Sample(newline, 0, idList[0])
                self.data.append(sample)
                idList[0] += 1
            elif self.label == 1:
                sample = Sample(newline, 1, idList[1])
                self.data.append(sample)
                idList[1] += 1
            elif self.label == 2:
                sample = Sample(newline, 2, idList[2])
                self.data.append(sample)
                idList[2] += 1
            elif self.label == 3:
                sample = Sample(newline, 3, idList[3])
                self.data.append(sample)
                idList[3] += 1
            elif self.label == 4:
                sample = Sample(newline, 4, idList[4])
                self.data.append(sample)
                idList[4] += 1
            elif self.label == 5:
                sample = Sample(newline, 5, idList[5])
                self.data.append(sample)
                idList[5] += 1
            elif self.label == 6:
                sample = Sample(newline, 6, idList[6])
                self.data.append(sample)
                idList[6] += 1
            elif self.label == 7:
                sample = Sample(newline, 7, idList[7])
                self.data.append(sample)
                idList[7] += 1
            elif self.label == 8:
                sample = Sample(newline, 8, idList[8])
                self.data.append(sample)
                idList[8] += 1
            elif self.label == 9:
                sample = Sample(newline, 9, idList[9])
                self.data.append(sample)
                idList[9] += 1

        print len(self.data)

    def writeResult(self):
        for i in xrange(len(self.data)):
            sample = self.data[i]
            print 'processing data %d' % int(i)
            basepath = "./semeionsamples/%s" % str(sample.number)
            if os.path.exists(basepath):
                pass
            else:
                os.makedirs(basepath)

            file = open("./semeionsamples/%s/%s.txt" % (str(sample.number), str(sample.id)), "wb")
            print "./semeionsamples/%s/%s.txt" % (str(sample.number), str(sample.id))

            for k in xrange(16):
                for j in xrange(16):
                    file.write(str(sample.data[16*k+j]))
                file.write('\n')
            file.close()

if __name__ == '__main__':
    processData = ProcessData("./semeion.txt")
    processData.process()
    processData.writeResult()

