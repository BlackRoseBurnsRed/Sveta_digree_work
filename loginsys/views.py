from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http.response import  HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.views.decorators.csrf import csrf_protect,  csrf_exempt, requires_csrf_token

# Create your views here.
@csrf_exempt
def login(request):
    args = {}
    print('ads: ')
    print(request.method)
    if request.method == "POST" and request.POST:
        username = request.POST.get('login', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            print('user is not none')
            return redirect('/')
        else:
            args['login_error'] = 'Пользователь не найден'
            return render_to_response('login.html', args)
    else:
        print('not post')
        return render_to_response('login.html', args)


def logout(request):
    auth.logout(request)
    print(request)
    return redirect('/')