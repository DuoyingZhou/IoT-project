from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Cities(models.Model):
    name = models.CharField(max_length=200, primary_key=True) 
    temp = models.CharField(max_length=200, default='None') 
    temp_kf = models.CharField(max_length=200, default='None') 
    temp_max = models.CharField(max_length=200, default='None') 
    temp_min = models.CharField(max_length=200, default='None') 
    
    def __str__(self):
        return self.name+";"+self.temp+";"+self.temp_kf+";"+self.temp_max+";"+self.temp_min
        
