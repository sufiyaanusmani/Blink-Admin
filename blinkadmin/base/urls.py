from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name='home-page'),
    path('orders/', views.ordersPage, name='orders-page'),
    path('customers/', views.customersPage, name='customers-page'),
    path('restaurants/', views.restaurantsPage, name='restaurants-page'),
    path('analytics/', views.analyticsPage, name='analytics-page'),
    path('login/', views.loginPage, name='login-page'),
]
