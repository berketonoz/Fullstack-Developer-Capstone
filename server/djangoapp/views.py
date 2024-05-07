"""views.py import statements"""
# from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponse
import logging
import json
from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
# from django.contrib import messages
# from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review

# Get an instance of a logger
logger = logging.getLogger(__name__)


def get_cars(request):
    """get_cars function for handling /get_cars route"""
    print(request)
    count = CarMake.objects.filter().count()
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append(
            {
                "CarModel": car_model.name,
                "CarMake": car_model.car_make.name
            })
    return JsonResponse({"CarModels": cars})


@csrf_exempt
def login_user(request):
    """login_user function for handling /login route"""
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)


def logout_request(request):
    """logout_request function for handling /logout route"""
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)


@csrf_exempt
def registration(request):
    """registration function for handling /register route"""
    # context = {}
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
    # email_exist = False
    try:
        # Check if user already exists
        User.objects.get(username=username)
        username_exist = True
    except LookupError as e:
        print(f"Error: {e}")
        # If not, simply log this is a new user
        message = f"{username} is new user"
        logger.debug(message)
    # If it is a new user
    if not username_exist:
        # Create user in auth_user table
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email)
        # Login the user and redirect to list page
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    else:
        data = {"userName": username, "error": "Already Registered"}
    return JsonResponse(data)


def get_dealerships(request, state="All"):
    """get_dealerships function for handling /dealers(/:id) route"""
    print(request)
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_reviews(request, dealer_id):
    """get_dealer_reviews function for handling /reviews/dealer/:id route"""
    print(request)
    if dealer_id:
        endpoint = '/fetchReviews/dealer/' + str(dealer_id)
        reviews = get_request(endpoint)
        for review in reviews:
            review["sentiment"] = analyze_review_sentiments(review["review"])
        return JsonResponse({"status": 200, "reviews": reviews})
    return JsonResponse({"status": 400, "reviews": "Bad Request"})


def get_dealer_details(request, dealer_id):
    """get_dealer_details function for handling /dealer/:id route"""
    print(request)
    if dealer_id:
        endpoint = '/fetchDealer/' + str(dealer_id)
        dealer = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealer})
    return JsonResponse({"status": 400, "reviews": "Bad Request"})


def add_review(request):
    """add_review function for handling /add_review route"""
    if request.user.is_anonymous is False:
        review = json.loads(request.body)
        try:
            response = post_review(review)
            return JsonResponse({"status": 200, "review": response})
        except ConnectionError as e:
            return JsonResponse({"status": 401, "message": e})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})
