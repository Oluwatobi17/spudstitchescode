from django.shortcuts import render, redirect, get_object_or_404
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.contrib import messages
from django.utils.crypto import get_random_string
from .models import User, Commodity, Cart, Order
from .forms import UserForm, CheckoutForm,UserUpdateForm,EditCommodityForm,CommodityForm
from decimal import Decimal
import requests
from spud import settings
import json
from django.core.mail import send_mail, EmailMessage

delivLoc1 = ['Ikoyi/VI','Oshodi','Surulere','Yaba','Ikeja','Festac','Ketu',
		'Ojota','Ogba','Maryland','Onipanu','Ilupeju','Mushin','Ikokun',
		'Ejigbo'
		]

delivLoc2 = ['Osapa/Agungi','VGC/Ikota','Lekki Phase 1','Egeda','Iyana Ipaja',
		'Ikotun','Abule Egba','Alagbado','Ipaja','Iju Ishaga','Ikorodu Garage'
		,'Omole Phase 2'
		]

delivLoc3 = ['Ajah/Sangotedo','Ikorodu Inside']

loc = []

def index(request):
	favset = [int(x) for x in request.session.get('favourites',{}).keys()]
	cartl = [int(x) for x in request.session.get('cart',{}).keys()]

	tags_id = []
	for i in request.session.get('recentlyviewed', {}).keys():
		c = list(Commodity.objects.get(id=i).tags.values_list('id', flat=True))
		tags_id.extend(c)

	recom = Commodity.objects.filter(tags__in=tags_id)
	recom = set(recom)
	return render(request, 'index.html', {
		'title': 'Spud Stitches',
		'tags': Tag.objects.all(),
		'popular': Commodity.objects.all().order_by('-qty_avail')[:9],
		'cart': request.session.get('cart', {}),
		'favourites': favset,
		'cartlist': cartl,
		'recommendation': list(recom)
		})

def search(request):
	if request.method=='POST':
		search = request.POST['search'].strip(' ').split(' ')
		results = []
		for keyword in search:
			if Commodity.objects.filter(title__icontains=keyword):
				results.extend(Commodity.objects.filter(title__icontains=keyword))
			if Commodity.objects.filter(description__icontains=keyword):
				results.extend(Commodity.objects.filter(description__icontains=keyword))
			if Commodity.objects.filter(tags__name=keyword.lower()):
				results.extend(Commodity.objects.filter(tags__name=keyword.lower()))
			
		results = set(results)
		favset = [int(x) for x in request.session.get('favourites',{}).keys()]
		cartl = [int(x) for x in request.session.get('cart',{}).keys()]
		return render(request, 'search.html', {
			'title': 'Search: Spud Stitches',
			'cart': list(results),
			'tags': Tag.objects.all(),
			'favourites': favset,
			'cartlist': cartl,
		})

	return redirect(shop, 'all')

def shop(request, category):
	# category = category.lower()
	if category=='all': commodities_obj = Commodity.objects.all() 
	elif category=='new': commodities_obj = Commodity.objects.all().order_by('-date')
	else:
		# tag = get_object_or_404(Tag, slug=category)
		commodities_obj = Commodity.objects.filter(tags__name=category)	

	paginator = Paginator(commodities_obj, 12)
	page = request.GET.get('page') or 1
	if int(page)<=paginator.num_pages:
		commodities = paginator.page(page)
	else:
		commodities = paginator.page(paginator.num_pages)

	favset = [int(x) for x in request.session.get('favourites',{}).keys()]
	cartl = [int(x) for x in request.session.get('cart',{}).keys()]
	return render(request, 'shop.html', {
		'title': category.upper()+': Shop now',
		'tags': Tag.objects.all(),
		'commodities': commodities,
		'category': category,
		'cart': request.session.get('cart', {}),
		'page': paginator,
		'favourites': favset,
		'cartlist': cartl
		})

