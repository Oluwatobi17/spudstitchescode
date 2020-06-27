from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('shop/', views.shop, name='shop'),
    re_path('^product/(?P<category>[A-Za-b]+)/$', views.products, name='products'),
    path('product/<int:id>', views.product, name='product'),
    path('contact/', views.contact, name='contact'),
    path('checkout/', views.checkout, name='checkout'),
    path('signin/', views.login, name='signin'),
    path('signup/', views.signup, name='signup'),
]
