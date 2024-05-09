from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres import fields
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class TeamMember(models.Model):
    id = models.BigAutoField(db_column='id', primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    title = models.CharField(db_column='title', max_length=250, null=True)
    def __str__(self):
        user = self.user.username
        return user
    class Meta:
        verbose_name = ('Team Member')
        db_table = 'team_member'
        managed = True