def account(request):
	if request.user.is_authenticated:
		if request.method=='POST':
			update = UserUpdateForm(request.POST)
			if update.is_valid():
				user = User.objects.get(username=request.user.username)
				user.first_name = update.cleaned_data['first_name']
				user.last_name = update.cleaned_data['last_name']
				user.address = update.cleaned_data['address']
				user.phoneno = update.cleaned_data['phoneno']
				user.email = update.cleaned_data['email']
				user.save()
				messages.success(request, 'Account Updated')
				return redirect(account)

			else: messages.error(request, 'Please fill all required form')

		return render(request, 'account.html', {
			'title': 'My Spud Stitches Account Summary',
			'tags': Tag.objects.all(),
			'cart': request.session.get('cart', {})
			})

	messages.error(request, "Please login or signup if you don't have an account yet")
	return redirect(login)


def forgotpass(request):
	if request.method=='POST':
		username = request.POST['username'].replace(' ', '')
		if username:
			if User.objects.filter(username=username):
				user = User.objects.get(username=username)
				newpass = get_random_string(6)
				message = "Hello, {}. Your new password is {}. \n Please ignore this message if you don't have a Project account".format(user.first_name, newpass)
				
				res = send_mail('Password reset', message, "ibdac2000@gmail.com",[user.email], fail_silently=True)
				if res==None:
					messages.error(request, 'Unable to reset password, please try again')
				else:
					user.set_password(newpass)
					user.save()
					messages.success(request, 'New Password has been sent to your email')
				return redirect(login)
			else:
				messages.error(request, 'Username does not exist. Please check your letter case')
				return redirect(login)
		else:
			messages.error(request, 'Please enter the username you want to reset password')
			return redirect(login)
	else:
		return redirect(login)


def orders(request):
	if request.user.is_authenticated:
		user = User.objects.get(username=request.user.username)
		return render(request, 'orders.html', {
			'title': 'My Spud Stitches Orders',
			'tags': Tag.objects.all(),
			'cart': request.session.get('cart', {}),
			'orders': user.cart_set.filter(delivered=True)
			})

	messages.error(request, "Please login or signup if you don't have an account yet")
	return redirect(login)



def pendingOrders(request):
	if request.user.is_authenticated:
		user = User.objects.get(username=request.user.username)
		return render(request, 'pendingOrders.html', {
			'title': 'My Spud Stitches Pending Orders',
			'tags': Tag.objects.all(),
			'cart': request.session.get('cart', {}),
			'pending': user.cart_set.filter(delivered=False)
			})

	messages.error(request, "Please login or signup if you don't have an account yet")
	return redirect(login)

def wishlist(request):
	if request.user.is_authenticated:
		wishlist = request.session.get('favourites', {})
		favset = [int(x) for x in wishlist.keys()]
		cartl = [int(x) for x in request.session.get('cart',{}).keys()]
		return render(request, 'wishlist.html', {
			'title': 'My Spud Stitches Wish List',
			'tags': Tag.objects.all(),
			'wishlist': wishlist,
			'cart': request.session.get('cart', {}),
			'favourites': favset,
			'cartlist': cartl
			})

	messages.error(request, "Please login or signup if you don't have an account yet")
	return redirect(login)

def recent(request):
	favset = [int(x) for x in request.session.get('favourites', {}).keys()]
	cartl = [int(x) for x in request.session.get('cart',{}).keys()]
	return render(request, 'recent.html', {
		'title': 'My Spud Stitches Recently viewed',
		'tags': Tag.objects.all(),
		'recent': request.session.get('recentlyviewed', {}),
		'cart': request.session.get('cart', {}),
		'favourites': favset,
		'cartlist': cartl
		})

