from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt  # Use only if testing without CSRF protection
from . import betclic
import json


# Create your views here.
def home(request):
    return HttpResponse("hello")

@csrf_exempt  # Remove in production, ensure proper CSRF handling
def stats(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Only POST requests are allowed.")
    
    try:
        # Decode the JSON body
        body = json.loads(request.body)
        # Extract the string value (assuming the string is sent with a key like "input")
        input_string = body.get("input")

        if not input_string:
            return HttpResponseBadRequest("Missing 'input' key in request body.")
        
        # Use the string as needed (pass it to betclic.main or other logic)
        data = betclic.main(input_string)

        # Prepare the JSON response
        return JsonResponse({"result": data})
    
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON payload.")