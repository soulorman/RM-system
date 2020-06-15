#encoding:utf-8
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

class Host(models.Model):
    ip = models.GenericIPAddressField(null=False, default='0.0.0.0')
    name = models.CharField(max_length=32, null=False, default='')
    os = models.CharField(max_length=64, null=False, default='')
    kernel = models.CharField(max_length=64, null=False, default='')

    cpu_number = models.IntegerField(null=False, default=0)  
    cpu_core = models.IntegerField(null=False, default=0)
    cpu_vcore = models.IntegerField(null=False, default=0)
    arch = models.CharField(max_length=16, null=False, default='x86')

    mem_info = models.CharField(max_length=512,null=False, default='[]')
    disk_info = models.CharField(max_length=512, null=False, default='{}')
    gpu_info = models.CharField(max_length=512,null=False, default='')
    
    remark = models.TextField(null=False, default='')
    project_name = models.CharField(max_length=64, null=False, default='ESD')
    discover_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(null=False)

    @classmethod
    def create_or_replace(cls, ip, name, os, kernel, cpu_number, cpu_core, cpu_vcore, arch, mem_info, disk_info, gpu_info, project_name):

        obj = None
        try:
            obj = cls.objects.get(ip=ip)
        except ObjectDoesNotExist as e:
            obj = cls()
            obj.ip = ip
            obj.remark = '无'
            obj.discover_time = timezone.now()

        obj.name = name
        obj.os = os
        obj.kernel = kernel
        obj.cpu_number =cpu_number
        obj.cpu_core = cpu_core
        obj.cpu_vcore = cpu_vcore
        obj.arch = arch
        obj.mem_info = mem_info
        obj.disk_info = disk_info
        obj.gpu_info = gpu_info
        obj.project_name = project_name

        obj.update_time = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        obj.save()
        return obj

    @classmethod
    def delete(cls, id):
        """删除数据

        :param id: 删除信息的id
        :return 删除成功的信息
        """
        return Host.objects.filter(pk=id).delete()


    @classmethod
    def update_remark(cls,ip,remark):
        """更新数据库

        :param ip: ip地址
        :param remark: 备注
        :return 更新成功的信息
        """
        return Host.objects.filter(ip=ip).update(remark=remark)


    def as_dict(self):
        """把对象转换为可序列化的dict

        :param self:传入对象
        :return: 返回字典
        """
        rt = {}
        for k, v in self.__dict__.items():
            if isinstance(v, (int, float, bool, str)):
                rt[k] = v

        return rt
