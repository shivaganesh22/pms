from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Companies(models.Model):
    name=models.CharField(max_length=50)
    place=models.CharField(max_length=50)
    annualpack=models.FloatField()
    highlights=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Placement(models.Model):
    company=models.ForeignKey(Companies,on_delete=models.CASCADE)
    student=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.company.name
class Notification(models.Model):
    msg=models.CharField(max_length=200)