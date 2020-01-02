from django.db import models

class DatabasePermission(models.Model):
    class Meta:
        permissions = (
            ('scan_database',"Can scan 数据库管理"),
            ('scan_sql',"Can scan SQL脚本管理")
        )

class Database(models.Model):
    schema_name = models.CharField(max_length=40,null=True,blank=True,verbose_name="数据库schema名称")
    schema_url = models.CharField(max_length=40,null=True,blank=True,verbose_name="数据库url")
    schema_username = models.CharField(max_length=40,null=True,blank=True,verbose_name="数据库用户名")
    schema_password = models.CharField(max_length=40,null=True,blank=True,verbose_name="数据库密码")
    schema_env = models.CharField(max_length=40,null=True,blank=True,verbose_name="数据库所属环境")
    is_sql = models.IntegerField(null=False,default=0,verbose_name='是否有sql文件')

    def __str__(self):
        return "{}-{}".format(self.schema_name,self.schema_url)
    class Meta:
        verbose_name = "数据库管理"
        verbose_name_plural = verbose_name

class SqlFile(models.Model):
    sql_name = models.CharField(max_length=40,null=True,blank=True,verbose_name="SQL脚本名称",unique=True)
    sql_version = models.CharField(max_length=40,null=True,blank=True,verbose_name="SQL脚本版本")
    sql_content = models.TextField(null=True,blank=True,verbose_name="SQL脚本内容")
    database = models.ForeignKey(Database,null=True,blank=True,db_constraint=False,verbose_name="所属schema")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True,verbose_name="更新时间")

    def __str__(self):
        return "V{}__{}.sql".format(self.sql_version,self.sql_name)

    class Meta:
        verbose_name = "SQL脚本管理"
        verbose_name_plural = verbose_name
        db_table = "sql_script"