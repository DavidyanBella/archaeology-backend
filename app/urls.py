from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="home"),
    path('place/<int:place_id>', place, name="place")
]