from django.db import models
from django.utils.translation import gettext_lazy as _

class Efficiency(models.Model):
    id = models.BigAutoField(db_column='id', primary_key=True)
    rho = models.FloatField(db_column='rho', default=1000)
    g = models.FloatField(db_column='gravity', default=9.81)
    Q = models.FloatField(db_column='volumetric_flow_rate', default=3)
    H = models.FloatField(db_column='effective_head', default=10)
    P_out = models.FloatField(db_column='output_power', default=250)
    P_in = models.FloatField(db_column='input_power')
    efficiency = models.FloatField(db_column='efficiency')
    class Meta:
        verbose_name = ('Efficiency')
        verbose_name_plural = 'Efficiencies'
        db_table = 'turbine_efficiency'
        managed = True