from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

# class Node(models.Model):
#     node_id = models.IntegerField(null=False,blank=False,verbose_name="节点ID",unique=True)
#     node_pid = models.IntegerField(null=False,blank=False,verbose_name="节点父ID")
#     name = models.CharField(max_length=255,null=False,blank=False,verbose_name="节点名称")
#     level = models.IntegerField(null=False,blank=False,verbose_name="层级")
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = "节点"
#         verbose_name_plural = verbose_name
#         permissions = (
#             ('scan_node','Can scan 节点'),
#         )

class Node(MPTTModel):
    name = models.CharField(max_length=255,null=True,blank=True,verbose_name="节点名称")
    parent = TreeForeignKey('self',null=True,blank=True,verbose_name="父节点")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "节点"
        verbose_name_plural = verbose_name
        db_table = "node"
        permissions = (
            ('scan_node','Can scan 节点'),
        )