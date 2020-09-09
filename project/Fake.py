import os, django
import random
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from faker import Faker
from apps.pointage.models import User, Team, Employe, Planing, Day, Shift
from django.utils import timezone
from datetime import datetime, timedelta


faker = Faker()

# name = fake_date.name(); print(name)

# address =fake_date.address(); print(address)

# email = fake_date.email(); print(email)



def add_user():
    p  = faker.simple_profile()
    last_name = faker.last_name()
    first_name = faker.first_name()
    email =faker.email()
    role = 1
    username = p['username']
    user = User.objects.get_or_create(last_name=last_name, first_name=first_name, role=role, email=email, username=username)[0]
    password = User.objects.make_random_password()
    print(user)
    user.save()
    user.set_password(password)
    user.save()
    return user

def add_days(p):
    for entry in range(7):
        h1 = faker.time()
        h2 = faker.time()
        h3 = faker.time()
        h4 = faker.time()
        jds = entry
        a = random.randint(1, 4)
        l = [h1, h2 ,h3, h4]
        list = sorted(l)
        if(a == 1 or a == 2):
            day = Day.objects.get_or_create(planing=p, he1=list[0], he2=list[2], hs1=list[1], hs2=list[3], jds=jds)
        elif(a == 3):
            day = Day.objects.get_or_create(planing=p, he1=list[0], hs1=list[1], jds=jds)
        elif(a == 4):
            day = Day.objects.get_or_create(planing=p, jds=jds)


def add_teams(N=3):
    for entry in range(N):
        titre = faker.company()
        print(titre)
        description = faker.text(max_nb_chars=160)
        managers = User.objects.filter(role=2)
        team = Team.objects.get_or_create(titre=titre, description=description, manager=random.choice(managers).employe)

def add_planning(N=3):
    for entry in range(N):
        titre = faker.company_suffix()
        description = faker.text(max_nb_chars=160)
        p = Planing.objects.get_or_create(titre=titre, description=description)
        add_days(p[0])

def add_shifts(employe):
    for entry in range(20):
        date = datetime(2020,8,10)+timedelta(days=entry)
        a = random.randint(1, 4)
        h1 = faker.time()
        h2 = faker.time()
        h3 = faker.time()
        h4 = faker.time()
        h5 = faker.time()
        h6 = faker.time()
        h7 = faker.time()
        h8 = faker.time()
        l = [h1, h2, h3, h4, h5, h6, h7, h8]
        list = sorted(l)
        for e in range(a):              
            shift = Shift.objects.get_or_create(employe=employe, day=date, number=e, he=list[e+e], hs=list[e+e+1])


def add_employes(N=3):
    for entry in range(N):
        address = faker.address()
        birthdate = faker.date_between(start_date='-60y', end_date='-25y')
        description = faker.text(max_nb_chars=140)
        birthplace = faker.city()
        fonction = faker.job()  
        list=['H', 'F']
        i=random.randint(0,1)
        gender = list[i]
        phone1 = faker.phone_number()
        phone2 = faker.phone_number()
        plannings = Planing.objects.all()
        teams = Team.objects.all()
        user = add_user()
        e = Employe.objects.get_or_create(user=user, address=address, birthdate=birthdate, description=description, 
        birthplace=birthplace, fonction=fonction, gender=gender, phone1=phone1, phone2=phone2, planing=random.choice(plannings), team=random.choice(teams))[0]
        e.save()
        add_shifts(e)


if __name__ == '__main__':
    print("Seeding the database")
    #add_planning(3)
    #add_teams(8)
    add_employes(24)
    print("Terminer")
