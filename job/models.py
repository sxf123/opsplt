from django.db import models

# Create your models here.

class Job(models.Model):
    job_name = models.CharField(max_length=255,null=False,blank=False,verbose_name="作业名称")
    job_desc = models.CharField(max_length=255,null=False,blank=False,verbose_name="作业描述")
    job_type = models.CharField(max_length=255,null=False,blank=False,verbose_name="作业类型")
    job_content = models.TextField(null=False,blank=False,verbose_name="作业内容")

    def __str__(self):
        return self.job_name

    class Meta:
        verbose_name = "作业"
        verbose_name_plural = verbose_name
        permissions = (
            ('scan_job','Can scan 作业'),
            ('exec_job','Can exec 作业'),
        )

class JobResult(models.Model):
    jobid = models.CharField(max_length=255,null=False,blank=False,verbose_name='作业ID')
    host = models.CharField(max_length=255,null=False,blank=False,verbose_name='主机')
    task = models.CharField(max_length=255,null=False,blank=False,verbose_name='任务名称')
    result = models.TextField(null=False,blank=False,verbose_name='任务结果')
    state = models.CharField(max_length=255,null=True,blank=True,verbose_name="任务执行状态")

    def __str__(self):
        return self.jobid + ',' + self.host + ',' + self.task

    class Meta:
        verbose_name = '作业结果'
        verbose_name_plural = verbose_name
        permissions = (
            ('scan_jobresult','Can scan 作业结果'),
        )

class JobState(models.Model):
    jobid = models.CharField(max_length=255,null=False,blank=False,unique=True,verbose_name='作业ID')
    jobname = models.CharField(max_length=255,null=False,blank=False,verbose_name='作业名称')
    start_time = models.CharField(max_length=255,null=False,blank=False,verbose_name="作业开始时间")
    stop_time = models.CharField(max_length=255,null=False,blank=False,verbose_name="作业结束时间")
    state = models.CharField(max_length=255,null=False,blank=False,verbose_name="作业执行状态")

    def __str__(self):
        return self.jobname

    class Meta:
        verbose_name = '作业执行状态'
        verbose_name_plural = verbose_name
        permissions = (
            ('scan_jobstate','Can scan 作业执行状态'),
        )