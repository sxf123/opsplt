from django.forms import TextInput,PasswordInput
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        widget = TextInput(attrs={"id":"username","placeholder":u"用户名称","class":"form-control","style":"border: 1px solid rgba(255, 255, 255, 0.1);background: rgba(0, 0, 0, 0.1);border-radius: 5px;color: #fff;height: 50px;"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"id": "password", "placeholder": u"密码","class":"form-control","style":"border: 1px solid rgba(255, 255, 255, 0.1);background: rgba(0, 0, 0, 0.1);border-radius: 5px;color: #fff;height: 50px;"})
    )