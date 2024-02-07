from django.shortcuts import render, redirect, HttpResponse
import firebase_admin
from firebase_admin import credentials, firestore
from .forms import RestaurantForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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
    try:
        ref = db.collection("restaurants")
        docs = ref.stream()
        for restaurant in docs:
            res = restaurant.to_dict()
            restaurants.append(Restaurant(
                restaurant.id, res["name"], res["ownername"], res["views"]))
    except Exception as e:
        print(e)
    return restaurants


def getTotalEarnings(orders):
    total = 0
    for order in orders:
        total += int(order.price)

    return total


def getTotalViews(restaurants):
    total = 0
    for restaurant in restaurants:
        total += int(restaurant.views)

    return total


def addNewRestaurant(data):
    restaurant = {
        "name": data["name"],
        "email": data["email"],
        "ownername": data["ownername"],
        "username": data["username"],
        "description": data["description"],
        "Estimated Time": 0,
        "Review": {
            "Rating Count": 0,
            "Stars": 0
        },
        "views": 0
    }

    collectionRef = db.collection("restaurants")
    updateTime, ref = collectionRef.add(restaurant)


def getRestaurant(id):
    docRef = db.collection('restaurants').document(id)
    restaurantRef = docRef.get()
    restaurant = restaurantRef.to_dict()
    print(restaurant)
    d = {"name": restaurant["name"], "email": restaurant["email"], "ownername": restaurant["ownername"],
         "description": restaurant["description"], "username": restaurant["username"]}
    return d


def updateRestaurant(id, restaurant):
    docRef = db.collection("restaurants").document(id)
    newData = {
        "name": restaurant["name"],
        "email": restaurant["email"],
        "ownername": restaurant["ownername"],
        "description": restaurant["description"],
        "username": restaurant["username"]
    }
    docRef.update(newData)
# Create your views here.


@login_required(login_url='login-page')
def homePage(request):
    orders = getOrders()
    earnings = getTotalEarnings(orders)
    totalViews = getTotalViews(getRestaurants())
    context = {"orders": orders, "earnings": earnings, "views": totalViews}
    return render(request, 'base/index.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home-page')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home-page')
    context = {}
    return render(request, 'base/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login-page')


@login_required(login_url='login-page')
def ordersPage(request):
    context = {}
    return render(context, 'base/orders.html', {'context': context})


@login_required(login_url='login-page')
def customersPage(request):
    context = {}
    return HttpResponse("Customers")


@login_required(login_url='login-page')
def restaurantsPage(request):
    restaurants = getRestaurants()
    context = {"restaurants": restaurants}
    return render(request, 'base/restaurants.html', context)


@login_required(login_url='login-page')
def analyticsPage(request):
    context = {}
    return HttpResponse("Analytics")


@login_required(login_url='login-page')
def newRestaurantPage(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST)

        if form.is_valid():
            addNewRestaurant(form.cleaned_data)
            return redirect('restaurants-page')
    else:
        form = RestaurantForm()

    context = {"form": form}
    return render(request, 'base/new_restaurant_form.html', context)


@login_required(login_url='login-page')
def deleteRestaurantPage(request, id):
    docRef = db.collection('restaurants').document(id)
    docRef.delete()
    return redirect('restaurants-page')


@login_required(login_url='login-page')
def editRestaurantPage(request, id):
    restaurant = getRestaurant(id)
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            updateRestaurant(id, form.cleaned_data)
        return redirect('restaurants-page')
    else:
        form = RestaurantForm(initial=restaurant)

    context = {"form": form, "id": id}
    return render(request, 'base/edit_restaurant_form.html', context)
