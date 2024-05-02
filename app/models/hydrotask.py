from django.db import models
from django.contrib.postgres import fields
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from datetime import timedelta



class HydroTask(models.Model):
    id = models.BigAutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=250)
    deadline = models.DateField(db_column='deadline')
    status = models.ForeignKey('TaskStatus', on_delete=models.CASCADE)
    description = models.TextField(db_column='description', max_length=1000)
    project = models.ForeignKey('HydroProject', on_delete=models.CASCADE)
    start_date = models.DateField(db_column='start_date')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = ('Hydro Task')
        db_table = 'hydrotask'
        managed = True    