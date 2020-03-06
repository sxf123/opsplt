from django.shortcuts import render
from django.views.generic import View
from account.forms import UserAddForm,UserUpdateForm,GroupAddForm,GroupUpdateForm
from django.contrib.auth.models import Group,User
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.db.models import Q

@require_http_methods(['GET'])
@login_required
@permission_required('account.scan_user',raise_exception=True)
def user_list(request):
    user = User.objects.all()
    context = {'user':user}
    return render(request,'account/user/user_list.html',context)


class UserAdd(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required('auth.add_user',raise_exception=True))
    def get(self,request,*args,**kwargs):
        user_add_form = UserAddForm()
        group = Group.objects.all()
        self.context = {'user_add_form':user_add_form,'group':[{'id':g.id,'text':g.name} for g in group]}
        return render(request,'account/user/user_add.html',self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required('auth.add_user',raise_exception=True))
    def post(self,request,*args,**kwargs):
        user_add_form = UserAddForm(request.POST)
        if user_add_form.is_valid():
            username = user_add_form.cleaned_data.get('username')
            password = user_add_form.cleaned_data.get('password')
            first_name = user_add_form.cleaned_data.get('first_name')
            last_name = user_add_form.cleaned_data.get('last_name')
            email = user_add_form.cleaned_data.get('email')
            is_superuser = True if request.POST.get('is_super_user') == 1 else False
            is_staff = True if request.POST.get('is_staff') == 1 else False
            group = request.POST.getlist('group')
            user = User(
                username = username,
                first_name = first_name,
                last_name=last_name,
                email = email,
                is_superuser = is_superuser,
                is_staff = is_staff
            )
            user.set_password(password)
            user.save()
            for g in group:
                user.groups.add(Group.objects.get(pk=g))
            return HttpResponseRedirect(reverse('user_list'))
        else:
            self.context = {'user_add_form': user_add_form,'errors': user_add_form.errors}
            return render(request,'account/user/user_add.html',self.context)

class UserUpdate(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required('auth.change_user',raise_exception=True))
    def get(self,request,*args,**kwargs):
        id = kwargs.get('id')
        user = User.objects.get(pk=id)
        user_update_form = UserUpdateForm(model_to_dict(user))
        group = Group.objects.all()
        self.context = {'user_update_form': user_update_form,'user':user,'group':[{'id':g.id,'text':g.name} for g in group],'group_id_list':[g.id for g in user.groups.all()]}
        return render(request,'account/user/user_update.html',self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required('auth.change_user',raise_exception=True))
    def post(self,request,*args,**kwargs):
        user_update_form = UserUpdateForm(request.POST)
        if user_update_form.is_valid():
            id = kwargs.get('id')
            user = User.objects.get(pk=id)
            user.username = user_update_form.cleaned_data.get('username')
            user.first_name = user_update_form.cleaned_data.get('first_name')
            user.last_name = user_update_form.cleaned_data.get('last_name')
            user.email = user_update_form.cleaned_data.get('email')
            user.is_superuser = True if request.POST.get('is_superuser') == 1 else False
            user.is_staff = True if request.POST.get('is_staff') == 1 else False
            user.save()
            group = request.POST.getlist('group')
            for g in user.groups.all():
                user.groups.remove(g)
                user.save()
            for g in group:
                user.groups.add(Group.objects.get(pk=g))
                user.save()
            return HttpResponseRedirect(reverse('user_list'))
        else:
            self.context = {'user_update_form':user_update_form,'errors':user_update_form.errors}
            return render(request,'account/user/user_update.html',self.context)

@require_http_methods(['POST'])
@login_required
@permission_required('auth.delete_user',raise_exception=True)
def user_delete(request):
    id = request.POST.get('id')
    user = User.objects.get(pk=id)
    for group in user.groups.all():
        user.groups.remove(group)
        user.save()
    user.delete()
    return JsonResponse({'message':'delete user {} success'.format(user.username)})

