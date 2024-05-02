from django.db import models
from django.contrib.postgres import fields
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from datetime import timedelta



class HydroTask(models.Model):
    id = models.BigAutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=250)
    deadline = models.DateField(db_column='deadline')
    status = models.ForeignKey('Status', on_delete=models.CASCADE)
    description = models.TextField(db_column='description', max_length=1000)
    project = models.ForeignKey('HydroProject', on_delete=models.CASCADE)
    start_date = models.DateField(db_column='start_date')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = ('Hydro Task')
        db_table = 'hydrotask'
        managed = True
        
'''
    def save(self, force_insert=False, force_update=False):
        new_task = False
        if not self.id:
            new_task = True
        super(HydroTask, self).save(force_insert, force_update)
        end = self.startDateTime + timedelta(minutes=24*60)
        title = "This is test Task"
        if new_task:
            event = Event(start=self.startDateTime, end=end,title=title,
                    description=self.description)
            event.save()
            rel = EventRelation.objects.create_relation(event, self)
            rel.save()
            try:
                cal = Calendar.objects.get(pk=1)
            except Calendar.DoesNotExist:
                cal = Calendar(name="Community Calendar")
                cal.save()
            cal.events.add(event)
        else:
            event = Event.objects.get_for_object(self)[0]
            event.start = self.startDateTime
            event.end = end
            event.title = title
            event.description = self.description
            event.save()   
'''    