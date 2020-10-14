from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
	re_path(r'^favourite/(?P<id>[0-9]+)/(?P<action>[%&+ \w+ \W+]+)/$', views.Favourite.as_view(), name='favourite'),
	re_path(r'^addcart/(?P<id>[0-9]+)/(?P<action>[%&+ \w+ \W+]+)/', views.Cart.as_view(), name='cart'),
	re_path(r'^deliver/(?P<id>[0-9]+)/', views.Deliver.as_view(), name='deliver'),
	re_path(r'^deliverycost/', views.DeliveryCost.as_view(), name='deliverycost'),

]

urlpatterns = format_suffix_patterns(urlpatterns)