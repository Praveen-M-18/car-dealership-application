from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging

from .models import CarMake, CarModel

# Get an instance of a logger
logger = logging.getLogger(__name__)

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('userName')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({"userName": username, "status": "Authenticated"})
        
        return JsonResponse({"userName": username, "status": "Authentication Failed"}, status=401)

def logout_user(request):
    username = request.user.username if request.user.is_authenticated else ""
    logout(request)
    return JsonResponse({"userName": username})

@csrf_exempt
def registration(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('userName')
        password = data.get('password')
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        email = data.get('email')
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({"userName": username, "error": "Already Registered"}, status=400)
            
        user = User.objects.create_user(
            username=username, 
            password=password, 
            first_name=first_name, 
            last_name=last_name, 
            email=email
        )
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})

def get_cars(request):
    count = CarMake.objects.filter().count()
    if count == 0:
        # Populate with mock data if completely empty
        toyota = CarMake.objects.create(name="Toyota", description="Japanese automotive manufacturer")
        CarModel.objects.create(car_make=toyota, name="Camry", type="Sedan", year=2024)
        CarModel.objects.create(car_make=toyota, name="RAV4", type="SUV", year=2025)
        
        ford = CarMake.objects.create(name="Ford", description="American automobile manufacturer")
        CarModel.objects.create(car_make=ford, name="Mustang", type="Coupe", year=2023)
        CarModel.objects.create(car_make=ford, name="F-150", type="Truck", year=2024)

    car_makes = CarMake.objects.all()
    cars_list = []
    for make in car_makes:
        models = CarModel.objects.filter(car_make=make)
        models_list = [{"name": m.name, "type": m.type, "year": m.year} for m in models]
        cars_list.append({
            "car_make": {"name": make.name, "description": make.description},
            "car_models": models_list
        })
    return JsonResponse(cars_list, safe=False)

# --- Microservice Proxy Endpoints (Mock implementations simulating remote microservices) ---

def get_dealerships(request, state=None):
    # Simulates Node.js/Express Dealership Microservice
    mock_dealers = [
        {"id": 1, "city": "Topeka", "state": "Kansas", "st": "KS", "address": "123 Main St", "zip": "66601", "full_name": "Topeka Car Dealership"},
        {"id": 2, "city": "Wichita", "state": "Kansas", "st": "KS", "address": "456 Oak Ave", "zip": "67201", "full_name": "Wichita Auto Center"},
        {"id": 3, "city": "Miami", "state": "Florida", "st": "FL", "address": "789 Palm Blvd", "zip": "33101", "full_name": "Miami Elite Motors"}
    ]
    if state:
        filtered = [d for d in mock_dealers if d['state'].lower() == state.lower()]
        return JsonResponse(filtered, safe=False)
    return JsonResponse(mock_dealers, safe=False)

def get_dealer_details(request, dealer_id):
    # Simulates fetching a specific dealership profile by its unique ID
    mock_dealers = {
        1: {"id": 1, "city": "Topeka", "state": "Kansas", "st": "KS", "address": "123 Main St", "zip": "66601", "full_name": "Topeka Car Dealership"}
    }
    dealer = mock_dealers.get(dealer_id, {"error": "Dealer not found"})
    return JsonResponse(dealer, safe=False)

def get_dealer_reviews(request, dealer_id):
    # Simulates MongoDB review backend query
    mock_reviews = [
        {
            "id": 1,
            "name": "John Doe",
            "dealership": 15,
            "review": "Excellent customer service and very friendly staff!",
            "purchase": True,
            "purchase_date": "02/14/2026",
            "car_make": "Toyota",
            "car_model": "Camry",
            "car_year": 2024,
            "sentiment": "positive"
        }
    ]
    return JsonResponse(mock_reviews, safe=False)

def analyze_review_sentiment(request, review_text):
    # Simulates external deployment calls to Watson NLU sentiment analyzer 
    if "fantastic" in review_text.lower() or "excellent" in review_text.lower():
        return JsonResponse({"sentiment": "positive"})
    elif "bad" in review_text.lower() or "terrible" in review_text.lower():
        return JsonResponse({"sentiment": "negative"})
    return JsonResponse({"sentiment": "neutral"})
