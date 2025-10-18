from django.db.models.signals import post_save,pre_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from allauth.account.models import EmailAddress
from allauth.account.signals import user_logged_in,user_signed_up
from django.conf import settings
from .models import UserProfile

User = get_user_model()

@receiver(post_save,sender=User)
def create_user_profie(sender,instance,created,**kwargs):
    user = instance
    if created:
        UserProfile.objects.create(user=user)

    else:
        try:
            email_address = EmailAddress.objects.get_primary(user)
            if email_address.email != user.email:
                email_address.email = user.email
                email_address.verified = False
                email_address.save()
        except EmailAddress.DoesNotExist:
            EmailAddress.objects.create(
                user = user,
                email = user.email,
                primary = True,
                verified = False
            )

@receiver(pre_save, sender=User)
def user_presave(sender,instance,**kwargs):
    if instance.email:
        instance.email = instance.email.lower()
    


