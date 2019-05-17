from django.db import models

class Application(models.Model):
    class Meta:
        permissions = (
            ('scan_application','Can scan 应用管理'),
        )