from django.db import models
from djangoratings.fields import AnonymousRatingField

from django.contrib.auth.models import User

import string, random

class DatingSite(models.Model):
	slug = models.CharField(max_length=128,unique=True)
	display_name = models.CharField(max_length=256,unique=True)
	domain = models.CharField(max_length=512)
	

class Profile(models.Model):
	dating_site = models.ForeignKey(DatingSite)
	name = models.CharField(max_length=256)
	owned_by = models.ForeignKey(User,null=True)
	
	class Meta(object):
		unique_together = ("dating_site", "name")


class ProfileVerification(models.Model):
	profile = models.ForeignKey(Profile)
	started = models.DateTimeField(auto_now_add=True)
	success = models.DateTimeField(null=True,blank=True)
	failed = models.DateTimeField(null=True,blank=True)
	key = models.CharField(max_length=64)
	
	def __init__(self,*args,**kwargs):
		if not kwargs.get('key'):
			kwargs.update({'key':''.join(random.sample(string.letters,6))})
		super(ProfileVerification,self).__init__(*args,**kwargs)


class Critic(models.Model):
	user = models.OneToOneField(User, blank=True)
	ip = models.IPAddressField()
		
	def __str__(self):
		return self.user.username if self.user else self.ip
		
	def user_or_anon(self):
		return self.user.username if self.user else 'Anonymous'

	
class ReviewPhoto(models.Model):
	photo = models.ImageField(upload_to="review_files")
	caption = models.TextField()

class Review(models.Model):
	rating = models.PositiveSmallIntegerField() # [1 to 5]
	text = models.TextField()
	title = models.CharField(max_length=512)
	
	photos = models.ManyToManyField(ReviewPhoto, null=True)
	
	meta_rating = AnonymousRatingField(range=10)
	by_critic = models.ForeignKey(Critic)
	of_profile = models.ForeignKey(Profile)
	
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	