@require_http_methods(['GET'])
@login_required
@permission_required('account.scan_group',raise_exception=True)
def group_list(request):
    group =Group.objects.all()
    context = {'group':group}
    return render(request,'account/group/group_list.html',context)

class GroupAdd(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required('auth.add_group',raise_exception=True))
    def get(self,request,*args,**kwargs):
        group_add_form = GroupAddForm()
        content = ContentType.objects.filter(Q(app_label='cmdb') | Q(app_label='job') | Q(app_label='application') | Q(app_label='account') | Q(app_label='auth') | Q(app_label='database') | Q(app_label='consul_manage') | Q(app_label='deployment'))
        permission_list = []
        for c in content:
            permission = Permission.objects.filter(content_type=c)
            for p in permission:
                permission_list.append({'id':p.codename,'text':p.name})
        self.context = {'group_add_form':group_add_form,'permission':permission_list}
        return render(request,'account/group/group_add.html',self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required('auth.add_group',raise_exception=True))
    def post(self,request,*args,**kwargs):
        group_add_form = GroupAddForm(request.POST)
        if group_add_form.is_valid():
            name = group_add_form.cleaned_data.get('name')
            select_permission = request.POST.getlist('permission')
            group = Group(name=name)
            group.save()
            for permission in select_permission:
                group.permissions.add(Permission.objects.get(codename=permission))
                group.save()
            return HttpResponseRedirect(reverse('group_list'))
        else:
            self.context = {'group_add_form': group_add_form,'errors':group_add_form.errors}
            return render(request,'account/group/group_add.html',self.context)

class GroupUpdate(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required('auth.change_group',raise_exception=True))
    def get(self,request,*args,**kwargs):
        id = kwargs.get('id')
        group = Group.objects.get(pk=id)
        group_update_form = GroupUpdateForm(model_to_dict(group))
        content = ContentType.objects.filter(Q(app_label='cmdb') | Q(app_label='job') | Q(app_label='application') | Q(app_label='account') | Q(app_label='auth') | Q(app_label='database') | Q(app_label='consul_manage') | Q(app_label='deployment'))
        permission_list = []
        for c in content:
            permission = Permission.objects.filter(content_type=c)
            for p in permission:
                permission_list.append({'id':p.codename,'text':p.name})
        self.context = {'group_update_form': group_update_form,'permission':permission_list,'permission_select':[p.codename for p in group.permissions.all()]}
        return render(request,'account/group/group_update.html',self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required('auth.change_group',raise_exception=True))
    def post(self,request,*args,**kwargs):
        group_update_form = GroupUpdateForm(request.POST)
        if group_update_form.is_valid():
            name = group_update_form.cleaned_data.get('name')
            permission_select = request.POST.getlist('permission')
            id = kwargs.get('id')
            group = Group.objects.get(pk=id)
            group.name = name
            group.save()
            for permission in group.permissions.all():
                group.permissions.remove(permission)
                group.save()
            for permission in permission_select:
                group.permissions.add(Permission.objects.get(codename=permission))
                group.save()
            return HttpResponseRedirect(reverse('group_list'))
        else:
            self.context = {'group_update_form':group_update_form,'errors':group_update_form.errors}
            return render(request,'account/group/group_update.html',self.context)

@require_http_methods(['POST'])
@login_required
@permission_required('auth.delete_group',raise_exception=True)
def group_delete(request):
    id = request.POST.get('id')
    group = Group.objects.get(pk=id)
    for permission in group.permissions.all():
        group.permissions.remove(permission)
        group.save()
    group.delete()
    return JsonResponse({'message':'delete group {} success'.format(group.name)})

class ChangePassword(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        username = request.user
        user = User.objects.get(username=username)
        self.context = {'user':user}
        return render(request,'account/user/change_password.html',self.context)
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        username = request.user
        user = User.objects.get(username=username)
        new_password = request.POST.get('new_password')
        user.set_password(new_password)
        user.save()
        return HttpResponseRedirect(reverse('index'))