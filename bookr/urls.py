from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
	url(r'^$', views.Main.as_view(), name='brr-landing'),
	url(r'^login/$', views.Login.as_view(), name='brr-login'),
	url(r'^register/$', views.Register.as_view(), name='brr-register'),
	url(r'^artistdashboard/$', views.ArtistDashboard.as_view(), name='brr-artdashboard'),
	url(r'^bookerdashboard/$', views.BookerDashboard.as_view(), name='brr-bkrdashboard'),
	url(r'^venue/$', views.Venues.as_view(), name='brr-venueindex'),
	url(r'^venue/$', views.Venues.as_view(), name='brr-addvenue'),
	url(r'^venue/(?P<venue_id>\d+)', views.SingleVenue.as_view(), name='brr-venueinfo'),
	url(r'^artist/$', views.Artists.as_view(), name='brr-artistindex'),
	url(r'^artist/$', views.Artists.as_view(), name='brr-addartist'),
	url(r'^artist/(?P<artist_id>\d+)', views.SingleArtist.as_view(), name='brr-artistinfo'),
	url(r'^addimg/$', views.AddImg.as_view(), name='brr-addimage'),
	url(r'^event/$', views.Events.as_view(), name='brr-event'),
	url(r'^event/(?P<event_id>\d+)', views.SingleEvent.as_view(), name='brr-eventinfo'),
	url(r'^message/$', views.Messages.as_view(), name='brr-message'),
	url(r'^logout/', views.Logout.as_view(), name='brr-logout')
	# url(r'^test/$', views.Test.as_view(), name='brr-test')
]
