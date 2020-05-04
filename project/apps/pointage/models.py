from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models import Count, Q



# Create your models here.

class EmployeManManager(models.Manager):
    def get_my_employe_stats(self, team_id, user_emp):
        return super().get_queryset().filter(Q(team_id__name__contains = team_id), ~Q(user = user_emp)).values('team_id').annotate(nb_emp_in=Count(
        'user', 
        filter=Q(iwssad=True)),
        nb_emp_out=Count(
        'user', 
        filter=Q(iwssad=False)
        ))


class User(AbstractUser):
    EMPLOYE = 1
    MANAGER = 2
    BOSS = 3

    ROLE_CHOICES = (
        (EMPLOYE, 'Employé'),
        (MANAGER, 'Manager'),
        (BOSS, 'Chef de projet'),
    )
    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES, blank=True, null=True)


class Employe(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    iwssad = models.BooleanField(default=False)
    finger_id = models.PositiveSmallIntegerField()
    is_uploaded = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    birthdate = models.DateField(auto_now=False, blank=True, null=True)
    birthplace = models.CharField(max_length=120, blank=True)
    address = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    observation = models.CharField(max_length=300, blank=True)
    team_id = models.ForeignKey('dash.Team', on_delete=models.CASCADE, null=True, blank=True)

    objects = models.Manager()
    manager= EmployeManManager()

    def __str__(self):
        return self.user.username



class Shift(models.Model):
    employe = models.ForeignKey('Employe', on_delete=models.CASCADE)
    date_heure_e = models.DateTimeField(auto_now_add=True)
    date_heure_s = models.DateTimeField(auto_now=False, blank=True, null=True)

    def __str__(self):
        return str(self.employe)
