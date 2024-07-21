from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from openpyxl import load_workbook
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
import datetime
#=====================================================================
from zcglxt.models import Data_All,Departments,Type_Names,Status,UploadFileForm,LoginForm,ObjectDoesNotExist,Edit_Log
from zcglxt.read_excel import ReadExcel
from zcglxt.export_excel import ExportExcel


# Create your views here.
def login_auth(request:WSGIRequest):
    if request.method == 'POST':
        form = LoginForm(request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request=request,username=username,password=password)
            if user is not None:
                login(request,user)
                return JsonResponse({'redirect_url':'/'},status=200)
            else:
                return JsonResponse({"error":"用户名或密码错误！"},status=401)
        else:
            return JsonResponse({"error":"用户名或密码错误！"},status=401)
    else:
        return render(request,'login.html')

def logout_auth(request):
    logout(request)
    return redirect('login')

@login_required
def index(request):
    return render(request,'index.html')

@login_required
def index_v1(request):
    return render(request,'index_v1.html')

@login_required
def zcdj(request:WSGIRequest):
    if request.method == 'POST':
        post = request.POST.dict()
        try:
            typeName = Type_Names.objects.get(id=int(post['type_name']))
            departName = Departments.objects.get(id=int(post['depart_name']))
            statusValue = Status.objects.get(id=int(post['status']))
            db = Data_All(number = post['number'],type_name = typeName, \
                        model = post['model'],depart_name = departName, \
                            pos = post['pos'],ip = post['ip'],descr = post['descr'], \
                            status = statusValue    )
        except ObjectDoesNotExist as error:
            return JsonResponse({'status':'error','message':str(error)})
        db.save()
        return JsonResponse({'status':'scuess','message':'登记成功'})
    return render(request,'zcdj.html',status=200)

@login_required
def get_options(request):
    depart_names = list(Departments.objects.values('id','name'))
    type_name = list(Type_Names.objects.values('id','name'))
    return JsonResponse({'depart_names':depart_names,'type_names':type_name},safe=False)

@login_required
def upload_file(request:WSGIRequest):
    if request.method == 'POST':
        form = UploadFileForm(request.POST,request.FILES)
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
    
@login_required
def zcly(request:WSGIRequest):
    if request.method == 'POST':
        post = request.POST.dict()
        try:
            depart = Departments.objects.get(id=int(post['depart_name']))
            try:
                number = Data_All.objects.get(number = post['number'])
            except ObjectDoesNotExist:
                return JsonResponse({'status':'error','message':'请输入正确的资产编号！'})
            try:
                statusValue = Status.objects.get(id=post['status'])
            except KeyError:
                if depart.name == '仓库':
                    statusValue = Status.objects.get(status='待用')
                else:
                    statusValue = Status.objects.get(status="在用")
        except ObjectDoesNotExist as error:
            return JsonResponse({'status':'error','message':str(error)})
        old_depart = number.depart_name.name
        new_depart = depart.name
        number.depart_name = depart
        number.status = statusValue
        number.pos = post['pos']
        number.descr = post['descr']
        number.ip = post['ip']
        number.save()
        start_date = datetime.date.today()
        end_date = datetime.datetime.now()
        download_link = '"/bgdc?old_depart=%s&new_depart=%s&start_date=%s&end_date=%s"' % (old_depart,new_depart,start_date,end_date)
        return JsonResponse({'message':'保存成功,点此','link':'<a href=%s>下载报表</a>'%(download_link)},status=200)
    return render(request,'zcly.html')

@login_required
def get_inactive(request):
    data = Data_All.objects.all().values()
    data_list = []
    try:
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
    except ObjectDoesNotExist as error:
        return JsonResponse({'status':'error','message':str(error)})
    return JsonResponse({'status':'scuess','data':data_list})

@login_required
def zcth(request):
    return render(request,'zcth.html')

@login_required
def zctb(request):
    return render(request,'zctb.html')

@login_required
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

@login_required
def bgdc(request:WSGIRequest):
    path = 'templates/zcglxt/test.xlsx'
    wb = load_workbook(path)
    export = ExportExcel(wb)
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    old_depart = request.GET['old_depart']
    new_depart = request.GET['new_depart']
    if old_depart != '仓库':
        export.wb.copy_worksheet(wb.worksheets[0])
        export.set_worksheet(start_date,end_date,0,old_depart)
    export.set_worksheet(start_date,end_date,1,new_depart)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=test.xlsx'
    export.wb.save(response)
    return response