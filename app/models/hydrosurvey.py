from django.db import models
from django.contrib.postgres import fields
from django.conf import settings
from django.utils.translation import gettext_lazy as _

CARDINAL_DIRECTIONS_TUPLE = (("N", "Észak"), ("E", "Kelet"), ("S", "Dél"), ("W", "Nyugat"))

class HydroSurvey(models.Model):
    id = models.BigAutoField(db_column='id', primary_key=True)
    deadline = models.DateTimeField(db_column='deadline', verbose_name="Határidő")
    status = models.CharField(db_column='status', max_length=250, verbose_name="Státusz")
    water_surface = models.CharField(db_column='water_surface', max_length=250, verbose_name="Vízfelület")
    location = models.CharField(db_column='location', max_length=250, verbose_name="Helyszín")
    flow_direction = models.CharField(db_column='flow_direction', max_length=10, choices=CARDINAL_DIRECTIONS_TUPLE, verbose_name="Áramlás iránya")
    flow_direction_speed = models.FloatField(db_column='flow_direction_speed', max_length=250, verbose_name="Áramlás mért sebessége")
    segment_width = models.DecimalField(db_column='segment_width', max_digits=1000, decimal_places=4, blank=True, verbose_name="Szelvény szélessége")
    segment_depth = models.DecimalField(db_column='segment_depth', max_digits=1000, decimal_places=4, blank=True, verbose_name="Szelvény mélysége")
    estimated_waterflow = models.CharField(db_column='estimated_waterflow', max_length=250, verbose_name="Becsült vízhozam")
    estimated_energy_production = models.DecimalField(db_column='estimated_energy_production', max_digits=1000, decimal_places=4, blank=True, verbose_name="Becsült energia termelés")
    
    class Meta:
        verbose_name = ('Hydro Survey')
        db_table = 'hydrosurvey'
        managed = True