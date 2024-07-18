from django.shortcuts import render
from django.http import JsonResponse
from django.core.handlers.wsgi import WSGIRequest
from zcglxt.models import data_all,departments,type_names,status,ObjectDoesNotExist
from zcglxt.froms import UploadFileForm
from django.views.decorators.csrf import csrf_exempt
from zcglxt.read_excel import ReadExcel,pandas
from openpyxl import load_workbook
# Create your views here.

def index(request):
    return render(request,'index.html')

def index_v1(request):
    return render(request,'index_v1.html')

@csrf_exempt
def zcdj(request:WSGIRequest):
    if request.method == 'POST':
        post = request.POST.dict()
        typeName = type_names.objects.get(id=int(post['type_name']))
        departName = departments.objects.get(id=int(post['depart_name']))
        statusValue = status.objects.get(id=int(post['status']))
        db = data_all(number = post['number'],type_name = typeName, \
                      model = post['model'],depart_name = departName, \
                        pos = post['pos'],ip = post['ip'],descr = post['descr'], \
                        status = statusValue    )
        db.save()
        return JsonResponse({'status':'scuess','message':'登记成功'})
    return render(request,'zcdj.html',status=200)

def get_options(request):
    depart_names = list(departments.objects.values('id','name'))
    type_name = list(type_names.objects.values('id','name'))
    return JsonResponse({'depart_names':depart_names,'type_names':type_name},safe=False)

@csrf_exempt
def upload_file(request:WSGIRequest):
    if request.method == 'POST':
        form = UploadFileForm(request.POST,request.FILES)
        print('上传成功')
        if form.is_valid():
            file = form.files['file']
            try:
                if file.content_type not in \
                    ['application/vnd.ms-excel',
                     'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']: \
                    return JsonResponse({'status':'error','message':'请上传Excel文件！!!!'})
            except Exception as error:
                return JsonResponse({'status':'error',
                                     'message':str(error)})
            excel_file = ReadExcel(file)
            excel_file.save_to_db(data_all,departments,type_names,status)
        return JsonResponse({'status':'scuess','message':'导入成功！'})

@csrf_exempt
def zcly(request:WSGIRequest):
    if request.method == 'POST':
        post = request.POST.dict()
        print(post)
        try:
            number = data_all.objects.get(number = post['number'])
        except ObjectDoesNotExist:
            return JsonResponse({'status':'error','message':'请输入正确的资产编号！'})
        depart = departments.objects.get(id=int(post['depart_name']))
        statusValue = status.objects.get(status='在用')
        if depart.name == '仓库':
            statusValue = status.objects.get(status='待用')
        number.depart_name = depart
        number.status = statusValue
        number.pos = post['pos']
        number.descr = post['descr']
        number.save()
        return JsonResponse({'status':'scuess','message':'保存成功'})
    return render(request,'zcly.html')

def get_inactive(request):
    data = data_all.objects.filter(status = status.objects.get(status = '待用'))
    data_list = []
    for row in data:
        data_list.append({
            'number' :row.number,
            'type': row.type_name.name,
            'model':row.model,
            'pos':row.pos,
            'ip':row.ip,
            'depart_name': row.depart_name.name,
            'status': row.status.status,
            'descr':row.descr
        })
    return JsonResponse({'status':'scuess','data':data_list})

def zcth(request):
    return render(request,'zcth.html')

def zctb(request):
    return render(request,'zctb.html')

def zcbb(request):
    return render(request,'zcbb.html')

def bgdc(request):
    path = 'templates/zcglxt/test.xlsx'
    wb = load_workbook(path)
    ws = wb.active
    data = data_all.objects.filter(status = status.objects.get(status = "待用"))
    col = []
    index = 1
    for row in data:
        col.append([index,row.number,row.type_name.name,row.model,row.pos,row.ip,row.descr])
        index += 1
    for col_idx,value in enumerate(col,start=1):
        ws.cell(row=4,column=col_idx,value=value)
    wb.save()
    return JsonResponse({"status":"scuess","message":wb})