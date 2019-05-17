from django.forms import TextInput,Select,PasswordInput,EmailInput
from django import forms

class UserAddForm(forms.Form):
    username = forms.CharField(
        widget = TextInput(attrs={'id':'username','class':'form-control','placeholder':'请输入用户名'})
    )
    password = forms.CharField(
        widget = PasswordInput(attrs={'id':'password','class':'form-control','placeholder':'请输入密码'})
    )
    first_name = forms.CharField(
        widget = TextInput(attrs={'id':'first_name','class':'form-control','placeholder':'请输入姓氏'}),required=False
    )
    last_name = forms.CharField(
        widget = TextInput(attrs={'id':'last_name','class':'form-control','placeholder':'请输入名字'}),required=False
    )
    email = forms.CharField(
        widget = EmailInput(attrs={'id':'email','class':'form-control','placeholder':'请输入邮箱'}),required=False
    )

class UserUpdateForm(UserAddForm):
    password = forms.CharField(
        widget = PasswordInput(attrs={'id':'password','class':'form-control','disabled':'disabled','value':'dddddddddd'}),
        required=False
    )

class UserUpdatePassword(forms.Form):
    username = forms.CharField(
        widget = TextInput(attrs={'id':'username','class':'form-control','disabled':'disabled'}),
        required=False
    )
    password = forms.CharField(
        widget = PasswordInput(attrs={'id':'password','class':'form-control','placeholder':'请输入新密码'})
    )
    confirm_password = forms.CharField(
        widget = PasswordInput(attrs={'id':'confirm_password','class':'form-control','placeholder':'请输入确认密码'})
    )

class GroupAddForm(forms.Form):
    name = forms.CharField(
        widget = TextInput(attrs={'id':'name','class':'form-control','placeholder':'请输入用户组名'})
    )

class GroupUpdateForm(GroupAddForm):
    def __init__(self,*args,**kwargs):
        super(GroupUpdateForm, self).__init__(*args,**kwargs)