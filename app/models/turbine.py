from django.db import models
from django.utils.translation import gettext_lazy as _

class Turbine(models.Model):
    id = models.BigAutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=50)
    vortex = models.IntegerField(db_column='vortex')
    turbine_type = models.CharField(db_column='turbine_type', max_length=50)
    water_level = models.IntegerField(db_column='water_level')
    continous = models.CharField(db_column='continous', max_length=3)
    class Meta:
        verbose_name = ('Turbine')
        db_table = 'turbine'
        managed = True