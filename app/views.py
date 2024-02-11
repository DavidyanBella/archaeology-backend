import requests
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.utils.dateparse import parse_datetime, parse_date
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .jwt_helper import *
from .permissions import *
from .serializers import *
from .utils import identity_user


def get_draft_find(request):
    user = identity_user(request)

    if user is None:
        return None

    find = Find.objects.filter(owner_id=user.id).filter(status=1).first()

    return find


@api_view(["GET"])
def search_places(request):
    query = request.GET.get("query", "")

    place = Place.objects.filter(status=1).filter(name__icontains=query)

    serializer = PlaceSerializer(place, many=True)

    draft_find = get_draft_find(request)

    resp = {
        "places": serializer.data,
        "draft_find_id": draft_find.pk if draft_find else None
    }

    return Response(resp)


@api_view(["GET"])
def get_place_by_id(request, place_id):
    if not Place.objects.filter(pk=place_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    place = Place.objects.get(pk=place_id)
    serializer = PlaceSerializer(place, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_place(request, place_id):
    if not Place.objects.filter(pk=place_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    place = Place.objects.get(pk=place_id)
    serializer = PlaceSerializer(place, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsModerator])
def create_place(request):
    place = Place.objects.create()

    serializer = PlaceSerializer(place)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_place(request, place_id):
    if not Place.objects.filter(pk=place_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    place = Place.objects.get(pk=place_id)
    place.status = 2
    place.save()

    place = Place.objects.filter(status=1)
    serializer = PlaceSerializer(place, many=True)

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_place_to_find(request, place_id):
    if not Place.objects.filter(pk=place_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    place = Place.objects.get(pk=place_id)

    find = get_draft_find(request)

    if find is None:
        find = Find.objects.create()

    if find.places.contains(place):
        return Response(status=status.HTTP_409_CONFLICT)

    find.places.add(place)
    find.owner = identity_user(request)
    find.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
def get_place_image(request, place_id):
    if not Place.objects.filter(pk=place_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    place = Place.objects.get(pk=place_id)

    return HttpResponse(place.image, content_type="image/png")


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_place_image(request, place_id):
    if not Place.objects.filter(pk=place_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    place = Place.objects.get(pk=place_id)
    serializer = PlaceSerializer(place, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_finds(request):
    user = identity_user(request)

    status_id = int(request.GET.get("status", -1))
    date_start = request.GET.get("date_start")
    date_end = request.GET.get("date_end")

    finds = Find.objects.exclude(status__in=[1, 5])

    if not user.is_moderator:
        finds = finds.filter(owner=user)

    if status_id != -1:
        finds = finds.filter(status=status_id)

    if date_start and parse_datetime(date_start) :
        finds = finds.filter(date_formation__gte=parse_datetime(date_start))

    if date_end and parse_datetime(date_end):
        finds = finds.filter(date_formation__lt=parse_datetime(date_end))

    serializer = FindsSerializer(finds, many=True)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_find_by_id(request, find_id):
    if not Find.objects.filter(pk=find_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    find = Find.objects.get(pk=find_id)
    serializer = FindSerializer(find, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_find(request, find_id):
    if not Find.objects.filter(pk=find_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    find = Find.objects.get(pk=find_id)
    serializer = FindSerializer(find, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsRemoteService])
def update_find_expedition_date(request, find_id):
    if not Find.objects.filter(pk=find_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    find = Find.objects.get(pk=find_id)

    expedition_date = request.data.get("expedition_date")
    if expedition_date and parse_date(expedition_date):
        find.expedition_date = parse_date(expedition_date)
        find.save()

    serializer = FindSerializer(find, many=False)
    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_status_user(request, find_id):
    if not Find.objects.filter(pk=find_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    find = Find.objects.get(pk=find_id)

    find.status = 2
    find.date_formation = timezone.now()
    find.save()

    calculate_expedition_date(find_id)

    serializer = FindSerializer(find, many=False)

    return Response(serializer.data)


def calculate_expedition_date(find_id):
    data = {
        "find_id": find_id
    }

    requests.post("http://127.0.0.1:8080/calc_expedition_date/", json=data, timeout=3)


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_status_admin(request, find_id):
    if not Find.objects.filter(pk=find_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = int(request.data["status"])

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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def delete_place_from_find(request, find_id, place_id):
    if not Find.objects.filter(pk=find_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not Place.objects.filter(pk=place_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    find = Find.objects.get(pk=find_id)
    find.places.remove(Place.objects.get(pk=place_id))
    find.save()

    if find.places.count() == 0:
        find.delete()
        return Response(status=status.HTTP_201_CREATED)

    serializer = FindSerializer(find)

    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(method='post', request_body=UserLoginSerializer)
@api_view(["POST"])
def login(request):
    serializer = UserLoginSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    user = authenticate(**serializer.data)
    if user is None:
        message = {"message": "invalid credentials"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    access_token = create_access_token(user.id)

    user_data = {
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "is_moderator": user.is_moderator,
        "access_token": access_token
    }

    return Response(user_data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    user = serializer.save()

    access_token = create_access_token(user.id)

    message = {
        'message': 'Пользователь успешно зарегистрирован!',
        'user_id': user.id,
        "access_token": access_token
    }
    return Response(message, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def check(request):
    user = identity_user(request)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    access_token = get_access_token(request)

    if access_token not in cache:
        cache.set(access_token, settings.JWT["ACCESS_TOKEN_LIFETIME"])

    message = {
        "message": "Вы успешно вышли из аккаунта"
    }

    return Response(message, status=status.HTTP_200_OK)
