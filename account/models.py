from django.db import models

class Account(models.Model):
    class Meta:
        permissions = (
            ('scan_account','Can scan 用户管理'),
            ('scan_user','Can scan 用户'),
            ('scan_group','Can scan 用户组'),
        )


