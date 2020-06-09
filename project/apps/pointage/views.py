from django.shortcuts import render
from django.http import HttpResponse
from .models import Employe, Shift, User, Day
from django.db.models import Max
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from datetime import date, time
from django.db.models import Q, Count

# Create your views here.


# @csrf_exempt
# def check(request):
#    if request.method == 'POST':
#         id_e = request.POST['id_e']
#         # Get object employe
#         emp = Employe.objects.get(id=id_e)
#         # Check if employe is inside then change the value of iwssad to False -> Employe is outside and find the last checkpoint and add date_heure_s
#         if emp.iwssad:
#             emp.iwssad = False
#             emp.save()
#             shift = Shift.objects.filter(employe=emp).latest('date_heure_e')
#             shift.date_heure_s = timezone.now()
#             shift.save()
#         else:  # Outside / Change the value of iwssad to True -> Employe is inside and create new checkpoint
#             emp.iwssad = True
#             emp.save()
#             Shift(employe=emp).save()

#     return HttpResponse(id_e)


@csrf_exempt
def getid(request):
    if request.method == 'POST':
        if 'Check_employe' in request.POST:
            #  get employe id
            id = request.POST['Check_employe']
        #  get the employe obj if it exists
            try:
                emp = Employe.objects.get(finger_id=id)
                print(f"lemploye :{emp}")
            except expression as identifier:
                print("vous netes paas un employe de notre entreprise")

        #  get employe planing
            try:
                planing = emp.planing
                print(f"le planing :{planing}")
            except:
                print("pas de planinig poour cette employé")
         #  get todays hours
            today = get_today_planing(planing)
            # print(today)
            # print(today.he1)
            # print(today.hs1)
            # print(today.he2)
            # print(today.hs2)

            if (today.he1 != None):
                #  get the last shift if it exists
                print(timezone.now().date())
                # Get number of shift by employe
                count_shift = Shift.objects.filter(Q(employe=emp),Q(day=timezone.now().date())).count()
                print("Count-------------------------",count_shift)
            
                if emp.iwssad:
                    last_shift = Shift.objects.get(
                        employe=emp, number=count_shift, day=timezone.now().date())
                    last_shift.set_hs()                   
                    emp.set_iwssad(False)
                else:
                    Shift(employe=emp, number=count_shift+1 ,day=timezone.now().date(), he=timezone.now()).save()
                    emp.set_iwssad(True)

            return HttpResponse("ID"+id)

    #     if request.method == 'POST':

    #         if 'Check_employe' in request.POST:
    #             id = request.POST['Check_employe']
    #             # Get object employe
    #             emp = Employe.objects.get(finger_id=id)
    #             # Check if employe is inside then change the value of iwssad to False -> Employe is outside and find the last checkpoint and add date_heure_s
    #             if emp.iwssad:
    #                 emp.check(False)
    #                 shift = Shift.objects.filter(
    #                     employe=emp).latest('date_heure_e')
    #                 shift.set_heure_s()
    #             else:  # Outside / Change the value of iwssad to True -> Employe is inside and create new checkpoint
    #                 emp.check(True)
    #                 Shift(employe=emp).save()

    #             return HttpResponse(id)

        elif 'Get_Fingerid' in request.POST:
            try:
                # Get the first employe if is_uploaded=False
                emp = Employe.objects.filter(is_uploaded=False).first()
                print("jimprime lemploye")
                print(emp)

                id_finger = 'add-id'+str(emp.finger_id)
                print(id_finger)
            except:
                id_finger = 'add-id0'
                print("dans le block exep")
                print("ObjectDoesNotExist")
                # Return finger_id to arduino
                return HttpResponse(str(id_finger))

            return HttpResponse(str(id_finger))

        elif 'confirm_id' in request.POST:
            id = request.POST['confirm_id']

            emp = Employe.objects.filter(finger_id=id).update(is_uploaded=True)
            return HttpResponse(str('add_id'))  # Return confirmation

        elif 'DeleteID' in request.POST:
            try:
                # Get the first employe if is_delete=True
                emp = Employe.objects.filter(is_delete=True).first()
                id_finger = 'del-id'+str(emp.finger_id)
                emp.user.delete()
            except:
                id_finger = 'del-id0'
            # Return finger_id to arduino
            return HttpResponse(str(id_finger))

        return HttpResponse(str(id_finger))


