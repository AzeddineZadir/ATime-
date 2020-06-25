from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models import Count, Q
from random import choice
from django.utils import timezone

# Create your models here.


class EmployeManManager(models.Manager):
    def get_my_employe_stats(self, team, user_emp):
        return super().get_queryset().filter(Q(team__nom__contains=team), ~Q(user=user_emp)).values('team').annotate(nb_emp_in=Count(
            'user',
            filter=Q(iwssad=True)),
            nb_emp_out=Count(
            'user',
            filter=Q(iwssad=False)),
            nb_emp=Count(
            'user'
        ))

    def get_my_employe(self, team, user_emp):
        return super().get_queryset().filter(Q(team__titre__contains=team), ~Q(user=user_emp))


class User(AbstractUser):
    EMPLOYE = 1
    MANAGER = 2
    BOSS = 3

    ROLE_CHOICES = (
        (EMPLOYE, 'Employé'),
        (MANAGER, 'Manager'),
        (BOSS, 'Responsable'),
    )
    email = models.EmailField(unique=True)
    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES, blank=True, null=True)


class Employe(models.Model):
    MAN = 'H'
    WOMAN = 'F'
    GENDER = (
        (MAN, 'Homme'),
        (WOMAN, 'Femme'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    iwssad = models.BooleanField(default=False)
    finger_id = models.PositiveSmallIntegerField(unique=True, blank=True)
    is_uploaded = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    birthdate = models.DateField(
        auto_now=False, blank=True, null=True, verbose_name="Date naissance")
    birthplace = models.CharField(max_length=120, blank=True)
    address = models.CharField(
        max_length=200, blank=True, verbose_name="Adresse")
    phone1 = models.CharField(max_length=200, blank=True, null=True,
                              verbose_name="Téléphone professionnel")
    phone2 = models.CharField(max_length=200, blank=True, null=True,
                              verbose_name="Téléphone personnel")
    description = models.CharField(
        max_length=300, blank=True, null=True, verbose_name="Description")
    observation = models.CharField(
        max_length=300, blank=True, verbose_name="remarque",null=True)
    picture = models.ImageField(
        upload_to='images/', default='images/nounours.png', verbose_name="Photo de profil")
    team = models.ForeignKey(
        'Team', on_delete=models.SET_NULL, null=True, blank=True, related_name='employes')
    planing = models.ForeignKey(
        'Planing', on_delete=models.SET_NULL, blank=True, null=True, related_name='pemployes')
    gender = models.CharField(
        max_length=1,
        choices=GENDER,
        blank=True, null=True,
        verbose_name="Genre"
    )
    fonction =models.CharField(max_length=200, blank=True, null=True,
                              verbose_name="Fonction",default=".")
    observation = models.CharField(max_length=300, blank=True, null=True,
                              verbose_name="Remarque") 
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

    def set_iwssad(self, is_iwssad):
        self.iwssad = is_iwssad
        self.save()

    # get the working hours of the corresponding day
    def get_today_hours(self):
        # get the day of the week
        today = timezone.now().date()
        dow = timezone.now().weekday()
        try:
            day = Day.objects.get(planing=self.planing, jds=dow)
            return day
        except:
            day = Day(jds=0, he1=timezone.now().time())
            return day
    # get the last shift of the employe

    def get_last_shift(self):
        try:
            shift = Shift.objects.filter(
                employe=self, day=timezone.now().date()).order_by('-number').first()
            print(f'last shift {shift}')
            return shift
        except:
            print('else of get_last_entry')
            return None


class Team(models.Model):
    titre = models.CharField(
        max_length=150, default='team', blank=True, null=True, verbose_name="Nom de l'équipe", unique=True)
    description = models.CharField(
        max_length=400, blank=True, null=True, verbose_name="Déscription de l'équipe")
    manager = models.ForeignKey(
        'Employe', verbose_name="manager de l'équipe", on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_team')

    def __str__(self):
        return str(self.titre)


class Shift(models.Model):
    employe = models.ForeignKey('Employe', on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField(blank=True, null=True)
    day = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True)
    he = models.TimeField(
        auto_now=False, auto_now_add=False, blank=True, null=True)
    hs = models.TimeField(
        auto_now=False, auto_now_add=False, blank=True, null=True)

    def __str__(self):
        return str(f"numero  : {self.number}/employé  : {self.employe}/joure  : {self.day}")

    def set_he(self):
        self.he = timezone.now()
        self.save()

    def set_hs(self):
        self.hs = timezone.now()
        self.save()


class Day(models.Model):

    DAY_OF_WEEK = ((5, 'Samedi'), (6, 'Dimanche'), (0, 'Lundi'),
                   (1, 'Mardi'), (2, 'Mercredi'), (3, 'Jeudi'), (4, 'Vendredi'))
    #titre = models.CharField(max_length=150)

    jds = models.PositiveIntegerField(
        choices=DAY_OF_WEEK, blank=True, null=True)
    he1 = models.TimeField(auto_now=False, auto_now_add=False,
                           blank=True, null=True)
    hs1 = models.TimeField(auto_now=False, auto_now_add=False,
                           blank=True, null=True)
    he2 = models.TimeField(auto_now=False, auto_now_add=False,
                           blank=True, null=True)
    hs2 = models.TimeField(auto_now=False, auto_now_add=False,
                           blank=True, null=True)
    planing = models.ForeignKey(
        'Planing', on_delete=models.SET_NULL, blank=True, null=True, related_name='planing_days')

    def __str__(self):
        return str(self.jds)


class Planing (models.Model):
    titre = models.CharField(
        max_length=150, unique=True, blank=False, null=False)
    description = models.CharField(max_length=400, blank=True, null=True)

    def __str__(self):
        return str(self.titre)


class Affectation(models.Model):
    employe = models.ForeignKey(
        'Employe', on_delete=models.CASCADE, blank=True, null=True, related_name='affected_set')
    team = models.ForeignKey(
        'Team', on_delete=models.SET_NULL, blank=True, null=True,)
    enter_day= models.DateTimeField(
        auto_now=False, auto_now_add=False, blank=True, null=True)    
    exit_day= models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True)
    team_name =models.CharField(max_length=250, blank=False, null=True)

    def __str__(self):
        return str(f"ID {self.id} {self.employe} a etais affecté a {self.team} le {self.enter_day} a quité le {self.exit_day}")
