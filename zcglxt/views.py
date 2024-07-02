from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
from zcglxt.models import data_all
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def index(request):
    return render(request,'index.html')


def index_v1(request):
    return render(request,'index_v1.html')
@csrf_exempt
def zcdj(request:WSGIRequest):
    if request.method == 'POST':
        print(request.POST.dict())
        post = request.POST.dict()
        db = data_all(number = post['number'],type_name = post['type_name'], \
                      model = post['model'],depart_name = post['depart_name'], \
                        pos = post['pos'],ip = post['ip'],descr = post['descr'], \
                            )
    return render(request,'zcdj.html',status=200)

def zcly(request):
    return render(request,'zcly.html')

def zcth(request):
    return render(request,'zcth.html')

def zctb(request):
    return render(request,'zctb.html')

def zcbb(request):
    return render(request,'zcbb.html')