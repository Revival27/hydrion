from django.db import models
from django.contrib.postgres import fields
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class HydroSurvey(models.Model):
    id = models.BigAutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=250)
    deadline = models.DateTimeField(db_column='deadline')
    status = models.CharField(db_column='status', max_length=250)
    water_surface = models.CharField(db_column='water_surface', max_length=250)
    location = models.CharField(db_column='location', max_length=250)
    flow_direction = models.CharField(db_column='flow_direction', max_length=250)
    flow_direction_speed = models.FloatField(db_column='flow_direction_speed', max_length=250)
    segment_width = models.DecimalField(db_column='segment_width', max_digits=1000, decimal_places=4, blank=True)
    segment_depth = models.DecimalField(db_column='segment_depth', max_digits=1000, decimal_places=4, blank=True)
    estimated_waterflow = models.CharField(db_column='estimated_waterflow', max_length=250)
    estimated_energy_production = models.DecimalField(db_column='estimated_energy_production', max_digits=1000, decimal_places=4, blank=True)
    
    class Meta:
        verbose_name = ('Hydro Survey')
        db_table = 'hydrosurvey'
        managed = True