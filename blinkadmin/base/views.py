from django.shortcuts import render, HttpResponse
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("blink-a34ae-firebase-adminsdk-5myau-fd79745951.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://blink-a34ae.firebaseio.com"})
db = firestore.client()

# Create your views here.


def homePage(request):
    ref = db.collection("customers")
    docs = ref.stream()

    for doc in docs:
        print(f"{doc.id} => {doc.to_dict()}")
    context = {}
    return render(request, 'base/index.html')


def ordersPage(request):
    context = {}
    return HttpResponse("Orders")


def customersPage(request):
    context = {}
    return HttpResponse("Customers")


def restaurantsPage(request):
    context = {}
    return HttpResponse("Restaurants")


def analyticsPage(request):
    context = {}
    return HttpResponse("Analytics")


def loginPage(request):
    context = {}
    return HttpResponse("Login")
