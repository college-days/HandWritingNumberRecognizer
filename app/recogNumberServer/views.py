# -*- coding: UTF-8 -*- 
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import os
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from filterImage import ImageFilter
from knn import Knn
from svm import svmdecision
from ann import anndecision

def root(request):
    return HttpResponseRedirect("/index/")

@csrf_exempt
def index(request):
    #return render_to_response("upload.html", {})
    return render_to_response("uploadnew.html", {'result': ''})

@csrf_exempt
def getImage(request):
    pic_obj = request.FILES.get('picfile', None)

    if pic_obj == None:
        pass
    else:
        file_name = str(pic_obj)
        file_full_path = str(os.path.join(os.path.dirname(__file__), '../testsamples').replace('\\', '/'))
        print file_full_path
        if os.path.exists(file_full_path):
            pass
        else:
            os.mkdir(file_full_path)
        des_origin_f = open(file_full_path + "/cleantha.png", "wb")
        for chunk in pic_obj.chunks():
            des_origin_f.write(chunk)
        des_origin_f.close()

    return HttpResponseRedirect("/process/")

def processImage(request):
    source = str(os.path.join(os.path.dirname(__file__), '../testsamples/cleantha.png').replace('\\', '/'))
    imagefilter = ImageFilter(source)
    vectorTarget = imagefilter.getVectorNormal()
    arrayTarget = imagefilter.getArrayNormal()
    #vectorTarget = imagefilter.getVectorNew()
    #arrayTarget = imagefilter.getArrayNew()

    knnmachine = Knn(3)
    knnmachine.test = vectorTarget
    knnresult = knnmachine.getNumber()

    svmresult = svmdecision(arrayTarget)
    annresult = anndecision(vectorTarget)
    
    #感觉靠谱程度是svm > knn > ann

    resultList = [knnresult, svmresult, annresult]
    print resultList
    result = -1
    if len(list(set(resultList))) == len(resultList):
        result = resultList[0]
    elif resultList[0] != resultList[1] and resultList[1] == resultList[2]:
        result = int(sum(resultList)/len(resultList))
    else:
        result = max(set(resultList), key=resultList.count)

    return render_to_response("uploadnew.html", {'result': '%d' % int(result)})

