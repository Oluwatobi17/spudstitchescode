from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^shop/(?P<category>[%&+ \w+ \W+]+)/$', views.shop, name='shop'),
    re_path(r'^product/(?P<category>[%&+ \w+ \W+]+)/$', views.products, name='products'),
    path('product/<int:id>', views.product, name='product'),
    path('account/', views.account, name='account'),
    path('account/orders/', views.orders, name='orders'),
    path('account/pending-orders/', views.pendingOrders, name='pending'),
    path('account/wishlist/', views.wishlist, name='wishlist'),
    path('account/recently-viewed/', views.recent, name='recent'),
    path('account/change-password/', views.changepassword, name='changepassword'),
    path('cart/', views.cart, name='cart'),
    path('contact/', views.contact, name='contact'),
    path('checkout/', views.checkout, name='checkout'),
    path('signin/', views.login, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.logout, name='signout'),
]

   # re_path(r'^comment/(?P<id>[0-9]+)/$', views.commentproject, name='commentproject'),
