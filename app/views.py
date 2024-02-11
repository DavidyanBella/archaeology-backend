from django.http import HttpResponse
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *
from .models import *


def get_draft_find():
    return Find.objects.filter(status=1).first()


@api_view(["GET"])
def search_place(request):
    query = request.GET.get("query", "")

    products = Place.objects.filter(status=1).filter(name__icontains=query)

    serializer = PlaceSerializer(products, many=True)

    draft_find = get_draft_find()

    resp = {
        "places": serializer.data,
        "draft_find": draft_find.pk if draft_find else None
    }

    return Response(resp)


@api_view(['GET'])
def get_place_by_id(request, place_id):
    if not Place.objects.filter(pk=place_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    place = Place.objects.get(pk=place_id)

    serializer = PlaceSerializer(place, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
def update_place(request, place_id):
    if not Place.objects.filter(pk=place_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    place = Place.objects.get(pk=place_id)
    serializer = PlaceSerializer(place, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
def create_place(request):
    Place.objects.create()

    places = Place.objects.all()
    serializer = PlaceSerializer(places, many=True)

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_place(request, place_id):
    if not Place.objects.filter(pk=place_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    place = Place.objects.get(pk=place_id)
    place.status = 2
    place.save()

    places = Place.objects.filter(status=1)
    serializer = PlaceSerializer(places, many=True)

    return Response(serializer.data)


@api_view(["POST"])
def add_place_to_find(request, place_id):
    if not Place.objects.filter(pk=place_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    place = Place.objects.get(pk=place_id)

    find = get_draft_find()

    if find is None:
        find = Find.objects.create()

    find.places.add(place)
    find.save()

    serializer = FindSerializer(find.places, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_place_image(request, place_id):
    if not Place.objects.filter(pk=place_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    service = Place.objects.get(pk=place_id)

    return HttpResponse(service.image, content_type="image/png")


@api_view(["PUT"])
def update_place_image(request, place_id):
    if not Place.objects.filter(pk=place_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    place = Place.objects.get(pk=place_id)
    serializer = PlaceSerializer(place, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["GET"])
def get_finds(request):
    status = int(request.GET.get("status", -1))
    date_start = request.GET.get("date_start")
    date_end = request.GET.get("date_end")

    finds = Find.objects.exclude(status__in=[1, 5])

    if status != -1:
        finds = finds.filter(status=status)

    if date_start and parse_datetime(date_start):
        finds = finds.filter(date_formation__gte=parse_datetime(date_start))

    if date_end and parse_datetime(date_end):
        finds = finds.filter(date_formation__lte=parse_datetime(date_end))

    serializer = FindSerializer(finds, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_find_by_id(request, find_id):
    if not Find.objects.filter(pk=find_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    find = Find.objects.get(pk=find_id)
    serializer = FindSerializer(find, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_find(request, find_id):
    if not Find.objects.filter(pk=find_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    find = Find.objects.get(pk=find_id)
    serializer = FindSerializer(find, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    find.status = 1
    find.save()

    return Response(serializer.data)


@api_view(["PUT"])
def update_status_user(request, find_id):
    if not Find.objects.filter(pk=find_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    find = Find.objects.get(pk=find_id)

    if find.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    find.status = 2
    find.date_formation = timezone.now()
    find.save()

    serializer = FindSerializer(find, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_status_admin(request, find_id):
    if not Find.objects.filter(pk=find_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = request.data["status"]

    if request_status not in [3, 4]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    find = Find.objects.get(pk=find_id)

    if find.status != 2:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    find.status = request_status
    find.date_complete = timezone.now()
    find.save()

    serializer = FindSerializer(find, many=False)

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_find(request, find_id):
    if not Find.objects.filter(pk=find_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    find = Find.objects.get(pk=find_id)

    if find.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    find.status = 5
    find.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["DELETE"])
def delete_place_from_find(request, find_id, place_id):
    if not Find.objects.filter(pk=find_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not Place.objects.filter(pk=place_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    find = Find.objects.get(pk=find_id)
    find.places.remove(Place.objects.get(pk=place_id))
    find.save()

    serializer = PlaceSerializer(find.places, many=True)

    return Response(serializer.data["places"])
