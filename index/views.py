from django.shortcuts import render


def index(request):
	return render(request, 'index.html', {
		'title': 'Spud Stitches'
		})

def shop(request):
	return render(request, 'shop.html', {
		'title': 'Shop now'
		})

def products(request, category):
	return render(request, 'shop.html', {
		'title': 'Sweat Shirts'
		})


def product(request, id):
	return render(request, 'product.html', {
		'title': 'A4 Hoodies'
		})

def contact(request):
	return render(request, 'contact.html', {
		'title': 'Contact Us'
		})

def checkout(request):
	return render(request, 'checkout.html', {
		'title': 'Checkout'
		})

def login(request):
	return render(request, 'login.html', {
		'title': 'Login'
		})

def signup(request):
	return render(request, 'signup.html', {
		'title': 'Create an Account'
		})