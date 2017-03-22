from django.shortcuts import render, redirect, render_to_response
from django.views.generic import View
from django.contrib.auth import forms, logout as django_logout, authenticate, login as django_login
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Artist, Venue, Event, Message, Comment, MyUser, ArtistImages
from .forms import brrLogForm, ArtistForm, ArtistImageForm
from .admin import UserCreationForm
from django.core.files.uploadedfile import SimpleUploadedFile


class Main(View):
    def get(self, request):
        logform = brrLogForm
        regform = UserCreationForm
        context = {
            'logform': logform,
            'regform': regform,
        }
        return render(request, 'bookrraven/landing.html', context)

class Login(View):
    regform = UserCreationForm
    def post(self, request):
        logform = brrLogForm(request.POST)
        if logform.is_valid():
	        username = request.POST['username']
	        password = request.POST['password']
	        user = authenticate(username=username, password=password)
        print user
        context = {
            'logform': logform,
            'regform': self.regform,
        }

        if user is not None:
        	if user.is_active:
				django_login(request, user)
				if request.user.groups == 'ART':
					return redirect('/artistdashboard/')
				elif request.user.groups == 'BKR':
					return redirect('/bookerdashboard/')
        else:
            print "in else"
            # form = AuthenticationForm()
            return render(request,'bookrraven/landing.html', context)

class Register(View):
    logform = brrLogForm
    def post(self, request):
        # for errors
        regform = UserCreationForm(request.POST)
        context = {
            'logform': self.logform,
            'regform': regform,
        }
        if regform.is_valid():
            regform.save()
            newUser = MyUser.objects.get(username=regform.cleaned_data['username'])
            print newUser, "this is the new user"
            # log 'em in
            user = authenticate(username=regform.cleaned_data['username'], password=regform.cleaned_data['password1'],)
            django_login(request, user)
            # send them to a dashboard(it'll sort 'em out)
            if request.user.groups == 'ART':
            	return redirect('/artistdashboard/')
            elif request.user.groups == 'BKR':
            	return redirect('/bookerdashboard/')
        else:
            return render(request, 'bookrraven/landing.html', context)

class ArtistDashboard(View):
    def get(self, request):
        artistform = ArtistForm
        artimgform = ArtistImageForm
        userinfo = MyUser.objects.get(id = request.user.id)
        try:
            artistInfo = Artist.objects.get(contact_id = userinfo.id)
        except:
        	artistInfo = None
        if artistInfo is not None:
            artImages = ArtistImages.objects.filter(artist = artistInfo)
            print artImages
            try:
                artImages = ArtistImages.objects.filter(artist = artistInfo)
                print artImages
            except:
                artImages = []
                print "in except"
            context = {
                'artistInfo': artistInfo,
                'artistImage': artImages[0],
                'artistform': artistform,
                'artimgform': artimgform,
            }
        else:
        	artistInfo = None
        	context = {
        		'artistInfo': artistInfo,
        		'artistform': artistform,
                'artimgform': artimgform,
        	}
        return render(request, 'bookrraven/artisthome.html', context)


class BookerDashboard(View):
	def get(self, request):
		bookerinfo = Venue.objects.filter(booker_id=request.user.id)
		context = {
			'booker_info': bookerinfo,
		}
		return render(request, 'bookrraven/bookerhome.html', context)

class VenueIndex(View):
	def get(self,request):
		venueList = Venue.objects.all()
		context = {
			'venueList': venueList,
		}
		return render(request, 'bookrraven/venueindex.html', context)


class Venues(View):

	def get(self,request,venue_id):
		get_venue = Venue.objects.get(id = venue_id)

		context= {
			'get_venue': get_venue
		}

		return render(request, 'bookrraven/venueindex.html', context)

	def get(self,request):
		venueInfo = Venue.objects.all()
		print(venueInfo)
		context = {
			'venueInfo': venueInfo,

		}
		return render(request, 'bookrraven/venue.html', context)


	def getEventList(self, request):
		# get event list info
		pass

class AddArtist(View):
    def post(self, request):
        artform = ArtistForm(request.POST)
        imgform = ArtistImageForm(request.FILES)
        userinfo= MyUser.objects.get(id = request.user.id)
        if artform.is_valid():
            newArtist = Artist(artist_name = request.POST['artist_name'], site = request.POST['site'], sound = request.POST['sound'], contact_id = userinfo)
            newArtist.save()
            newImage = ArtistImages(image = request.FILES['image'], artist = newArtist)
            newImage.save()
            print newArtist, "New Artist Created"
        else:
            form = ArtistForm()
        return redirect('/artistdashboard/')

class AddArtImg(View):
    def post(self, request):
        print request
        artistInfo = Artist.objects.get(id = request.POST['artist_id'])
        print artistInfo, "In Add Image"
        newImage = ArtistImages(image = request.FILES['image'], artist = artistInfo)
        newImage.save()
        return redirect('/artist/'+request.POST['artist_id'])

class SingleArtist(View):
    def get(self, request, artist_id):
        artistInfo = Artist.objects.get(id = artist_id)
        artImages = ArtistImages.objects.filter(artist = artistInfo)
        print artImages, "artist images in get artist"
        venueInfo = Venue.objects.all()
        context = {
            'artistInfo': artistInfo,
            'artistImages': artImages,
            'venueInfo': venueInfo,
        }
        return render(request, 'bookrraven/artistprofile.html', context)



class ArtistIndex(View):
    def get(self,request):
        userinfo = MyUser.objects.get(id = request.user.id)
        artistList = Artist.objects.all()
        try:
        	artistInfo = Artist.objects.get(contact_id = userinfo)
        except:
            artistInfo = None
        for art in artistList:
        	print art.id
        context = {
        	'artistList': artistList,
        	'artistInfo': artistInfo
        }
        return render(request, 'bookrraven/artistindex.html', context)

class AddEventInfo(View):
	def post(self, request):
		form = Event(request.POST)
		if form.is_valid():
			art_id = form.cleaned_data['artist_id']
			stat = form.cleaned_data['status']
			ven_id = form.cleaned_data['venue_id']
			e_date = form.cleaned_data['event_date']
		newEvent = Event(artist_id = art_id, status = stat, venue_id = ven_id, event_date = e_date)
		newEvent.save()
		return render(request, 'bookrraven/')

class ActiveEvent(View):
	pass

class Logout(View):
    def get(self,request):
		django_logout(request)
		return redirect('/')
