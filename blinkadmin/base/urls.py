from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name='home-page'),

    # Core URLs
    path('login/', views.loginPage, name='login-page'),
    path('logout/', views.logoutUser, name='logout'),
    path('orders/', views.ordersPage, name='orders-page'),
    path('customers/', views.customersPage, name='customers-page'),
    path('restaurants/', views.restaurantsPage, name='restaurants-page'),
    path('analytics/', views.analyticsPage, name='analytics-page'),

    path('restaurants/add-new-restaurant/', views.newRestaurantPage,
         name='new-restaurant-page'),
    path('restaurants/delete-restaurant/<str:id>', views.deleteRestaurantPage,
         name='delete-restaurant-page'),
    path('restaurants/edit-restaurant/<str:id>', views.editRestaurantPage,
         name='edit-restaurant-page'),
    # Dynamic URLs
]
