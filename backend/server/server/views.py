import logging
from sqlite3 import IntegrityError
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt  # Use only if testing without CSRF protection
import json
from .models import UserAccount
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

from . import fortuna

User = get_user_model()

# Create your views here.
def home(request):
    return HttpResponse("hello")

def login_view(request):
    return render(request, "login.html")

def users(request):
    users = UserAccount.objects.all()
    return render(request, "users.html", {"users":users})

@csrf_exempt
def register_post(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            return JsonResponse({"message": "Email and password are required."}, status=400)
        
        try:
            hashed_password = make_password(password)
            UserAccount.objects.create(email=email, password=hashed_password)
            return redirect("users")  # Redirect to the users page
        except IntegrityError:
            return JsonResponse({"message": "This email is already registered."}, status=400)
    else:
        return JsonResponse({"message": "Only POST requests are allowed."}, status=400)

@csrf_exempt
def stats(request):
    if request.method != "POST":
        return JsonResponse({"message": "Only POST requests are allowed."}, status=400)
    
    try:
        # Decode the JSON body
        body = json.loads(request.body)
        # Extract the string value (assuming the string is sent with a key like "input")
        input_string = body.get("input")

        if not input_string:
            return JsonResponse({"message": "Missing 'input' key in request body."}, status=400)
        
        # Use the string as needed (pass it to betclic.main or other logic)
        data = betclic.main(input_string)

        # Prepare the JSON response
        return JsonResponse({"result": data})
    
    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON payload."}, status=400)
    

@csrf_exempt
def register_account(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return JsonResponse({"message": "Email and password are required."}, status=400)

            hashed_password = make_password(password)
            UserAccount.objects.create(email=email, password=hashed_password)
            return JsonResponse({"message": "User registered successfully."})
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON payload."}, status=400)
    return JsonResponse({"message": "Only POST requests are allowed."}, status=400)


@csrf_exempt
def sign_in(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            logging.info(f"Received sign-in request for email: {email}")

            if not email or not password:
                return JsonResponse({"message": "Email and password are required."}, status=400)

            user = UserAccount.objects.filter(email=email).first()
            if user:
                logging.info(f"User found: {user.email}")
                if check_password(password, user.password):
                    logging.info(f"Password hash matches for user: {user.email}")
                    # Directly log in the user without re-authenticating
                    login(request, user)
                    logging.info(f"User {email} authenticated successfully.")
                    return JsonResponse({"message": "Sign in successful."})
                else:
                    logging.warning(f"Password hash does not match for user: {user.email}")
                    return JsonResponse({"message": "Invalid email or password."}, status=400)
            else:
                logging.warning(f"No user found with email: {email}")
                return JsonResponse({"message": "Invalid email or password."}, status=400)
        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error: {e}")
            return JsonResponse({"message": "Invalid JSON payload."}, status=400)
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return JsonResponse({"message": "An unexpected error occurred."}, status=500)
    return JsonResponse({"message": "Only POST requests are allowed."}, status=400)


def matches(request):
    url = "https://www.efortuna.pl/zaklady-bukmacherskie/pilka-nozna/1-anglia"
    all_matches = fortuna.get_all_matches(url)
    return JsonResponse(all_matches, safe=False)

