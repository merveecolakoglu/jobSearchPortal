from django.db.models.signals import *
from users.models import User, ProfileModel
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        ProfileModel.objects.create(
            user=user,
        )


@receiver(post_save, sender=ProfileModel)
def update_profile(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if created == False:
        user.save()


@receiver(post_delete, sender=ProfileModel)
def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass
