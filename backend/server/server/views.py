from sqlite3 import IntegrityError
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt  # Use only if testing without CSRF protection
from . import betclic
import json
from .models import Login

# Create your views here.
def home(request):
    return HttpResponse("home.html")

def login_view(request):
    return render(request, "login.html")

def users(request):
    users = Login.objects.all()
    return render(request, "users.html", {"users":users})

@csrf_exempt
def login_post(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            return HttpResponseBadRequest("Email and password are required.")
        
        try:
            Login.objects.create(email=email, password=password)
            return redirect("users")  # Redirect to the users page
        except IntegrityError:
            return HttpResponseBadRequest("This email is already registered.")
    else:
        return HttpResponseBadRequest("Only POST requests are allowed.")

@csrf_exempt
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