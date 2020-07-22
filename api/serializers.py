from rest_framework import serializers
from index.models import Order

class CartSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = ['commodity', 'color', 'size', 'quantity']

