from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django_rpx.models import RpxData
from django.conf import settings

def permute_name(name_string, num):
    num_str=str(num)
    max_len=29-len(num_str)
    return ''.join([name_string[0:max_len], '-', num_str])

def rpx_response(request):
    token = request.GET.get('token', '')
    if not token:
        token = request.POST.get('token', '')
    if not token: return HttpResponseForbidden()
    user=authenticate(token=token)
    if user and user.is_active:
        return HttpResponseRedirect('/')
    else:
        return HttpResponseForbidden()
