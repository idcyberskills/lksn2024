from django.db import models

class Reminder(models.Model):
    title = models.CharField(max_length=100,blank=False)
    execdate = models.DateTimeField(blank=False)
    period = models.BigIntegerField()

# Internal application used only
class DataRahasia(models.Model):
    title = models.CharField(max_length=100,blank=False,unique=True)
    data = models.CharField(max_length=100,blank=False)