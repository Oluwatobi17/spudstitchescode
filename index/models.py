from django.db import models
from django.contrib.auth.models import AbstractUser
from taggit.managers import TaggableManager

class User(AbstractUser):
	phoneno = models.CharField(max_length=20)
	favorites = models.CharField(max_length=1000) # My array
	address = models.CharField(max_length=200, default='No address')

	def __str__(self):
		return self.username

class Commodity(models.Model):
	title = models.CharField(max_length=500)
	qty_avail = models.IntegerField()
	price = models.DecimalField(decimal_places=2, max_digits=4)
	formerprice = models.DecimalField(decimal_places=2, max_digits=4)
	description = models.TextField()
	colors = models.CharField(max_length=1000) # Blue***Green
	sizes = models.CharField(max_length=1000) # X***XL
	picture1 = models.FileField(upload_to="commodityPictures/")
	picture2 = models.FileField(upload_to="commodityPictures/")
	picture3 = models.FileField(upload_to="commodityPictures/")
	tags = TaggableManager() # All tags should be in Small letter

	def __str__(self):
		return self.title

	def inStock(self):
		if self.qty_avail>0:
			return True
		return False

class Cart(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=500) # First_name and last_name
	address = models.CharField(max_length=500)
	town = models.CharField(max_length=100)
	phoneno = models.CharField(max_length=20)
	email = models.CharField(max_length=50)
	delivered = models.BooleanField(default=False)
	date = models.DateTimeField(auto_now_add=True)
	total_price = models.DecimalField(decimal_places=2, max_digits=10, default=0)

	def __str__(self):
		return self.user.first_name +' '+self.user.last_name

	def isDelivered(self):
		if self.delivered:
			return True
			
		return False


class Order(models.Model):
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
	commodity = models.ForeignKey(Commodity, on_delete=models.DO_NOTHING)
	color = models.CharField(max_length=1000)
	size = models.CharField(max_length=1000)
	quantity = models.IntegerField(default=1)

	def __str__(self):
		return self.commodity.title
