from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Artist, Venue, Event, MyUser

admin.site.register(Artist)
admin.site.register(Venue)
admin.site.register(Event)

class UserCreationForm(forms.ModelForm):
    BOOKER = 'BKR'
    ARTIST = 'ART'
    ACCESS_CHOICES = (
        (BOOKER, 'Booker'),
        (ARTIST, 'Artist')
        )
    username = forms.CharField(widget=forms.TextInput, label="Username")
    first_name = forms.CharField(widget=forms.TextInput, label="First Name")
    last_name = forms.CharField(widget=forms.TextInput, label="Last Name")
    email = forms.EmailField(widget=forms.TextInput,label="Email")
    phone = forms.CharField(widget=forms.TextInput,label="Phone")
    groups = forms.ChoiceField(widget=forms.Select, choices=ACCESS_CHOICES, label="Access")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = MyUser
        fields = ['username','first_name', 'last_name', 'email', 'phone', 'groups', 'password1', 'password2']

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    BOOKER = 'BKR'
    ARTIST = 'ART'
    ACCESS_CHOICES = (
        (BOOKER, 'Booker'),
        (ARTIST, 'Artist')
        )
    username = forms.CharField(widget=forms.TextInput, label="Username")
    first_name = forms.CharField(widget=forms.TextInput, label="First Name")
    last_name = forms.CharField(widget=forms.TextInput, label="Last Name")
    email = forms.EmailField(widget=forms.TextInput,label="Email")
    phone = forms.CharField(widget=forms.TextInput,label="Phone")
    groups = forms.ChoiceField(widget=forms.Select, choices=ACCESS_CHOICES, label="Access")
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('username','first_name', 'last_name', 'email', 'phone', 'groups', 'password')

    def clean_password(self):
        return self.initial['password']

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'first_name', 'last_name', 'email', 'phone', 'groups', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'groups')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'phone', 'groups', 'password1', 'password2')}
        ),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name', 'groups')
    ordering = ('first_name', 'last_name', 'email', 'groups')
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
