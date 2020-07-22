from django.shortcuts import  get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from index.models import User, Commodity, Cart
from .serializers import CartSerializer


class Favourite(APIView):
	def get(self, request, id, action):
		commodity = get_object_or_404(Commodity, id=id)
		id = str(id)
		if not request.session.get('favourites'):
			request.session['favourites'] = {}

		if action=='remove': # If user want to remove item from fav list
			del request.session['favourites'][id]

			return Response(True)

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

		request.session['favourites'][id] = item 

		return Response(True)

class Cart(APIView):
	def get(self, request, id, action):
		if not request.session.get('cart'):
			request.session['cart'] = {}
			
		if action=='remove':
			del request.session['cart'][str(id)]
			print('After removal')
			print(request.session['cart'])
			return Response(True)

		commodity = get_object_or_404(Commodity, id=id)
		item = {
			'title': commodity.title,
			'price': float(commodity.price),
			'color': commodity.colors.split('***')[0],
			'size': commodity.sizes.split('***')[0],
			'quantity': 1
		}
		
		commodity_id = str(commodity.id)
		request.session['cart'][commodity_id] = item

		print('Cart')
		print(request.session['cart'])
		return Response(True)


	def post(self, request, id, action):
		if not request.session.get('cart'):
			request.session['cart'] = {}
			
		serializer = CartSerializer(data=request.data)

		commodity = get_object_or_404(Commodity, id=serializer.data.commodity)
		item = {
			'title': commodity.title,
			'price': float(commodity.price),
			'color': serializer.data.color,
			'size': serializer.data.size,
			'quantity': serializer.data.quantity
		}
		
		commodity_id = str(commodity.id)
		request.session['cart'][commodity_id] = item
		# if request.session['cart'].get(commodity_id, False):
		# 	request.session['cart'][commodity_id] = item
		# else:
		# 	request.session['cart'][commodity_id]['quantity'] += 1

		print('Cart')
		print(request.session['cart'])
		return Response(True)

# cart = {
# 	3: {
# 		'title': 'adada'
# 		price: 42.43,
# 		color: 'Blue',
# 		size: 'XL',
# 		qty: 4,
# 	}
# }
# Product_title, price, color, size, quantity, commodity_id

# ['commodity', 'color', 'size', 'quantity']