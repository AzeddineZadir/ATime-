from django.db import models


# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=120, blank=True)
    manager = models.OneToOneField('pointage.Employe', on_delete=models.CASCADE)


    def __str__(self):
        return str(self.name)