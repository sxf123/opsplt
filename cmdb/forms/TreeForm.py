from django.forms import TextInput,Textarea,Select
from django import forms
from cmdb.models.Product import Product
from cmdb.models.Project import Project

class TreeForm(forms.Form):
    nodetype = forms.CharField(
        widget=Select(
            attrs={'id':'nodetype','class':'form-control'},
            choices=(
                ('','----------'),
                ('product','Product'),
                ('project','Project'),
                ('service','Service')
            )
        )
    )
    name = forms.CharField(
        widget=TextInput(attrs={'id':'name','class':'form-control','placeholder':'请输入节点名称'})
    )
    desc = forms.CharField(
        widget=Textarea(attrs={'id':'desc','class':'form-control'})
    )
    product = forms.CharField(
        widget=Select(attrs={'id':'product','class':'form-control'}),
        required=False
    )
    project = forms.CharField(
        widget=Select(attrs={'id':'product','class':'form-control'}),
        required=False
    )
    parent = forms.CharField(
        widget=Select(attrs={'id':'parent','class':'form-control'},choices=(('','----------'),('demo','父节点'))),
        required=False
    )
    def __init__(self,*args,**kwargs):
        super(TreeForm,self).__init__(*args,**kwargs)
        product_choices = list(Product.objects.all().values_list('name','name'))
        project_choices = list(Project.objects.all().values_list('name','name'))
        product_choices.insert(0,('','----------'))
        project_choices.insert(0,('','----------'))
        self.fields['product'].widget.choices = product_choices
        self.fields['project'].widget.choices = project_choices

