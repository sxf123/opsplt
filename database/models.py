from django.db import models

class Database(models.Model):
    schema_name = models.CharField(max_length=40,null=True,blank=True,verbose_name="数据库schema名称")
    schema_url = models.CharField(max_length=40,null=True,blank=True,verbose_name="数据库url")
    schema_username = models.CharField(max_length=40,null=True,blank=True,verbose_name="数据库用户名")
    schema_password = models.CharField(max_length=40,null=True,blank=True,verbose_name="数据库密码")
    schema_env = models.CharField(max_length=40,null=True,blank=True,verbose_name="数据库所属环境")

    def __str__(self):
        return "{}-{}".format(self.schema_name,self.schema_url)
    class Meta:
        verbose_name = "数据库管理"
        verbose_name_plural = verbose_name
