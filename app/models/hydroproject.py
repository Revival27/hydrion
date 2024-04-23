from django.db import models
from django.contrib.postgres import fields
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class HydroProject(models.Model):
    id = models.BigAutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=250)
    created_at = models.DateTimeField(db_column='created_at')
    status = models.CharField(db_column='status', max_length=250)
    deadline = models.DateField(db_column='deadline')
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    description = models.TextField(db_column='description')
    #tasks = models.    
    class Meta:
        verbose_name = ('Hydro Project')
        db_table = 'hydroproject'
        managed = True