from django.shortcuts import render
from django.http import JsonResponse
from django.core.handlers.wsgi import WSGIRequest
from zcglxt.models import data_all,departments,type_names,status
from zcglxt.froms import UploadFileForm
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
        
        typeName = type_names.objects.get(id=int(post['type_name']))
        departName = departments.objects.get(id=int(post['depart_name']))
        statusValue = status.objects.get(id=int(post['status']))
        db = data_all(number = post['number'],type_name = typeName, \
                      model = post['model'],depart_name = departName, \
                        pos = post['pos'],ip = post['ip'],descr = post['descr'], \
                        status = statusValue    )
        db.save()
    return render(request,'zcdj.html',status=200)
def get_options(request):
    depart_names = list(departments.objects.values('id','name'))
    type_name = list(type_names.objects.values('id','name'))
    return JsonResponse({'depart_names':depart_names,'type_names':type_name},safe=False)
@csrf_exempt
def upload_file(request:WSGIRequest):
    if request.method == 'POST':
        form = UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            try:
                if file.content_type not in \
                    ['application/vnd.ms-excel','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']: \
                    return JsonResponse({'status':'error','message':'请上传Excel文件！'})
                
def zcly(request):
    return render(request,'zcly.html')

def zcth(request):
    return render(request,'zcth.html')

def zctb(request):
    return render(request,'zctb.html')

def zcbb(request):
    return render(request,'zcbb.html')