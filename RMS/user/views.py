# encoding: utf-8
from django.shortcuts import render, redirect
from django.http import JsonResponse

from .models import User
from utils.login_auth import login_required
from .validator import UserValiator

def login(request):
    if 'GET' == request.method:
        return render(request, 'user/login.html')
    else:
        name = request.POST.get('name')
        password = request.POST.get('password')
        user = UserValiator.valid_login(name, password)
        if user:
            request.session['user'] = user.as_dict()
            return redirect('user:index')
        else:
            return render(request, 'user/login.html', {
                'errors': {'default':'用户名或者密码错误'}
                })


@login_required
def index(request):
    users = User.objects.all()
    for user in users:
        user.password = len(user.password) * '*'
    return render(request, 'user/index.html', {'users':users})


def logout(request):
    request.session.flush()
    return redirect('user:login')


@login_required
def create_ajax(request):
    """创建用户

    :param request:前端页面返回的请求内容
    :return: 根据验证结果，返回创建成功，或者返回报错信息
    """
    is_valid, user, errors = UserValiator.valid_create(request.POST)
    if is_valid:
        user.save()
        return JsonResponse({'code' : 200 })
    else:
        return JsonResponse({'code' : 400, 'errors' : errors })



@login_required
def delete_ajax(request):
    """创建用户

    :param request:前端页面返回的请求内容
    :return: 根据验证结果，返回创建成功，或者返回报错信息
    """
    id = request.GET.get('id', '')

    try:
        User.objects.filter(pk=id).delete()    
        return JsonResponse({'code' : 200 })
    except BaseException as e:
        return JsonResponse({'code' : 400, 'errors' : e })



@login_required
def changepass_ajax(request):
    """修改用户密码
    
    :param request:前端页面返回的请求内容
    :return: 修改成功或者报错信息
    """
    is_valid, user, errors = UserValiator.valid_changepass(request.POST)
    if is_valid:
        User.objects.filter(pk=user.id).update(password=user.password)
        return JsonResponse({'code' : 200 })
    else:
        return JsonResponse({'code' : 400, 'errors' : errors })
