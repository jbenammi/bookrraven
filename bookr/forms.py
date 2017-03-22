from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django import forms
from django.forms import ModelForm, widgets
from .models import MyUser, Event, Comment, Message, Venue, Artist, ArtistImages


class brrLogForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.widgets.TextInput)
    password = forms.CharField(label='Password', widget=forms.widgets.PasswordInput)
    class Meta:
        fields = ['username', 'password']

class NewEventForm(forms.ModelForm):
    artist_id = forms.CharField(widget=forms.widgets.HiddenInput)
    status = forms.CharField(widget=forms.widgets.HiddenInput)
    venue_id = forms.CharField(label='Venue', widget=forms.widgets.Select)
    event_date = forms.CharField(label='Event Date',widget=forms.widgets.DateInput)


class ArtistForm(forms.ModelForm):
    artist_name = forms.CharField(label='Artist Name', widget=forms.widgets.TextInput)
    site = forms.URLField(label='Website', widget=forms.widgets.TextInput, required=False)
    sound = forms.URLField(label='Sample Sound', widget=forms.widgets.TextInput, required=False)
    class Meta:
        model = Artist
        fields = ['artist_name', 'site', 'sound']

class ArtistImageForm(forms.ModelForm):
    image = forms.ImageField(label='Artist Photo', required=False)

    class Meta:
        model = ArtistImages
        fields = ['image']
