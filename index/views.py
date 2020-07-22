from django.shortcuts import render, redirect, get_object_or_404
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.contrib import messages
from .models import User, Commodity, Cart, Order
from .forms import UserForm, CheckoutForm




def index(request):
	request.session['favourites'] = {}
	request.session['cart'] = {}
	return render(request, 'index.html', {
		'title': 'Spud Stitches',
		'popular': Commodity.objects.all().order_by('-qty_avail')[:5]
		})

def shop(request, category):
	category = category.lower()
	if category=='all':
		commodities_obj = Commodity.objects.all() 
	else:
		# tag = get_object_or_404(Tag, slug=category)
		commodities_obj = Commodity.objects.filter(tags__name=category)

	paginator = Paginator(commodities_obj, 9)
	page = request.GET.get('page') or 1
	if int(page)<=paginator.num_pages:
		commodities = paginator.page(page)
	else:
		commodities = paginator.page(paginator.num_pages)
	return render(request, 'shop.html', {
		'title': category.upper()+': Shop now',
		'commodities': commodities,
		'category': category
		})

def account(request):
	if request.user.is_authenticated:
		return render(request, 'account.html', {
			'title': 'My Spud Stitches Account Summary'
			})

	messages.error(request, "Please login or signup if you don't have an account yet")
	return redirect(login)

def orders(request):
	if request.user.is_authenticated:
		return render(request, 'orders.html', {
			'title': 'My Spud Stitches Orders'
			})

	messages.error(request, "Please login or signup if you don't have an account yet")
	return redirect(login)


def pendingOrders(request):
	if request.user.is_authenticated:
		return render(request, 'pendingOrders.html', {
			'title': 'My Spud Stitches Pending Orders'
			})

	messages.error(request, "Please login or signup if you don't have an account yet")
	return redirect(login)

def wishlist(request):
	if request.user.is_authenticated:
		wishlist = request.session.get('favourites', {})
		return render(request, 'wishlist.html', {
			'title': 'My Spud Stitches Wish List',
			'wishlist': wishlist
			})

	messages.error(request, "Please login or signup if you don't have an account yet")
	return redirect(login)

def recent(request):
	if request.user.is_authenticated:
		if not request.session.get('recentlyviewed'):
			request.session['recentlyviewed'] = {}
		return render(request, 'recent.html', {
			'title': 'My Spud Stitches Recently viewed',
			'recent': request.session['recentlyviewed']
			})

	messages.error(request, "Please login or signup if you don't have an account yet")
	return redirect(login)

def changepassword(request):
	if request.user.is_authenticated:
		if request.method=='POST':
			user = User.objects.get(username=request.user.username)

			if (request.POST['password']==request.POST['password2']) and request.POST['password']!='':
				if user.check_password(request.POST['password']):
					user.set_password(request.POST['password'])
					user.save()
					messages.success(request, 'Password successful changed')

				else:
					messages.error(request, 'Wrong old password specified')
			else:
				messages.error(request, 'Password and Confirm password does not match')


		return render(request, 'changepassword.html', {
			'title': 'My Spud Stitches Change Password'
			})

	messages.error(request, "Please login or signup if you don't have an account yet")
	return redirect(login)


def cart(request):
	return render(request, 'cart.html', {
		'title': 'My Spud Stitches Cart'
		})


def products(request, category):
	return render(request, 'shop.html', {
		'title': 'Sweat Shirts'
		})


def product(request, id):
	if not request.session.get('recentlyviewed'):
		request.session['recentlyviewed'] = {}

	commodity = get_object_or_404(Commodity, id=id)
	id = str(id)

	if not commodity.picture1:
		picture1, picture2 = 'Empty', 'Empty'
	else:
		picture1, picture2 = commodity.picture1.url, commodity.picture2.url
	item = {
		'title': commodity.title,
		'price': float(commodity.price),
		'picture1': picture1,
		'picture2': picture2
	}

	request.session['recentlyviewed'][id] = item 

	return render(request, 'product.html', {
		'title': commodity.title
		})

def contact(request):
	return render(request, 'contact.html', {
		'title': 'Contact Us'
		})

def checkout(request):
	if request.method=='POST':
		if request.user.is_authenticated:
			cartform = CheckoutForm(request.POST)
			if cartform.is_valid():
				
				cartform.cleaned_data['name'] += ' '+request.POST['last_name']
				cartobj = cartform.save(commit=True)
				
				cart = request.session['cart']
				for id in cart:
					id_obj = Commodity.objects.get(pk=id)
					Order.objects.create(cart=cartobj,commodity=id_obj \
						,color=cart[id]['color'],size=cart[id]['size'],quantity=cart[id]['quantity'])
					
					cartobj.total_price += (id_obj.price*cart[id]['quantity'])

				# cartobj.user = User.objects.get(username=request.user.username)
				cartobj.save()
				messages.success(request, 'Order received')
				return redirect(account) 

			print(cartform.errors)
			messages.error(request, 'Please ensure you fill all required fields')
			return redirect(checkout)

		messages.error(request, 'Please login or register to proceed to carting')
		return redirect(login)

	return render(request, 'checkout.html', {
		'title': 'Checkout'
		})


def login(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			if user.is_active:
				login_user(request, user)
				
				return redirect(shop, 'all')
				
			messages.error(request, 'Your account has been disabled')
				
		else:
			messages.error(request, 'Invalid login')
		
		return redirect(login)
	else:
		return render(request, 'login.html', {
			'title': 'Sign In or Sign Up to Spud Stitches Store'
			})

def signup(request):
	if request.method=='POST':
		if not request.POST['password'] == request.POST['password2']:
			messages.error(request, 'Password chosen mismatch. Please try again')
			return redirect(login)

		if User.objects.filter(username=request.POST['username']):
			messages.error(request, 'Username you chose has been taken')
			return redirect(login)

		form = UserForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user.set_password(password)

			user.save()
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login_user(request, user)
				
				messages.success(request, 'Welcome, enjoy the best shopping experience')
				return redirect(shop, 'all')
		
		messages.error(request, 'Please ensure the all the field are filled')
		return redirect(signup)
	else:
		return redirect(login)


def logout(request):
	logout_user(request)
	return redirect(login)
