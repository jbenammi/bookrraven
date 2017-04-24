from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from datetime import datetime


class Base_User_Manager(BaseUserManager):
    def create_user(self, username, first_name, last_name, email, phone, groups="ART", password1=None):
        if not username:
            raise ValueError('Accounts must have a username')
        newUser = self.model(
            username= username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            groups=groups
        )
        newUser.set_password(password1)
        newUser.save(using=self._db)
        return newUser

    def create_superuser(self, username, first_name, last_name, email, phone, password):
        newUser = self.create_user(
            username= username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            password1 = password
        )
        newUser.is_admin = True
        newUser.save(using=self._db)
        return newUser

class MyUser(AbstractBaseUser):
    BOOKER = 'BKR'
    ARTIST = 'ART'
    ACCESS_CHOICES = (
        (BOOKER, 'Booker'),
        (ARTIST, 'Artist')
        )
    username = models.CharField('Username', max_length=150, unique=True)
    email = models.EmailField('Email Address', max_length=255)
    first_name = models.CharField('First Name', max_length=45)
    last_name = models.CharField('Last Name', max_length=45)
    groups = models.CharField('Access', max_length=3, choices=ACCESS_CHOICES)
    phone = models.CharField('Phone', max_length=11)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'phone']
    objects = Base_User_Manager()
    def __str__(self):
        return 'ID: %s | Username: %s | Email: %s | Name: %s %s | Access: %s | Pass: %s' % (self.id, self.username, self.email, self.first_name, self.last_name, self.groups, self.password)

    def get_full_name(self):
        # The user is identified by their email address
        return self.username

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Artist(models.Model):
    artist_name = models.CharField(max_length=100)
    site = models.URLField(max_length=200, blank=True)
    sound = models.URLField(max_length=200, blank=True)
    about = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    contact_id = models.ForeignKey('MyUser', related_name="artist_contact")
    def __str__(self):
        return 'ID: %s | Artist: %s | Main Contact: %s' % (self.id, self.artist_name, self.contact_id.email)

class ArtistImages(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to='uploads/%Y/%m/%d/')
    defaultimage = models.BooleanField(default=False)
    artist = models.ForeignKey('Artist')
    def __str__(self):
        return '\nID: %s | Artist: %s | Default: %s | Image: %s' % (self.artist.id, self.artist.artist_name, self.defaultimage, self.image)

class VenueList(models.Model):
    STATE_CHOICES = (
    ( "AL", "Alabama" ),
    ( "AK", "Alaska" ),
    ( "AZ", "Arizona" ),
    ( "AR", "Arkansas" ),
    ( "CA", "California" ),
    ( "CO", "Colorado" ),
    ( "CT", "Connecticut" ),
    ( "DE", "Delaware" ),
    ( "FL", "Florida" ),
    ( "GA", "Georgia" ),
    ( "HI", "Hawaii" ),
    ( "ID", "Idaho" ),
    ( "IL", "Illinois" ),
    ( "IN", "Indiana" ),
    ( "IA", "Iowa" ),
    ( "KS", "Kansas" ),
    ( "KY", "Kentucky" ),
    ( "LA", "Louisiana" ),
    ( "ME", "Maine" ),
    ( "MD", "Maryland" ),
    ( "MA", "Massachusetts" ),
    ( "MI", "Michigan" ),
    ( "MN", "Minnesota" ),
    ( "MS", "Mississippi" ),
    ( "MO", "Missouri" ),
    ( "MT", "Montana" ),
    ( "NE", "Nebraska" ),
    ( "NV", "Nevada" ),
    ( "NH", "New Hampshire" ),
    ( "NJ", "New Jersey" ),
    ( "NM", "New Mexico" ),
    ( "NY", "New York" ),
    ( "NC", "North Carolina" ),
    ( "ND", "North Dakota" ),
    ( "OH", "Ohio" ),
    ( "OK", "Oklahoma" ),
    ( "OR", "Oregon" ),
    ( "PA", "Pennsylvania" ),
    ( "RI", "Rhode Island" ),
    ( "SC", "South Carolina" ),
    ( "SD", "South Dakota" ),
    ( "TN", "Tennessee" ),
    ( "TX", "Texas" ),
    ( "UT", "Utah" ),
    ( "VT", "Vermont" ),
    ( "VA", "Virginia" ),
    ( "WA", "Washington" ),
    ( "WV", "West Virginia" ),
    ( "WI", "Wisconsin" ),
    ( "WY", "Wyoming" ),
    )
    venue_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=45)
    state= models.CharField(max_length=2, choices=STATE_CHOICES)
    zipcode = models.CharField(max_length=5)
    phone = models.CharField(max_length=10)
    site = models.URLField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    contact_id = models.ForeignKey('MyUser', related_name="venue_contact")
    def __str__(self):
        return 'ID: %s | Venue: %s | Booker: %s %s' % (self.id, self.venue_name, self.contact_id.first_name, self.contact_id.last_name)

class VenueImages(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to='uploads/%Y/%m/%d/')
    defaultimage = models.BooleanField(default=False)
    venue = models.ForeignKey('VenueList', related_name="venue_image")

    def __str__(self):
        return '\nID: %s | Venue: %s | Default: %s | Image: %s' % (self.venue.id, self.venue.venue_name, self.defaultimage, self.image)

class Event(models.Model):
    PENDING = 'Pend'
    ACCEPTED = 'Acpt'
    DECLINED = 'Decl'
    STATUS_CHOICES = (
    	(PENDING, 'Pending Event'),
    	(ACCEPTED, 'Accepted Event'),
    	(DECLINED, 'Declined Event')
    	)
    event_date = models.DateField()
    status = models.CharField(max_length=45, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    venue_id = models.ForeignKey('VenueList', related_name="venue")
    artist_id = models.ForeignKey('Artist', related_name="artist")
    requestor_id = models.ForeignKey('MyUser', related_name="requestor")
    def __str__(self):
    	return 'ID: %s | Venue: %s | Artist: %s | Date: %s' % (self.id, self.venue_id.venue_name, self.artist_id.artist_name, self.event_date)

class Message(models.Model):
    message = models.CharField(max_length=255)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    event_id = models.ForeignKey('Event', related_name="event")
    author_id = models.ForeignKey('MyUser', related_name="author")
    def __str__(self):
        return 'Message ID: %s | Read: %s | Author: %s %s | Artist: %s | Venue: %s' % (self.id, self.read, self.author_id.first_name, self.author_id.last_name, self.event_id.artist_id.artist_name, self.event_id.venue_id.venue_name)

class Comment(models.Model):
	comment = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	message_id = models.ForeignKey('Message')
	event_id = models.ForeignKey('Event')
	author_id = models.ForeignKey('MyUser')
