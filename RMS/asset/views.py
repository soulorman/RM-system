from django.shortcuts import render
from utils.login_auth import login_required
from django.http import JsonResponse
from .models import Host

@login_required
def index(request):
    return  render(request, 'asset/index.html')

@login_required
def list_ajax(request):
    result = []
    try:
        a = [host.as_dict() for host in Host.objects.all()]

        # for i in a:
        #     info_mem = eval(i.mem_info)
        #     temp_mem = ''
        #     for index, mem in enumerate(info_mem):
        #         temp_mem += str(index) + mem + '<br />'
        #     i.mem_info = temp_mem

        #     info_disk = eval(i.disk_info)

        #     temp_disk = "磁盘名称\t磁盘总容量<br />"
        #     for name,volume in info_disk.items():
        #         temp_disk += name + '\t\t' + str(volume) + '<br />'
        #     i.disk_info = temp_disk

        #     if '无显卡' != i.gpu_info:

        #         info_gpu = eval(i.gpu_info)
        #         temp_gpu = ''
        #         for gpu in info_gpu:
        #             temp_gpu += gpu + '<br />'
        #         i.gpu_info = temp_gpu

        #     info_remark = i.remark
        #     if '无' == info_remark:
        #         i.remark = i.project_name

        #     result.append(i.as_dict())



    except BaseException as e:
        print(e)
    
    return JsonResponse({'code' : 200, 'result': a })


@login_required
def delete_ajax(request):
    """删除主机信息

    :param request:前端页面返回的请求内容
    :return: 删除成功或者报错信息
    """
    _id = request.GET.get('id', 0)
    try:
        Host.delete(_id)
        return JsonResponse({'code' : 200 })
    except ObjectDoesNotExist as e:
        return JsonResponse({'code' : 400 ,'errors' : e})
