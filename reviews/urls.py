from django.conf.urls.defaults import *


urlpatterns = patterns('reviews.views',
	(r'^$','main_page'),
	(r'^which/$', 'write_which'),
	(r'^write/(?P<domain>[-\.\w]+)/$', 'write_review'),
	(r'^write/(?P<domain>[-\.\w]+)/(?P<profile>[ -\.\w]+)/$', 'write_review_profile'),
	(r'^reviews/$','all_latest_reviews'),
	(r'^reviews/(?P<domain>[-\.\w]+)/$','latest_reviews'),
	(r'^reviews/(?P<domain>[-\.\w]+)/(?P<profile>[ -\.\w]+)/$','reviews_of'),
	(r'^search/(?P<dating_site_term>[-\.\w]+)/(?P<profile_term>[ -\.\w]+)/$','search'),
)