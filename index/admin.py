from django.contrib import admin
from .models import User, Commodity, Cart


admin.site.register(User)
admin.site.register(Commodity)
admin.site.register(Cart)