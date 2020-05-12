from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.db import IntegrityError
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import CustomUserBase
import json
from django.middleware.csrf import get_token



def csrf(request):
    return JsonResponse({'x-csrftoken': get_token(request)})


def check(user):
    '''Checks the user_type to grant permission to access certain function'''
    if (user.user_type == "MANAGER"):
        return True
    else:
        return False

@require_http_methods(['POST'])
def user_login(request):
    '''user login function'''
    response_json = {}
    try:    
        if request.user.is_authenticated:
            response_json['status'] = True
            return JsonResponse(response_json)
        else:
            if request.method == 'POST':
                json_str = request.body.decode(encoding='UTF-8')
                data_json = json.loads(json_str)
                username = data_json['username']
                password = data_json['password']
                user = authenticate(request, username = username, password = password)
                if user is not None:
                    login(request,user)
                    response_json['status'] = True
                    return JsonResponse(response_json)
                else:
                    response_json = {'status':False, 'msg':'Username or Password is not correct.'}
                    return JsonResponse(response_json)
    except (KeyError, json.decoder.JSONDecodeError, Exception) as exp:
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})


@login_required
def user_logout(request):
    '''User logout function'''
    logout(request)
    return HttpResponseRedirect('/login')


@require_http_methods(['POST'])
def get_current_user(request):
    try:
        if (request.user.uuid):
            if request.method == 'POST':
                user = CustomUserBase.objects.get(id=int(request.user.id), uuid=request.user.uuid)
                user_json = {'first_name':user.first_name,
                    'last_name':user.last_name,
                    'user_type':user.user_type,
                    'username':user.username
                    }
                response_json = {'status':True, 'user_data':user_json}
                return JsonResponse(response_json)
        else:
            response_json = {'status':False, 'user_data':{}}
            return JsonResponse(response_json)
    except (KeyError, json.decoder.JSONDecodeError, ObjectDoesNotExist, IntegrityError, Exception) as exp:
        return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})