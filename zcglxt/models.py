from django.db import models

# Create your models here.


class edit_log(models.Model):
    number = models.CharField(max_length=18)
    old_depart = models.CharField(max_length=20,null=True)
    old_ip = models.GenericIPAddressField(null=True,protocol='ipv4')
    old_position = models.CharField(max_length=20,null=True)
    date = models.DateTimeField(auto_now=True)


class departments(models.Model):
    name = models.CharField(max_length=20,verbose_name='机构名称')

class type_names(models.Model):
    name = models.CharField(max_length=20,verbose_name='分类名称')

class status(models.Model):
    status = models.CharField(max_length=6,verbose_name='状态')

class data_all(models.Model):
    number = models.CharField(max_length=18,verbose_name='资产编号')
    type_name = models.ForeignKey(type_names,verbose_name='分类名称',on_delete=models.PROTECT)
    model = models.CharField(max_length=20,verbose_name='规格型号')
    depart_name = models.ForeignKey(departments,verbose_name='使用机构',on_delete=models.PROTECT)
    ip = models.GenericIPAddressField(null=True,protocol='ipv4')
    status = models.ForeignKey(status,verbose_name='状态',on_delete=models.PROTECT)
    pos = models.CharField(max_length=20)
    descr = models.TextField(max_length=100,null=True)
    date = models.DateTimeField(auto_now=True)