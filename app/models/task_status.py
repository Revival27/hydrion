from django.db import models
from django.contrib.postgres import fields
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class TaskStatus(models.Model):
    id = models.BigAutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=250)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = ('Task Status')
        verbose_name_plural = 'Task Stasuses'
        db_table = 'task_status'
        managed = True