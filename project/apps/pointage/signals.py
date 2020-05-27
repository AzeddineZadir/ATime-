from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Employe
from django.core.exceptions import ObjectDoesNotExist


@receiver(post_save, sender=User)
def user_is_saved(sender, instance, created, **kwargs):
    print(instance)
    # If user role is not define
    if instance.role != None:
        # If a new record was created
        try:
            if created:
                Employe.objects.create(user=instance)
            else:
                instance.employe.save()
        except ObjectDoesNotExist:
            Employe.objects.create(user=instance)