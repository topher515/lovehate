from django import forms

from django.forms.widgets import Widget, Select
from django.utils.safestring import mark_safe

import models

class StarSelect(Select):
	
	class Media:
		css = {
			'all':('css/jquery.ui.stars.css',)
		}
		js = ('js/jquery.ui.stars.min.js','js/okreview.starwidget.js')
	
	def render(self,*args,**kwargs):
		
		return mark_safe("""<div class="star-wrapper">%s</div>""" % \
			super(StarSelect,self).render(*args,**kwargs))
		
		
		

class ReviewForm(forms.ModelForm):
	
	of_profile = forms.CharField(max_length=128)
	#domain = forms.CharField(max_length=256,widget=forms.HiddenInput)
	
	class Meta:
		model = models.Review
		
		fields = ('title','text','rating',)
		
		widgets = {
			'rating': StarSelect(choices=((1,'Shoot me!'),(2,'Awful'),(3,'Meh'),(4,'Me Likey'),(5,'Amazing')))
		}
		