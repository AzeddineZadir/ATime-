from django.shortcuts import render
from django.http import HttpResponse
from .models import Employe, Shift, User
from django.db.models import Max
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

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
            id = request.POST['Check_employe']
            # Get object employe
            emp = Employe.objects.get(finger_id=id)
            # Check if employe is inside then change the value of iwssad to False -> Employe is outside and find the last checkpoint and add date_heure_s
            if emp.iwssad:
                emp.iwssad = False
                emp.save()
                shift = Shift.objects.filter(
                    employe=emp).latest('date_heure_e')
                shift.date_heure_s = timezone.now()
                shift.save()
            else:  # Outside / Change the value of iwssad to True -> Employe is inside and create new checkpoint
                emp.iwssad = True
                emp.save()
                Shift(employe=emp).save()

            return HttpResponse(id)

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
                emp.delete()
            except:
                id_finger = 'del-id0'
                # Return finger_id to arduino
                return HttpResponse(str(id_finger))

            return HttpResponse(str(id_finger))

def test(request):
    emp = Employe.objects.filter(user=request.user).get()
    test = Employe.manager.get_my_employe_stats(team_id=emp.team_id, user_emp=request.user)
    print()

    return HttpResponse("nombre d'employés total: "+str(test[0]['nb_emp'])+"nombre d'employés in: "+str(test[0]['nb_emp_in'])+" nombre d'employés out: "+str(test[0]['nb_emp_out']))

