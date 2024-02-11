from django.core.management.base import BaseCommand
from ...models import *


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Place.objects.all().delete()
        Find.objects.all().delete()
        CustomUser.objects.all().delete()