from django.shortcuts import render, redirect
from django.http import HttpResponse

from datetime import datetime
from .models import User
import hashlib



def login(request):
    if 'GET' == request.method:
        return render(request, 'user/login.html')
    if 'POST' == request.method:
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 验证:
        try:
            user = User.objects.get(name=username)
        except:
            return HttpResponse('用户名/密码错误')

        if user.password != password:
            return HttpResponse('用户名/密码错误')

        if user:
            request.session['user'] = user.as_dict()
            return redirect('user:index')
        else:
            return HttpResponse('用户名/密码错误')


def index(request):
    if not request.session.get('user'):
        return redirect('user:login')


    return render(request, 'user/index.html', {'users':User.objects.all()})



def logout(request):
    request.session.flush()
    return redirect('user:login')


def create(request):
    if 'GET' == request.method:
        return render(request, 'user/create.html')
    if 'POST' == request.method:
        errors = {}
        is_valid = True
        user = User()

        user.name = request.POST.get('username')
        user.password = request.POST.get('password')
        user.password_1 = request.POST.get('password_1')

        if user.name == '':
            errors['name'] = '用户名为空'
            is_valid = False

        try:
            User.objects.get(name=user.name)
            errors['name'] = '用户名已存在'
            is_valid = False
        except:
            pass



        if user.password == '' or user.password != user.password_1:
            errors['password'] = '密码不能为空，或者2次密码不相等'
            is_valid = False
        user.create_time = datetime.now()

        password = str(user.password).encode()

        md5 = hashlib.md5()
        md5.update(password)
        user.password = md5.hexdigest()

        if is_valid:
            user.save()
            return redirect('user:index')
        else: 
            return render(request, 'user/create.html', {'errors':errors})


def delete(request):
    user_id = request.GET.get('uid')
    try:
        User.objects.filter(id=user_id).delete()
        return redirect('user:index')
    except:
        return HttpResponse('删除失败')

def update(request):
    if 'GET' == request.method:
        uid = request.GET.get('uid')
        try:
            res = User.objects.get(id=uid)
            return render(request, 'user/view.html', {'user':res.as_dict()})
        except:
            pass
    if 'POST' == request.method:
        is_valid = True
        errors = {}

        uid = request.POST.get('id')
        password_old = request.POST.get('password_old')
        password = request.POST.get('password')
        password_1 = request.POST.get('password_1')

        user = User.objects.get(id=uid)
        if password_old != user.password:
            errors['password_old'] = '旧密码失败'
            is_valid = False

        if password == '' or password != password_1:
            errors['password_new'] = '密码不能为空，或者2次密码不相等'
            is_valid = False

        if is_valid:
            user.password = password
            user.save()
            return redirect('user:index')
        else:
            return render(request, 'user/view.html', {'errors':errors,'user':user})