from django.db import models
from django.utils.translation import gettext_lazy as _
from app.models import HydroTask, TaskStatus

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
        task_names = []
        completion_statuses = []
        for task in tasks:
           task_status = TaskStatus.objects.get(pk=task.status_id)
           task_names.append(task.name)
           completion_statuses.append(task_status.completion_value)
        return (task_names, completion_statuses)
    
    class Meta:
        verbose_name = ('Report')
        db_table = 'report'
        managed = True