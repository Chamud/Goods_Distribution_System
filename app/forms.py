from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app.models import Information
from django import forms
from django.core.validators import RegexValidator

#Regex
phone_regex = RegexValidator(regex=r'^(\+\d{1,3})?\s?\d{2}\s?\d{3}\s?\d{4,7}$', message="Phone number format: '+94 79 999 9999'")
id_regex = RegexValidator('^[0-9]{12}$|^[0-9]{9}[VX]$', message="Not a valid NIC number.")

class CreateUserForm(UserCreationForm):
	nic = forms.CharField(validators=[id_regex])
	city = forms.IntegerField()
	class Meta:
		model = User
		fields = ['username', 'email', 'first_name', 'last_name', 'nic', 'city', 'password1', 'password2']

class InformationForm(ModelForm):
	cityid = forms.IntegerField()
	description = forms.CharField(min_length=25)
	title = forms.CharField(max_length=25)
	contact= forms.CharField(validators=[phone_regex])
	class Meta:
		model = Information
		fields = ['title', 'description', 'address', 'contact', 'cityid']