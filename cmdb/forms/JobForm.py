from django import forms
from django.forms import TextInput

class JobAddForm(forms.Form):
    module = forms.CharField(
        widget = TextInput(attrs={'id':'module','class':'form-control','placeholder':'请输入模块'})
    )
    vars = forms.CharField(
        widget = TextInput(attrs={'id':'vars','class':'form-control','placeholder':'请输入参数'})
    )