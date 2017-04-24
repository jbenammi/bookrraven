from django.shortcuts import render, redirect, render_to_response
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth import forms, logout as django_logout, authenticate, login as django_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from .models import Artist, Event, Message, Comment, MyUser, ArtistImages, VenueList, VenueImages
from .forms import brrLogForm, ArtistForm, ImageForm, VenueForm, EventForm, MessageForm
from .admin import UserCreationForm
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime


def getArtist(field, id):
    if field == 'id':
        try:
            artistInfo = Artist.objects.get(id = id)
        except ObjectDoesNotExist:
            artistInfo = None
    elif field == 'contact_id':
        try:
            artistInfo = Artist.objects.get(contact_id = id)
        except ObjectDoesNotExist:
            artistInfo = None
    return artistInfo

def getVenue(field, id):
    if field == 'id':
        try:
            venueInfo = VenueList.objects.get(id = id)
        except ObjectDoesNotExist:
            venueInfo = None
    elif field == 'contact_id':
        try:
            venueInfo = VenueList.objects.get(contact_id = id)
        except ObjectDoesNotExist:
            venueInfo = None
    return venueInfo

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
        userinfo = MyUser.objects.get(id = request.user.id)
        artistInfo = getArtist("contact_id", userinfo)
        context = {
        'artistInfo': artistInfo,
        'artistForm': ArtistForm,
        'artimgform': ImageForm,
        'eventForm': EventForm,
        'messageForm': MessageForm,
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
        userinfo = MyUser.objects.get(id=request.user.id)
        venueProfile = getVenue("contact_id", userinfo)
        context = {
        'venueProfile': venueProfile,
        'venueform': VenueForm,
        'venueimgform': ImageForm,
        'eventForm': EventForm,
        'messageForm': MessageForm,
        }
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
        images = VenueImages.objects.filter(defaultimage=True)
        userinfo= MyUser.objects.get(id = request.user.id)
        venueProfile = getVenue("contact_id", userinfo)
        artistInfo = getArtist("contact_id", userinfo)
        venues = []
        for venue in venueList:
            for image in images:
                if venue.id == image.venue.id:
                    venues.append({
                        "venue": venue,
                        "defaultimage": image,
                    })
    	context = {
    		'venueList': venues,
            'venueform': venueform,
            'artistInfo': artistInfo,
            'venueProfile': venueProfile,
    	}
    	return render(request, 'bookrraven/venueindex.html', context)

    def post(self, request):
        venform = VenueForm(request.POST)
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
        venueProfile = getVenue('id', venue_id)
        artistInfo = getArtist('contact_id', userinfo)
        venImages = VenueImages.objects.filter(venue=venueProfile)
        print venueProfile, "venue Profile is"
    	context= {
            'venueProfile': venueProfile,
            'venueImages': venImages,
            'artistInfo': artistInfo,
            'eventForm': EventForm,
            'messageForm': MessageForm,
            'venueForm': VenueForm,
            'artistForm': ArtistForm,
            'today': datetime.today()
    	}
        print context['today'], "This is todays date"
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
            if 'defimage' in request.POST:
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
        artistInfo = getArtist('id', artist_id)
        venueProfile = getVenue('contact_id', userinfo)
        artImages = ArtistImages.objects.filter(artist = artistInfo)
        context = {
            'venueForm': VenueForm,
            'artistInfo': artistInfo,
            'artistImages': artImages,
            'venueProfile': venueProfile,
            'eventForm': EventForm,
            'messageForm': MessageForm,
            'artistForm': ArtistForm,
            'today': datetime.today()
        }
        print context['today'], "This is today's Date"
        return render(request, 'bookrraven/artistprofile.html', context)

class Artists(View):
    def get(self,request):
        userinfo = MyUser.objects.get(id = request.user.id)
        artistList = Artist.objects.all()
        images = ArtistImages.objects.filter(defaultimage=True)
        artistInfo = getArtist('contact_id', userinfo)
        venueProfile = getVenue('contact_id', userinfo)
        artists = []
        for artist in artistList:
            for image in images:
                if artist.id == image.artist.id:
                    artists.append({
                        "artist": artist,
                        "defaultimage": image,
                    })
        print artists
        context = {
        	'artistList': artists,
        	'artistInfo': artistInfo,
            'venueProfile': venueProfile,
        }
        return render(request, 'bookrraven/artistindex.html', context)

    def post(self, request):
        artform = ArtistForm(request.POST)
        imgform = ImageForm(request.FILES)
        userinfo= MyUser.objects.get(id = request.user.id)
        if artform.is_valid():
            newArtist = Artist(artist_name = request.POST['artist_name'], bio = request.POST['bio'], site = request.POST['site'], sound = request.POST['sound'], contact_id = userinfo)
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
        today = datetime.now().date()
    	if eventForm.is_valid() and messageForm.is_valid() and eventForm.cleaned_data['event_date'] >= today:
            artist = Artist.objects.get(id=request.POST['artist_id'])
            venue = VenueList.objects.get(id=request.POST['venue_id'])
            newEvent = Event(artist_id = artist , venue_id =venue , event_date = eventForm.cleaned_data['event_date'], requestor_id = requestor)
            newEvent.save()
            newMessage = Message(message = messageForm.cleaned_data['message'], event_id = newEvent, author_id = requestor)
            newMessage.save()
            if request.user.groups == 'ART':
                messages.success(request, "A pending event request has been created and your message sent to the Venue")
                email = venue.contact_id.email
            elif request.user.groups == 'BKR':
                messages.success(request, "A pending event request has been created and your message sent to the Artist")
                email = artist.contact_id.email

            send_mail(
            'BookeRRaven New Event Request',
            '<h1>New Event Details</h1>\nArtist: %s\nVenue: %s\nDate: %s\nMessage: %s' % (artist.artist_name, venue.venue_name, newEvent.event_date, newMessage.message),
            'bookrraven@gmail.com',
            [email],
            fail_silently=False,
            html_message = unicode('''<body style="background-color: rgba(100, 100, 100, 0.5);">
              <div style="background-color: #C20A00;">
                <img style="width: 25%%;" src="https://s3-us-west-2.amazonaws.com/bookrraven-images/BookRRaven_light.png" alt="BookRRaven Logo">
              </div>
              <div style="margin: 2%%;">
              <h1 style="color: #9A6200; font-family: sans-serif; border-left: 5px double #9A0800; border-bottom: 5px double #9A0800; padding: 5px;">BookRRaven New Event Request</h1>
              <p style="font-family: sans-serif; color: #FFFFFF;">A new event has been requested. Please log into <a style="text-decoration: none;" href="http://bookrraven.com" target="_blank">BookRRaven.com</a> to respond to the request.</p>
              <table style="font-family: sans-serif;">
                <tbody>
                  <tr>
                    <td style="color: #540165; font-weight:bold;">Venue:</td>
                    <td style="color: #FFFFFF;">%s</td>
                  </tr>
                  <tr>
                    <td style="color: #540165; font-weight:bold;">Artist:</td>
                    <td style="color: #FFFFFF;">%s</td>
                  </tr>
                  <tr>
                    <td style="color: #540165; font-weight:bold;">Date:</td>
                    <td style="color: #FFFFFF;">%s</td>
                  </tr>
                  <tr>
                    <td style="color: #540165; font-weight:bold;">Message:</td>
                    <td style="color: #FFFFFF;">%s</td>
                  </tr>
                </tbody>
              </table>
              <p style="font-family: sans-serif; font-style: italic; color: #FFFFFF;">do not respond to this email</p>
              </div>
              </body>''') % (venue.venue_name, artist.artist_name, newEvent.event_date, newMessage.message),
            )
        else:
            messages.error(request, "Your event request was unsuccessfull. Please make sure you have selected a future date and filled out the event details.")
        if request.user.groups == 'ART':
        	return redirect('/artistdashboard/')
        elif request.user.groups == 'BKR':
        	return redirect('/bookerdashboard/')

class SingleEvent(View):
    def get(self, request, event_id):
        userinfo = MyUser.objects.get(id = request.user.id)
        artistInfo = getArtist('contact_id', userinfo)
        venueProfile = getVenue('contact_id', userinfo)
        Message.objects.filter(event_id__id=event_id).exclude(author_id=userinfo).update(read=True)
        messageList = Message.objects.filter(event_id__id=event_id).order_by('-created_at')
        if request.user.groups == "ART":
            try:
                event = Event.objects.get(id=event_id, artist_id__contact_id=userinfo)
            except ObjectDoesNotExist:
                messages.error(request, "Error accessing event.")
                return redirect('/artistdashboard/')
        elif request.user.groups == "BKR":
            try:
                event = Event.objects.get(id=event_id, venue_id__contact_id=userinfo)
            except ObjectDoesNotExist:
                messages.error(request, "Error accessing event.")
                return redirect('/bookerdashboard/')
        context = {
            "eventMessages": messageList,
            "eventInfo": event,
            "messageForm": MessageForm,
            "artistInfo": artistInfo,
            "venueProfile": venueProfile,
            "today": datetime.today(),
        }
        return render(request, 'bookrraven/event.html', context)

    def post(self, request, event_id):
        userinfo = MyUser.objects.get(id = request.user.id)
        if request.user.groups == "ART":
            try:
                currentEvent = Event.objects.get(id=event_id, artist_id__contact_id=userinfo)
                currentEvent.status = request.POST['status']
                currentEvent.event_date = request.POST['event_date']
                currentEvent.save()
                messages.success(request, "Event Updated")
            except ObjectDoesNotExist:
                messages.error(request, "Error accessing event.")
                return redirect('/artistdashboard/')
        elif request.user.groups == "BKR":
            try:
                currentEvent = Event.objects.filter(id=event_id, venue_id__contact_id=userinfo).update(status=request.POST['status'], event_date=request.POST['event_date'])
                print currentEvent, "in BKR"
            except ObjectDoesNotExist:
                messages.error(request, "Error accessing event.")
                return redirect('/bookerdashboard/')
        return redirect('/event/{}'.format(event_id))

class Messages(View):
    def post(self, request):
        messageForm = MessageForm(request.POST)
        userinfo = MyUser.objects.get(id = request.user.id)
        event = Event.objects.get(id = request.POST['event_id'])
        if event.venue_id.contact_id == userinfo:
            email = event.venue_id.contact_id.email
        elif event.artist_id.contact_id == userinfo:
            email = event.artist_id.contact_id.email
        if messageForm.is_valid():
            newMessage = Message(message = messageForm.cleaned_data['message'], event_id = event, author_id = userinfo)
            newMessage.save()
            eventDate = newMessage.event_id.event_date.strftime("%A, %B %d, %Y")
            send_mail(
            'BookeRRaven New Message',
            'New Message\nA new message has been sent to you on the event taking place on %s. Please log into BookRRaven.com to respond.' % (eventDate),
            'bookrraven@gmail.com',
            [email],
            fail_silently=False,
            html_message = '''<body style="background-color: rgba(100, 100, 100, 0.5);">
              <div style="background-color: #C20A00;">
                <img style="width: 25%%;" src="https://s3-us-west-2.amazonaws.com/bookrraven-images/BookRRaven_light.png" alt="BookRRaven Logo">
              </div>
              <div style="margin: 2%%;">
                  <h1 style="color: #9A6200; font-family: sans-serif; border-left: 5px double #9A0800; border-bottom: 5px double #9A0800; padding: 5px;">New Message</h1>
                  <p style="font-family: sans-serif; color: #FFFFFF;">A new message has been sent to you on the event taking place on %s. Please log into <a style="text-decoration: none;" href="http://bookrraven.com" target="_blank">BookRRaven.com</a> to respond.</p>
                  <p style="font-family: sans-serif; font-style: italic; color: #FFFFFF;">do not respond to this email</p>
              </div>
              </body>''' % (eventDate),
            )
        else:
            messages.error(request, "Error while processing message.")
        return redirect('/event/{}'.format(event.id))

class Logout(View):
    def get(self,request):
		django_logout(request)
		return redirect('/')
