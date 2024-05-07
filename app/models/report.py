from django.db import models
from django.utils.translation import gettext_lazy as _
from app.models import HydroTask

#feladatok teljesítési arányáról, a csapat termelékenységéről és a projekt ütemezéséről
class Report(models.Model):
    id = models.BigAutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=250)
    created_at = models.DateField(db_column='created_at')
    efficiency = models.CharField(db_column='efficiency', max_length=250)
    project = models.ForeignKey('HydroProject', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    def tasks_completion(self):
        tasks = HydroTask.objects.filter(project=self.project)
        completion_statuses = []
        status_to_value = {'Preparing': 0, 'In progress': 0.5, 'Done': 1}
        task_names = []
        for task in tasks:
            completion_statuses.append(task.status.name)
            task_names.append(task.name)
        completion_ratios = [status_to_value[status] for status in completion_statuses]
        return(task_names, completion_ratios)

    class Meta:
        verbose_name = ('Reports')
        db_table = 'report'
        managed = True