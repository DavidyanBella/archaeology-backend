from rest_framework import serializers
from .models import *


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Place
        # Поля, которые мы сериализуем (Все поля)
        fields = '__all__'


class FindSerializer(serializers.ModelSerializer):
    places = PlaceSerializer(read_only=True, many=True)

    class Meta:
        # Модель, которую мы сериализуем
        model = Find
        # Поля, которые мы сериализуем (Все поля)
        fields = '__all__'