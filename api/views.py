from django.shortcuts import  get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from index.models import User, Commodity
from index.models import Cart as CartModel
from .serializers import CartSerializer
from index.views import delivLoc1,delivLoc2,delivLoc3


class Favourite(APIView):
	def get(self, request, id, action):
		commodity = get_object_or_404(Commodity, id=id)
		id = str(id)
		if not request.session.get('favourites'):
			request.session['favourites'] = {}
			# request.session['favSet'] = []

		if action=='remove' and (id in request.session['favourites'].keys()): # If user want to remove item from fav list
			
			del request.session['favourites'][id]
			# favset = set(request.session['favSet']); favset.remove(id)
			# request.session['favSet'] = list(favset)
			return Response(True)

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

		
		# request.session['favourites'][id] = item 
		request.session['favourites'].update({id:item})
		# favset = set(request.session['favSet']); favset.add(id)
		# request.session['favSet'] = list(favset)

		return Response(True)

class Cart(APIView):
	def get(self, request, id, action):
		commodity = get_object_or_404(Commodity, id=id)
		id = str(id)
		if not request.session.get('cart'):
			request.session['cart'] = {}
			
		if action=='remove' and (id in request.session['cart'].keys()):
			q = request.session['cart'][id]['quantity']
			del request.session['cart'][id]
			return Response({'status':True, 'content': {
				'price':commodity.price,
				'qty': q
			}})

		if not commodity.picture1:
			picture1, picture2 = 'Empty', 'Empty'
		else:
			picture1, picture2 = commodity.picture1.url, commodity.picture2.url
		
		item = {
			'title': commodity.title,
			'price': float(commodity.price),
			'color': commodity.colors.split('***')[0],
			'size': commodity.sizes.split('***')[0],
			'quantity': 1,
			'picture1': picture1,
			'picture2': picture2
		}
		
		request.session['cart'][id] = item

		return Response({'status':True, 'content': item})


	def post(self, request, id, action):
		if not request.session.get('cart'):
			request.session['cart'] = {}
			
		serializer = CartSerializer(data=request.data)

		if serializer.is_valid():
			commodity = get_object_or_404(Commodity, id=id)
			if not commodity.picture1:
				picture1, picture2 = 'Empty', 'Empty'
			else:
				picture1, picture2 = commodity.picture1.url, commodity.picture2.url
			
			item = {
				'id': id,
				'title': commodity.title,
				'price': float(commodity.price),
				'color': serializer.data['color'],
				'size': serializer.data['size'],
				'quantity': serializer.data['quantity'],
				'picture1': picture1,
				'picture2': picture2
			}
			
			commodity_id = str(commodity.id)
			request.session['cart'][commodity_id] = item
			# if request.session['cart'].get(commodity_id, False):
			# 	request.session['cart'][commodity_id] = item
			# else:
			# 	request.session['cart'][commodity_id]['quantity'] += 1

			return Response({'status':True, 'content': request.session['cart']})
		return Response({'status':False})


class Deliver(APIView):
	def get(self, request, id):
		if request.user.is_superuser:
			cart = get_object_or_404(CartModel, id=id)
			cart.delivered = True 
			cart.save()

			return Response(True)

		return Response(False)

class DeliveryCost(APIView):
	def post(self, request):
		loc = request.data['location']

		if loc in delivLoc1:
			price = 1000
		elif loc in delivLoc2:
			price = 1500
		elif loc in delivLoc3:
			price = 2000
		else:
			price = 1500

		request.session['deliverycost'] = price
		return Response({'delivPrice': price})