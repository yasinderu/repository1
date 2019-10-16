from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

class UserProfileManager(models.Manager):
	pass

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	description = models.TextField(null=True)
	phone_number = models.IntegerField(default=0)
	
	def __str__(self):
		return self.user.username

def createProfile(sender, **kwargs):
	if kwargs['created']:
		user_profile = UserProfile.objects.created(user=kwargs['instance'])

		post_save.connect(createProfile, sender=User)