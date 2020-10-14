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
		fields = ['user','name', 'address','town', 'phoneno', 'email', 'paymentmethod']


class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name','last_name', 'address', 'phoneno', 'email']


class CommodityForm(forms.ModelForm):
	class Meta:
		model = Commodity
		fields = ['title','qty_avail', 'price','sizes','colors','picture1',
			'picture2','picture3','description']

	
class EditCommodityForm(forms.ModelForm):
	picture1 = forms.FileField(required=False)
	picture2 = forms.FileField(required=False)
	picture3 = forms.FileField(required=False)
	class Meta:
		model = Commodity
		fields = ['title','qty_avail', 'price','description', 'colors', 'sizes',
		'picture1','picture2','picture3']

