from django.urls import path
from . import views


app_name = 'profiles'
urlpatterns = [
    path('', views.profile, name='profile'),
    path('decrement-service', views.decrement_service,
         name='decrement_service'),
]
