from django.db import models
from django.utils.translation import gettext_lazy as _

class Report(models.Model):
    id = models.BigAutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=250)
    created_at = models.DateField(db_column='created_at')
    efficiency = models.CharField(db_column='efficiency', max_length=250)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = ('Reports')
        db_table = 'report'
        managed = True