from django.contrib import admin
import models



class ReviewInline(admin.TabularInline):
	model = models.Review
	extra = 0


class ProfileAdmin(admin.ModelAdmin):
	list_display = ('name','dating_site')	

	inlines = [ReviewInline,]
	
	
class DatingSiteAdmin(admin.ModelAdmin):
	list_display = ('display_name','domain')
	


admin.site.register(models.DatingSite,DatingSiteAdmin)
admin.site.register(models.Profile,ProfileAdmin)