from django.db import models

class DeploymentPermissions(models.Model):
    class Meta:
        permissions = (
            ("scan_deployment","Can scan 发布管理"),
            ("scan_project","Can scan 项目管理"),
            ("scan_ticket","Can scan 工单管理")
        )
        db_table = "deploy_permission"

class Project(models.Model):
    project_name = models.CharField(max_length=40,null=True,blank=True,verbose_name="项目名称")
    project_git_url = models.CharField(max_length=255,null=True,blank=True,verbose_name="项目gitlab地址")
    project_port = models.CharField(max_length=20,null=True,blank=True,verbose_name="项目端口")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True,verbose_name="更新时间")

    def __str__(self):
        return self.project_name
    class Meta:
        verbose_name = "项目"
        verbose_name_plural = verbose_name
        db_table = "project"

class Ticket(models.Model):
    ticket_no = models.CharField(max_length=20,null=True,blank=True,verbose_name="工单编号")
    deploy_title = models.CharField(max_length=255,null=True,blank=True,verbose_name="工单标题")
    project = models.CharField(max_length=255,null=True,blank=True,verbose_name="所属项目")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    sql_content = models.TextField(null=True,blank=True,verbose_name="SQL脚本")
    config_content = models.TextField(null=True,blank=True,verbose_name="配置项")
    status = models.IntegerField(null=True,blank=True,verbose_name="工单状态")

    def __str__(self):
        return self.ticket_no
    class Meta:
        verbose_name = "工单"
        verbose_name_plural = verbose_name
        db_table = "deploy_ticket"
