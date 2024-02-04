from django.shortcuts import render, HttpResponse

# Create your views here.


def homePage(request):
    context = {}
    return HttpResponse("Index")


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
