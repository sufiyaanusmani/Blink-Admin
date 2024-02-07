from django.shortcuts import render, HttpResponse
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(
    "blink-a34ae-firebase-adminsdk-5myau-fd79745951.json")
firebase_admin.initialize_app(
    cred, {"databaseURL": "https://blink-a34ae.firebaseio.com"})
db = firestore.client()


class Customer:
    def __init__(self, uid, firstName, lastName, email):
        self.uid = uid
        self.firstName = firstName
        self.lastName = lastName
        self.email = email


class Restaurant:
    def __init__(self, id, name, owner, views):
        self.id = id
        self.name = name
        self.owner = owner
        self.views = views


class Product:
    def __init__(self, name, customer, restaurant, price):
        self.name = name
        self.customer = customer
        self.restaurant = restaurant
        self.price = price


class Order:
    def __init__(self, id, price):
        self.id = id
        self.products = self.getProducts()
        self.status = self.getStatus()
        self.price = price

    def getProducts(self):
        return []

    def getStatus(self):
        return ""

    def getPrice(self):
        return 0


def getOrders():
    orders = []
    ref = db.collection("orders")
    docs = ref.stream()
    for order in docs:
        ord = order.to_dict()
        orders.append(Order(order.id, int(ord["price"])))
    return orders


def getRestaurants():
    restaurants = []
    ref = db.collection("restaurants")
    docs = ref.stream()
    for restaurant in docs:
        res = restaurant.to_dict()
        restaurants.append(Restaurant(
            restaurant.id, res["name"], res["ownername"], res["views"]))
    return restaurants


def getTotalEarnings(orders):
    total = 0
    for order in orders:
        total += order.price

    return total

# Create your views here.


def homePage(request):
    orders = getOrders()
    earnings = getTotalEarnings(orders)
    context = {"orders": orders, "earnings": earnings}
    return render(request, 'base/index.html', context)


def ordersPage(request):
    context = {}
    return HttpResponse("Orders")


def customersPage(request):
    context = {}
    return HttpResponse("Customers")


def restaurantsPage(request):
    restaurants = getRestaurants()
    context = {"restaurants": restaurants}
    return render(request, 'base/restaurants.html', context)


def analyticsPage(request):
    context = {}
    return HttpResponse("Analytics")


def loginPage(request):
    context = {}
    return HttpResponse("Login")
