#encoding: utf-8

import json
import time

from django.views.generic import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from asset.models import Host
import hmac
import urllib


def get_sign(data, time, key, secret):
    sign_data = data.copy()
    sign_data['time'] = time

    # 排序，不然会乱
    sorted_sign_data= sorted(sign_data.items())
    text_sign_data =  secret + ':' + urllib.parse.urlencode(sorted_sign_data)

    _hmac = hmac.HMAC(key.encode())
    _hmac.update(text_sign_data.encode())

    return _hmac.hexdigest()


class APIView(View):

    def __init__(self):
        super(APIView, self).__init__()
        self.secret_key = {'123456789' : 'abcdef'}


    def valid_sign(self, request):
        data = {}
        for key in request.GET:
            data[key] = request.GET.get(key)

        for key in request.POST:
            data[key] = request.POST.get(key)

        data.update(self.get_json())

        key = data.pop('key', '')
        sign = data.pop('sign', '')
        unix_time = data.pop('time', '')

        secret = self.secret_key.get(key, '')
        
        if not secret:
            return False, 'error key'


        data_sign = get_sign(data, unix_time, key, secret)
        if sign != data_sign:
            return False, 'sing error'

        try:
            unix_time = int(unix_time)
            current_unix_time = time.time()
            if not(unix_time >= current_unix_time - 5 *60 and unix_time <= current_unix_time + 5 *60):
                return False, 'error time'
        except BaseException as e:
            return False, 'error time'

        return True, ''


    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        is_valid, errors =  self.valid_sign(request)
        if is_valid:
            return super(APIView, self).dispatch(request, *args, **kwargs)
        else:
            return self.response(code=400, errors=errors)

    def get_json(self):
        try:
            return json.loads(self.request.body.decode('utf-8'))
        except BaseException as e:
            return {}

    def response(self, result=None, code=200, errors={}):

        return JsonResponse({'code': code, 'result' : result, 'errors' : errors})
        

class ClientView(APIView):

    def post(self, request, *args, **kwargs):
        _ip = kwargs.get('ip', '')
        _Json = self.get_json()

        host = Host.create_or_replace(
                                        _ip, \
                                        _Json.get('name', ''), \
                                        _Json.get('os', ''), \
                                        _Json.get('kernel', ''), \
                                        _Json.get('cpu_number', 0), \
                                        _Json.get('cpu_core', 0), \
                                        _Json.get('cpu_vcore', 0), \
                                        _Json.get('arch', ''), \
                                        _Json.get('get_mem_info', '[]'), \
                                        _Json.get('disk_info', '{}'), \
                                        _Json.get('get_gpu_info', '无'),
                                        _Json.get('project', ''),
                                    )

        return self.response(host.as_dict())


    def get(self, request, *args, **kwargs):
        _ip = kwargs.get('ip', '')
        if _ip == '':
            hosts = Host.objects.all()
            return self.response([host.as_dict() for host in hosts])
        else:
            try:            
                host = Host.objects.get(ip=_ip)
                return self.response(host.as_dict())
            except ObjectDoesNotExist as e:
                return self.response(code=404)


    def delete(self, request, *args, **kwargs):
        _ip = kwargs.get('ip', '')
        if _ip != '':
            try:
                host = Host.objects.get(ip=_ip)
                # 没做相应的函数
                host.delete()
                return self.response(host.as_dict())
            except ObjectDoesNotExist as e:
                pass
        return self.response(code=404)

