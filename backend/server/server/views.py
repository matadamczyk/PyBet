import logging
from sqlite3 import IntegrityError
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import (
    csrf_exempt,
)  # Use only if testing without CSRF protection
import json
from .models import UserAccount, UserPickedOption
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

# from . import matches
import sys
import os

# Add the project root directory to Python path
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from algorithms.optimized_algorithm import predict_match_outcome
from datacollection.bookmakers.normalize import normalize_team_name

User = get_user_model()


# Create your views here.
def home(request):
    return HttpResponse("hello")


def login_view(request):
    return render(request, "login.html")


def users(request):
    users = UserAccount.objects.all()
    return render(request, "users.html", {"users": users})


@csrf_exempt
def register_post(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            return JsonResponse(
                {"message": "Email and password are required."}, status=400
            )

        try:
            hashed_password = make_password(password)
            UserAccount.objects.create(email=email, password=hashed_password)
            return redirect("users")  # Redirect to the users page
        except IntegrityError:
            return JsonResponse(
                {"message": "This email is already registered."}, status=400
            )
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
            return JsonResponse(
                {"message": "Missing 'input' key in request body."}, status=400
            )

        # Use the string as needed (pass it to betclic.main or other logic)
        data = betclic.main(input_string)

        # Prepare the JSON response
        return JsonResponse({"result": data})

    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON payload."}, status=400)


@csrf_exempt
def register_account(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")

            if not email or not password:
                return JsonResponse(
                    {"message": "Email and password are required."}, status=400
                )

            hashed_password = make_password(password)
            UserAccount.objects.create(email=email, password=hashed_password)
            return JsonResponse({"message": "User registered successfully."})
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON payload."}, status=400)
    return JsonResponse({"message": "Only POST requests are allowed."}, status=400)


@csrf_exempt
def sign_in(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")

            try:
                user = UserAccount.objects.get(email=email)
                if check_password(password, user.password):
                    login(request, user)
                    response = JsonResponse(
                        {
                            "message": "Login successful",
                            "tokens": request.session.session_key,
                            "pycoins": user.pycoins,
                        }
                    )
                    response["Access-Control-Allow-Origin"] = "http://localhost:5173"
                    response["Access-Control-Allow-Credentials"] = "true"
                    return response
            except UserAccount.DoesNotExist:
                pass

            return JsonResponse({"message": "Invalid credentials."}, status=401)
        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error: {e}")
            return JsonResponse({"message": "Invalid JSON payload."}, status=400)
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return JsonResponse(
                {"message": "An unexpected error occurred."}, status=500
            )
    return JsonResponse({"message": "Only POST requests are allowed."}, status=400)


# example of json to be sent
# {
#     "selectedOption": "Option A",
#     "date": "2023-10-15",
#     "selectedOdds": 2.5,
#     "stake": 100.0
# }
@csrf_exempt
def user_picked_option(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            selected_option = data.get("selectedOption")
            date = data.get("date")
            selected_odds = data.get("selectedOdds")
            stake = data.get("stake")

            if not selected_option or not date or not selected_odds or not stake:
                return JsonResponse({"message": "All fields are required."}, status=400)

            UserPickedOption.objects.create(
                selectedOption=selected_option,
                date=date,
                selectedOdds=selected_odds,
                stake=stake,
            )
            return JsonResponse({"message": "User picked option saved successfully."})
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON payload."}, status=400)
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return JsonResponse(
                {"message": "An unexpected error occurred."}, status=500
            )
    return JsonResponse({"message": "Only POST requests are allowed."}, status=400)


def get_user_picked_options(request):
    if request.method == "GET":
        try:
            email = request.GET.get("email")
            if not email:
                return JsonResponse(
                    {"message": "Email parameter is required."}, status=400
                )

            user = UserAccount.objects.get(email=email)
            options = UserPickedOption.objects.filter(user=user).values()
            return JsonResponse(list(options), safe=False)
        except UserAccount.DoesNotExist:
            return JsonResponse({"message": "User not found."}, status=404)
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return JsonResponse(
                {"message": "An unexpected error occurred."}, status=500
            )
    return JsonResponse({"message": "Only GET requests are allowed."}, status=400)


def matches(request):
    url = "https://www.efortuna.pl/zaklady-bukmacherskie/pilka-nozna/1-anglia"
    from .matches import get_all_matches

    all_matches = get_all_matches(url)
    return JsonResponse(all_matches, safe=False)


@csrf_exempt
def get_profitable_odds(request):
    if request.method == "GET":
        try:
            file_path = "server/data/profitable/profitable.json"
            full_path = os.path.abspath(file_path)

            with open(full_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            return JsonResponse(data, safe=False)
        except FileNotFoundError:
            logging.error("File not found: %s", file_path)
            return JsonResponse(
                {"message": "Profitable data file not found"}, status=404
            )
        except json.JSONDecodeError:
            logging.error("Error decoding JSON from file: %s", file_path)
            return JsonResponse(
                {"message": "Error reading profitable data"}, status=500
            )
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return JsonResponse(
                {"message": "Error reading profitable data"}, status=500
            )
    return JsonResponse({"message": "Only GET requests are allowed."}, status=400)


@csrf_exempt
def add_pycoins(request):
    if request.method != "POST":
        return JsonResponse({"message": "Only POST requests are allowed."}, status=400)

    try:
        data = json.loads(request.body)
        amount = data.get("amount")
        email = data.get("email")

        try:
            user = UserAccount.objects.get(email=email)
            user.pycoins += float(amount)
            user.save()

            response = JsonResponse({"pycoins": user.pycoins})
            response["Access-Control-Allow-Origin"] = "http://localhost:5173"
            response["Access-Control-Allow-Credentials"] = "true"
            return response
        except UserAccount.DoesNotExist:
            return JsonResponse({"message": "User not found."}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON payload."}, status=400)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)


@csrf_exempt
def place_bet(request):
    if request.method != "POST":
        return JsonResponse({"message": "Only POST requests are allowed."}, status=400)

    try:
        data = json.loads(request.body)
        email = data.get("email")

        try:
            user = UserAccount.objects.get(email=email)
        except UserAccount.DoesNotExist:
            return JsonResponse({"message": "User not found."}, status=404)

        if user.pycoins < data["stake"]:
            return JsonResponse({"message": "Insufficient PyCoins."}, status=400)

        user.pycoins -= data["stake"]
        user.save()

        UserPickedOption.objects.create(
            user=user,
            matchTeams=f"{data['homeTeam']} vs {data['awayTeam']}",
            selectedOption=data["selectedOption"],
            date=data["date"],
            selectedOdds=data["selectedOdds"],
            stake=data["stake"],
        )

        response = JsonResponse(
            {"message": "Bet placed successfully", "pycoins": user.pycoins}
        )
        response["Access-Control-Allow-Origin"] = "http://localhost:5173"
        response["Access-Control-Allow-Credentials"] = "true"
        return response
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)


@csrf_exempt
def get_user_pycoins(request):
    if request.method != "GET":
        return JsonResponse({"message": "Only GET requests are allowed."}, status=400)

    email = request.GET.get("email")
    if not email:
        return JsonResponse({"message": "Email parameter is required."}, status=400)

    try:
        user = UserAccount.objects.get(email=email)
        return JsonResponse({"pycoins": user.pycoins})
    except UserAccount.DoesNotExist:
        return JsonResponse({"message": "User not found."}, status=404)
