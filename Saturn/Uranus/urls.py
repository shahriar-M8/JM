from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('registration', views.registration, name='registration'),
    path('logout', views.logout, name='logout'),
    path('product', views.product, name='product'),
    path('search', views.search, name='search'),
    path('checkout/<id>', views.checkout, name='checkout'),
    path('add-product', views.add_products, name='add-product'),
    path('update-product/<id>', views.update_products, name='update-product')
]