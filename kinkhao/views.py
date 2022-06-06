from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import modelform_factory
from kinkhao.models import *
from kinkhao.forms import *


# Create your views here.

def index(request):
    return render(request, "index.html")


def menu(request):
    return render(request, "menu.html")


def reservations(request):
    return render(request, "reservations.html")


# This Part is taking advantage of the functionality that can create a form basing on the models the describe the table
BookingForm = modelform_factory(Bookings1, exclude=[])


def newBooking(request):
    form = BookingForm()
    return render(request, "newBooking.html", {"form": form})


def createMeal(request):
    if request.method == 'POST':
        # form = CreateMealForm(request.POST)
        form = CreateMealForm1(request.POST)
        if form.is_valid():
            # mn = form.cleaned_data['theMealName']
            # ct = form.cleaned_data['theCuisineType']
            #
            # theCreatedMeal = Meal(mealName=mn,cuisineType=ct)
            # theCreatedMeal.save()
            form.save()
            return HttpResponse("the new meal was created")
    else:
        form = CreateMealForm1()
        # form = CreateMealForm()
    return render(request, "createCuisine.html", {"form": form})


def createTable(request):
    if request.method == 'POST':  # a submit button has been clicked or similar action
        # create another instance  of TableForm, but this one contains the data submitted
        # form = TableForm(request.POST)
        form = TestTableForm1(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:  # This means the request is GET
        form = TestTableForm1()
        # form = TableForm()

    return render(request, "createTable.html", {"form": form})


# This view will handle the form that was created manually in the forms.py file
def createReservation(request):
    # if this is a POST request we need to process the form Data
    if request.method == 'POST':
        # create a form instance and populate it with data form
        form = MakeReservationForm(request.POST)
        # check whether the form is valid
        if form.is_valid():
            # process the data in the form.cleaned_data as required
            # to return a response
            # return HttpResponse("The Data was okay now process the data")
            # redirect to new URL
            form.save()
            return HttpResponseRedirect("/createReservations/")
    # if a GET (or any other method ) a black form will be created
    else:
        form = MakeReservationForm()

    return render(request, "makeReservation.html", {'form': form})


def facebook(request):
    return render(request, "https://twitter.com/home")
