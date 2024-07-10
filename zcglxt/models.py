from django.core.exceptions import ObjectDoesNotExist  
from django.db import models
import json

# Create your models here.


class edit_log(models.Model):
    model_name = models.CharField(max_length=100)
    instance_id = models.IntegerField()
    changes = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


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
    pos = models.CharField(max_length=20,verbose_name='位置')
    descr = models.TextField(max_length=100,null=True,verbose_name='备注')
    date = models.DateTimeField(auto_now=True,verbose_name='修改日期')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):  
        if self._state.adding:  # 检查对象是否是新创建的  
            # 如果是新对象，则不需要比较旧值  
            super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)  
            return  
  
        try:  
            old_record = self.__class__.objects.get(pk=self.pk)  
            changes = []  
            for field in self._meta.get_fields():  # 使用 get_fields() 来获取所有字段，包括关系字段  
                if field.name in self.get_deferred_fields():  # 排除延迟加载的字段  
                    continue  
                if field.is_relation:  # 如果是关系字段，可能需要特殊处理  
                    continue  # 或者您可以根据需要记录关系字段的变化  
                old_value = getattr(old_record, field.name)  
                new_value = getattr(self, field.name)  
                if old_value != new_value:  
                    changes.append({'field': field.name, 'old_value': old_value, 'new_value': new_value})  
            if changes:  
                # 记录更改日志  
                edit_log.objects.create(  
                    model_name=self.__class__.__name__,  
                    instance_id=self.pk,  
                    changes=json.dumps(changes)  
                )  
        except ObjectDoesNotExist:  
            # 理论上，这里不应该发生，除非数据库中的记录被意外删除  
            pass  
  
        # 最后，调用原始的 save 方法  
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)  
  
        