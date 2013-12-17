def calcAccuracy(sourcepath, resultpath):
    file = open(sourcepath, "r")
    numbers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    totalNumber = 0

    for line in file.readlines():
        resultList = line[:-1].split('-')
        result = resultList[0]
        number = resultList[1]

        if int(number) == 0 and result == 'true': 
            numbers[0] += 1
        elif int(number) == 1 and result == 'true':
            numbers[1] += 1
        elif int(number) == 2 and result == 'true':
            numbers[2] += 1
        elif int(number) == 3 and result == 'true':
            numbers[3] += 1
        elif int(number) == 4 and result == 'true':
            numbers[4] += 1
        elif int(number) == 5 and result == 'true':
            numbers[5] += 1
        elif int(number) == 6 and result == 'true':
            numbers[6] += 1
        elif int(number) == 7 and result == 'true':
            numbers[7] += 1
        elif int(number) == 8 and result == 'true':
            numbers[8] += 1
        elif int(number) == 9 and result == 'true':
            numbers[9] += 1
        else:
            pass

        if result == 'true':
            totalNumber += 1

    file.close()

    totalFile = open("./staticResult.txt", "r")
    resultFile = open(resultpath, "w")
    for line in totalFile.readlines():
        resultList = line[:-1].split('-')
        total = resultList[1]
        number = resultList[0]

        accuracy = float(numbers[int(number)])/float(total)

        print int(accuracy*1000)

        resultFile.write("%d-%d" % (int(number), int(accuracy*1000)))
        resultFile.write('\n')

    totalAccuracy = float(totalNumber)/float(1593)
    resultFile.write("total-%d" % int(totalAccuracy*1000))

    resultFile.close()
    totalFile.close()

if __name__ == '__main__':
    calcAccuracy("../knn/semeionknnresult.txt", "./accuracyresult/knn.txt")
    calcAccuracy("../logistic/semeionlogisticresult.txt", "./accuracyresult/logistic.txt")
    calcAccuracy("../svm/semeionsvmresult.txt", "./accuracyresult/svm.txt")
    calcAccuracy("../ann/semeionannresult.txt", "./accuracyresult/ann.txt")
    calcAccuracy("../svm/semeionsvmresultnew.txt", "./accuracyresult/svmnew.txt")
