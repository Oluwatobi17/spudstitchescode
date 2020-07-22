from django import forms
from .models import User, Commodity, Cart


class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name','email', 'password']


class CheckoutForm(forms.ModelForm):
	class Meta:
		model = Cart
		fields = ['user','name', 'address','town', 'phoneno', 'email']