""" def entrée(emp, day, shift):
    #  now  < day.hs1
    #  shift.he1=now
    if (now_time() < day.hs1):
        #  print('timezone.now().time() < day.hs1 ============ TRUE ')
        #  print(timezone.localtime(timezone.now()).time())
        shift.he1 = now_time()
        shift.save()
        emp.check_employe(True)
        emp.save()
    elif (day.hs2 != non):

        if (now_time() > day.hs1)and (timezone.now().time() < day.hs2):
            #print('(timezone.now().time()> day.hs1)and (timezone.now().time()< day.hs2) ============ TRUE ')
            shift.he2 = now_time()
            print(f'he2  {shift.he2}')
            shift.save()
            emp.check_employe(True)
            emp.save() """


""" def sortie(emp, day, shift):
    # if now < day.he2  then shift.hs1 <-now+
    # the exit in the first periode
    if (he2 != None):
        if (now_time() < day.he2)and (shift.he1):
            print('now_time() < day.he2 ============ TRUE ')
            shift.hs1 = now_time()
            print(f'hs1  {shift.hs1}')
            shift.save()
            emp.check_employe(False)
            emp.save()
        elif(shift.he2):
            # exit in the second periode
            print('shift.he2 ============ TRUE ')
            shift.hs2 = now_time()
            print(f'hs2  {shift.hs2}')
            shift.save()
            emp.check_employe(False)
            emp.save()
        elif(shift.he1)and(now_time() > day.hs2):
            # exit in the seconde periode but without a pause
            print('(shift.he1)and( now_time()> day.hs2 ')
            shift.hs2 = now_time()
            print(f'hs2  {shift.hs2}')
            shift.save()
            emp.check_employe(False)
            emp.save() """


def now_time():
    return timezone.localtime(timezone.now()).time()


def get_today_planing(pla):
    # get the day of the week
    today = timezone.now().date()
    dow = timezone.now().weekday()
    day = Day.objects.get(planing=pla, jds=dow)
    return day


# @csrf_exempt
# def getid2(request):
#     if request.method == 'POST':
#         if 'Check_employe' in request.POST:
#             id = request.POST['Check_employe']
#             # Get object employe
#             emp = Employe.objects.get(finger_id=id)
#             # Check if employe is inside then change the value of iwssad to False -> Employe is outside and find the last checkpoint and add date_heure_s
#             if emp.iwssad:
#                 emp.iwssad = False
#                 emp.save()
#                 shift = Shift.objects.filter(
#                     employe=emp).latest('date_heure_e')
#                 shift.date_heure_s = timezone.now()
#                 shift.save()
#             else:  # Outside / Change the value of iwssad to True -> Employe is inside and create new checkpoint
#                 emp.iwssad = True
#                 emp.save()
#                 Shift(employe=emp).save()

#             return HttpResponse(id)
#     elif request.method == 'GET':
#         if 'Get_Fingerid' in request.POST:
#             try:
#                 # Get the first employe if is_uploaded=False
#                 emp = Employe.objects.filter(is_uploaded=False).first()
#                 print("jimprime lemploye")
#                 print(emp)

#                 id_finger = 'add-id'+str(emp.finger_id)
#                 print(id_finger)
#             except:
#                 id_finger = 'add-id0'
#                 print("dans le block exep")
#                 print("ObjectDoesNotExist")
#                 # Return finger_id to arduino
#                 return HttpResponse(str(id_finger))

#             return HttpResponse(str(id_finger))

#         elif 'confirm_id' in request.POST:
#             id = request.POST['confirm_id']

#             emp = Employe.objects.filter(finger_id=id).update(is_uploaded=True)
#             return HttpResponse(str('add_id'))  # Return confirmation

#     elif request.method == 'DELETE':
#         if 'DeleteID' in request.POST:
#             try:
#                 # Get the first employe if is_delete=True
#                 emp = Employe.objects.filter(is_delete=True).first()
#                 id_finger = 'del-id'+str(emp.finger_id)
#                 emp.delete()
#             except:
#                 id_finger = 'del-id0'
#                 # Return finger_id to arduino
#                 return HttpResponse(str(id_finger))

#             return HttpResponse(str(id_finger))


def test(request):
    emp = Employe.objects.filter(user=request.user).get()
    test = Employe.manager.get_my_employe_stats(
        team_id=emp.team_id, user_emp=request.user)
    print()

    return HttpResponse("nombre d'employés total: "+str(test[0]['nb_emp'])+"nombre d'employés in: "+str(test[0]['nb_emp_in'])+" nombre d'employés out: "+str(test[0]['nb_emp_out']))
