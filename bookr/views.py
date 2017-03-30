from django.shortcuts import render, redirect, render_to_response
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth import forms, logout as django_logout, authenticate, login as django_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Artist, Event, Message, Comment, MyUser, ArtistImages, VenueList, VenueImages
from .forms import brrLogForm, ArtistForm, ImageForm, VenueForm, EventForm, MessageForm
from .admin import UserCreationForm
from django.core.files.uploadedfile import SimpleUploadedFile


def has_profile():
    userinfo = MyUser.objects.get(id=request.user.id)
    if reequest.user.group == "ART":
        checkprofile = Artist.objects.filter(artist=userinfo)
    elif reequest.user.group == "BKR":
        checkprofile = Artist.objects.filter(artist=userinfo)
    if checkprofile:
        return True
    return False

class Main(View):
    def get(self, request):
        if request.user.groups == "ART":
            return redirect('/artistdashboard/')
        elif request.user.groups == "BKR":
            return redirect('/bookerdashboard/')
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
            messages.error(request, "Username or Password is invalid")
            return redirect('/')

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

class ArtistDashboard(LoginRequiredMixin, View):
    def get(self, request):
        artistform = ArtistForm
        imgform = ImageForm
        print imgform
        userinfo = MyUser.objects.get(id = request.user.id)
        try:
            artistInfo = Artist.objects.get(contact_id = userinfo.id)
        except:
        	artistInfo = None
        context = {
        'artistInfo': artistInfo,
        'artistform': artistform,
        'artimgform': imgform,
        'eventForm': EventForm,
        'messageForm': MessageForm
        }
        if artistInfo:
            artImages = ArtistImages.objects.filter(artist = artistInfo, defaultimage=True)
            if artImages:
            	context["artistImage"] = artImages[0]
            artistEvents = Event.objects.filter(artist_id = artistInfo).order_by('event_date')
            context['artistEvents'] = artistEvents
            messages = Message.objects.filter(event_id__artist_id=artistInfo).exclude(author_id=userinfo).exclude(read=True)
            print messages
            context['eventMessages'] = messages
        return render(request, 'bookrraven/artisthome.html', context)

class BookerDashboard(View):
    def get(self, request):
        venueform = VenueForm
        imgform = ImageForm
        userinfo = MyUser.objects.get(id=request.user.id)
        try:
            venueProfile = VenueList.objects.get(contact_id= userinfo)
        except:
            venueProfile = None
        context = {
        'venueProfile': venueProfile,
        'venueform': venueform,
        'venueimgform': imgform,
        'eventForm': EventForm,
        'messageForm': MessageForm,
        }
        print venueProfile
        if venueProfile:
            venueImages = VenueImages.objects.filter(venue = venueProfile, defaultimage=True)
            if venueImages:
                context['venueImage'] = venueImages[0]
            venueEvents = Event.objects.filter(venue_id = venueProfile).order_by('event_date')
            context['venueEvents'] = venueEvents
            messages = Message.objects.filter(event_id__venue_id=venueProfile).exclude(author_id=userinfo).exclude(read=True)
            print messages
            context['eventMessages'] = messages
        return render(request, 'bookrraven/bookerhome.html', context)

class Venues(View):
    def get(self,request):
        venueform = VenueForm
        imgform = ImageForm
        venueList = VenueList.objects.all()
        userinfo= MyUser.objects.get(id = request.user.id)
        try:
            venueProfile = VenueList.objects.get(contact_id= userinfo)
        except:
            venueProfile = None
        try:
        	artistInfo = Artist.objects.get(contact_id = userinfo)
        except:
            artistInfo = None
    	context = {
    		'venueList': venueList,
            'venueform': venueform,
            'artistInfo': artistInfo,
            'venueProfile': venueProfile,
    	}
    	return render(request, 'bookrraven/venueindex.html', context)

    def post(self, request):
        venform = VenueForm(request.POST)
        # imgform = ImageForm(request.FILES)
        userinfo= MyUser.objects.get(id = request.user.id)
        print venform.is_valid(), "is valid?"
        if venform.is_valid():
            new_venue = VenueList(venue_name = venform.cleaned_data['venue_name'], address=venform.cleaned_data['address'], city=venform.cleaned_data['city'], state=venform.cleaned_data['state'], zipcode=venform.cleaned_data['zipcode'], phone=venform.cleaned_data['phone'], site = venform.cleaned_data['site'], contact_id = userinfo)
            print new_venue.contact_id
            new_venue.save()
            if request.FILES['image']:
                newImage = VenueImages(image = request.FILES['image'], venue = new_venue, defaultimage=True)
                newImage.save()
            print new_venue, "New Venue Created"
        return redirect('/bookerdashboard/')

class SingleVenue(View):
    def get(self,request,venue_id):
        userinfo= MyUser.objects.get(id = request.user.id)
        venueInfo = VenueList.objects.get(id=venue_id)
        try:
            venueProfile = VenueList.objects.get(id = venue_id)
        except:
            venueProfile = None
        try:
        	artistInfo = Artist.objects.get(contact_id = userinfo)
        except:
            artistInfo = None
        venImages = VenueImages.objects.filter(venue=venueInfo)
        print venueProfile, "venue Profile is"
    	context= {
            'venueProfile': venueProfile,
    		'venueInfo': venueInfo,
            'venueImages': venImages,
            'artistInfo': artistInfo,
            'eventForm': EventForm,
            'messageForm': MessageForm,
    	}
    	return render(request, 'bookrraven/venue.html', context)

