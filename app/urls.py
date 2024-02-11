from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name="home"),
    path('places/<int:place_id>/', place_details),
    path('places/<int:place_id>/delete/', place_delete)
]
