from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^shop/(?P<category>[%&+ \w+ \W+]+)/$', views.shop, name='shop'),
    #re_path(r'^product/(?P<category>[%&+ \w+ \W+]+)/$', views.products, name='products'),
    path('product/<int:id>/', views.product, name='product'),
    path('search/', views.search, name='search'),
    path('account/', views.account, name='account'),
    path('account/orders/', views.orders, name='orders'),
    path('account/orders/<int:id>', views.order, name='order'),
    path('account/pending-orders/', views.pendingOrders, name='pending'),
    path('account/wishlist/', views.wishlist, name='wishlist'),
    path('account/recently-viewed/', views.recent, name='recent'),
    path('account/change-password/', views.changepassword, name='changepassword'),
    path('cart/', views.cart, name='cart'),
    path('cccomplete-payment/', views.completepayment, name='completepayment'),
    path('contact/', views.contact, name='contact'),
    path('checkout/', views.checkout, name='checkout'),
    path('signin/', views.login, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.logout, name='signout'),

    # Super Users link
    path('superuser/', views.superOrders, name='superorders'),
    path('superuser/cart/<int:id>/', views.superOrder, name='superorder'),
    path('superuser/add/', views.superAdd, name='superadd'),
    path('superuser/items/', views.superItems, name='superitems'),
    path('superuser/edit/<int:id>/', views.superEdit, name='superedit'),
    path('superuser/delete/<int:id>/', views.superDelete, name='superdelete'),
    path('superuser/users/', views.superUsers, name='superusers'),
]

   # re_path(r'^comment/(?P<id>[0-9]+)/$', views.commentproject, name='commentproject'),
