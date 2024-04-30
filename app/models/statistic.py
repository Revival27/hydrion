from django.db import models
from django.contrib.postgres import fields
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Statistic(models.Model):
    id = models.BigAutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=250)
    created_at = models.DateTimeField(db_column='created_at')
    efficiency = models.CharField(db_column='efficiency', max_length=250)
    class Meta:
        verbose_name = ('Statistics')
        db_table = 'statistics'
        managed = True