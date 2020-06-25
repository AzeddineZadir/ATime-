from django.db.models.signals import post_save ,pre_save
from django.dispatch import receiver
from .models import User, Employe
from django.core.exceptions import ObjectDoesNotExist


# @receiver(post_save, sender=User)
# def user_is_saved(sender, instance, created, **kwargs):
#     print(instance)
#     # If user role is not define
#     if instance.role != None:
#         # If a new record was created
#         try:
#             if created:
#                 Employe.objects.create(user=instance)
#             else:
#                 instance.employe.save()
#         except ObjectDoesNotExist:
#             Employe.objects.create(user=instance)

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, Employe, Affectation
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


@receiver(post_save, sender=User)
def user_is_saved(sender, instance, created, **kwargs):
    print(instance)
    # If user role is not define
    #if instance.role != None:
        # If a new record was created
        #try:
        #    if created:
        #        Employe.objects.create(user=instance)
        #    else:
        #        instance.employe.save()
        #except ObjectDoesNotExist:
        #    Employe.objects.create(user=instance)

@receiver(pre_save, sender=Employe)
def employe_is_saved(sender, instance, **kwargs):
    try:
        emp_before_save = Employe.objects.get(pk=instance.pk)
        if emp_before_save.team != None:
            if instance.team == None:
                
                try:
                    affectation = Affectation.objects.filter(employe=instance.pk).latest('enter_day')
                    print("delete de l'équipe")
                    affectation.exit_day = timezone.now()
                    affectation.save()
                except:
                    print("aucune affectation")
            elif emp_before_save.team != instance.team:
                try:
                    affectation = Affectation.objects.filter(employe=instance.pk).latest('enter_day')
                    affectation.exit_day = timezone.now()
                    affectation.save()
                    print("changement d'équipe") 
                except:
                    print("aucune affectation")
                Affectation(employe=instance,team=instance.team,enter_day=timezone.now()).save()
            else:
                print("aucun changement")
        else:
            if instance.team != None:
                print("affectation d'une équipe")
                Affectation(employe=instance,team=instance.team,enter_day=timezone.now()).save()
            else:
                print("aucun changement")
    except:
        print("Création")

@receiver(post_save, sender=Employe)
def employe_is_created(sender, instance, created,**kwargs):
    if created:
        if instance.team != None:
            Affectation(employe=instance,team=instance.team,enter_day=timezone.now()).save()


