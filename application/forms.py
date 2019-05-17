from django.forms import TextInput,Select,Textarea
from django import forms

class ServiceAddForm(forms.Form):
    name = forms.CharField(
        widget = TextInput(attrs={'id':'name','class':'form-control','placeholder':'请输入服务名称'})
    )
    desc = forms.CharField(
        widget = Textarea(attrs={'id':'desc','class':'form-control'}),required=False
    )
    port = forms.CharField(
        widget = TextInput(attrs={'id':'port','class':'form-control','placeholder':'请输入服务端口'})
    )
    log_dir = forms.CharField(
        widget = TextInput(attrs={'id':'log_dir','class':'form-control','placeholder':'请输入日志路径'})
    )

class ServiceUpdateForm(ServiceAddForm):
    def __init__(self,*args,**kwargs):
        super(ServiceAddForm,self).__init__(*args,**kwargs)