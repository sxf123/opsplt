from django.db import models

class Cmdb(models.Model):
    class Meta:
        permissions = (
            ('scan_cmdb','Can scan 资源管理'),
        )