class AddBooker(View):
    def post(self, request):
        venform = VenueForm(request.POST)
        imgform = ImageForm(request.FILES)
        userinfo= MyUser.objects.get(id = request.user.id)
        if venform.is_valid():
            newVenue = Venue(venue_name= request.POST['venue_name'], address = request.POST['address'], city=request.POST['city'], state=request.POST['state'], zipcode=request.POST['zipcode'] )
        return redirect('/bookerdashboard/')
# class to add images to artist and venue profiles
class AddImg(View):
    def post(self, request):
        if request.user.groups == "ART":
            posterInfo = Artist.objects.get(id = request.POST['artist_id'])
            newImage = ArtistImages(image = request.FILES['image'], artist = posterInfo)
            if request.POST['defimage'] == "on":
                print "in defimage check"
                try:
                    curDefImg = ArtistImages.objects.get(artist=posterInfo, defaultimage=True)
                except:
                    curDefImg = None
                print curDefImg, "this is the current def image"
                if curDefImg:
                    curDefImg.defaultimage = False
                    curDefImg.save()
                    newImage.defaultimage = True
            url = '/artist/'+request.POST['artist_id']
        elif request.user.groups == "BKR":
            posterInfo = VenueList.objects.get(id = int(request.POST['venue_id']))
            newImage = VenueImages(image = request.FILES['image'], venue = posterInfo)
            if "defimage" in request.POST:
                print "inside defimage if"
                try:
                    curDefImg = VenueImages.objects.get(venue=posterInfo, defaultimage=True)
                except:
                    curDefImg = None
                print curDefImg
                if curDefImg:
                    curDefImg.defaultimage = False
                    curDefImg.save()
                    newImage.defaultimage = True
            url = '/venue/'+request.POST['venue_id']
        newImage.save()
        print newImage, "This is the new image after save"
        return redirect(url)

class SingleArtist(View):
    def get(self, request, artist_id):
        userinfo = MyUser.objects.get(id = request.user.id)
        try:
        	artistInfo = Artist.objects.get(id = artist_id)
        except:
            artistInfo = None
        try:
            venueProfile = VenueList.objects.get(contact_id= userinfo)
        except:
            venueProfile = None
        print artistInfo, "In SingleArtist - artistInfo"
        print venueProfile, "In SingleArtist - venueProfile"
        artImages = ArtistImages.objects.filter(artist = artistInfo)
        print artImages, "artist images in get artist"
        context = {
            'venueForm': VenueForm,
            'artistInfo': artistInfo,
            'artistImages': artImages,
            'venueProfile': venueProfile,
            'eventForm': EventForm,
            'messageForm': MessageForm,
        }
        return render(request, 'bookrraven/artistprofile.html', context)

class Artists(View):
    def get(self,request):
        userinfo = MyUser.objects.get(id = request.user.id)
        artistList = Artist.objects.all()
        try:
        	artistInfo = Artist.objects.get(contact_id = userinfo)
        except:
            artistInfo = None
        try:
            venueProfile = VenueList.objects.get(contact_id= userinfo.id)
        except:
            venueProfile = None
        for art in artistList:
        	print art.id

        print venueProfile, "in Artists - venueInfo"
        context = {
        	'artistList': artistList,
        	'artistInfo': artistInfo,
            'venueProfile': venueProfile,
        }
        return render(request, 'bookrraven/artistindex.html', context)

    def post(self, request):
        artform = ArtistForm(request.POST)
        imgform = ImageForm(request.FILES)
        userinfo= MyUser.objects.get(id = request.user.id)
        if artform.is_valid():
            newArtist = Artist(artist_name = request.POST['artist_name'], site = request.POST['site'], sound = request.POST['sound'], contact_id = userinfo)
            newArtist.save()
            if request.FILES['image']:
                newImage = ArtistImages(image = request.FILES['image'], artist = newArtist, defaultimage=True)
                newImage.save()
            print newArtist, "New Artist Created"
        else:
            form = ArtistForm()
        return redirect('/artistdashboard/')

class Events(View):
    def post(self, request):
    	eventForm = EventForm(request.POST)
        messageForm = MessageForm(request.POST)
        requestor = MyUser.objects.get(id = request.user.id)
    	if eventForm.is_valid() and messageForm.is_valid():
            artist = Artist.objects.get(id=request.POST['artist_id'])
            venue = VenueList.objects.get(id=request.POST['venue_id'])
            newEvent = Event(artist_id = artist , venue_id =venue , event_date = eventForm.cleaned_data['event_date'], requestor_id = requestor)
            newEvent.save()
            newMessage = Message(message = messageForm.cleaned_data['message'], event_id = newEvent, author_id = requestor)
            newMessage.save()
            if request.user.groups == 'ART':
                messages.success(request, "A pending event request has been created and your message sent to the Venue")
            elif request.user.groups == 'BKR':
                messages.success(request, "A pending event request has been created and your message sent to the Artist")
        else:
            messages.error(request, "Your event request was unsuccessfull. Please make sure you have selected a future date and filled out the event details.")
        if request.user.groups == 'ART':
        	return redirect('/artistdashboard/')
        elif request.user.groups == 'BKR':
        	return redirect('/bookerdashboard/')

class Messages(View):
    def get(self, request):
        pass

    def post(self, request):
        pass

class Logout(View):
    def get(self,request):
		django_logout(request)
		return redirect('/')
