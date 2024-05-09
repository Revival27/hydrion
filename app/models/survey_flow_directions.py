from django.db import models
from django.utils.translation import gettext_lazy as _

class HydroSurveyFlowDirection(models.Model):
    id = models.BigAutoField(db_column='id', primary_key=True)
    name = models.DateField(db_column='name', verbose_name="Áramlási irány")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = ('Hydro Survey Flow Direction')
        db_table = 'hydrosurvey_flow_direction'
        managed = True