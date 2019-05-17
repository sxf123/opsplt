from django.db import models
from cmdb.models.Node import Node

class Host(models.Model):
    hostname = models.CharField(max_length=255,blank=False,null=False,verbose_name="主机名",unique=True)
    ipaddress = models.CharField(max_length=255, blank=False, null=False, verbose_name="IP地址", unique=True)
    hosttype = models.CharField(max_length=255,blank=False,null=True,verbose_name="服务器类型")
    cpu_nums = models.IntegerField(blank=False,null=True,verbose_name="CPU核数")
    memory = models.IntegerField(blank=False,null=True,verbose_name="内存")
    disk = models.IntegerField(blank=False,null=True,verbose_name="磁盘")
    node = models.ManyToManyField(Node,db_constraint=False,null=True)
    state = models.CharField(max_length=255,null=True,blank=True,verbose_name="主机状态")


    def __str__(self):
        return self.hostname

    class Meta:
        verbose_name = "主机"
        verbose_name_plural = verbose_name
        permissions = (
            ('scan_host','Can scan 主机'),
        )