def changepassword(request):
	if request.user.is_authenticated:
		if request.method=='POST':
			user = User.objects.get(username=request.user.username)

			if (request.POST['password']==request.POST['password2']) and request.POST['password']!='':
				if user.check_password(request.POST['oldpassword']):
					user.set_password(request.POST['password'])
					user.save()
					messages.success(request, 'Password successful changed')

				else:
					messages.error(request, 'Wrong old password specified')
			else:
				messages.error(request, 'Password and Confirm password does not match')


		return render(request, 'changepassword.html', {
			'title': 'My Spud Stitches Change Password',
			'tags': Tag.objects.all(),
			'cart': request.session.get('cart', {})
			})

	messages.error(request, "Please login or signup if you don't have an account yet")
	return redirect(login)


def cart(request):
	favset = [str(x) for x in request.session.get('favourites',{}).keys()]
	cartl = [str(x) for x in request.session.get('cart',{}).keys()]
	return render(request, 'cart.html', {
		'title': 'My Spud Stitches Cart',
		'tags': Tag.objects.all(),
		'cart': request.session.get('cart', {}),
		'favourites': favset,
		'cartlist': cartl
		})

def order(request, id):
	cart = get_object_or_404(Cart, id=id)
	if request.user.is_authenticated:
		favset = [int(x) for x in request.session.get('favourites',{}).keys()]
		cartl = [int(x) for x in request.session.get('cart',{}).keys()]
		return render(request, 'order.html', {
			'title': 'My Spud Stitches Cart',
			'tags': Tag.objects.all(),
			'cart': request.session.get('cart', {}),
			'order': cart,
			'favourites': favset,
			'cartlist': cartl
			})

	messages.error(request, "Please login or signup if you don't have an account yet")
	return redirect(login)
# def products(request, category):
# 	return render(request, 'shop.html', {
# 		'title': 'Sweat Shirts',
# 		'cart': request.session.get('cart', {})
# 		})


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
		'id': commodity.id,
		'title': commodity.title,
		'price': float(commodity.price),
		'picture1': picture1,
		'picture2': picture2
	}

	request.session['recentlyviewed'][id] = item 
	favset = [int(x) for x in request.session.get('favourites',{}).keys()]
	cartl = [int(x) for x in request.session.get('cart',{}).keys()]
	return render(request, 'product.html', {
		'title': commodity.title,
		'tags': Tag.objects.all(),
		'commodity': commodity,
		'colors': commodity.colors.split("***"),
		'sizes': commodity.sizes.split("***"),
		'cart': request.session.get('cart', {}),
		'favourites': favset,
		'cartlist': cartl
		})

def contact(request):
	return render(request, 'contact.html', {
		'title': 'Contact Us',
		'tags': Tag.objects.all(),
		'cart': request.session.get('cart', {})
		})


