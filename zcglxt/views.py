from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
# Create your views here.

def index(request):
    return render(request,'index.html')


def index_v1(request):
    return render(request,'index_v1.html')

def zcdj(request:WSGIRequest):
    if request.GET != {}:
        print(request.COOKIES)
        print(request.GET)
        
    return render(request,'zcdj.html')

def zcly(request):
    return render(request,'zcly.html')

def zcth(request):
    return render(request,'zcth.html')

def zctb(request):
    return render(request,'zctb.html')

def zcbb(request):
    return render(request,'zcbb.html')