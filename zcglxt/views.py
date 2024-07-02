from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest

from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def index(request):
    return render(request,'index.html')


def index_v1(request):
    return render(request,'index_v1.html')
@csrf_exempt
def zcdj(request:WSGIRequest):
    if request.method == 'POST':
        print(request.POST)
    return render(request,'zcdj.html',status=200)

def zcly(request):
    return render(request,'zcly.html')

def zcth(request):
    return render(request,'zcth.html')

def zctb(request):
    return render(request,'zctb.html')

def zcbb(request):
    return render(request,'zcbb.html')