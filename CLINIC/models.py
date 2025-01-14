from django.db import models
from django.contrib.auth.models import User
import uuid
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
        
class Patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, max_length=40)
    name= models.CharField(max_length=20)
    date_of_birth = models.DateField()
    age = models.PositiveIntegerField()
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_CHOICES = [(GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female')]
    gender = models.IntegerField(choices=GENDER_CHOICES)
    country = models.CharField(max_length=100,)
    phone_number = models.CharField(max_length=11)
    address = models.TextField()

    def __str__(self):
        return self.name

class Staffs(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    nurses = 2
    doctors = 3
    category = [(nurses,'Nurse'),(doctors,'Doctor')]
    profession = models.IntegerField(choices=category,null=True)

    class Meta:
        verbose_name_plural = "Staffs"
    
    def __str__(self):
        return self.user.username

class Profile(models.Model):
    profile=models.OneToOneField(Patient,on_delete=models.CASCADE)

    def __str__(self):
        return self.profile.name
    

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(post_save, sender=Patient)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(profile=instance)
  
@receiver(post_save, sender=Patient)
def save_profile(sender, instance, **kwargs):
        instance.profile.save()

@receiver(post_save, sender=User)
def create_staff(sender, instance, created, **kwargs):
    if created:
        Staffs.objects.create(user=instance)
  
# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#         instance.user.save()

 