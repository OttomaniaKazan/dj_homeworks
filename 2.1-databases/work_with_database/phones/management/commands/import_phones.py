import csv
from decimal import Decimal
from datetime import datetime
from django.utils import timezone
from django.utils.text import slugify
from django.core.management.base import BaseCommand
from phones.models import Phone


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('phones.csv', 'r', encoding='utf-8') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

        for phone in phones:
            phone_id = int(phone['id'])
            name = phone['name']
            image = phone['image']
            price = Decimal(phone['price'].replace(',', '.'))
            
            # Создаем aware datetime с временной зоной по умолчанию
            naive_datetime = datetime.strptime(phone['release_date'], '%Y-%m-%d')
            release_date = timezone.make_aware(naive_datetime).date()
            
            lte_exists = phone['lte_exists'].strip().lower() == 'true'
            slug = slugify(name)

            Phone.objects.create(
                id=phone_id,
                name=name,
                image=image,
                price=price,
                release_date=release_date,
                lte_exists=lte_exists,
                slug=slug
            )

        self.stdout.write(self.style.SUCCESS('Данные из phones.csv успешно импортированы в модель Phone.'))