import random

from django.core import management
from django.core.management.base import BaseCommand
from ...models import *
from .utils import random_date, random_timedelta
from ...utils import random_text


def add_places():
    Place.objects.create(
        name="Территория объекта культурного наследия федерального значения «Городище Горгиппия»",
        description="Участок работ располагается в 25 м к югу от музеефицированных кварталов древнего города, входящих в территорию археологического заповедника «Горгиппия». Оказалось, что место раскопок почти не пострадало от техногенного воздействия в XX в. Это дало возможность проследить все периоды, значимые для античной Горгиппии и ранней Анапы.",
        image="places/1.jpg"
    )

    Place.objects.create(
        name="Территория западного участка Благовещенского останца на территории г.о. Анапа, станица Благовещенская, Бугазская коса.",
        description="Поселение «Благовещенское-9» находится на краю северо-западной части полей ст. Благовещенская, на территории береговой части Кизилташского лимана в прикорневой части косы Голенькая. Памятник, как «Благовещенское-10» и могильник «Дюна», был выявлен в 2023 г. сотрудниками исследовательского отряда Института археологии РАН Н.И. Сударевым, И.В. Рукавишниковой, Д.В. Бейлиным под общим методическим руководством П.С. Успенского.",
        image="places/2.jpg"
    )

    Place.objects.create(
        name="Юго-Восточный Казахстан, в предгорьях Северного Тянь-Шаня и южной части бассейна озера Балхаш",
        description="До начала 2000-х гг. регион был «белым» пятном в археологии каменного века: здесь не было известно ни одного памятника палеолита, мезолита и неолита, были получены лишь единичные находки. К настоящему времени, благодаря в том числе работе отряда, открыто уже более десятка стратифицированных (с погребенными культурными слоями) стоянок палеолита, в основном верхнепалеолитических.",
        image="places/3.jpg"
    )

    Place.objects.create(
        name="Правый берег реки Амур и Малышевской протоки Амура в районе села Малышево и нанайского национального села Сикачи-Алян",
        description="Древние рисунки Сикачи-Аляна, нанесённые на валуны и скалы, ученые объединили в 6 местонахождений, каждое из которых имеет свою специфику. На основании сопоставления особенностей изображений с материалами археологических культур региона петроглифы датируются от эпохи неолита (XIII–X тыс. до н.э.) до раннего Средневековья (IV–XIII в.н.э.)",
        image="places/4.jpg"
    )

    print("Услуги добавлены")


def add_finds():
    owners = CustomUser.objects.filter(is_superuser=False)
    moderators = CustomUser.objects.filter(is_superuser=True)

    if len(owners) == 0 or len(moderators) == 0:
        print("Заявки не могут быть добавлены. Сначала добавьте пользователей с помощью команды add_users")
        return

    places = Place.objects.all()

    for _ in range(30):
        find = Find.objects.create()
        find.name = "Находка №" + str(find.pk)
        find.status = random.randint(2, 5)
        find.description = random_text(15)
        find.expedition = random_text(5)
        find.owner = random.choice(owners)

        if find.status in [3, 4]:
            find.date_complete = random_date()
            find.date_formation = find.date_complete - random_timedelta()
            find.date_created = find.date_formation - random_timedelta()
            find.moderator = random.choice(moderators)
        else:
            find.date_formation = random_date()
            find.date_created = find.date_formation - random_timedelta()

        if find.status in [2, 3, 4]:
            find.expedition_date = random_date()

        for i in range(random.randint(1, 3)):
            find.places.add(random.choice(places))

        find.save()

    print("Заявки добавлены")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        management.call_command("clean_db")
        management.call_command("add_users")

        add_places()
        add_finds()









