from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.

class User(AbstractUser):
    EMPLOYE = 1
    MANAGER = 2
    BOSS = 3
      
    ROLE_CHOICES = (
        (EMPLOYE, 'Employé'),
        (MANAGER, 'Manager'),
        (BOSS, 'Chef de projet'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)


class Employe(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    iwssad = models.BooleanField(default=False)
    finger_id = models.PositiveSmallIntegerField()
    is_uploaded = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    birthdate = models.DateField(default=False)
    birthplace = models.CharField(max_length=120, blank=True)
    address = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=18, blank=True)
    observation = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.user.username

class Shift(models.Model):
    employe = models.ForeignKey('Employe', on_delete=models.CASCADE)
    date_heure_e = models.DateTimeField(auto_now_add=True)
    date_heure_s = models.DateTimeField(auto_now=False, blank=True, null=True)

    def __str__(self):
        return str(self.employe)