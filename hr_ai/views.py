
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import csv
def index(request):
     # data = pd.read_csv("") ee
    return render(request,'index.html')

def result(request):
    # if (request.method == 'POST'):
    #
    #     print(request)
    #     temp = request.POST.get('test','')
    #     print(temp)
    #     t = request.POST.get('fileInput','')
    #     print(t)
    #     print(type(t))
    #     # print(request.FILES['fileInput'])
    #     data = pd.read_csv('C:\Users\wasif\Downloads\final.csv')
    #     print(type(data))
    return HttpResponse('res.html')