def checkout(request):
	print(settings.PAYSTACK_PK)
	if request.method=='POST':
		if request.user.is_authenticated:
			if request.session.get('cart', False):

				cartform = CheckoutForm(request.POST)
				if cartform.is_valid():
					method = cartform.cleaned_data['paymentmethod']
					global cart
					cart = request.session.get('cart',{})
					if method=='cc':
						total = 0
						for item in cart:
							total += (cart[item]['price'] * cart[item]['quantity'])

						headers = {
							'Authorization': 'Bearer '+settings.PAYSTACK_PK,
							'Content-Type': 'application/json'
						}
						['user','name', 'address','town', 'phoneno', 'email', 'paymentmethod']
						metadata = {
							'user': User.objects.get(username=request.user.username).pk,
							'name': cartform.cleaned_data['name'],
							'address': cartform.cleaned_data['address'],
							'town': cartform.cleaned_data['town'],
							'phoneno': cartform.cleaned_data['phoneno']
						}
				

						data = {
							'amount': str((request.session['deliverycost']+total)*100),
							'email': str(cartform.cleaned_data['email']),
							'metadata': metadata
							#'callback': 'http://localhost:3000/cccomplete-payment/'
						}

						url = 'https://api.paystack.co/transaction/initialize/'
						response = requests.post(url, headers=headers,data=json.dumps(data))
						
						res = response.json()
						if res['status']==True:
							request.session['paystackpaymentref'] = res['data']['reference']
							request.session['carttotal'] = data['amount']
							return redirect('https://checkout.paystack.com/'+res['data']['access_code'])

						messages.error(request, 'Error processing the payment gateway')
						return redirect('checkout')

					# if not cc

					cartobj = cartform.save(commit=True)
					for id in cart:
						id_obj = Commodity.objects.get(pk=id)
						Order.objects.create(cart=cartobj,commodity=id_obj \
							,color=cart[id]['color'],size=cart[id]['size'],quantity=cart[id]['quantity'])
						
						cartobj.paymentref = get_random_string(length=15)
						cartobj.total_price += (id_obj.price*cart[id]['quantity'])

					# cartobj.user = User.objects.get(username=request.user.username)
					cartobj.save()
					admin = User.objects.filter(is_superuser=True)[0]
					message = "Hello, {}. New Order received, ref: {}".format(admin.first_name, cartobj.paymentref)
				
					res = send_mail('Password reset', message, "ibdac2000@gmail.com",[admin.email], fail_silently=True)
					messages.success(request, 'Order received. Thanks for Shopping with us')
					return redirect(pendingOrders) 

				print(cartform.errors)
				messages.error(request, 'Please ensure you fill all required fields')
				return redirect(checkout)
			else:
				messages.error(request, 'Cannot proceed because you have an empty cart')
				return redirect(product, 'all')

		messages.error(request, 'Please login or register to proceed to carting')
		return redirect(login)

	return render(request, 'checkout.html', {
		'title': 'Checkout',
		'tags': Tag.objects.all(),
		'cart': request.session.get('cart', {}),
		'delivLoc1': delivLoc1,
		'delivLoc2': delivLoc2,
		'delivLoc3': delivLoc3
		})

def completepayment(request):
	ref = request.GET.get('reference')
	
	headers = {
		'Authorization': 'Bearer '+settings.PAYSTACK_PK
	}
	url = 'https://api.paystack.co/transaction/verify/{}'.format(ref)
	response = requests.get(url, headers=headers)
	response = response.json()
	if response['status']==True:
		carttotal = int(  float( request.session.get('carttotal', 0) )  )

		if response['data']['status']=='success' and response['data']['amount']==carttotal:
			cart = request.session.get('cart', {})

			user = User.objects.get(pk=response['data']['metadata']['user'])
			cartobj = Cart.objects.create(user=user)
			cartobj.name = response['data']['metadata']['name']
			cartobj.address = response['data']['metadata']['address']
			cartobj.town = response['data']['metadata']['town']
			cartobj.phoneno = response['data']['metadata']['phoneno']
			cartobj.email = response['data']['customer']['email']
			cartobj.paymentmethod = 'cc'
			cartobj.paymentref = ref
			cartobj.total_price = carttotal/100
			for id in cart:
				id_obj = Commodity.objects.get(pk=id)
				Order.objects.create(cart=cartobj,commodity=id_obj \
					,color=cart[id]['color'],size=cart[id]['size'],quantity=cart[id]['quantity'])
				
			# cartobj.user = User.objects.get(username=request.user.username)
			cartobj.save()

		admin = User.objects.filter(is_superuser=True)[0]
		message = "Hello, {}. New Order received, ref: {}".format(admin.first_name, cartobj.paymentref)
	
		res = send_mail('Password reset', message, "ibdac2000@gmail.com",[admin.email], fail_silently=True)
		messages.success(request, 'Payment Complete and order received. Thanks for Shopping with us')
		return redirect(pendingOrders)

	messages.error(request, 'Unable to process payment. Try again')
	return redirect(checkout)

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
			'title': 'Sign In or Sign Up to Spud Stitches Store',
			'tags': Tag.objects.all(),
			'cart': request.session.get('cart', {})
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


############### Super User Views ##############
def superOrders(request):
	""" Give list of orders (delivered or not) """
	if request.user.is_superuser:
		return render(request, 'superorders.html', {
			'title': 'Spud Orders',
			'tags': Tag.objects.all(),
			'cart': request.session.get('cart', {}),
			'carts': Cart.objects.all().order_by('-date')
			})
	messages.error(request,'Access Denied')
	return redirect(index)

