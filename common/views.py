from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from common.forms import LoginForm
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

@login_required
def index(request):
    return render(request,'common/base.html')

class LoginView(View):
    def __init__(self):
        self.context = {}
    def get(self,request,*args,**kwargs):
        login_form = LoginForm()
        self.context = {'login_form': login_form}
        return render(request,'common/login.html',self.context)
    def post(self,request,*args,**kwargs):
        url = request.GET.get('next')
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get("username")
            password = login_form.cleaned_data.get("password")
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                if url is not None:
                    return HttpResponseRedirect(url)
                else:
                    return HttpResponseRedirect(reverse('index'))
            else:
                self.context = {'login_form':login_form, 'password_is_wrong': True}
                return render(request,'common/login.html',self.context)
        else:
            self.context = {'login_form': login_form,'errors': login_form.errors}
            return render(request,'common/login.html',self.context)

class LogoutView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        auth.logout(request)
        return HttpResponseRedirect(reverse('login'))


@csrf_exempt
@require_http_methods(['POST'])
def user_exists(request):
    username = request.POST.get('username')
    user = User.objects.filter(username=username)
    if not user.exists():
        return JsonResponse(False,safe=False)
    else:
        return JsonResponse(True,safe=False)

@csrf_exempt
@require_http_methods(['POST'])
def password_check(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(username=username,password=password)
    if user is not None and user.is_active:
        return JsonResponse(True,safe=False)
    else:
        return JsonResponse(False,safe=False)

@require_http_methods(['GET'])
@login_required
def permission_denied(request):
    return render(request,'common/403.html')
