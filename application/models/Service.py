from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=255,blank=False,null=False,unique=True,verbose_name="服务名称")
    desc = models.CharField(max_length=255,blank=False,null=False,verbose_name="服务描述")
    port = models.IntegerField(blank=False,null=False,verbose_name="服务端口")
    product = models.CharField(max_length=255,blank=False,null=False,verbose_name="所属产品")
    log_dir = models.CharField(max_length=255,blank=True,null=True,verbose_name="日志路径")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "服务"
        verbose_name_plural = verbose_name
        permissions = (
            ('scan_service','Can scan 服务'),
            ('download_log','Can download 服务日志'),
        )