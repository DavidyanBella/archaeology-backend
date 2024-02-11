from django.db import connection
from django.shortcuts import render, redirect

from .models import *


def index(request):
    query = request.GET.get("query", "")
    places = Place.objects.filter(name__icontains=query).filter(status=1)

    context = {
        "query": query,
        "places": places
    }

    return render(request, "home_page.html", context)


def place_details(request, place_id):
    context = {
        "place": Place.objects.get(id=place_id)
    }

    return render(request, "place_page.html", context)


def place_delete(request, place_id):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE places SET status = 2 WHERE id = %s", [place_id])

    return redirect("/")
