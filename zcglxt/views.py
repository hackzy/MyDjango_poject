from django.shortcuts import render
from django.http import JsonResponse
from django.core.handlers.wsgi import WSGIRequest
from zcglxt.models import Data_All,Departments,Type_Names,Status,ObjectDoesNotExist
from zcglxt.froms import UploadFileForm
from django.views.decorators.csrf import csrf_exempt
from zcglxt.read_excel import ReadExcel
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
        typeName = Type_Names.objects.get(id=int(post['type_name']))
        departName = Departments.objects.get(id=int(post['depart_name']))
        statusValue = Status.objects.get(id=int(post['status']))
        db = Data_All(number = post['number'],type_name = typeName, \
                      model = post['model'],depart_name = departName, \
                        pos = post['pos'],ip = post['ip'],descr = post['descr'], \
                        status = statusValue    )
        db.save()
        return JsonResponse({'status':'scuess','message':'登记成功'})
    return render(request,'zcdj.html',status=200)

def get_options(request):
    depart_names = list(Departments.objects.values('id','name'))
    type_name = list(Type_Names.objects.values('id','name'))
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
            excel_file.save_to_db(Data_All,Departments,Type_Names,Status)
        return JsonResponse({'status':'scuess','message':'导入成功！'})

@csrf_exempt
def zcly(request:WSGIRequest):
    if request.method == 'POST':
        post = request.POST.dict()
        print(post)
        try:
            number = Data_All.objects.get(number = post['number'])
        except ObjectDoesNotExist:
            return JsonResponse({'status':'error','message':'请输入正确的资产编号！'})
        depart = Departments.objects.get(id=int(post['depart_name']))
        statusValue = Status.objects.get(status='在用')
        if depart.name == '仓库':
            statusValue = Status.objects.get(status='待用')
        number.depart_name = depart
        number.status = statusValue
        number.pos = post['pos']
        number.descr = post['descr']
        number.save()
        return JsonResponse({'status':'scuess','message':'保存成功'})
    return render(request,'zcly.html')

def get_inactive(request):
    data = Data_All.objects.filter(status = Status.objects.get(status = '待用')).values()
    data_list = []
    for row in data:
        data_list.append({
            'number' :row['number'],
            'type': Type_Names.objects.get(id=row['type_name_id']).name,
            'model':row['model'],
            'pos':row['pos'],
            'ip':row['ip'],
            'depart_name': Departments.objects.get(id=row['depart_name_id']).name,
            'status': Status.objects.get(id=row['status_id']).status,
            'descr':row['descr']
        })
    return JsonResponse({'status':'scuess','data':data_list})

def zcth(request):
    return render(request,'zcth.html')

def zctb(request):
    return render(request,'zctb.html')

def zcbb(request):
    path = "./test.xlsx"
    wb = load_workbook(path)
    ws = wb.active
    status = Status.objects.get(status="待用")
    data = Data_All.objects.filter(status = status)
    index = 1
    for value in data:
        ws.append([index,
                   value.number,
                   value.type_name.name,
                   value.model,
                   value.pos,
                   value.ip,
                   value.descr])
        index += 1
    wb.save("savetest.xlsx")
    return render(request,'zcbb.html')