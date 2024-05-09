from django.db import models
from django.contrib.postgres import fields
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Team(models.Model):
    id = models.BigAutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=250)   
    class Meta:
        verbose_name = ('Team')
        db_table = 'team'
        managed = True