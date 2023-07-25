
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('add_to_bookmarked',views.add_to_bookmarked),
    path('regLog', views.regLog),
    path('book', views.book),
    path('register', views.register),
    path('login', views.login),
    path('admin', views.admin),
    path('user', views.user),
    path('add', views.add), 
    path('addCar', views.addCar),
    path('logout', views.logout),
    path('edit/<int:car_id>', views.edit), 
    path('editCar/<int:car_id>', views.editCar),
    path('delete/<int:car_id>', views.delete),
    path('addToCart', views.add_to_cart),
    path('cart', views.cart),	  
    path('checkout', views.checkout), 
    path('bookmarked', views.bookmarked),
    path('remove_bookmark/<int:car_id>', views.remove_from_bookmarked),
    path('sort_cars', views.sort_properties),
]