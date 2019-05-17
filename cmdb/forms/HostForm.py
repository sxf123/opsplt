from django.forms import TextInput,Select,HiddenInput
from django import forms

class HostAddForm(forms.Form):
    hostname = forms.CharField(
        widget=TextInput(attrs={'id':'hostname','class':'form-control','placeholder':'请输入主机名'})
    )
    ipaddress = forms.GenericIPAddressField(
        widget=TextInput(attrs={'id':'ipaddress','class':'form-control','placeholder':'请输入IP地址'})
    )
    hosttype = forms.CharField(
        widget=Select(attrs={'id':'hsottype','class':'form-control'},choices=(('','----------'),('virtual','虚拟机'),('hyper','物理机')))
    )
    cpu_nums = forms.IntegerField(
        widget=TextInput(attrs={'id':'cpu_nums','class':'form-control','placeholder':'请输入CPU核数'})
    )
    memory = forms.IntegerField(
        widget=TextInput(attrs={'id':'memory','class':'form-control','placeholder':'请输入内存'})
    )
    disk = forms.IntegerField(
        widget=TextInput(attrs={'id':'disk','class':'form-control','placeholder':'请输入磁盘'})
    )

class HostUpdateForm(HostAddForm):
    hostname = forms.CharField(
        widget = TextInput(attrs={'id':'hostname','class':'form-control','disabled':'true'}),required=False
    )
    hostname_hidden = forms.CharField(
        widget = HiddenInput(attrs={'id':'hostname_hidden','class':'form-control','hidden':'true'})
    )