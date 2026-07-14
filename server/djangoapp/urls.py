from django.urls import path
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # Session management routes
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.registration, name='register'),
    
    # Inventory routes
    path('get_cars', views.get_cars, name='getcars'),
    
    # Dealer & Review proxy microservice routes
    path('get_dealers', views.get_dealerships, name='get_dealers'),
    path('get_dealers/state/<str:state>', views.get_dealerships, name='get_dealers_by_state'),
    path('get_dealers/id/<int:dealer_id>', views.get_dealer_details, name='get_dealer_by_id'),
    path('reviews/dealer/<int:dealer_id>', views.get_dealer_reviews, name='get_dealer_reviews'),
    path('analyze/<str:review_text>', views.analyze_review_sentiment, name='analyze_review'),
]
