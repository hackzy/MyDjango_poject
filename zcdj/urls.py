from django.contrib import admin
from django.urls import path,include
from zcdj.views import index,index_v1,zcdj,zcbb,zcly,zctb,zcth
urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', index),
    path('index_v1',index_v1),
    path('zcdj',zcdj), 
    path('zcbb',zcbb),
    path('zcly',zcly),
    path('zctb',zctb),
    path('zcth',zcth),
]