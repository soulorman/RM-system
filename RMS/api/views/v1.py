#encoding: utf-8
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from asset.models import Host
from django.core.exceptions import ObjectDoesNotExist
import json


class APIView(View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_json(self):
        try:
            return json.loads(self.request.body.decode('utf-8'))
        except:
            return {}

    def response(self, result=None, code=200, errors={}):

        return JsonResponse({'code': code, 'result' : result, 'errors' : errors})


class ClientView(APIView):

    def post(self, request, *args, **kwargs):
        _ip = kwargs.get('ip', '')
        _Json = self.get_json()
        print(_Json)
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
                return self.response(code=404, errors='网页丢失')


    def delete(self, request, *args, **kwargs):
        _ip = kwargs.get('ip', '')
        if _ip != '':
            try:
                host = Host.objects.get(ip=_ip)
                host.delete()
                return self.response(host.as_dict())
            except ObjectDoesNotExist as e:
                pass
        return self.response(code=404)
