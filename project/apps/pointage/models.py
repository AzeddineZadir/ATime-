from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models import Count, Q
from random import choice


# Create your models here.


class EmployeManManager(models.Manager):
    def get_my_employe_stats(self, team_id, user_emp):
        return super().get_queryset().filter(Q(team_id__name__contains=team_id), ~Q(user=user_emp)).values('team_id').annotate(nb_emp_in=Count(
            'user',
            filter=Q(iwssad=True)),
            nb_emp_out=Count(
            'user',
            filter=Q(iwssad=False)),
            nb_emp=Count(
            'user'
        ))

    def get_my_employe(self, team_id, user_emp):
        return super().get_queryset().filter(Q(team_id__name__contains=team_id), ~Q(user=user_emp))


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
    finger_id = models.PositiveSmallIntegerField(unique=True, blank=True)
    is_uploaded = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    birthdate = models.DateField(auto_now=False, blank=True, null=True)
    birthplace = models.CharField(max_length=120, blank=True)
    address = models.CharField(max_length=200, blank=True)
    phone1 = models.CharField(max_length=200, blank=True, null=True,
                              verbose_name="telephone 1")
    phone2 = models.CharField(max_length=200, blank=True, null=True,
                              verbose_name="telephone 2")
    observation = models.CharField(max_length=300, blank=True)
    picture = models.ImageField(
        upload_to='images/', default='images/nounours.png')
    team = models.ForeignKey(
        'Team', on_delete=models.SET_NULL, null=True, blank=True, related_name='employes')
    planing = models.ForeignKey(
        'Planing', on_delete=models.SET_NULL, blank=True, null=True)
    objects = models.Manager()
    manager = EmployeManManager()

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.genrate_finger_id()

        super(Employe, self).save(*args, **kwargs)

    def genrate_finger_id(self):
        # get ids alredy used
        used_id = self.get_used_id()
        # a liste of the interval
        my_list = list(range(2, 128))
        # a liste with thee possible valeus =interval-alredy used elements
        possible_values_list = set(my_list)-set(used_id)
        # print(possible_values_list)
        # a random ellment from this liste
        # print(choice(list(possible_values_list)))
        # set  the value to the finger id attribut
        self.finger_id = choice(list(possible_values_list))

    def get_used_id(self):
        my_id_list = [1, ]
        # get employes
        employes = Employe.objects.all()
        # get used finger id
        for employe in employes:
            my_id_list.append(employe.finger_id)
       # print(my_id_list)
        return my_id_list

    def delete_employe(self):
        self.is_delete = True
        self.save()


class Team(models.Model):
    titre = models.CharField(
        max_length=150, default='team', blank=True, null=True)
    description = models.CharField(max_length=400, blank=True, null=True)
    manager = models.ForeignKey(
        'Employe', verbose_name="manager", on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_team')


class Shift(models.Model):
    employe = models.ForeignKey('Employe', on_delete=models.CASCADE)
    date_heure_e = models.DateTimeField(auto_now_add=True)
    date_heure_s = models.DateTimeField(auto_now=False, blank=True, null=True)

    def __str__(self):
        return str(self.employe)


class Jour(models.Model):
    SAMEDI = 1
    DIMANCHE = 2
    LUNDI = 3
    MARDI = 4
    MERCREDI = 5
    JEUDI = 6
    VENDREDI = 7
    DAY_OF_WEEK = ((SAMEDI, 'Samedi'), (DIMANCHE, 'Dimanche'), (LUNDI, 'Lundi'),
                   (MARDI, 'Mardi'), (MERCREDI, 'Mercredi'), (JEUDI, 'Jeudi'), (VENDREDI, 'Vendredi'))
    jds = models.PositiveSmallIntegerField(
        choices=DAY_OF_WEEK, blank=True, null=True)
    he1 = models.TimeField(auto_now=False, auto_now_add=False)
    hs1 = models.TimeField(auto_now=False, auto_now_add=False)
    he2 = models.TimeField(auto_now=False, auto_now_add=False)
    hs2 = models.TimeField(auto_now=False, auto_now_add=False)


class Planing (models.Model):
    titre = models.CharField(
        max_length=150, unique=True, blank=False, null=False)
    description = models.CharField(max_length=400, blank=True, null=True)
    jour1 = models.ForeignKey(
        'Jour', on_delete=models.SET_NULL, blank=True, null=True, related_name='+')
    jour2 = models.ForeignKey(
        'Jour', on_delete=models.SET_NULL, blank=True, null=True, related_name='+')
    jour3 = models.ForeignKey(
        'Jour', on_delete=models.SET_NULL, blank=True, null=True, related_name='+')
    jour4 = models.ForeignKey(
        'Jour', on_delete=models.SET_NULL, blank=True, null=True, related_name='+')
    jour5 = models.ForeignKey(
        'Jour', on_delete=models.SET_NULL, blank=True, null=True, related_name='+')
    jour6 = models.ForeignKey(
        'Jour', on_delete=models.SET_NULL, blank=True, null=True, related_name='+')
    jour7 = models.ForeignKey(
        'Jour', on_delete=models.SET_NULL, blank=True, null=True, related_name='+')
