from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django import forms
from django.forms import ModelForm, widgets
from .models import MyUser, Event, Comment, Message, Artist, ArtistImages, VenueList


class brrLogForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.widgets.TextInput)
    password = forms.CharField(label='Password', widget=forms.widgets.PasswordInput)
    class Meta:
        fields = ['username', 'password']

class ArtistForm(forms.ModelForm):
    artist_name = forms.CharField(label='Artist Name', required=True, widget=forms.widgets.TextInput)
    bio = forms.CharField(label="Biography", required=True, widget=forms.widgets.Textarea(attrs={'row': '8', 'col': '80'}))
    site = forms.URLField(label='Website', widget=forms.widgets.TextInput, required=False)
    sound = forms.URLField(label='Sample Sound', widget=forms.widgets.TextInput, required=False)
    class Meta:
        model = Artist
        fields = ['artist_name', 'bio', 'site', 'sound']

class VenueForm(forms.ModelForm):
    STATE_CHOICES = (
        ('AL', 'Alabama'),
        ('AK', 'Alaska'),
        ('AZ', 'Arizona'),
        ('AR', 'Arkansas'),
        ('CA', 'California'),
        ('CO', 'Colorado'),
        ('CT', 'Connecticut'),
        ('DE', 'Delaware'),
        ('FL', 'Florida'),
        ('GA', 'Georgia'),
        ('HI', 'Hawaii'),
        ('ID', 'Idaho'),
        ('IL', 'Illinois'),
        ('IN', 'Indiana'),
        ('IA', 'Iowa'),
        ('KS', 'Kansas'),
        ('KY', 'Kentucky'),
        ('LA', 'Louisiana'),
        ('ME', 'Maine'),
        ('MD', 'Maryland'),
        ('MA', 'Massachusetts'),
        ('MI', 'Michigan'),
        ('MN', 'Minnesota'),
        ('MS', 'Mississippi'),
        ('MO', 'Missouri'),
        ('MT', 'Montana'),
        ('NE', 'Nebraska'),
        ('NV', 'Nevada'),
        ('NH', 'New Hampshire'),
        ('NJ', 'New Jersey'),
        ('NM', 'New Mexico'),
        ('NY', 'New York'),
        ('NC', 'North Carolina'),
        ('ND', 'North Dakota'),
        ('OH', 'Ohio'),
        ('OK', 'Oklahoma'),
        ('OR', 'Oregon'),
        ('PA', 'Pennsylvania'),
        ('RI', 'Rhode Island'),
        ('SC', 'South Carolina'),
        ('SD', 'South Dakota'),
        ('TN', 'Tennessee'),
        ('TX', 'Texas'),
        ('UT', 'Utah'),
        ('VT', 'Vermont'),
        ('VA', 'Virginia'),
        ('WA', 'Washington'),
        ('WV', 'West Virginia'),
        ('WI', 'Wisconsin'),
        ('WY', 'Wyoming')
        )
    venue_name = forms.CharField(label='Venue Name', widget=forms.widgets.TextInput)
    address = forms.CharField(label='Address', widget=forms.widgets.TextInput)
    city = forms.CharField(label='City', widget=forms.widgets.TextInput)
    state = forms.ChoiceField(label='State', widget=forms.widgets.Select, choices=STATE_CHOICES)
    zipcode = forms.CharField(label='Zip Code', widget=forms.widgets.TextInput)
    phone = forms.CharField(label='Phone', widget=forms.widgets.TextInput)
    site = forms.URLField(label='Website', widget=forms.widgets.TextInput, required=False)
    class Meta:
        model = VenueList
        fields = ['venue_name', 'address', 'city', 'state', 'zipcode', 'phone', 'site',]

class ImageForm(forms.Form):
    image = forms.ImageField(label='Image', required=False)
    default = forms.BooleanField(label="Default Image", widget=forms.widgets.CheckboxInput, required=False)
    class Meta:
        fields = ['image', 'default']

class EventForm(forms.ModelForm):
    event_date = forms.DateField(label="Event Date", required=True, widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Event
        fields = ['event_date',]

class MessageForm(forms.ModelForm):
    message = forms.CharField(label="Event Message", required=True, widget=forms.widgets.Textarea(attrs={'row': '8', 'col': '80'}))

    class Meta:
        model = Message
        fields = ('message',)
