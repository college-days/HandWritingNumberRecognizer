import cv2
import numpy as np
from cv2 import cv
import sys
import os

class ImageFilter:
    def __init__(self, source, number=33, name='clea'):
        self.source = source
        self.number = number
        self.name = name
        image = cv2.imread(self.source)
        self.image = image

    def getVectorNormal(self):
        height = self.image.shape[0]
        width = self.image.shape[1]
        
        widthList = []
        finalList = []
        for i in xrange(height):
            for j in xrange(width):
                data = self.image[i][j][0]
                if data == 255:
                    #widthList.append(0)
                    widthList.append(0.0)
                else:
                    #widthList.append(1)
                    widthList.append(1.0)
            finalList += widthList
            widthList = []
        return finalList

    def getArrayNormal(self):
        height = self.image.shape[0]
        width = self.image.shape[1]

        widthList = []
        finalArray = []
        for i in xrange(height):
            for j in xrange(width):
                data = self.image[i][j][0]
                if data == 255:
                    #widthList.append(0)
                    widthList.append(0.0)
                else:
                    #widthList.append(1)
                    widthList.append(1.0)
            finalArray.append(widthList)
            widthList = []
        return np.array(finalArray)

    def resizeImage(self, newwidth, newheight, origin):
        resize = cv2.resize(origin, (newwidth, newheight), interpolation=cv2.INTER_NEAREST)
        return resize

    def filterImage(self):
        resize = self.resizeImage(300, 300, self.image)
        grayImage = cv2.cvtColor(resize, cv2.COLOR_RGB2GRAY)
        ret, thresh = cv2.threshold(grayImage, 48, 255, cv.CV_THRESH_BINARY_INV)
        thresh = cv2.medianBlur(thresh, 3)

        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) == 0:
            print 'can not find any contours'
            return 

        contoursLen = [len(contour) for contour in contours]
        targetContour = contours[contoursLen.index(max(contoursLen))]
        xlist = [item[0][0] for item in targetContour]
        ylist = [item[0][1] for item in targetContour]
        leftTop = (min(xlist), min(ylist))
        rightBottom = (max(xlist), max(ylist))
        crop = resize[leftTop[1]:rightBottom[1], leftTop[0]:rightBottom[0]]

        #cv2.imwrite("./result/step1_%d.png" % self.number, crop)
        final = self.resizeImage(32, 32, crop)
        #final = self.resizeImage(300, 300, crop)

        height = final.shape[0]
        width = final.shape[1]

        widthList = []
        finalList = []
        for i in xrange(height):
            for j in xrange(width):
                #print final[i][j]
                if final[i][j][0] < 100:
                    #widthList.append(3)
                    #if i < 16 and j <16:
                    if 8 < i and i < 24 and 8 < j and j < 24:
                        widthList.append(9)
                    else:
                        widthList.append(1)

                else:
                    widthList.append(0)

            finalList.append(widthList)
            widthList = []

        self.writeToFileNew(finalList)

    def getVectorNew(self):
        resize = self.resizeImage(300, 300, self.image)
        grayImage = cv2.cvtColor(resize, cv2.COLOR_RGB2GRAY)
        ret, thresh = cv2.threshold(grayImage, 48, 255, cv.CV_THRESH_BINARY_INV)
        thresh = cv2.medianBlur(thresh, 3)

        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) == 0:
            print 'can not find any contours'
            return 

        contoursLen = [len(contour) for contour in contours]
        targetContour = contours[contoursLen.index(max(contoursLen))]
        xlist = [item[0][0] for item in targetContour]
        ylist = [item[0][1] for item in targetContour]
        leftTop = (min(xlist), min(ylist))
        rightBottom = (max(xlist), max(ylist))
        crop = resize[leftTop[1]:rightBottom[1], leftTop[0]:rightBottom[0]]

        #cv2.imwrite("./result/step1_%d.png" % self.number, crop)
        #final = self.resizeImage(32, 32, crop)
        #final = self.resizeImage(32, 32, crop)
        final = self.resizeImage(16, 16, crop)

        height = final.shape[0]
        width = final.shape[1]

        widthList = []
        finalList = []
        finalArray = []
        for i in xrange(height):
            for j in xrange(width):
                #print final[i][j]
                if final[i][j][0] < 100:
                    #if 8 < i and i < 24 and 8 < j and j < 24:
                    #    widthList.append(255)
                    #else:
                        #widthList.append(1)
                    #widthList.append(1)
                    widthList.append(1.0)
                else:
                    #widthList.append(0)
                    widthList.append(0.0)

            #finalList.append(widthList)
            finalList += widthList
            finalArray.append(widthList)
            widthList = []

        return finalList

    def getArrayNew(self):
        resize = self.resizeImage(300, 300, self.image)
        grayImage = cv2.cvtColor(resize, cv2.COLOR_RGB2GRAY)
        ret, thresh = cv2.threshold(grayImage, 48, 255, cv.CV_THRESH_BINARY_INV)
        thresh = cv2.medianBlur(thresh, 3)

        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) == 0:
            print 'can not find any contours'
            return 

        contoursLen = [len(contour) for contour in contours]
        targetContour = contours[contoursLen.index(max(contoursLen))]
        xlist = [item[0][0] for item in targetContour]
        ylist = [item[0][1] for item in targetContour]
        leftTop = (min(xlist), min(ylist))
        rightBottom = (max(xlist), max(ylist))
        crop = resize[leftTop[1]:rightBottom[1], leftTop[0]:rightBottom[0]]

        #cv2.imwrite("./result/step1_%d.png" % self.number, crop)
        #final = self.resizeImage(32, 32, crop)
        #final = self.resizeImage(32, 32, crop)
        final = self.resizeImage(16, 16, crop)

        height = final.shape[0]
        width = final.shape[1]

        widthList = []
        finalList = []
        finalArray = []
        for i in xrange(height):
            for j in xrange(width):
                #print final[i][j]
                if final[i][j][0] < 100:
                    #if 8 < i and i < 24 and 8 < j and j < 24:
                    #    widthList.append(255)
                    #else:
                        #widthList.append(1)
                    #widthList.append(1)
                    widthList.append(1.0)
                else:
                    #widthList.append(0)
                    widthList.append(0.0)

            #finalList.append(widthList)
            finalList += widthList
            finalArray.append(widthList)
            widthList = []

        return finalArray

    def normalFilter(self):
        resize = self.resizeImage(32, 32, self.image)

        height = resize.shape[0]
        width = resize.shape[1]

        widthList = []
        finalList = []
        for i in xrange(height):
            for j in xrange(width):
                #print resize[i][j]
                if resize[i][j][0] < 100:
                    #widthList.append(3)
                    if 8 < i and i < 24 and 8 < j and j < 24:
                        widthList.append(9)
                    else:
                        widthList.append(1)

                else:
                    widthList.append(0)
            finalList.append(widthList)
            widthList = []

        self.writeToFileNew(finalList)

    def getVector(self):
        resize = self.resizeImage(32, 32, self.image)

        height = resize.shape[0]
        width = resize.shape[1]

        widthList = []
        finalList = []
        for i in xrange(height):
            for j in xrange(width):
                #print resize[i][j]
                if resize[i][j][0] < 100:
                    #widthList.append(3)
                    #if 8 < i and i < 24 and 8 < j and j < 24:
                    if 75 < i and i < 225 and 75 < j and j < 255:
                        widthList.append(9)
                    else:
                        widthList.append(1)
                else:
                    widthList.append(0)
            finalList += widthList
            widthList = []

        return finalList

    def writeToFile(self, list):
        file = open("./files/%d.txt" % self.number, "wb")
        for line in list:
            for item in line:
                file.write(str(item))
            file.write("\n")

        file.close()

    def writeToFileNew(self, list):
        basePath = "../files/%d/" % self.number
        if os.path.exists(basePath):
            pass
        else:
            os.mkdir(basePath)

        file = open("%s/%s.txt" % (basePath, self.name), "wb")
        for line in list:
            for item in line:
                file.write(str(item))
            file.write("\n")

        file.close()

    def writeToFileNew(self, list):
        #basePath = "../files/%d/" % self.number
        basePath = str(os.path.join(os.path.dirname(__file__), '../files/%d' % self.number).replace('\\', '/'))
 
        if os.path.exists(basePath):
            pass
        else:
            os.mkdir(basePath)

        file = open("%s/%s.txt" % (basePath, self.name), "wb")
        for line in list:
            for item in line:
                file.write(str(item))
            file.write("\n")

        file.close()

    def show(self, image):
        """docstring for show"""
        cv2.imshow("cleantha", image)
        cv2.waitKey(3000)

if __name__ == '__main__':
    #for i in xrange(10):
        #source = "./0-9/%d.jpg" % i
        #imagefilter = ImageFilter(source, i)
        #imagefilter.filterImage()
        #imagefilter.normalFilter()
        #result = imagefilter.getVector()
        #print result
    basedir = "../numbers/"
    dirs = os.listdir(basedir)
    for dir in dirs:
        files = os.listdir(basedir + dir)
        for file in files:
            source = basedir + dir + "/" + file
            imagefilter = ImageFilter(source, number=int(dir[0]), name=str(file[0]))
            #imagefilter.normalFilter()
            imagefilter.filterImage()
