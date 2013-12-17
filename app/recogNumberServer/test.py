from filterImage import ImageFilter

source = "../testsamples/cleantha.png"
imagefilter = ImageFilter(source)
vector, array = imagefilter.getVectorNew()
print len(vector)

file = open("./result.txt", "w")
for line in array:
    for item in line:
        file.write(str(item))
    file.write('\n')
file.close()
