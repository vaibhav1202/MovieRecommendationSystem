from django.db import models

# Create your models here.
class BasedOnId(models.Model):
    user_id = models.IntegerField()
     
class BasedOnTitle(models.Model):
    title = models.CharField(max_length=100)


