# encoding: utf-8
from django.shortcuts import redirect
from functools import wraps
from django.http import JsonResponse



def login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.session.get('user') is None:
            if request.is_ajax():
                return JsonResponse({'code':403,'result':[]})
            return redirect('user:login')
        return func(request, *args, **kwargs)
    return wrapper