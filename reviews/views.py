from django.shortcuts import render_to_response, redirect
from django.shortcuts import get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.contrib.auth.models import User
from django.conf import settings

import models
import forms

def write_review_profile(request,domain,profile):
	
	return redirect('%s#%s' % (reverse(write_review, kwargs={'domain':domain}), profile) )
	

def write_review(request,domain):
	
	if request.POST:
		review_form = forms.ReviewForm(request.POST)
		if review_form.is_valid():
			
			user = request.user if request.user.is_authenticated() else None
			
			dating_site = get_object_or_404(models.DatingSite, domain=domain)
			
			profile_obj, prof_created = models.Profile.objects.get_or_create(dating_site=dating_site,
				name=review_form.cleaned_data['of_profile'])
			
			review = models.Review.objects.create(
				rating = review_form.cleaned_data['rating'],
				text = review_form.cleaned_data['text'],
				title = review_form.cleaned_data['title'],
				by_critic = models.Critic.objects.get_or_create(user=user,ip=request.META['REMOTE_ADDR'])[0],
				of_profile = profile_obj,
			)
			
			return redirect(reviews_of,domain=domain, \
				profile=review_form.cleaned_data['of_profile'])
			
	else:

		review_form = forms.ReviewForm()
	
	return render_to_response('write_review.html',{
			'review_form':review_form,
			'domain':domain
		},RequestContext(request))


def latest_reviews(request,domain):
	dating_site = get_object_or_404(models.DatingSite,domain=domain)
	reviews = models.Review.objects.filter(of_profile__dating_site=dating_site) \
		.order_by('modified')
	return render_to_response('latest_reviews.html',{
			'reviews':reviews,
			'dating_site':dating_site,
		},RequestContext(request))


def reviews_of(request,domain,profile):
	
	try:
		profile = models.Profile.objects.get(name=profile,dating_site__domain=domain)
	except models.Profile.DoesNotExist:
		return redirect(search, dating_site_term=domain, profile_term=profile)
		
	reviews = models.Review.objects.filter(of_profile=profile)
	
	return render_to_response('reviews_of.html',{
			'profile':profile,
			'reviews':reviews
		},RequestContext(request))
		
def reviews_by(request,username):
	
	reviews = models.Review.objects.filter(by_critic__user__username=username)
	return render_to_response('review_by.html',{'reviews':reviews},RequestContext(request))
	
		
def search(request,dating_site_term,profile_term):
	
	results = models.Profile.objects.filter(
		Q(dating_site__domain__icontains=dating_site_term)
		| Q(dating_site__display_name__icontains=dating_site_term)
	).filter(
		Q(name__icontains=profile_term)
	)
	
	return render_to_response('search.html',{'results':results},RequestContext(request))
	