from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
	re_path(r'^favourite/(?P<id>[0-9]+)/(?P<action>[%&+ \w+ \W+]+)/$', views.Favourite.as_view(), name='favourite'),
	re_path(r'^addcart/(?P<id>[0-9]+)/(?P<action>[%&+ \w+ \W+]+)/', views.Cart.as_view(), name='cart'),

]

urlpatterns = format_suffix_patterns(urlpatterns)