from django.db import models
from django.utils.translation import gettext_lazy as _

class Efficiency(models.Model):
    id = models.BigAutoField(db_column='id', primary_key=True)
    ρ = models.IntegerField(db_column='rho', default=1000)
    g = models.FloatField(db_column='gravity', default=9.81)
    Q = models.FloatField(db_column='volumetric_flow_rate', default=3)
    H = models.FloatField(db_column='effective_head', default=10)
    P_out = models.FloatField(db_column='output_power', default=250)
    P_in = models.FloatField(db_column='input_power')
    efficiency = models.FloatField(db_column='efficiency')
    vortex = models.IntegerField(db_column='vortex')
    turbine_type = models.CharField(db_column='turbine_type', max_length=50)
    water_level = models.IntegerField(db_column='water_level')
    continous = models.CharField(db_column='continous', max_length=3)
    class Meta:
        verbose_name = ('Efficiency')
        db_table = 'turbine_efficiency'
        managed = True