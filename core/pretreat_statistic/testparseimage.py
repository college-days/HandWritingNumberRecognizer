def parse_image(path):
    sampleList = []
    fp = open(path, "r") 
    for line in fp:
        line = line[:-1]
        #print line
        #sampleList += line.replace('1', '9')
        print line
        print '\n'
        sampleList += line
    return sampleList

if __name__ == '__main__':
    basepath = "./semeionsamples/0/3.txt"
    print parse_image(basepath)
