"""restapis.py import statements"""
import os
import requests
from django.http import JsonResponse
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv(
    'backend_url', default = "http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default = "http://localhost:5000")

def get_request(endpoint, **kwargs):
    """get_request function for handling the get endpoints and api requests"""
    params = ""
    if kwargs:
        for key,value in kwargs.items():
            params=params+key+"="+value+"&"

    request_url = backend_url + endpoint + "?" + params

    print(f"GET from {request_url} ")
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url, timeout = 10)
        return response.json()
    except ConnectionError as e:
        # If any error occurs
        print("Network exception occurred -> ", e)
        return JsonResponse({"status": 400, "message": e})


def analyze_review_sentiments(text):
    """analyze_review_sentiments function for handling sentiment api request"""
    request_url = sentiment_analyzer_url+"/analyze/"+text
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url, timeout = 10)
        return response.json()["sentiment"]
    except ConnectionError as e:
        print(f"Unexpected {e=}, {type(e)=}")
        print("Network exception occurred")
        return JsonResponse({"status": 400, "message": e})


def post_review(data_dict):
    """post_review function for handling the post endpoints and api requests"""
    request_url = backend_url+"/insert_review"
    try:
        response = requests.post(request_url,json=data_dict, timeout = 10)
        return response.json()
    except ConnectionError as e:
        print("Network exception occurred -> ", e)
        return JsonResponse({"status": 400, "message": e})
