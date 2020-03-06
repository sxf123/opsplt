from django.db import models

# Create your models here.

class ConsulPermission(models.Model):
    class Meta:
        permissions = (
            ('scan_consul',"Can scan Consul"),
        )
        db_table = "consul_permissions"

class ConsulStatus(models.Model):
    address = models.CharField(max_length=20,null=True,blank=True,verbose_name="consul地址")
    port = models.IntegerField(null=True,blank=True,verbose_name="consul端口")
    custom = models.CharField(max_length=30,null=True,blank=True,verbose_name="所属客户")
    status = models.IntegerField(null=True,blank=True,verbose_name="状态")

    def __str__(self):
        return self.custom
    class Meta:
        verbose_name = "Consul"
        verbose_name_plural = verbose_name
        db_table = "consul_manage"