def superOrder(request, id):
	""" Give details about a single order """
	if request.user.is_superuser:
		cart = get_object_or_404(Cart, id=id)
		return render(request, 'superorder.html', {
			'title': 'Spud Order',
			'tags': Tag.objects.all(),
			'cart': request.session.get('cart', {}),
			'carts': cart
			})

	messages.error(request,'Access Denied')
	return redirect(index)


def superAdd(request):
	""" Adding new commodity to store """
	if request.user.is_superuser:
		if request.method=='POST':
			# Handle the Commodity adding post request
			form = CommodityForm(request.POST, request.FILES)
			if form.is_valid():
				commodity = form.save(commit=False)
				# commodity.price = float(form.cleaned_data['price'])
				commodity.formerprice = Decimal(float(form.cleaned_data['price'])*1.43)
				commodity.colors = form.cleaned_data['colors'].strip(' ').replace(',','***')
				commodity.sizes = form.cleaned_data['sizes'].strip(' ').replace(',','***')
				
				commodity.save()
				for tag in request.POST['tags'].split(','):
					commodity.tags.add(tag.strip(' '))

				commodity.save()
				messages.success(request, 'Commodity Added')
				return redirect(superAdd)
			else:
				messages.error(request, 'Please fill required fields')
				print(form.errors)
				return redirect(superAdd)

		return render(request, 'superadd.html', {
			'title': 'Add Commodity',
			'tags': Tag.objects.all(),
			'cart': request.session.get('cart', {})
			})
	messages.error(request,'Access Denied')
	return redirect(index)

def superEdit(request, id):
	""" Editing  existing commodity information """
	if request.user.is_superuser:
		commodity = get_object_or_404(Commodity, id=id)
		if request.method=='POST':
			# Handles the Commodity editing post request
			form = EditCommodityForm(request.POST, request.FILES, instance=commodity)
			if form.is_valid():
				comm = form.save(commit=False)
				comm.colors = request.POST['colors'].replace(',', '***')
				comm.sizes = request.POST['sizes'].replace(',', '***')

				comm.tags.all().delete()
				for tag in request.POST['tags'].split(','):
					comm.tags.add(tag.strip(' '))

				comm.save()
				messages.success(request, 'Update Successful')
				return redirect(superItems)
			else:
				messages.error(request, 'Please fill required fields')
				print(form.errors)
				return redirect(superEdit, id)

		return render(request, 'superedit.html', {
			'title': 'Editing',
			'tags': Tag.objects.all(),
			'cart': request.session.get('cart', {}),
			'commodity': commodity 
			})
	messages.error(request,'Access Denied')
	return redirect(index)

def superDelete(request, id):
	""" Delete  existing commodity information """
	if request.user.is_superuser:
		# commodity = get_object_or_404(Commodity, id=id)
		commodity = Commodity.objects.get(id=id)
		commodity.delete()
		# commodity.delete_object()
		# print(type(commodity))
		# print(commodity)
		# Commodity.objects.get(id=id).delete()

		messages.success(request, 'Item Deleted')
		return redirect(superAdd)

	messages.error(request,'Access Denied')
	return redirect(index)


def superUsers(request):
	""" Give list of all members """
	if request.user.is_superuser:
		return render(request, 'superusers.html', {
			'title': 'Spud Stitches',
			'tags': Tag.objects.all(),
			'cart': request.session.get('cart', {}),
			'users': User.objects.all() 
			})
	messages.error(request,'Access Denied')
	return redirect(index)


def superItems(request):
	""" Give list of all items on the store """
	if request.user.is_superuser:
		return render(request, 'superitems.html', {
			'title': 'Spud Stitches Items',
			'tags': Tag.objects.all(),
			'cart': request.session.get('cart', {}),
			'items': Commodity.objects.all() 
			})
	messages.error(request,'Access Denied')
	return redirect(index)